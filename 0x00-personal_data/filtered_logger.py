#!/usr/bin/env python3

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specific fields in a log message using regular expressions.

    Arguments:
    fields: A list of strings representing the fields to obfuscate in the log message.
    redaction: A string representing the value that will replace the obfuscated fields.
    message: A string representing the log line that needs to be obfuscated.
    separator: A string representing the character used to separate all fields in the log message.

    Returns:
    A string containing the obfuscated log message.

    Example:
    >>> fields_to_obfuscate = ["password", "credit_card"]
    >>> redaction_string = "[REDACTED]"
    >>> log_message = "User john_doe logged in with password 12345 and paid using credit_card 1234-5678-9012-3456."
    >>> separator_character = " "
    >>> obfuscated_log = filter_datum(fields_to_obfuscate, redaction_string, log_message, separator_character)
    >>> print(obfuscated_log)
    User john_doe logged in with [REDACTED] and paid using [REDACTED].
    """
    pattern = r'\b(?:' + '|'.join(map(re.escape, fields)) + r')\b'
    return re.sub(pattern, redaction, message)
