"""Play sounds without freezing the window. Windows only; silent elsewhere."""
import random
import threading

from clawd_pacer.sounds import recipe
from clawd_pacer.synth import render

try:
    import winsound
except ImportError:          # not Windows: stay quiet
    winsound = None


class Player:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.muted = False

    def play(self, name: str) -> None:
        if self.muted or winsound is None:
            return
        data = render(recipe(name, self.rng))
        threading.Thread(target=self._play_bytes, args=(data,),
                         daemon=True).start()

    @staticmethod
    def _play_bytes(data: bytes) -> None:
        try:
            winsound.PlaySound(data, winsound.SND_MEMORY)
        except RuntimeError:  # no audio device: ignore
            pass
