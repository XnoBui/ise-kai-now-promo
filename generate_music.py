#!/usr/bin/env python3
"""Generate a short upbeat electronic synth track for promo (~30s, 120bpm)."""
import wave
import math
import struct

SAMPLE_RATE = 44100
DURATION = 30  # seconds
BPM = 120
BEAT = SAMPLE_RATE * 60 / BPM  # samples per beat

def make_sine(freq, duration, volume=0.5, phase=0):
    frames = int(duration * SAMPLE_RATE)
    data = []
    for i in range(frames):
        t = (i / SAMPLE_RATE) + phase
        val = math.sin(2 * math.pi * freq * t) * volume
        data.append(val)
    return data

def make_saw(freq, duration, volume=0.3):
    frames = int(duration * SAMPLE_RATE)
    data = []
    period = SAMPLE_RATE / freq
    for i in range(frames):
        t = i / SAMPLE_RATE
        val = 2 * (t * freq - math.floor(t * freq + 0.5)) * volume
        data.append(val)
    return data

def mix_tracks(tracks, master_vol=0.8):
    length = max(len(t) for t in tracks)
    mixed = [0.0] * length
    for track in tracks:
        for i, v in enumerate(track):
            if i < length:
                mixed[i] += v
    # normalize
    max_val = max(abs(v) for v in mixed) or 1
    return [v * master_vol / max_val for v in mixed]

def to_wav(filename, samples):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(max(min(s, 1), -1) * 32767)))

# Upbeat energetic melody: bass + lead + arpeggio
print("Generating upbeat synth track...")

# Bass line (low saw)
bass_freqs = [110, 110, 130.8, 146.8] * 8  # A2, A2, C3, D3 etc
bass = []
for i, f in enumerate(bass_freqs):
    bass += make_saw(f, 0.5, 0.4)

# Lead melody (sine higher)
lead_notes = [440, 523.25, 659.25, 783.99, 659.25, 523.25] * 5  # A4 C5 E5 G5
lead = []
for f in lead_notes:
    lead += make_sine(f, 0.25, 0.35)

# Pad / chords low
pad = make_sine(220, DURATION, 0.15)  # simple pad

# Hi-hat like noise bursts (short high freq)
hihat = [0.0] * int(DURATION * SAMPLE_RATE)
for beat in range(int(BPM * DURATION / 60 * 2)):  # 8th notes
    pos = int(beat * BEAT / 2)
    if pos < len(hihat):
        for j in range(int(0.05 * SAMPLE_RATE)):
            if pos + j < len(hihat):
                hihat[pos + j] += math.sin(2 * math.pi * 8000 * (j / SAMPLE_RATE)) * 0.2 * math.exp(-j / 200)

tracks = [bass[:int(DURATION*SAMPLE_RATE)], lead[:int(DURATION*SAMPLE_RATE)], pad, hihat]
mixed = mix_tracks(tracks, 0.85)
to_wav("upbeat_promo.wav", mixed)
print("Created upbeat_promo.wav (30s energetic synth)")