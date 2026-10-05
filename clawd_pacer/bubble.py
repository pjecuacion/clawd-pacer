"""Speech bubble drawn on the canvas, just above Clawd's head."""

FILL = "#FFFFFF"
INK = "#2B2522"
PAD = 6


def draw_bubble(canvas, text: str, center_x: int, bottom_y: int,
                max_width: int) -> None:
    """Draw a white rounded-ish bubble whose tail points down at Clawd."""
    clear_bubble(canvas)
    t = canvas.create_text(center_x, bottom_y - 8 - PAD, text=text, anchor="s",
                           width=max_width - 2 * PAD, justify="center",
                           fill=INK, font=("Segoe UI", 8), tags="bubble")
    x1, y1, x2, y2 = canvas.bbox(t)
    x1, y1, x2, y2 = x1 - PAD, y1 - PAD, x2 + PAD, y2 + PAD
    r = 6   # corner radius
    for xa, ya, xb, yb in ((x1 + r, y1, x2 - r, y2), (x1, y1 + r, x2, y2 - r)):
        canvas.create_rectangle(xa, ya, xb, yb, fill=FILL, width=0, tags="bubble")
    for cx, cy in ((x1, y1), (x2 - 2 * r, y1), (x1, y2 - 2 * r), (x2 - 2 * r, y2 - 2 * r)):
        canvas.create_oval(cx, cy, cx + 2 * r, cy + 2 * r, fill=FILL, width=0,
                           tags="bubble")
    canvas.create_polygon(center_x - 5, y2, center_x + 5, y2, center_x, y2 + 7,
                          fill=FILL, tags="bubble")
    canvas.tag_raise(t)


def clear_bubble(canvas) -> None:
    canvas.delete("bubble")
