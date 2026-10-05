"""Frame-by-frame idle life: bob, blink, wave, hop. Pure (no UI)."""
import random

TICK_MS = 350          # one animation frame
WAVE_CHANCE = 1 / 250  # random wave about every 90 s


class Animator:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.frame = 0
        self.wave_left = 0
        self.hop_left = 0
        self.blink_in = rng.randint(12, 22)

    def start(self, pose: str) -> None:
        if pose == "hop":
            self.hop_left = 4
        elif pose == "wave":
            self.wave_left = 6

    def tick(self):
        """Advance one frame. Returns (pose, y_offset_px)."""
        self.frame += 1
        dy = 2 if (self.frame // 2) % 2 else 0          # gentle bob
        if self.hop_left:
            self.hop_left -= 1
            dy = -8 if self.hop_left % 2 else 0
        if not self.wave_left and self.rng.random() < WAVE_CHANCE:
            self.wave_left = 6
        if self.wave_left:
            self.wave_left -= 1
            return ("wave" if self.wave_left % 2 else "idle"), dy
        self.blink_in -= 1
        if self.blink_in <= 0:
            self.blink_in = self.rng.randint(12, 22)
            return "blink", dy
        return "idle", dy
