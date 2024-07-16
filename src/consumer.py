from time import sleep
import logging
from typing import Any
from typing import Callable, Awaitable

from faststream import FastStream, Logger, Depends, BaseMiddleware
from faststream.kafka import KafkaBroker

from redpanda import brokers

broker = KafkaBroker(brokers)
app = FastStream(broker)

@broker.subscriber("current-master")
async def current_master(msg: Any, logger: Logger):
    logger.info(msg)
