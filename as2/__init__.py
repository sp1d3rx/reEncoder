"""Minimal AS2 (RFC 4130) implementation.

This package provides a very small subset of an AS2 client as described
in :rfc:`4130`.  It supports building and transmitting AS2 messages over
HTTP and parsing Message Disposition Notifications (MDNs).

The goal of this module is educational; it does not aim to be a complete
or production ready implementation of the AS2 specification.
"""

from .client import AS2Client
from .mdn import MDN, parse_mdn

__all__ = ["AS2Client", "MDN", "parse_mdn"]
