import logging
import traceback

from pythonjsonlogger import jsonlogger


class YcLoggingFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(YcLoggingFormatter, self).add_fields(log_record, record, message_dict)
        log_record["logger"] = record.name
        log_record["level"] = str.replace(
            str.replace(record.levelname, "WARNING", "WARN"), "CRITICAL", "FATAL"
        )


logHandler = logging.StreamHandler()
logHandler.setFormatter(YcLoggingFormatter("%(message)s %(level)s %(logger)s"))

logger = logging.getLogger("logger")
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)


def find_in_args(args, target_type):
    for arg in args:
        if isinstance(arg, target_type):
            return arg


def find_in_kwargs(kwargs, target_type):
    return find_in_args(kwargs.values(), target_type)


def logged_execution(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            logger.info(
                f"[LOG] Finished execution",
                extra={
                    "arg": str(args),
                    "kwarg": str(kwargs),
                },
            )
        except Exception as exc:
            logger.error(
                f"[LOG] Failed {func.__name__}",
                extra={
                    "arg": str(args),
                    "kwarg": str(kwargs),
                    "exception": exc,
                    "traceback": traceback.format_exc(),
                },
            )

    return wrapper
