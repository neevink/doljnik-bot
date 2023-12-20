import ydb

from logs import logger


def _format_kwargs(kwargs):
    return {"${}".format(key): value for key, value in kwargs.items()}


def execute_update_query(pool, query, **kwargs):
    def update_callee(session):
        prepared_query = session.prepare(query)
        session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )

    return pool.retry_operation_sync(update_callee)


def execute_select_query(pool, query, **kwargs):
    def select_callee(session):
        prepared_query = session.prepare(query)
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )
        logger.debug(f"in callee {query} {_format_kwargs(kwargs)}")
        logger.debug(f"result_sets in callee {result_sets}")
        return result_sets[0].rows

    logger.debug(f"{query} {_format_kwargs(kwargs)}")
    return pool.retry_operation_sync(select_callee)
