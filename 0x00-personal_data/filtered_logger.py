#!/usr/bin/env python3
"""  0. Regex-ing """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
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
    
    arr = message.split(separator)
    for field in fields:
        find_field = re.compile(f"(?:{field})=([^{separator}]+)")
        string_to_replace = find_field.search(message).group()
        for idx, target in enumerate(arr):
            if target == string_to_replace:
                arr.pop(idx)
                target = re.sub(f"(?:{field})=([^{separator}]+)", f"{field}={redaction}", target)
                arr.insert(idx, target)

    return f'{separator}'.join(arr)
