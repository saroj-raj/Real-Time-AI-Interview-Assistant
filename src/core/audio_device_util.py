from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import List, Optional

import sounddevice as sd
import numpy as np


@dataclass
class DevicePick:
    index: int
    samplerate: int
    name: str
    hostapi_name: str
    wasapi_loopback: bool  # True only if hostapi is WASAPI on an output device


def _hostapi_name(hostapi_index: int) -> str:
    try:
        return sd.query_hostapis(hostapi_index)["name"]
    except Exception:
        return "Unknown"


def _safe_default_samplerate(dev: dict, prefer: int = 48000) -> int:
    sr = int(dev.get("default_samplerate") or 0)
    return sr if sr > 0 else prefer


def _test_loopback_device(device_index: int, samplerate: int, test_duration: float = 0.3) -> bool:
    """
    Test if a WASAPI loopback device is working and has active audio.
    """
    try:
        frames = []
        
        def callback(indata, frames_count, time_info, status):
            if indata.size > 0:
                # Convert to mono if stereo
                mono = np.mean(indata, axis=1) if indata.ndim > 1 else indata
                frames.append(mono)
        
        # Test WASAPI loopback
        with sd.InputStream(
            device=(None, device_index),  # Input from output device
            samplerate=samplerate,
            channels=2,
            dtype='float32',
            callback=callback,
            extra_settings=sd.WasapiSettings(loopback=True)
        ):
            time.sleep(test_duration)
        
        if not frames:
            return False
        
        # Check if there's actual audio activity
        audio = np.concatenate(frames)
        rms = np.sqrt(np.mean(np.square(audio)))
        
        # Consider it working if there's some audio activity above noise floor
        return rms > 1e-6
        
    except Exception:
        return False


def _test_input_device(device_index: int, samplerate: int) -> bool:
    """
    Test if a regular input device can be opened.
    """
    try:
        with sd.InputStream(
            device=device_index,
            samplerate=samplerate,
            channels=1,
            dtype='float32',
            blocksize=512
        ):
            time.sleep(0.1)
        return True
    except Exception:
        return False


