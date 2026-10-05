"""Pixel-art Clawd drawn on a tkinter Canvas. One face per mood."""

ORANGE = "#D97757"
EYE = "#1F1A17"
SWEAT = "#7EC8F0"

# 12 x 8 body. '#' = orange pixel, '.' = empty.
BODY = [
    ".##########.",
    ".##########.",
    ".##########.",
    "############",
    "############",
    ".##########.",
    ".#.#....#.#.",
    ".#.#....#.#.",
]

# (row, col, color) pixels painted on top of the body for each mood.
FACES = {
    "ok": [(1, 3, EYE), (2, 3, EYE), (1, 8, EYE), (2, 8, EYE)],
    "happy": [(2, 2, EYE), (1, 3, EYE), (2, 4, EYE),
              (2, 7, EYE), (1, 8, EYE), (2, 9, EYE)],
    "worried": [(1, 3, EYE), (2, 3, EYE), (1, 8, EYE), (2, 8, EYE),
                (0, 11, SWEAT), (1, 11, SWEAT)],
    "sleepy": [(2, 2, EYE), (2, 3, EYE), (2, 8, EYE), (2, 9, EYE)],
}

COLS, ROWS = len(BODY[0]), len(BODY)

CLOSED_EYES = [(2, 2, EYE), (2, 3, EYE), (2, 8, EYE), (2, 9, EYE)]
# Wave: arms move from rows 3-4 up to rows 1-2.
ARMS_DOWN = {(3, 0), (4, 0), (3, 11), (4, 11)}
ARMS_UP = {(1, 0), (2, 0), (1, 11), (2, 11)}


def face_pixels(mood: str):
    """Pixels for a mood; unknown moods fall back to 'ok'."""
    return FACES.get(mood, FACES["ok"])


def body_pixels(pose: str = "idle"):
    """Set of (row, col) orange pixels for a pose."""
    cells = {(r, c) for r, line in enumerate(BODY)
             for c, ch in enumerate(line) if ch == "#"}
    return (cells - ARMS_DOWN) | ARMS_UP if pose == "wave" else cells


def pose_face(mood: str, pose: str = "idle"):
    """Face pixels; a blink closes the eyes but keeps extras like sweat."""
    face = face_pixels(mood)
    if pose != "blink":
        return face
    return CLOSED_EYES + [p for p in face if p[2] != EYE]


def _pixel(canvas, row, col, color, x0, y0, px):
    x, y = x0 + col * px, y0 + row * px
    canvas.create_rectangle(x, y, x + px, y + px, fill=color, width=0,
                            tags="clawd")


def draw_clawd(canvas, mood: str, x0: int, y0: int, px: int,
               pose: str = "idle") -> None:
    """Erase the old Clawd and draw a new one with its top-left at (x0, y0)."""
    canvas.delete("clawd")
    for r, c in body_pixels(pose):
        _pixel(canvas, r, c, ORANGE, x0, y0, px)
    for r, c, color in pose_face(mood, pose):
        _pixel(canvas, r, c, color, x0, y0, px)
    if mood == "sleepy":
        canvas.create_text(x0 + COLS * px + 2, y0, text="z", fill=SWEAT,
                           font=("Consolas", 10, "bold"), tags="clawd")
