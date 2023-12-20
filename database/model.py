import json

from database import queries
from database.utils import execute_select_query, execute_update_query
from logs import logger


def get_state(pool, user_id, chat_id):
    results = execute_select_query(pool, queries.get_user_state, user_id=user_id, chat_id=chat_id)
    logger.debug(f"results in get_state: {results}")
    if not results or len(results) == 0:
        return None
    if results[0]["state"] is None:
        return None
    return json.loads(results[0]["state"])


def set_state(pool, user_id, chat_id, state):
    execute_update_query(
        pool, queries.set_user_state, user_id=user_id, chat_id=chat_id, state=json.dumps(state)
    )


def clear_state(pool, user_id, chat_id):
    execute_update_query(pool, queries.set_user_state, user_id=user_id, chat_id=chat_id, state=None)


def save_user_id_username_mapping(pool, user_id, username):
    execute_update_query(pool, queries.set_user_info, user_id=user_id, username=username)


def get_user_id_by_username(pool, username):
    results = execute_select_query(pool, queries.get_user_id_by_username, username=username)
    if not results or len(results) == 0:
        return None
    if results[0]["user_id"] is None:
        return None
    return results[0]["user_id"]


def add_debt(pool, debtor_id, creditor_id, amount_of_debt):  # debtor_id - кто должен денег, creditor_id - кто даёт денег
    execute_update_query(pool, queries.add_user_debt, debtor_id=debtor_id, creditor_id=creditor_id, amount_of_debt=amount_of_debt)


def get_debts_of_creditor(pool, creditor_id):
    results = execute_select_query(pool, queries.show_debtors, creditor_id=creditor_id)
    if not results or len(results) == 0:
        return None
    return [["@{}".format(row["username"]), row["amount_of_debt"]] for row in results]


def get_debts(pool, debtor_id):
    results = execute_select_query(pool, queries.show_debts, debtor_id=debtor_id)
    if not results or len(results) == 0:
        return None
    return [["@{}".format(row["username"]), row["amount_of_debt"]] for row in results]


def close_debt(pool, debtor_id, creditor_id):  # debtor_id - должник (кто должен денег), creditor_id - кто даёт денег в долг
    execute_update_query(pool, queries.close_user_debt, debtor_id=debtor_id, creditor_id=creditor_id)


def get_debtors(pool):
    results = execute_select_query(pool, queries.get_debtor_ids)
    return [r['creditor_id'] for r in results] if results else []
