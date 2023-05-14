from http.server import BaseHTTPRequestHandler, HTTPServer

class HealthCheckRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, content_type, content):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_GET(self):
        if self.path == "/healthcheck":
            self._send_response(200, "text/plain", "OK")
        else:
            self._send_response(404, "text/plain", "Not Found")

def run_healthcheck_server(port):
    server_address = ("", port)
    httpd = HTTPServer(server_address, HealthCheckRequestHandler)
    print(f"Healthcheck Server running on port {port}")
    httpd.serve_forever()