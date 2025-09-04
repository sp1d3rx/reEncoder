"""Utilities for parsing AS2 Message Disposition Notifications (MDNs)."""

from __future__ import annotations

from dataclasses import dataclass
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from typing import Optional


def parse_mdn(data: bytes) -> "MDN":
    """Parse raw MDN bytes into an :class:`MDN` instance."""

    parser = BytesParser(policy=policy.default)
    msg = parser.parsebytes(data)
    return MDN(msg)


@dataclass
class MDN:
    """Representation of an AS2 MDN."""

    message: EmailMessage

    @property
    def disposition(self) -> Optional[str]:
        """Return the value of the ``Disposition`` field if present."""

        if self.message.is_multipart():
            for part in self.message.walk():
                if part.get_content_type() == "message/disposition-notification":
                    payload = part.get_payload(0)
                    if isinstance(payload, EmailMessage):
                        return payload.get("Disposition")
        else:
            return self.message.get("Disposition")
        return None

    # ------------------------------------------------------------------
    def is_success(self) -> bool:
        """Whether the MDN indicates successful processing."""

        disp = self.disposition or ""
        return "processed" in disp.lower()
