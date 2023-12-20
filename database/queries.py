DEPRECATED_USERS_INFO_TABLE_PATH = "user_personal_info"
STATES_TABLE_PATH = "states"

DEBTS_TABLE_PATH = "debt_table"
USER_INFO_TABLE_PATH = "user_info"


get_user_state = f"""
    DECLARE $chat_id AS Int64;
    DECLARE $user_id AS Int64;

    SELECT state
    FROM `{STATES_TABLE_PATH}`
    WHERE user_id == $user_id
    AND chat_id == $chat_id;
"""

set_user_state = f"""
    DECLARE $chat_id AS Int64;
    DECLARE $user_id AS Int64;
    DECLARE $state AS Utf8?;

    UPSERT INTO `{STATES_TABLE_PATH}` (`chat_id`, `user_id`, `state`)
    VALUES ($chat_id, $user_id, $state);
"""

set_user_info = f"""
    DECLARE $user_id AS Int64;
    DECLARE $username AS Utf8;

    UPSERT INTO `{USER_INFO_TABLE_PATH}` (`user_id`, `username`)
    VALUES ($user_id, $username);
"""

get_user_id_by_username = f"""
    DECLARE $username AS Utf8;

    SELECT user_id FROM `{USER_INFO_TABLE_PATH}`
    WHERE username == $username;
"""

get_debtor_ids = f"""
    SELECT DISTINCT creditor_id FROM `{DEBTS_TABLE_PATH}`;
"""

add_user_debt = f"""
    DECLARE $debtor_id AS Int64;
    DECLARE $creditor_id AS Int64;
    DECLARE $amount_of_debt AS Float;

    UPSERT INTO `{DEBTS_TABLE_PATH}` (`debtor_id`, `creditor_id`, `amount_of_debt`)
    VALUES ($debtor_id, $creditor_id, $amount_of_debt);
"""

close_user_debt = f"""
    DECLARE $debtor_id AS Int64;
    DECLARE $creditor_id AS Int64;

    DELETE FROM `{DEBTS_TABLE_PATH}`
    WHERE debtor_id == $debtor_id
    AND creditor_id == $creditor_id;
"""

show_debtors = f"""
    DECLARE $creditor_id AS Int64;

    SELECT username, amount_of_debt FROM `{DEBTS_TABLE_PATH}`
    JOIN `{USER_INFO_TABLE_PATH}` ON `user_info`.user_id == `debt_table`.debtor_id
    WHERE creditor_id == $creditor_id;
"""

show_debts = f"""
    DECLARE $debtor_id AS Int64;

    SELECT username, amount_of_debt FROM `{DEBTS_TABLE_PATH}`
    JOIN `{USER_INFO_TABLE_PATH}` ON `user_info`.user_id == `debt_table`.creditor_id
    WHERE debtor_id == $debtor_id;
"""

init_db = f"""
    CREATE TABLE debt_table
    (
        debtor_id Int64,
        creditor_id Int64,
        amount_of_debt Float,
        PRIMARY KEY (`debtor_id`, `creditor_id`)
    );
    COMMIT;
    CREATE TABLE user_info
    (
        user_id Int64,
        username Utf8,
        PRIMARY KEY (`user_id`)
    );
"""
