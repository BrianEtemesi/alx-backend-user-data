#!/usr/bin/env python3
"""
implementation of a log filter
"""
import re
from typing import List
import logging
import mysql.connector
import os


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    returns a log message obfuscated
    """
    for fld in fields:
        message = re.sub(r'{}=[^{}]+'.format(fld, separator),
                         '{}={}'.format(fld, redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        initializes instance
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter and format log records
        """
        msg = super().format(record)
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return msg


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object
    """

    # create a logger instance
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    # create a console handler and set level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # create instance of RedactingFormatter with desired fields
    red_formatter = RedactingFormatter(fields=["name",
                                               "email",
                                               "ssn", "password", "ip"])

    # set RedactingFormatter as formatter for the console handler
    console_handler.setFormatter(red_formatter)

    # add the console handler to the logger
    logger.addHandler(console_handler)

    # disable message propagation to parent loggers
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to a mysql database
    """
    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD"),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )

    return connection


PII_FIELDS = ("name", "email", "ssn", "password", "phone")
