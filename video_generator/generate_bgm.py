"""
generate_bgm.py
Synthesizes a warm, inspiring, low-fi tech ambient background track.
"""

import numpy as np
from scipy.io import wavfile
import subprocess
import imageio_ffmpeg
import os

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "audio")

def generate_ambient_track(duration_sec=190, sample_rate=44100):
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # Chord frequencies (Hz) for an uplifting ambient progression:
    # Cmaj9 -> Am9 -> Fmaj7 -> Gsus4/add9
    chords = [
        [130.81, 164.81, 196.00, 246.94, 293.66],  # C, E, G, B, D
        [110.00, 130.81, 164.81, 196.00, 246.94],  # A, C, E, G, B
        [87.31, 130.81, 174.61, 220.00, 261.63],   # F, C, F, A, C
        [98.00, 146.83, 196.00, 220.00, 293.66]    # G, D, G, A, D
    ]
    
    chord_duration = 6.0  # seconds per chord
    audio_left = np.zeros_like(t)
    audio_right = np.zeros_like(t)
    
    num_chords = int(duration_sec / chord_duration) + 1
    
    for i in range(num_chords):
        chord = chords[i % len(chords)]
        start_idx = int(i * chord_duration * sample_rate)
        end_idx = min(len(t), int((i + 1) * chord_duration * sample_rate))
        chunk_len = end_idx - start_idx
        if chunk_len <= 0:
            break
            
        t_chunk = np.linspace(0, chunk_len / sample_rate, chunk_len, False)
        # Smooth attack-decay envelope
        envelope = np.sin(np.pi * np.linspace(0, 1, chunk_len)) ** 1.5
        
        chord_wave_l = np.zeros(chunk_len)
        chord_wave_r = np.zeros(chunk_len)
        
        for idx, freq in enumerate(chord):
            # Rich soft pad with sub-harmonics
            w1 = np.sin(2 * np.pi * freq * t_chunk)
            w2 = 0.4 * np.sin(2 * np.pi * (freq * 1.002) * t_chunk)  # Chorus detune
            w3 = 0.25 * np.sin(2 * np.pi * (freq * 2.0) * t_chunk)   # Octave harmonic
            
            pan = (idx / len(chord))  # Stereo spread
            chord_wave_l += (w1 + w2 + w3) * (1 - pan * 0.4)
            chord_wave_r += (w1 + w2 + w3) * (0.6 + pan * 0.4)
            
        audio_left[start_idx:end_idx] += chord_wave_l * envelope * 0.18
        audio_right[start_idx:end_idx] += chord_wave_r * envelope * 0.18

    # Add gentle high-pass / low-pass warmth
    audio_stereo = np.vstack([audio_left, audio_right]).T
    
    # Global Fade-in (2s) and Fade-out (3s)
    fade_in_len = sample_rate * 2
    fade_out_len = sample_rate * 4
    audio_stereo[:fade_in_len] *= np.linspace(0, 1, fade_in_len)[:, None]
    audio_stereo[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)[:, None]
    
    # Normalize to prevent clipping
    max_val = np.max(np.abs(audio_stereo))
    if max_val > 0:
        audio_stereo = audio_stereo / max_val * 0.85
        
    wav_path = os.path.join(OUTPUT_DIR, "ambient_bgm.wav")
    mp3_path = os.path.join(OUTPUT_DIR, "ambient_bgm.mp3")
    
    wavfile.write(wav_path, sample_rate, (audio_stereo * 32767).astype(np.int16))
    
    # Convert to MP3 using ffmpeg
    subprocess.run([
        FFMPEG_EXE, "-y", "-i", wav_path,
        "-codec:a", "libmp3lame", "-qscale:a", "2",
        mp3_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(wav_path):
        os.remove(wav_path)
        
    print(f"✅ Generated background music: {mp3_path}")

if __name__ == "__main__":
    generate_ambient_track()

