"""
Purpose: check the tiny synthesizer and that every named sound renders.
Expected: valid mono 16-bit WAV, right length, same bytes for same seed.
Related: plan v0.2.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. No audio device used; nothing is played.
"""
import io
import random
import wave

import pytest

from clawd_pacer.sounds import SOUNDS, recipe
from clawd_pacer.synth import RATE, Tone, render, rest


def read(data: bytes):
    w = wave.open(io.BytesIO(data))
    return w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()


def test_render_valid_wav_with_expected_length():
    ch, width, rate, frames = read(render([Tone(440, 880, 100), rest(50)]))
    assert (ch, width, rate) == (1, 2, RATE)
    assert frames == int(RATE * 0.1) + int(RATE * 0.05)


def test_silence_is_all_zero():
    data = render([rest(20)])
    w = wave.open(io.BytesIO(data))
    assert set(w.readframes(w.getnframes())) == {0}


@pytest.mark.parametrize("name", sorted(SOUNDS))
def test_every_sound_renders_and_is_short(name):
    *_, frames = read(render(recipe(name, random.Random(1))))
    assert 0 < frames / RATE < 1.5     # never a long, annoying noise


def test_same_seed_same_sound():
    a = render(recipe("beeps", random.Random(7)))
    b = render(recipe("beeps", random.Random(7)))
    assert a == b
