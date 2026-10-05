"""Wires everything: fetch in a background thread, react on the UI thread."""
import queue
import random
import threading
import tkinter as tk
from datetime import datetime, timezone

from clawd_pacer.config import POLL_SECONDS
from clawd_pacer.credentials import CredentialsError, load_token
from clawd_pacer.personality import Action, Personality
from clawd_pacer.player import Player
from clawd_pacer.status import Status, build_status, error_status
from clawd_pacer.usage_client import UsageError, fetch_usage
from clawd_pacer.window import Callbacks, PetWindow

CHATTER_CHECK_MS = 30_000
EVENT_GAP_MS = 3_500     # space out several reactions so each can be read


def get_status() -> Status:
    """One full check: token -> server -> status. Never raises."""
    try:
        usage = fetch_usage(load_token())
    except (CredentialsError, UsageError) as e:
        return error_status(str(e))
    return build_status(usage, datetime.now(timezone.utc))


class App:
    def __init__(self):
        rng = random.Random()
        self.root = tk.Tk()
        self.results: "queue.Queue[Status]" = queue.Queue()
        self.personality = Personality(rng)
        self.player = Player(rng)
        self.window = PetWindow(self.root, Callbacks(
            refresh=self.refresh, quit=self.root.destroy,
            poke=lambda: self._do(self.personality.poke()),
            mute=self._set_mute))
        self.window.show(error_status("checking..."))

    def refresh(self) -> None:
        threading.Thread(target=lambda: self.results.put(get_status()),
                         daemon=True).start()

    def _set_mute(self, muted: bool) -> None:
        self.player.muted = muted

    def _do(self, action: Action) -> None:
        self.window.act(action.text, action.pose)
        if action.sound:
            self.player.play(action.sound)

    def _poll_loop(self) -> None:
        self.refresh()
        self.root.after(POLL_SECONDS * 1000, self._poll_loop)

    def _chatter_loop(self) -> None:
        action = self.personality.tick(datetime.now())
        if action:
            self._do(action)
        self.root.after(CHATTER_CHECK_MS, self._chatter_loop)

    def _drain(self) -> None:
        while not self.results.empty():
            status = self.results.get()
            self.window.show(status)
            actions = self.personality.on_status(status, datetime.now())
            for i, action in enumerate(actions):
                self.root.after(i * EVENT_GAP_MS, self._do, action)
        self.root.after(500, self._drain)

    def run(self) -> None:
        self._poll_loop()
        self._chatter_loop()
        self._drain()
        self.root.mainloop()
