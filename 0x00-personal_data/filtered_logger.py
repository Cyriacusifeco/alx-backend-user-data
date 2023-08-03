#!/usr/bin/env python3
"""
A module to obfuscate sensitive information.
"""
import re
from typing import List
import logging
import csv
from logging import StreamHandler


# Define the PII_FIELDS constant containing the fields considered PII
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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

    for field in fields:
        message = re.sub(
                f'{field}=.*?{separator}',
                f'{field}={redaction}{separator}',
                message
                )
    return message


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


def get_logger() -> logging.Logger:
    """ Creates and configures the "user_data" logger.

    Returns:
    A logging.Logger object with the specified configuration.
    """
    # Create a RedactingFormatter with PII_FIELDS as parameters
    formatter = RedactingFormatter(
            fields=PII_FIELDS,
            redaction="***",
            separator=";"
            )

    # Create and configure the "user_data" logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Add a StreamHandler with the RedactingFormatter to the logger
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
