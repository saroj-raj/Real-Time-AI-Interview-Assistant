from __future__ import annotations

import os
import sys
import threading
import time
import queue
import textwrap
import shutil
import numpy as np
import sounddevice as sd
import importlib.util
from pathlib import Path

# Add src/core to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

from audio_device_util import pick_system_audio_device, pretty_selection
from audio_transcriber import load_whisper, transcribe_chunk

class WordWrapper:
    """Real-time word wrapper for streaming text"""
    
    def __init__(self, width: int = None, indent: str = ""):
        self.width = width or min(shutil.get_terminal_size().columns - 4, 100)
        self.indent = indent
        self.buffer = ""
        self.current_line = ""
        self.current_line_length = len(indent)
        
    def add_token(self, token: str) -> str:
        """Add token and return any complete lines to print"""
        self.buffer += token
        output = ""
        
        # Process complete words (split on spaces)
        while ' ' in self.buffer or '\n' in self.buffer:
            # Find the next word boundary
            space_pos = self.buffer.find(' ')
            newline_pos = self.buffer.find('\n')
            
            if newline_pos != -1 and (space_pos == -1 or newline_pos < space_pos):
                # Handle newline
                word = self.buffer[:newline_pos]
                self.buffer = self.buffer[newline_pos + 1:]
                
                if word:  # Add word if not empty
                    result = self._add_word_to_line(word)
                    if result:
                        output += result
                
                # Force line break
                if self.current_line.strip():  # Only if line has content
                    output += self.current_line + '\n'
                self._reset_line()
                
            elif space_pos != -1:
                # Handle space-separated word
                word = self.buffer[:space_pos]
                self.buffer = self.buffer[space_pos + 1:]
                
                if word:  # Add word if not empty
                    result = self._add_word_to_line(word)
                    if result:
                        output += result
        
        return output
    
    def _add_word_to_line(self, word: str) -> str:
        """Add word to current line, wrapping if necessary"""
        word_length = len(word)
        
        # Check if word fits on current line (leave space for one space)
        if self.current_line_length + word_length + 1 <= self.width:
            # Add word to current line
            if self.current_line:
                self.current_line += " " + word
                self.current_line_length += word_length + 1
            else:
                self.current_line = self.indent + word
                self.current_line_length = len(self.indent) + word_length
            return ""
        else:
            # Need to wrap - finish current line and start new one
            output = ""
            if self.current_line.strip():  # Only output if line has content
                output = self.current_line + '\n'
            
            # Start new line with the word
            self.current_line = self.indent + word
            self.current_line_length = len(self.indent) + word_length
            return output
    
    def _reset_line(self):
        """Reset current line"""
        self.current_line = ""
        self.current_line_length = len(self.indent)
    
    def flush(self) -> str:
        """Flush any remaining content"""
        output = ""
        
        # Add any remaining buffer content
        if self.buffer.strip():
            result = self._add_word_to_line(self.buffer.strip())
            if result:
                output += result
            self.buffer = ""
        
        # Output current line if it has content
        if self.current_line.strip():
            output += self.current_line + '\n'
            self._reset_line()
        
        return output

def select_profile():
    """Simple profile selection from profiles directory"""
    print("=" * 60)
    print("AI Interview Assistant - Profile Selection")
    print("=" * 60)
    
    profiles_dir = Path("profiles")
    if not profiles_dir.exists():
        print("ERROR: No profiles directory found!")
        print("Please create: ./profiles/your_name/your_role.py")
        return None, None, None
    
    # Get available users
    users = []
    for item in profiles_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            users.append(item.name)
    
    if not users:
        print("ERROR: No user profiles found!")
        print("Please create: ./profiles/your_name/your_role.py")
        return None, None, None
    
    # Select user
    print(f"\nAvailable users:")
    for i, user in enumerate(users, 1):
        print(f"  {i}. {user}")
    
    try:
        user_choice = int(input(f"\nSelect user (1-{len(users)}): ")) - 1
        if not 0 <= user_choice < len(users):
            print("Invalid selection")
            return None, None, None
        
        selected_user = users[user_choice]
        print(f"Selected user: {selected_user}")
    except (ValueError, KeyboardInterrupt):
        print("Selection cancelled")
        return None, None, None
    
    # Get available roles for selected user
    user_dir = profiles_dir / selected_user
    roles = []
    for item in user_dir.iterdir():
        if item.is_file() and item.suffix == '.py' and not item.name.startswith('__'):
            role_name = item.stem.replace('_', ' ').title()
            roles.append((item.stem, role_name))
    
    if not roles:
        print(f"ERROR: No role profiles found for {selected_user}")
        print(f"Please create: ./profiles/{selected_user}/your_role.py")
        return None, None, None
    
    # Select role
    print(f"\nAvailable roles for {selected_user}:")
    for i, (role_file, role_display) in enumerate(roles, 1):
        print(f"  {i}. {role_display}")
    
    try:
        role_choice = int(input(f"\nSelect role (1-{len(roles)}): ")) - 1
        if not 0 <= role_choice < len(roles):
            print("Invalid selection")
            return None, None, None
        
        selected_role_file, selected_role_display = roles[role_choice]
        print(f"Selected role: {selected_role_display}")
        
        return selected_user, selected_role_file, selected_role_display
        
    except (ValueError, KeyboardInterrupt):
        print("Selection cancelled")
        return None, None, None

