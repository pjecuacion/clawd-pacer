"""The floating window: see-through, always on top, draggable, animated.

Layout (top to bottom): speech-bubble area, Clawd, info panel.
"""
import random
import tkinter as tk
from dataclasses import dataclass
from typing import Callable

from clawd_pacer.animator import TICK_MS, Animator
from clawd_pacer.bubble import clear_bubble, draw_bubble
from clawd_pacer.config import BUBBLE_SECONDS
from clawd_pacer.sprite import COLS, ROWS, draw_clawd
from clawd_pacer.status import Status

KEY = "#FF00FF"          # this color becomes see-through (and click-through)
PANEL = "#2B2522"
PX = 6                   # size of one Clawd pixel
WIDTH = 170
BUBBLE_H = 64            # space reserved above Clawd for the bubble
SPRITE_X = (WIDTH - COLS * PX) // 2
SPRITE_Y = BUBBLE_H + 10
CLICK_SLOP = 4           # moved less than this = a click (poke), not a drag


@dataclass(frozen=True)
class Callbacks:
    refresh: Callable[[], None]
    quit: Callable[[], None]
    poke: Callable[[], None]
    mute: Callable[[bool], None]


class PetWindow:
    def __init__(self, root: tk.Tk, cb: Callbacks):
        self.root, self.cb = root, cb
        self.mood = "sleepy"
        self.animator = Animator(random.Random())
        self._bubble_job = None
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-transparentcolor", KEY)
        root.configure(bg=KEY)
        self.canvas = tk.Canvas(root, width=WIDTH, height=SPRITE_Y + ROWS * PX + 4,
                                bg=KEY, highlightthickness=0)
        self.canvas.pack()
        self.label = tk.Label(root, bg=PANEL, fg="white", padx=8, pady=4,
                              font=("Segoe UI", 9), justify="center",
                              wraplength=WIDTH - 16)
        self.label.pack(fill="x")
        self._menu()
        self._mouse_bindings()
        self._place_bottom_right()
        self._animate()

    def show(self, status: Status) -> None:
        self.mood = status.mood
        self.label.config(text=f"{status.line1}\n{status.line2}")

    def act(self, text: str, pose: str) -> None:
        """Say something in a bubble and do a move (wave / hop / idle)."""
        draw_bubble(self.canvas, text, WIDTH // 2, BUBBLE_H, WIDTH)
        self.animator.start(pose)
        if self._bubble_job:
            self.root.after_cancel(self._bubble_job)
        self._bubble_job = self.root.after(BUBBLE_SECONDS * 1000,
                                           lambda: clear_bubble(self.canvas))

    def _animate(self) -> None:
        pose, dy = self.animator.tick()
        draw_clawd(self.canvas, self.mood, SPRITE_X, SPRITE_Y + dy, PX, pose)
        self.root.after(TICK_MS, self._animate)

    def _menu(self) -> None:
        self.muted = tk.BooleanVar(value=False)
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Refresh now", command=self.cb.refresh)
        menu.add_checkbutton(label="Mute sounds", variable=self.muted,
                             command=lambda: self.cb.mute(self.muted.get()))
        menu.add_separator()
        menu.add_command(label="Quit", command=self.cb.quit)
        for w in (self.canvas, self.label):
            w.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    def _mouse_bindings(self) -> None:
        for w in (self.canvas, self.label):
            w.bind("<Button-1>", self._press)
            w.bind("<B1-Motion>", self._drag)
            w.bind("<ButtonRelease-1>", self._release)

    def _press(self, e) -> None:
        self._start = (e.x_root, e.y_root)
        self._dx = e.x_root - self.root.winfo_x()
        self._dy = e.y_root - self.root.winfo_y()

    def _drag(self, e) -> None:
        self.root.geometry(f"+{e.x_root - self._dx}+{e.y_root - self._dy}")

    def _release(self, e) -> None:
        sx, sy = self._start
        if abs(e.x_root - sx) < CLICK_SLOP and abs(e.y_root - sy) < CLICK_SLOP:
            self.cb.poke()

    def _place_bottom_right(self) -> None:
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - WIDTH - 40
        y = self.root.winfo_screenheight() - self.root.winfo_height() - 90
        self.root.geometry(f"+{x}+{y}")
