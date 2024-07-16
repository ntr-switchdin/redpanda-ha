import logging
from sys import api_version
from time import sleep
from typing import Any
from uuid import uuid4

from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from faststream import FastStream
from faststream.kafka import KafkaBroker

from redpanda import brokers

broker = KafkaBroker(brokers)
app = FastStream(broker)

topics = [
    NewTopic(name="current-master", replication_factor=3, num_partitions=1)
]

@app.on_startup
async def setup():
    log = logging.getLogger("faststream")
    log.info("starting")
    publisher = broker.publisher("current-master")
    await broker.connect()

    admin = AIOKafkaAdminClient(bootstrap_servers=', '.join(brokers), client_id="gsf-admin", api_version="0.11")
    log.info(admin._client.api_version)
    await admin.start()

    new_topics = await admin.create_topics(new_topics=topics)
    log.info(new_topics)

    while True:
        # Fetch metadata for the topic
        cluster_metadata = await admin.describe_topics(["current-master"])
        topic_metadata = cluster_metadata[0]

        log.info(await admin.describe_configs(config_resources=[]))

        for partition in topic_metadata.get("partitions"):
            partition_id = partition.get("partition")
            leader_id = partition.get("leader")
            log.info(f"Partition: {partition_id}, Leader Broker ID: {leader_id}")

            id = str(uuid4())
            msg = await publisher.publish(leader_id, correlation_id=id)
            log.info(msg)


        sleep(5)
