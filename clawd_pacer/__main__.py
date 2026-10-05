"""Entry point.

    pythonw -m clawd_pacer          start the desktop pet (no console)
    python  -m clawd_pacer --check  print one status line and exit
"""
import sys


def main() -> None:
    if "--check" in sys.argv:
        from clawd_pacer.app import get_status
        s = get_status()
        print(f"[{s.mood}] {s.line1} | {s.line2}")
        return
    from clawd_pacer.app import App
    App().run()


if __name__ == "__main__":
    main()
