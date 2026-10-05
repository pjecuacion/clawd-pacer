"""
Purpose: check quip picking and that every line formats with real numbers.
Expected: no line repeats twice in a row; placeholders always filled.
Related: plan v0.2.0 (docs/tasks/todo.md). No bug/lesson ID.
Preconditions: none. Seeded random.Random only.
"""
import random

import pytest

from clawd_pacer.quips import QUIPS, QuipPicker

VALUES = {"used": 20, "target": 16, "room": 8, "day": 2}


@pytest.mark.parametrize("category", sorted(QUIPS))
def test_every_line_formats(category):
    for line in QUIPS[category]:
        text = line.format(**VALUES)
        assert "{" not in text and len(text) <= 60
        assert text.isascii()          # emoji can break Tk 8.6 on Windows


def test_no_immediate_repeats():
    picker = QuipPicker(random.Random(3))
    lines = [picker.pick("poke", **VALUES) for _ in range(50)]
    assert all(a != b for a, b in zip(lines, lines[1:]))


def test_single_line_category_still_works():
    picker = QuipPicker(random.Random(3))
    assert picker.pick("reset", **VALUES) == picker.pick("reset", **VALUES)
