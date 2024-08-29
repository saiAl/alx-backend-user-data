#!/usr/bin/env python3
"""  0. Regex-ing """
from typing import List
import re
import logging


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
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        logging.basicConfig(level=logging.INFO)
        record.msg = filter_datum(
                self.fields, self.REDACTION,
                record.getMessage(), self.SEPARATOR
                )
        return super(RedactingFormatter, self).format(record)
