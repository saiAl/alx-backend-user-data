#!/usr/bin/env python3
"""  0. Regex-ing """
import os
import re
from typing import List, Tuple
import logging
import mysql.connector


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """returns the log message obfuscated

        Args:
            fields (List[str]):
                a list of strings representing all fields to obfuscate
            redaction (str):
                a string representing by what the field will be obfuscated
            message (str):
                a string representing the log line
            separator (str):
                a string representing by which character is separating
                    all fields in the log line (message)
    """

    list_of_strings: List[str] = message.split(separator)
    for field in fields:
        find_field = re.compile(f"(?:{field})=([^{separator}]+)")
        string_to_replace = find_field.search(message).group()
        for idx, target in enumerate(list_of_strings):
            if target == string_to_replace:
                list_of_strings.pop(idx)
                target = re.sub(
                        f"(?:{field})=([^{separator}]+)",
                        f"{field}={redaction}",
                        target
                        )
                list_of_strings.insert(idx, target)

    return f'{separator}'.join(list_of_strings)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initiate RedactingFormatter instance """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Formats the LogRecord, filtering sensitive fields

            Args:
                record (logging.LogRecord):
                    The log record containing the message
                        and metadata about the log event.

            Returns:
                str: The formatted log message with sensitive fields redacted.
        """

        record.msg = filter_datum(
                self.fields, self.REDACTION,
                record.getMessage(), self.SEPARATOR
                )
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and returns a logging.Logger
        object configured to handle sensitive user data.

        Returns:
            logging.Logger:
                A configured logger
                    instance for handling user data logs.
    """

    logger = logging.getLoager("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PIT_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Establishes a connection to a MySQL database using
        credentials from environment variables.

        Returns:
            mysql.connector.connection.MySQLConnection:
                A connection object to interact with the database.
    """
    connector = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD')
    )
    return connector


def main():
    """Retrieves and logs user data from a MySQL database.
    """
    get_db = get_db()
    logger = get_logger()

    cursor = db.crusor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        message = (
            "name={}; email={}; phone={}; ssn={}; "
            "password={}; ip={}; last_login={}; user_agent={};"
        ).format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
            )
        logger.info(message)
    crusor.close()
    db.close()


if __name__ == '__main__':
    main()
