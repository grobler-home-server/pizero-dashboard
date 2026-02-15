from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import subprocess

PORT = 8085
DIRECTORY = "/opt/pizero/dashboard"

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/render":
            try:
                subprocess.run(["python3", os.path.join(DIRECTORY, "renderer.py")], check=True)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Render successful")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Render failed: {e}".encode())
        else:
            if self.path == "/":
                self.path = "/latest.png"
            return super().do_GET()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    server = HTTPServer(("0.0.0.0", PORT), DashboardHandler)
    print(f"Serving dashboard on port {PORT}")
    server.serve_forever()
