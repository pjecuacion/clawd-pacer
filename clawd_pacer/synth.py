"""Tiny synthesizer: turn tone segments into WAV bytes. Pure, no audio device."""
import io
import math
import struct
import wave
from dataclasses import dataclass

RATE = 22050
FADE_MS = 5


@dataclass(frozen=True)
class Tone:
    start_hz: float      # 0 = silence
    end_hz: float        # sweep to this pitch
    ms: int
    volume: float = 0.25


def rest(ms: int) -> Tone:
    return Tone(0, 0, ms, 0)


def _samples(tone: Tone):
    n = int(RATE * tone.ms / 1000)
    fade = int(RATE * FADE_MS / 1000) or 1
    phase = 0.0
    for i in range(n):
        if tone.start_hz <= 0:
            yield 0.0
            continue
        hz = tone.start_hz + (tone.end_hz - tone.start_hz) * i / max(n - 1, 1)
        phase += 2 * math.pi * hz / RATE
        edge = min(1.0, i / fade, (n - 1 - i) / fade)   # soft edges, no clicks
        yield math.sin(phase) * tone.volume * edge


def render(tones) -> bytes:
    """Return a complete mono 16-bit WAV file as bytes."""
    frames = bytearray()
    for tone in tones:
        for s in _samples(tone):
            frames += struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767))
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(bytes(frames))
    return buf.getvalue()
