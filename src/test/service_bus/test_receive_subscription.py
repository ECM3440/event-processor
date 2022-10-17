import mock
from src.main.service_bus.receive_subscription import consume_service_bus


class MockServiceBusMessageReceived:
    def __init__(self, message: str):
        self.message = message


class MockServiceBusReceiver:
    def receive_messages():
        return [
            MockServiceBusMessageReceived("testMessage1"),
            MockServiceBusMessageReceived("testMessage2"),
        ]


class MockServiceBusClient:
    connection_str = ""

    @classmethod
    def from_connection_string(conn_str: str):
        MockServiceBusClient.connection_str = conn_str
        return MockServiceBusClient()

    def get_subscription_receiver(topic_name: str, subscription_name: str):
        return MockServiceBusReceiver()


@mock.patch(
    "src.main.service_bus.receive_subscription.ServiceBusClient",
    new=MockServiceBusClient(),
)
def test_consume_service_bus():
    sensor_readings = []
    consume_service_bus("conn_str", "topic", "subscription", sensor_readings)

    assert True
