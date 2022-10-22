import logging
import os
import argparse
from threading import Thread

from server.server import SensorServer
from setting.setting import server_setting, setting_setup
from service_bus.receive_subscription import consume_service_bus


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        nargs=1,
        help="--profile can either be 'dev' or 'prod'",
        default="dev",
        type=str,
    )
    args = parser.parse_args()

    if "profile" not in args:
        raise Exception("profile flag must be set")

    parsed_profile = args.profile

    if parsed_profile != "dev":
        parsed_profile = args.profile.pop()

    if parsed_profile != "dev":
        if parsed_profile != "prod":
            raise Exception("profile flag must either be 'dev' or 'prod'")

    setting_setup(parsed_profile)

    sensor_readings = []
    actuator_readings = []

    logging.basicConfig(level=logging.INFO)

    server = SensorServer(
        server_setting.host_name,
        server_setting.port,
        sensor_readings,
        actuator_readings,
    )

    logging.info(
        "Server started at http://%s:%s"
        % (server_setting.host_name, str(server_setting.port))
    )

    try:
        server_thread = Thread(target=server.start)
        server_thread.start()
    except KeyboardInterrupt:
        server.close()
        logging.info("Server stopped")

    try:
        sensor_thread = Thread(
            target=consume_service_bus,
            args=(
                os.environ["SERVICEBUS_CONNECTION_STR"],
                os.environ["SERVICEBUS_SENSOR_TOPIC"],
                os.environ["SERVICEBUS_SUBSCRIPTION_NAME"],
                sensor_readings,
            ),
        )
        sensor_thread.start()
    except Exception:
        logging.error(
            "Couldn't consume messages from the service bus on the sensor topic"
        )

    try:
        consume_service_bus(
            connection_str=os.environ["SERVICEBUS_CONNECTION_STR"],
            topic_name=os.environ["SERVICEBUS_ACTUATOR_TOPIC"],
            subscription_name=os.environ["SERVICEBUS_SUBSCRIPTION_NAME"],
            sensor_readings=actuator_readings,
        )
    except Exception:
        logging.error(
            "Couldn't consume messages from the service bus on the actuator topic"
        )


if __name__ == "__main__":
    run()
