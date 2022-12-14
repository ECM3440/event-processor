import time
import json
import logging
from typing import Any, Dict, List
from azure.servicebus import ServiceBusClient, ServiceBusReceiver


def consume_service_bus(
    connection_str: str,
    topic_name: str,
    subscription_name: str,
    sensor_readings: List[Dict[str, Any]],
) -> None:
    if connection_str == "":
        raise Exception("connection_str is not set")
    if topic_name == "":
        raise Exception("topic_name is not set")
    if subscription_name == "":
        raise Exception("subscription_name is not set")
    if sensor_readings is None:
        raise Exception("sensor_readings is not set")
    try:
        servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=connection_str
        )
    except Exception as e:
        logging.error(e)
        return

    logging.info("Consuming events")

    while True:
        with servicebus_client:
            receiver = servicebus_client.get_subscription_receiver(
                topic_name=topic_name, subscription_name=subscription_name
            )
            with receiver:
                received_msgs = receiver.receive_messages(
                    max_message_count=5, max_wait_time=10
                )
                for msg in received_msgs:
                    logging.info("message received: {}".format(str(msg)))
                    nmsg = json.loads(str(msg))
                    sensor_readings.append(nmsg)
                    receiver.complete_message(msg)
        time.sleep(10)
