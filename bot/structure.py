from functools import partial

from telebot import TeleBot, custom_filters

from bot import handlers as handlers
from bot import states as bot_states


class Handler:
    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.kwargs = kwargs


def get_start_handlers():
    return [
        Handler(callback=handlers.handle_start, commands=["start"]),
    ]


def get_debt_handlers():
    return [
        Handler(callback=handlers.handle_add_debt, commands=["add_debt"]),
        Handler(callback=handlers.handle_show_debts, commands=["show_debts"]),
        Handler(callback=handlers.handle_close_debt, commands=["close_debt"]),
    ]


def create_bot(bot_token, pool):
    state_storage = bot_states.StateYDBStorage(pool)
    bot = TeleBot(bot_token, state_storage=state_storage)

    handlers = []
    handlers.extend(get_start_handlers())
    handlers.extend(get_debt_handlers())

    for handler in handlers:
        bot.register_message_handler(
            partial(handler.callback, pool=pool), **handler.kwargs, pass_bot=True
        )

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    return bot
