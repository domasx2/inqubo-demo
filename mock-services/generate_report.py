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
async def get_data():
    logger.info('getting the data')
    await dowork()
    return {'data': ['FOO', 'BAR']}


@step()
async def process_data(payload):
    logger.info('processing data: {}'.format(payload['data']))
    await dowork()
    return { 'data': [x + '-processed' for x in payload['data']] }


@step()
async def convert_data_to_csv(payload):
    logger.info('converting data to csv {}'.format(payload['data']))
    await dowork()
    return '\n'.join(payload['data'])


@step()
async def upload_data(payload):
    logger.info('uploading {}'.format(payload))
    await dowork()


@step()
async def generate_report(payload):
    logger.info('generating report form {}'.format(payload['data']))
    await dowork()
    return 'report'


@step()
async def send_report(payload):
    logger.info('sending report')
    await dowork()


flow = Workflow('generate_report')

flow.start(get_data)\
    .then(process_data)\
    .then(
        convert_data_to_csv.then(upload_data),
        generate_report.then(send_report)
    )

loop = asyncio.get_event_loop()
pika_client = PikaClient(os.getenv('AMQP_URI'), loop)
pika_runner = PikaRunner(flow, pika_client, loop, retry_strategy=LimitedRetries(20, 3000))
loop.run_until_complete(pika_runner.start())
loop.run_forever()
