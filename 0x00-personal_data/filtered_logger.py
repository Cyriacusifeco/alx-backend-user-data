#!/usr/bin/env python3
"""
A module to obfuscate sensitive information.
"""
import re
from typing import List
import logging


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
    Obfuscates specific fields in a log message using regular expressions.

    Arguments:
    fields: A list of strings representing the
    fields to obfuscate in the log message.
    redaction: A string representing the value
    that will replace the obfuscated fields.
    message: A string representing the log line that needs to be obfuscated.
    separator: A string representing the
    character used to separate all fields in the log message.

    Returns:
    A string containing the obfuscated log message.

    Example:
    >>> fields_to_obfuscate = ["password", "credit_card"]
    >>> redaction_string = "[REDACTED]"
    >>> log_message = "User john_doe logged in with password 12345
    and paid using credit_card 1234-5678-9012-3456."
    >>> separator_character = " "
    >>> obfuscated_log = filter_datum(
            fields_to_obfuscate,
            redaction_string,
            log_message,
            separator_character
            )
    >>> print(obfuscated_log)
    User john_doe logged in with [REDACTED] and paid using [REDACTED].
    """
    fields_set = set(fields)
    parts = message.split(separator)
    for i, part in enumerate(parts):
        field_value = part.split("=")
        if len(field_value) == 2 and field_value[0].strip() in fields_set:
            parts[i] = f"{field_value[0]}={redaction}"
    return separator.join(parts)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        constructor method.
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        formatter
        """
        log_message = super().format(record)
        return filter_datum(
                self.fields,
                self.REDACTION,
                log_message,
                self.SEPARATOR
                )
