from loguru import logger
from telebot.custom_filters import StateFilter

import handlers  # noqa
from database.database_class import create_models
from loader import bot
from utils.set_bot_commands import set_default_commands

logger.add('logs/info_logs.log', level='INFO', rotation='1 day', compression='zip')
logger.add('logs/error_logs.log', level='ERROR', rotation='1 day', compression='zip')

if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
