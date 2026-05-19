import http.server
import socketserver
import webbrowser
import os

PORT = 8000
BASE_DIR = os.path.join(os.path.dirname(__file__), "web")


def run(port: int = PORT) -> int:
    os.chdir(BASE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), handler) as httpd:
        url = f"http://127.0.0.1:{port}"
        print(f"Serving Interactive World Map at {url}")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
