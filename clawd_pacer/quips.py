"""Cheerful-coach lines. Placeholders: {used} {target} {room} {day}."""
import random

QUIPS = {
    "greeting": [
        "Hi there! Today's budget: 14%. Let's make it count!",
        "New day, fresh claws! {room}% of room today.",
        "Day {day}, let's go! You've got this.",
    ],
    "happy": [
        "We're cruising! {used}% used, goal {target}%.",
        "Snip snip, nicely under pace!",
        "Look at you, pacing like a pro.",
        "Plenty of room left. Go build something!",
    ],
    "ok": [
        "Right on pace. Steady claws!",
        "Balanced like a crab on a rock.",
        "{room}% left today. Smooth sailing.",
    ],
    "worried": [
        "Easy there... {used}% already!",
        "Maybe a coffee break? We're ahead of pace.",
        "Pace check: {used}% vs goal {target}%. Slow and steady!",
    ],
    "sleepy": [
        "zzz... can't see your usage right now.",
        "*yawn* Poke Claude Code and I'll wake up.",
    ],
    "over_pace": ["Uh-oh, we just went over pace. Deep breaths!"],
    "back_on_pace": ["Back on track! Nice recovery."],
    "reset": ["New week, new limits! Fresh start!"],
    "day_win": ["Day done under budget! Claws up!"],
    "poke": [
        "Hey! That tickles.",
        "Boop! Need something?",
        "*happy crab noises*",
        "Still here, still counting.",
        "{used}% this week. You're doing fine.",
    ],
}


class QuipPicker:
    """Random line per category, never the same line twice in a row."""

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.last = {}

    def pick(self, category: str, **values) -> str:
        lines = QUIPS[category]
        choices = [l for l in lines if l != self.last.get(category)] or lines
        line = self.rng.choice(choices)
        self.last[category] = line
        return line.format(**values)
