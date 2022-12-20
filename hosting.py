import json
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

import handlers
from utils.DBManager import db_manager

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

db_manager.save_catalog_quests()
bot = Bot(os.environ.get('BOT_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
handlers.setup(dp)


async def handler(event, _):
    if event['httpMethod'] == 'POST':
        update = json.loads(event['body'])
        log.info(update)
        result = await dp.feed_update(bot=bot, update=Update(**update))
        return {'statusCode': 200, 'body': result}
    return {'statusCode': 405}
