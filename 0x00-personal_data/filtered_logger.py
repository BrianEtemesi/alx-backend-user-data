#!/usr/bin/env python3
"""
implementation of a log filter
"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    returns a log message obfuscated
    """
    for fld in fields:
        message = re.sub(r'{}=[^{}]+'.format(fld, separator),
                         '{}={}'.format(fld, redaction), message)
    return message
