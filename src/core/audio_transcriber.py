from __future__ import annotations

import queue
import sys
import threading
import time
from typing import Tuple, Optional, List

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


# Keep a global model singleton
_model_lock = threading.Lock()
_model_singleton: Optional[WhisperModel] = None


def load_whisper(model_size: str = None) -> WhisperModel:
    """
    Load Whisper model with stable defaults.
    """
    global _model_singleton
    with _model_lock:
        if _model_singleton is None:
            size = model_size or "large"  # Use large for better accuracy
            print(f"Loading Whisper model: {size}")
            _model_singleton = WhisperModel(size, device="cpu", compute_type="int8")
        return _model_singleton


def _kbhit_enter(stop_event: threading.Event):
    """
    Cross-platform 'press Enter to stop' watcher.
    """
    try:
        import msvcrt  # Windows only
        while not stop_event.is_set():
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch == "\r" or ch == "\n":
                    stop_event.set()
                    return
            time.sleep(0.02)
    except ImportError:
        # Fallback for non-Windows: blocking read
        try:
            sys.stdin.readline()
            stop_event.set()
        except:
            pass


def record_until_enter(
    device_index: int,
    samplerate: int,
    channels: int = 2,
    blocksize: int = 2048,
    wasapi_loopback: bool = False,
) -> Tuple[np.ndarray, float]:
    """
    Records audio from the selected device until Enter is pressed.
    Fixed to properly handle WASAPI loopback.
    """
    q_frames: "queue.Queue[np.ndarray]" = queue.Queue()
    stop = threading.Event()
    t = threading.Thread(target=_kbhit_enter, args=(stop,), daemon=True)
    t.start()

    # Capture callback
    def _cb(indata, frames, time_info, status):
        if status:
            # Log but don't crash on minor audio issues
            pass
        q_frames.put(indata.copy())

    # Configure stream parameters based on loopback mode
    if wasapi_loopback:
        # For WASAPI loopback: capture from output device
        stream_params = {
            'device': (None, device_index),  # (input_device, output_device)
            'samplerate': samplerate,
            'channels': channels,
            'dtype': 'float32',
            'blocksize': blocksize,
            'callback': _cb,
            'extra_settings': sd.WasapiSettings(loopback=True)
        }
    else:
        # For regular input devices
        stream_params = {
            'device': device_index,
            'samplerate': samplerate,
            'channels': channels,
            'dtype': 'float32',
            'blocksize': blocksize,
            'callback': _cb,
        }

    # Try to open stream with preferred settings
    stream = None
    try:
        stream = sd.InputStream(**stream_params)
        stream.start()
    except Exception as e:
        print(f"Failed to open stream with {channels} channels: {e}")
        # Fallback: try with mono
        if stream:
            stream.close()
        
        if wasapi_loopback:
            stream_params.update({
                'channels': 1,
            })
        else:
            stream_params.update({
                'channels': 1,
            })
        
        try:
            stream = sd.InputStream(**stream_params)
            stream.start()
            channels = 1  # Update for later processing
        except Exception as e2:
            print(f"Failed to open stream with mono: {e2}")
            raise

    print(f"Recording from device {device_index} ({'loopback' if wasapi_loopback else 'input'})...")
    
    start = time.time()
    frames: List[np.ndarray] = []
    
    try:
        while not stop.is_set():
            try:
                item = q_frames.get(timeout=0.1)
                frames.append(item)
            except queue.Empty:
                pass
    finally:
        stream.stop()
        stream.close()

    elapsed = time.time() - start
    print(f"Recorded {elapsed:.1f} seconds of audio")
    
    if not frames:
        return np.zeros((1, 1), dtype=np.float32), elapsed

    # Concatenate all audio frames
    chunk = np.concatenate(frames, axis=0)  # shape (N, channels)
    
    # Convert to mono if needed
    if chunk.ndim == 2 and chunk.shape[1] > 1:
        chunk = np.mean(chunk, axis=1, keepdims=True)
    elif chunk.ndim == 1:
        chunk = chunk.reshape(-1, 1)
        
    return chunk.astype(np.float32), elapsed


def transcribe_chunk(model: WhisperModel, audio_mono: np.ndarray, input_rate: int) -> str:
    """
    Transcribe audio chunk with proper preprocessing.
    """
    # Ensure we have the right shape
    if audio_mono.ndim == 2:
        audio = audio_mono[:, 0]  # Take first channel
    else:
        audio = audio_mono
    
    # Check for silence
    rms = np.sqrt(np.mean(np.square(audio)))
    if rms < 1e-4:  # Very quiet audio
        return "(no speech detected)"
    
    # Resample to 16000 Hz for Whisper
    target_sr = 16000
    if input_rate != target_sr:
        # Simple linear interpolation resampling
        import math
        ratio = target_sr / float(input_rate)
        new_length = int(math.ceil(len(audio) * ratio))
        
        # Create new time indices
        old_indices = np.linspace(0, len(audio) - 1, len(audio))
        new_indices = np.linspace(0, len(audio) - 1, new_length)
        
        # Interpolate
        audio16 = np.interp(new_indices, old_indices, audio).astype(np.float32)
    else:
        audio16 = audio.astype(np.float32)

    # Transcribe with Whisper
    try:
        segments, info = model.transcribe(
            audio16,
            language="en",
            temperature=0.0,
            beam_size=1,
            best_of=1,
            vad_filter=False,  # Keep consistent across versions
        )
        
        # Collect transcription text
        text_parts = []
        for seg in segments:
            if seg.text.strip():
                text_parts.append(seg.text.strip())
        
        text = " ".join(text_parts).strip()
        return text if text else "(no speech detected)"
        
    except Exception as e:
        print(f"Transcription error: {e}")
        return "(transcription failed)"