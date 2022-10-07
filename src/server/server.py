import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List


class SensorServer:
    def __init__(
        self, host_name: str, port: int, sensor_readings: List[Dict[str, Any]]
    ):
        self.server = HTTPServer((host_name, port), SensorHandlerServer)
        SensorHandlerServer.sensor_readings = sensor_readings

    def start(self) -> None:
        self.server.serve_forever()

    def close(self) -> None:
        self.server.server_close()


class SensorHandlerServer(BaseHTTPRequestHandler):
    sensor_readings = []

    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path != "/favicon.ico":
            self._set_response()
            response = json.dumps(SensorHandlerServer.sensor_readings)
            response = bytes(response, "utf-8")
            self.wfile.write(response)
