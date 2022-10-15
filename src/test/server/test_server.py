import sys
import requests
from threading import Thread
from src.main.server.server import SensorServer


def test_server():
    sensor_readings = [{"test_time": {"sensor": 18}}]
    server = SensorServer(
        host_name="localhost", port=8082, sensor_readings=sensor_readings
    )

    thread = Thread(target=server.start)
    thread.daemon = True
    thread.start()

    url = "http://localhost:8082"

    response = requests.request("GET", url, headers={}, data={})

    response_json = response.json()

    print(response_json)

    time_key = list(response_json[0].keys())[0]
    assert time_key == "test_time"
    assert response_json[0][time_key] == {"sensor": 18}

    server.close()