def load_profile_module(user, role_file):
    """Load the selected profile module dynamically"""
    profile_path = Path("profiles") / user / f"{role_file}.py"
    
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile not found: {profile_path}")
    
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("selected_profile", profile_path)
    profile_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile_module)
    
    return profile_module

def load_role_job_description(user, role_file):
    """Load job description specific to the selected role"""
    # Try multiple possible locations for job descriptions
    possible_paths = [
        f"profiles/{user}/{role_file}_job_description.txt",
        f"profiles/{user}/job_descriptions/{role_file}.txt", 
        f"job_descriptions/{user}_{role_file}.txt",
        f"job_descriptions/{role_file}.txt",
        "job_description.txt",  # fallback to global
        "jd.txt"  # fallback to global
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        print(f"✓ Job Description loaded from: {path}")
                        return content
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}")
                continue
    
    return ""

def show_startup_info():
    """Show all technical info upfront with profile selection"""
    print("=" * 60)
    print("AI Interview Assistant - Initializing...")
    print("=" * 60)
    
    # Profile selection
    user, role_file, role_display = select_profile()
    if not user or not role_file:
        print("No profile selected. Exiting...")
        sys.exit(1)
    
    # Load the selected profile
    try:
        print(f"\nLoading profile: {user} - {role_display}")
        profile_module = load_profile_module(user, role_file)
        llm = profile_module.make_llm()
        print("✓ Profile loaded successfully")
    except Exception as e:
        print(f"ERROR: Failed to load profile: {e}")
        print("Make sure your profile file has a 'make_llm()' function")
        sys.exit(1)
    
    # Load context files
    print("\n--- Context Loading ---")
    context = load_context()
    job_description = load_role_job_description(user, role_file)
    
    if context:
        print(f"✓ General context: {len(context.split())} words loaded")
    else:
        print("⚠ No general context loaded (create my_context.txt)")
    
    if job_description:
        print(f"✓ Role-specific job description: {len(job_description.split())} words loaded")
    else:
        print("⚠ No role-specific job description found")
        print(f"  Create: profiles/{user}/{role_file}_job_description.txt")
    
    # Audio setup
    print("\n--- Audio Setup ---")
    device_pick = pick_system_audio_device(prefer_rate=48000)
    print(f"Device: {device_pick.name}")
    print(f"Mode: {'Loopback' if device_pick.wasapi_loopback else 'Virtual Input'}")
    print(f"Rate: {device_pick.samplerate}Hz")
    
    # Model loading
    print("\n--- Model Loading ---")
    print("Loading Whisper...", end="", flush=True)
    model = load_whisper()
    print(" ✓")
    
    print("LLM already loaded ✓")
    
    # Terminal info
    terminal_width = shutil.get_terminal_size().columns
    print(f"\n--- Display Setup ---")
    print(f"Terminal width: {terminal_width} columns")
    print(f"Response width: {min(terminal_width - 4, 100)} columns (optimized for readability)")
    
    print(f"\n{'='*60}")
    print("READY FOR INTERVIEW")
    print(f"User: {user} | Role: {role_display}")
    print(f"{'='*60}")
    print("Controls:")
    print("• Press ENTER to START recording")
    print("• Press ENTER again to STOP recording")
    print("• Press SPACE during AI response to interrupt")
    print("• Press CTRL+C to exit")
    print(f"{'='*60}\n")
    
    return device_pick, model, llm, context, job_description

def load_context() -> str:
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

