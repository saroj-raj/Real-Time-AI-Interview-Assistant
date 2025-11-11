from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import os
import sys
import threading
import queue
import time
import numpy as np
import sounddevice as sd
import importlib.util
from pathlib import Path
import json

# Add src/core to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

from audio_device_util import pick_system_audio_device
from audio_transcriber import load_whisper, transcribe_chunk

app = Flask(__name__)
CORS(app)

# Global state
class InterviewState:
    def __init__(self):
        self.device_pick = None
        self.model = None
        self.llm = None
        self.context = ""
        self.job_description = ""
        self.profile_user = None
        self.profile_role = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recording_event = threading.Event()
        self.audio_frames = []
        self.stream = None
        self.question_count = 0
        
state = InterviewState()

def audio_callback(indata, frames, time_info, status):
    """Callback for audio recording"""
    if state.recording_event.is_set():
        state.audio_frames.append(indata.copy())

def load_profile_module(user, role_file):
    """Load the selected profile module dynamically"""
    profile_path = Path("profiles") / user / f"{role_file}.py"
    
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    
    spec = importlib.util.spec_from_file_location("selected_profile", profile_path)
    profile_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile_module)
    
    return profile_module

def load_role_job_description(user, role_file):
    """Load job description specific to the selected role"""
    possible_paths = [
        f"profiles/{user}/{role_file}_job_description.txt",
        f"profiles/{user}/job_descriptions/{role_file}.txt", 
        f"job_descriptions/{user}_{role_file}.txt",
        f"job_descriptions/{role_file}.txt",
        "job_description.txt",
        "jd.txt"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except:
                continue
    return ""

def load_context():
    """Load general context file"""
    paths = ["my_context.txt", os.environ.get("CONTEXT_FILE", "")]
    for path in paths:
        if path and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except:
                pass
    return ""

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Get available profiles"""
    profiles_dir = Path("profiles")
    
    if not profiles_dir.exists():
        return jsonify({"error": "No profiles directory found"}), 404
    
    users = []
    for user_dir in profiles_dir.iterdir():
        if user_dir.is_dir() and not user_dir.name.startswith('.') and not user_dir.name.startswith('__'):
            roles = []
            for role_file in user_dir.iterdir():
                if role_file.is_file() and role_file.suffix == '.py' and not role_file.name.startswith('__'):
                    role_name = role_file.stem.replace('_', ' ').title()
                    roles.append({
                        'file': role_file.stem,
                        'display': role_name
                    })
            
            if roles:
                users.append({
                    'name': user_dir.name,
                    'roles': roles
                })
    
    return jsonify({"users": users})

@app.route('/api/initialize', methods=['POST'])
def initialize():
    """Initialize the interview session with selected profile"""
    try:
        data = request.json
        user = data.get('user')
        role_file = data.get('role')
        
        if not user or not role_file:
            return jsonify({"error": "User and role required"}), 400
        
        # Load profile
        profile_module = load_profile_module(user, role_file)
        state.llm = profile_module.make_llm()
        state.profile_user = user
        state.profile_role = role_file
        
        # Load context and job description
        state.context = load_context()
        state.job_description = load_role_job_description(user, role_file)
        
        # Load Whisper model
        if state.model is None:
            state.model = load_whisper()
        
        # Setup audio device
        if state.device_pick is None:
            state.device_pick = pick_system_audio_device(prefer_rate=48000)
        
        return jsonify({
            "success": True,
            "message": "Profile loaded successfully",
            "profile": {
                "user": user,
                "role": role_file,
                "has_context": len(state.context) > 0,
                "has_job_description": len(state.job_description) > 0
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/start-recording', methods=['POST'])
def start_recording():
    """Start audio recording"""
    try:
        if state.is_recording:
            return jsonify({"error": "Already recording"}), 400
        
        if state.device_pick is None:
            return jsonify({"error": "Not initialized"}), 400
        
        # Clear previous frames
        state.audio_frames = []
        
        # Setup audio stream if not exists
        if state.stream is None:
            if state.device_pick.wasapi_loopback:
                stream_params = {
                    'device': (None, state.device_pick.index),
                    'samplerate': state.device_pick.samplerate,
                    'channels': 2,
                    'dtype': 'float32',
                    'callback': audio_callback,
                    'extra_settings': sd.WasapiSettings(loopback=True)
                }
            else:
                stream_params = {
                    'device': state.device_pick.index,
                    'samplerate': state.device_pick.samplerate,
                    'channels': 1,
                    'dtype': 'float32',
                    'callback': audio_callback,
                }
            state.stream = sd.InputStream(**stream_params)
            state.stream.start()
        
        # Start recording
        state.recording_event.set()
        state.is_recording = True
        
        return jsonify({
            "success": True,
            "message": "Recording started"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stop-recording', methods=['POST'])
def stop_recording():
    """Stop audio recording and transcribe"""
    try:
        if not state.is_recording:
            return jsonify({"error": "Not recording"}), 400
        
        # Stop recording
        state.recording_event.clear()
        state.is_recording = False
        
        # Give a moment for last frames
        time.sleep(0.1)
        
        if not state.audio_frames:
            return jsonify({"error": "No audio recorded"}), 400
        
        # Process audio
        audio = np.concatenate(state.audio_frames, axis=0)
        if audio.ndim == 2 and audio.shape[1] > 1:
            audio = np.mean(audio, axis=1, keepdims=True)
        elif audio.ndim == 1:
            audio = audio.reshape(-1, 1)
        
        # Transcribe
        text = transcribe_chunk(state.model, audio.astype(np.float32), state.device_pick.samplerate)
        
        if not text or text == "(no speech detected)":
            return jsonify({"error": "No speech detected"}), 400
        
        state.question_count += 1
        
        return jsonify({
            "success": True,
            "question": text,
            "question_number": state.question_count
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-response', methods=['POST'])
def generate_response():
    """Generate response to question (streaming)"""
    try:
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "Question required"}), 400
        
        if state.llm is None:
            return jsonify({"error": "Not initialized"}), 400
        
        def generate():
            try:
                for token in state.llm.generate_response_stream(
                    question, 
                    state.context, 
                    state.job_description
                ):
                    yield f"data: {json.dumps({'token': token})}\n\n"
                
                yield f"data: {json.dumps({'done': True})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current status"""
    return jsonify({
        "initialized": state.llm is not None,
        "recording": state.is_recording,
        "question_count": state.question_count,
        "profile": {
            "user": state.profile_user,
            "role": state.profile_role
        } if state.profile_user else None
    })

if __name__ == '__main__':
    # Create templates directory if not exists
    os.makedirs('templates', exist_ok=True)
    
    # Get local IP for mobile access
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("=" * 60)
    print("AI Interview Assistant - Web Server")
    print("=" * 60)
    print(f"\nServer starting...")
    print(f"\nAccess from:")
    print(f"  Local:   http://localhost:5000")
    print(f"  Network: http://{local_ip}:5000")
    print(f"\nOpen this URL on your mobile browser!")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)