def pick_system_audio_device(prefer_rate: int = 48000) -> DevicePick:
    """
    Enhanced device picker that actually tests devices.
    Strategy:
      1) If FORCE_DEVICE_INDEX is set, use that.
      2) Test WASAPI output devices for loopback capability with active audio.
      3) Test virtual capture inputs (CABLE Output / Voicemeeter / Stereo Mix).
      4) Fallback to any working input device.
    """
    force_idx = os.environ.get("FORCE_DEVICE_INDEX", "").strip()
    if force_idx.isdigit():
        i = int(force_idx)
        d = sd.query_devices(i)
        host = _hostapi_name(d.get("hostapi", 0))
        wasapi_loopback = ("WASAPI" in host) and (d.get("max_output_channels", 0) > 0)
        return DevicePick(
            index=i,
            samplerate=_safe_default_samplerate(d, prefer_rate),
            name=d.get("name", f"device {i}"),
            hostapi_name=host,
            wasapi_loopback=wasapi_loopback,
        )

    devices = sd.query_devices()
    print("Scanning for system audio devices...")

    # 1) WASAPI speakers (loopback capture) - test for active audio
    working_loopbacks: List[DevicePick] = []
    for i, d in enumerate(devices):
        host = _hostapi_name(d.get("hostapi", 0))
        name = d.get("name", "")
        
        if "WASAPI" in host and d.get("max_output_channels", 0) > 0:
            # Prioritize certain device names
            is_priority = re.search(r"(Speakers|Headphones|Realtek|Output|Default)", name, re.I)
            
            if is_priority or "loopback" in name.lower():
                samplerate = _safe_default_samplerate(d, prefer_rate)
                
                print(f"Testing WASAPI loopback: {name} @ {samplerate}Hz...")
                if _test_loopback_device(i, samplerate):
                    print(f"  ✓ Active audio detected")
                    working_loopbacks.append(DevicePick(
                        index=i,
                        samplerate=samplerate,
                        name=name,
                        hostapi_name=host,
                        wasapi_loopback=True,
                    ))
                else:
                    print(f"  ✗ No active audio")

    # 2) Virtual inputs - test for functionality
    working_virtuals: List[DevicePick] = []
    for i, d in enumerate(devices):
        host = _hostapi_name(d.get("hostapi", 0))
        name = d.get("name", "")
        
        if d.get("max_input_channels", 0) > 0:
            # Look for virtual audio devices
            is_virtual = re.search(
                r"(CABLE Output|VB-Audio|Voicemeeter Out|Stereo Mix|Virtual|Monitor)", 
                name, re.I
            )
            
            if is_virtual:
                samplerate = _safe_default_samplerate(d, prefer_rate)
                
                print(f"Testing virtual input: {name} @ {samplerate}Hz...")
                if _test_input_device(i, samplerate):
                    print(f"  ✓ Device accessible")
                    working_virtuals.append(DevicePick(
                        index=i,
                        samplerate=samplerate,
                        name=name,
                        hostapi_name=host,
                        wasapi_loopback=False,
                    ))
                else:
                    print(f"  ✗ Device not accessible")

    # Return best available option
    if working_loopbacks:
        choice = working_loopbacks[0]
        print(f"Selected: WASAPI loopback from {choice.name}")
        return choice
        
    if working_virtuals:
        choice = working_virtuals[0]
        print(f"Selected: Virtual input {choice.name}")
        return choice

    # 3) Fallback: any input device that works
    print("Falling back to any available input device...")
    for i, d in enumerate(devices):
        if d.get("max_input_channels", 0) > 0:
            host = _hostapi_name(d.get("hostapi", 0))
            samplerate = _safe_default_samplerate(d, prefer_rate)
            
            if _test_input_device(i, samplerate):
                return DevicePick(
                    index=i,
                    samplerate=samplerate,
                    name=d.get("name", f"device {i}"),
                    hostapi_name=host,
                    wasapi_loopback=False,
                )

    # Last resort: default device
    print("Using system default device...")
    try:
        default_info = sd.query_devices(None, 'input')
        return DevicePick(
            index=0,
            samplerate=prefer_rate,
            name=default_info.get("name", "Default Input"),
            hostapi_name=_hostapi_name(default_info.get("hostapi", 0)),
            wasapi_loopback=False,
        )
    except:
        # Really last resort
        return DevicePick(
            index=0,
            samplerate=prefer_rate,
            name="Default Device",
            hostapi_name="Unknown",
            wasapi_loopback=False,
        )


def pretty_selection(p: DevicePick) -> str:
    if p.wasapi_loopback:
        mode_desc = "WASAPI speaker loopback (captures system audio directly)"
        setup_note = "Captures whatever is playing through your speakers"
    else:
        mode_desc = "Audio input device"
        setup_note = "Route your meeting/browser audio to this device"
    
    return (
        f"Selected: {p.name}\n"
        f"Host API: {p.hostapi_name}\n"
        f"Mode    : {mode_desc}\n"
        f"Setup   : {setup_note}\n"
        f"Index   : {p.index} @ {p.samplerate} Hz"
    )


def list_all_devices():
    """Debug function to list all audio devices"""
    devices = sd.query_devices()
    print("\n=== ALL AUDIO DEVICES ===")
    for i, d in enumerate(devices):
        name = d.get('name', 'Unknown')
        host = _hostapi_name(d.get('hostapi', 0))
        max_in = d.get('max_input_channels', 0)
        max_out = d.get('max_output_channels', 0)
        sr = d.get('default_samplerate', 0)
        
        io_str = []
        if max_in > 0:
            io_str.append(f"IN:{max_in}")
        if max_out > 0:
            io_str.append(f"OUT:{max_out}")
        io_info = "/".join(io_str) if io_str else "NONE"
        
        print(f"{i:2d}: {name[:50]:<50} [{host}] {io_info} @{sr}Hz")


if __name__ == "__main__":
    # Test the device picker
    try:
        pick = pick_system_audio_device()
        print("\n" + "="*60)
        print(pretty_selection(pick))
        print("="*60)
    except Exception as e:
        print(f"Error: {e}")
        print("\nAll devices:")
        list_all_devices()