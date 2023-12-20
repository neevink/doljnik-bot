from telebot import TeleBot

from bot import keyboards
from database import model as db_model
from database.model import get_debtors
from logs import logged_execution, logger
from user_interaction import texts


@logged_execution
def handle_start(message, bot: TeleBot, pool):
    logger.info(message)
    db_model.save_user_id_username_mapping(pool, message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id,
        texts.START,
        reply_markup=keyboards.get_reply_keyboard([
            "/start",
            "/add_debt",
            "/close_debt",
            "/show_debts",
        ])
    )


@logged_execution
def handle_add_debt(message, bot: TeleBot, pool):
    try:
        message_text = message.text.split(' ', 2)
        username = message_text[1]
        if username[0] == "@":
            username = username[1:]
        amount_of_debt = int(message_text[2])
    except:
        bot.send_message(message.chat.id, texts.INCORRECT_ADD_DEBT_FORMAT, reply_markup=keyboards.EMPTY)
        return

    creditor_id = db_model.get_user_id_by_username(pool, username)

    # if creditor_id == message.from_user.id:  # fixme uncomment in production
    #     bot.send_message(message.chat.id, texts.CANT_SET_DEBT_TO_YOURSEFL, reply_markup=keyboards.EMPTY)
    #     return

    if creditor_id is None:
        bot.send_message(message.chat.id, texts.USER_NOT_FOUND, reply_markup=keyboards.EMPTY)
        return
    db_model.add_debt(pool, message.from_user.id, creditor_id, amount_of_debt)
    bot.send_message(
        message.chat.id,
        texts.DEBT_WAS_SUCCESFULLY_ADDED.format(username, amount_of_debt),
        reply_markup=keyboards.EMPTY,
    )


@logged_execution
def handle_show_debts(message, bot: TeleBot, pool):
    debts = db_model.get_debts_of_creditor(pool, message.from_user.id)
    your_debtors = db_model.get_debts(pool, message.from_user.id)

    bot.send_message(
        message.chat.id,
        texts.YOUR_DEBTS.format(
            "\n".join([f"{d[0]}: {d[1]}₽" for d in (debts if debts else [])])
        ) + "\n\n" +
        texts.YOUR_DEBTORS.format(
            "\n".join([f"{d[0]}: {d[1]}₽" for d in (your_debtors if your_debtors else [])])
        ),
        reply_markup=keyboards.EMPTY
    )


@logged_execution
def handle_close_debt(message, bot: TeleBot, pool):
    try:
        message_text = message.text.split(' ', 1)
        username = message_text[1]
        if username[0] == "@":
            username = username[1:]
    except:
        bot.send_message(message.chat.id, texts.INCORRECT_CLOSE_DEBT_FORMAT, reply_markup=keyboards.EMPTY)
        return

    creditor_id = db_model.get_user_id_by_username(pool, username)
    if creditor_id is None:
        bot.send_message(message.chat.id, texts.USER_NOT_FOUND, reply_markup=keyboards.EMPTY)
        return

    debtor_id = message.from_user.id
    db_model.close_debt(pool, debtor_id, creditor_id)

    bot.send_message(
        message.chat.id,
        texts.DEBT_CLOSED_SUCCESSFULLY,
        reply_markup=keyboards.EMPTY,
    )


@logged_execution
def handle_notify_about_debt(bot: TeleBot, pool):
    debtor_ids = get_debtors(pool)
    for id in debtor_ids:
        bot.send_message(id, texts.YOU_OWE_MONEY_REMINDER, reply_markup=keyboards.EMPTY)
