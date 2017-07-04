import asyncio
import logging
import random
import os

from inqubo.retry_strategies import LimitedRetries
from inqubo.workflow import Workflow
from inqubo.decorators import step
from inqubo.runners.pika_runner import PikaRunner, PikaClient

logger = logging.getLogger('inqubo')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class RandomFailure(Exception):
    def __str__(self):
        return 'random failure'


async def dowork():
    await asyncio.sleep(random.random() * 7)
    if random.random() > 0.5:
        raise RandomFailure


@step()
async def validate_order(meta, payload):
    logger.info('validating order {}'.format(meta.get('order-id', 'NO_ORDER_ID')))
    await dowork()
    return {'order': payload}


@step()  # more attempts for this step
async def process_order(meta, payload):
    logger.info('processing order {}'.format(meta.get('order-id', 'NO_ORDER_ID')))
    await dowork()


flow = Workflow('order')
flow.start(validate_order).then(process_order)

loop = asyncio.get_event_loop()
pika_client = PikaClient(os.getenv('AMQP_URI'), loop)
pika_runner = PikaRunner(flow, pika_client, loop, retry_strategy=LimitedRetries(20, 3000))
loop.run_until_complete(pika_runner.start())
loop.run_forever()
