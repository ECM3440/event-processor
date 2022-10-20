from threading import Thread

import requests
from src.main.server.server import SensorServer


def test_server():
    sensor_readings = [{"test_time": {"sensor": 18}}]
    actuator_readings = [
        {
            "name": "LED",
            "sensor_type": "Temperature",
            "time": "2022-10-20T10:53:43.442139",
        }
    ]
    server = SensorServer(
        host_name="localhost",
        port=8082,
        sensor_readings=sensor_readings,
        actuator_readings=actuator_readings,
    )

    thread = Thread(target=server.start)
    thread.daemon = True
    thread.start()

    sensor_url = "http://localhost:8082/sensors"

    sensor_res = requests.request("GET", sensor_url, headers={}, data={})

    sensor_json = sensor_res.json()

    time_key = list(sensor_json[0].keys())[0]
    assert time_key == "test_time"
    assert sensor_json[0][time_key] == {"sensor": 18}

    actuator_url = "http://localhost:8082/actuators"

    actuator_res = requests.request("GET", actuator_url, headers={}, data={})
    actuator_json = actuator_res.json()

    got = actuator_json[0]
    print(got)
    assert got["name"] == "LED"
    assert got["sensor_type"] == "Temperature"
    assert got["time"] == "2022-10-20T10:53:43.442139"

    server.close()
