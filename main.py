import sys

if "--desktop" in sys.argv:
    try:
        from worldmap.app import WorldAtlasApp
    except Exception as exc:
        print("Desktop mode unavailable. Install PyQt6 and ModernGL, or run `python3 main.py` for browser mode.")
        raise SystemExit(1) from exc
    if __name__ == "__main__":
        app = WorldAtlasApp()
        raise SystemExit(app.run())
else:
    from browser_main import run

    if __name__ == "__main__":
        raise SystemExit(run())
