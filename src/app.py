import os
import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

azure_blob_connection_string = os.getenv("AZURE_BLOB_CONNECTION_STRING")
if azure_blob_connection_string is None:
    raise Exception("AZURE_BLOB_CONNECTION_STRING is not set")

azure_blob_name = os.getenv("AZURE_BLOB_NAME")
if azure_blob_name is None:
    raise Exception("AZURE_BLOB_NAME is not set")

azure_events_connection_string = os.getenv("AZURE_EVENTS_CONNECTION_STRING")
if azure_events_connection_string is None:
    raise Exception("AZURE_EVENTS_CONNECTION_STRING is not set")

azure_consumer_group = os.getenv("AZURE_CONSUMER_GROUP")
if azure_consumer_group is None:
    raise Exception("AZURE_CONSUMER_GROUP is not set")

azure_eventhub_name = os.getenv("AZURE_EVENTHUB_NAME")
if azure_eventhub_name is None:
    raise Exception("AZURE_EVENTHUB_NAME is not set")

async def on_event(partition_context, event):
    # Print the event data.
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(azure_blob_connection_string, azure_blob_name)

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(azure_events_connection_string, consumer_group=azure_consumer_group, eventhub_name=azure_eventhub_name, checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="-1")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())
