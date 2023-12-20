START = (
    "Привет! Это специальный бот для учёта должников.\n\n"
    "Список доступных команд:\n"
    "/start\n"
    "/add_debt @username 500\n"
    "/close_debt @username\n"
    "/show_debts"
)

DEBT_WAS_SUCCESFULLY_ADDED = "Долг {} {}₽ был успешно обновлён."
USER_NOT_FOUND = "Информация о долге не была обновлена. Пользовалель, которому вы пытаетесь начислить долг должен запустить бота через /start."
INCORRECT_ADD_DEBT_FORMAT = "Некорректный формат, нужно ввести: \\add_debt @username 1337"
INCORRECT_CLOSE_DEBT_FORMAT = "Некорректный формат, нужно ввести: \\close_debt @username"
CANT_SET_DEBT_TO_YOURSELF = "Вы не можете начислить долг самому себе."
YOUR_DEBTS = "Вы должны деньги следующим пользователям:\n{}"
YOUR_DEBTORS = "Следующие пользователи должны вам деньги:\n{}"
DEBT_CLOSED_SUCCESSFULLY = "Данный пользователь больше вам ничего не должен"
YOU_OWE_MONEY_REMINDER = "Вы должны деньги людям. Чтобы посмотреть ведите /show_debts"
