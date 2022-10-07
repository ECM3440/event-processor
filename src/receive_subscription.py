import logging
import os
from threading import Thread

from server.server import SensorServer
from setting.setting import server_setting, setting_setup
from azure.receive_subscription import consume_service_bus


def run() -> None:
    sensor_readings = []

    setting_setup()

    logging.basicConfig(level=logging.INFO)

    server = SensorServer(
        server_setting.host_name,
        server_setting.port,
        sensor_readings,
    )

    logging.info(
        "Server started at http://%s:%s"
        % (server_setting.host_name, str(server_setting.port))
    )

    try:
        thread = Thread(target=server.start)
        thread.start()
    except KeyboardInterrupt:
        server.close()
        logging.info("Server stopped")

    try:
        consume_service_bus(
            connection_str=os.environ["SERVICEBUS_CONNECTION_STR"],
            topic_name=os.environ["SERVICEBUS_TOPIC_NAME"],
            subscription_name=os.environ["SERVICEBUS_SUBSCRIPTION_NAME"],
            sensor_readings=sensor_readings,
        )
    except Exception:
        logging.error("Couldn't consume messages from the service bus")


if __name__ == "__main__":
    run()