def record_manual_control(device_index: int, samplerate: int, wasapi_loopback: bool):
    """Manual start/stop recording with ENTER key"""
    
    audio_queue = queue.Queue()
    recording = threading.Event()
    
    def audio_callback(indata, frames, time_info, status):
        if recording.is_set():
            audio_queue.put(indata.copy())
    
    # Setup audio stream
    if wasapi_loopback:
        stream_params = {
            'device': (None, device_index),
            'samplerate': samplerate,
            'channels': 2,
            'dtype': 'float32',
            'callback': audio_callback,
            'extra_settings': sd.WasapiSettings(loopback=True)
        }
    else:
        stream_params = {
            'device': device_index,
            'samplerate': samplerate,
            'channels': 1,
            'dtype': 'float32',
            'callback': audio_callback,
        }
    
    try:
        with sd.InputStream(**stream_params):
            # Wait for first ENTER to start
            input()
            print("🔴 RECORDING... (Press ENTER to stop)")
            recording.set()
            start_time = time.time()
            
            # Wait for second ENTER to stop
            input()
            recording.clear()
            elapsed = time.time() - start_time
            print(f"⏹ Stopped ({elapsed:.1f}s)")
            
            # Collect recorded audio
            frames = []
            while not audio_queue.empty():
                frames.append(audio_queue.get())
            
            if not frames:
                return np.zeros((1, 1), dtype=np.float32), elapsed
            
            # Process audio
            audio = np.concatenate(frames, axis=0)
            if audio.ndim == 2 and audio.shape[1] > 1:
                audio = np.mean(audio, axis=1, keepdims=True)
            elif audio.ndim == 1:
                audio = audio.reshape(-1, 1)
                
            return audio.astype(np.float32), elapsed
            
    except Exception as e:
        print(f"Recording error: {e}")
        return np.zeros((1, 1), dtype=np.float32), 0.0

def print_wrapped_response(llm, question: str, context: str, job_description: str, stop_generation: threading.Event):
    """Print response with proper word wrapping"""
    
    # Initialize word wrapper
    wrapper = WordWrapper(width=min(shutil.get_terminal_size().columns - 4, 100))
    
    response_text = ""
    word_count = 0
    
    try:
        for token in llm.generate_response_stream(question, context, job_description):
            if stop_generation.is_set():
                break
                
            # Add token to wrapper and get any complete lines
            wrapped_output = wrapper.add_token(token)
            
            # Print wrapped lines immediately
            if wrapped_output:
                print(wrapped_output, end="", flush=True)
            
            response_text += token
        
        # Flush any remaining content
        if not stop_generation.is_set():
            final_output = wrapper.flush()
            if final_output:
                print(final_output, end="", flush=True)
                
            # Add final newline if needed
            if not response_text.endswith('\n'):
                print()
        
        # Count words for summary
        word_count = len(response_text.split())
        
        return response_text, word_count
        
    except Exception as e:
        print(f"\n⚠ LLM error: {e}")
        fallback = "Based on my experience, I can address this technical challenge using proven methodologies and best practices from my background."
        print(textwrap.fill(fallback, width=wrapper.width))
        return fallback, len(fallback.split())

def run_interview_session(device_pick, model, llm, context, job_description):
    """Enhanced interview loop with word wrapping"""
    
    question_count = 0
    
    try:
        while True:
            question_count += 1
            
            # Manual recording control
            print(f"\n[Q{question_count}] Press ENTER to start recording...")
            
            try:
                audio, elapsed = record_manual_control(
                    device_pick.index, 
                    device_pick.samplerate, 
                    device_pick.wasapi_loopback
                )
                
                if elapsed < 0.5:
                    print("⚠ Too short, try again")
                    continue
                    
            except Exception as e:
                print(f"⚠ Recording failed: {e}")
                continue

            # Fast transcription
            print("⚡ Transcribing...")
            text = transcribe_chunk(model, audio, device_pick.samplerate)
            
            if not text or text == "(no speech detected)":
                print("⚠ No speech detected")
                continue
                
            # Show question with wrapping
            print(f"\n🎤 QUESTION:")
            print(textwrap.fill(text, width=min(shutil.get_terminal_size().columns - 4, 100)))
            print(f"\n🤖 RESPONSE:")
            print("-" * min(shutil.get_terminal_size().columns - 4, 100))
            
            # Response generation with interrupt and word wrapping
            stop_generation = threading.Event()
            
            def watch_for_space():
                try:
                    import msvcrt
                    while not stop_generation.is_set():
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b' ':
                                stop_generation.set()
                                print("\n\n⏹ INTERRUPTED")
                                return
                        time.sleep(0.01)
                except ImportError:
                    # For non-Windows systems, you could implement alternative interrupt handling
                    pass

            interrupt_thread = threading.Thread(target=watch_for_space, daemon=True)
            interrupt_thread.start()
            
            # Generate wrapped response
            response_text, word_count = print_wrapped_response(
                llm, text, context, job_description, stop_generation
            )
            
            if not stop_generation.is_set():
                print(f"\n✓ Complete ({word_count} words)")
            
            print("-" * min(shutil.get_terminal_size().columns - 4, 100))

    except KeyboardInterrupt:
        print(f"\n\nSession ended. Answered {question_count-1} questions.")

def main():
    try:
        device_pick, model, llm, context, job_description = show_startup_info()
        run_interview_session(device_pick, model, llm, context, job_description)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()