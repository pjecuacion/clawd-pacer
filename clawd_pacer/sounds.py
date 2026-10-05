"""Clawd's sound library: named recipes made of Tones. Pure; rng passed in."""
import random

from clawd_pacer.synth import Tone, rest

C5, E5, G5, C6, E6 = 523, 659, 784, 1047, 1319


def beeps(rng: random.Random):
    """R2-D2 style babble: 4-6 quick random pitches."""
    out = []
    for _ in range(rng.randint(4, 6)):
        a, b = rng.randint(800, 2400), rng.randint(800, 2400)
        out += [Tone(a, b, rng.randint(50, 90)), rest(25)]
    return out


def chirp(rng: random.Random):
    """Bird-ish double chirp."""
    base = rng.randint(1900, 2300)
    return [Tone(base, base + 1200, 60), rest(45), Tone(base + 200, base + 1400, 70)]


def click(rng: random.Random):
    """Crab claw snaps."""
    out = []
    for _ in range(rng.randint(2, 4)):
        out += [Tone(3200, 2600, 12, 0.3), rest(rng.randint(60, 110))]
    return out


def boop(rng: random.Random):
    return [Tone(650, 320, 130)]


def jingle(rng: random.Random):
    return [Tone(n, n, 110) for n in (C5, E5, G5, C6)]


def celebrate(rng: random.Random):
    up = [Tone(n, n, 80) for n in (C5, E5, G5, C6)]
    return up + [rest(60)] + up[2:] + [Tone(E6, E6, 220)]


def uhoh(rng: random.Random):
    return [Tone(700, 680, 150), rest(70), Tone(520, 430, 260)]


def yawn(rng: random.Random):
    return [Tone(520, 240, 450, 0.18)]


SOUNDS = {
    "beeps": beeps, "chirp": chirp, "click": click, "boop": boop,
    "jingle": jingle, "celebrate": celebrate, "uhoh": uhoh, "yawn": yawn,
}
CHATTER_SOUNDS = ("beeps", "chirp", "click")


def recipe(name: str, rng: random.Random):
    """Tones for a sound name. Unknown names raise KeyError (a bug, not user input)."""
    return SOUNDS[name](rng)
