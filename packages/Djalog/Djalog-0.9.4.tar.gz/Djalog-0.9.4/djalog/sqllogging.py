import logging

from djalog.conf import settings
from djalog.loggers import DjalogLogger

def sql(msg):
    """
    Basic log sql function.
    """
    # Preformat message
    msg = msg.replace('SELECT', '\n    SELECT')\
        .replace('FROM', '\n    FROM')\
        .replace('ORDER BY', '\n    ORDER BY')\
        .replace('LIMIT', '\n    LIMIT')\
        .replace('WHERE', '\n    WHERE')\
        .replace('AND', '\n    AND')\
        .replace('LEFT', '\n    LEFT')\
        .replace('INNER', '\n    INNER')\
        .replace('INSERT', '\n    INSERT')\
        .replace('DELETE', '\n    DELETE')
        
    DjalogLogger.log(logging.SQL, msg)

def init_sql_logging():
    """
    Initializes SQL logging settings or
    removes it from logging module.
    """
    # Clears SQL level / log_sql method
    def remattr(obj, attr):
        if hasattr(obj, attr):
            delattr(obj, attr)
    #DjalogLogger.debug("settings.LOG_SQL is set to %s" % settings.LOG_SQL)
    if settings.LOG_SQL:
        logging.addLevelName(settings.LOG_SQL_LEVEL, levelName='SQL')
        logging.SQL = settings.LOG_SQL_LEVEL
        logging.sql = sql
        DjalogLogger.sql = sql
    else:
        remattr(logging, 'SQL')
        remattr(logging, 'sql')
        remattr(DjalogLogger, 'sql')

