"""Simple AS2 client implementation.

This module implements a tiny subset of the AS2 protocol defined in
:mod:`rfc4130 <https://datatracker.ietf.org/doc/html/rfc4130>`.

Only plain, unsigned and unencrypted messages with synchronous MDN
support are provided.  The intent is to demonstrate the structure of AS2
messages and the workflow for sending a message and receiving an MDN.
"""

from __future__ import annotations

import uuid
from email.message import EmailMessage
from email import policy
from email.generator import BytesGenerator
from io import BytesIO
from typing import Tuple, Optional


class AS2Client:
    """Client capable of sending minimal AS2 messages.

    Parameters
    ----------
    as2_id:
        Identifier that represents the sender's AS2 name.
    url:
        Endpoint of the AS2 trading partner.
    """

    def __init__(self, as2_id: str, url: str) -> None:
        self.as2_id = as2_id
        self.url = url

    # ------------------------------------------------------------------
    def _serialize(self, msg: EmailMessage) -> bytes:
        """Serialize an :class:`~email.message.EmailMessage` to bytes.

        The AS2 specification requires CRLF line endings.  The default
        :mod:`email` generator honours this when using a policy with
        ``linesep="\r\n"``.
        """

        buffer = BytesIO()
        BytesGenerator(buffer, policy=policy.default.clone(linesep="\r\n")).flatten(msg)
        return buffer.getvalue()

    # ------------------------------------------------------------------
    def build_message(
        self,
        as2_to: str,
        payload: bytes | str,
        *,
        content_type: str = "application/edi-x12",
        subject: str = "AS2 Message",
        message_id: Optional[str] = None,
    ) -> tuple[str, EmailMessage]:
        """Build an AS2 message.

        Returns the generated ``Message-ID`` and the constructed
        :class:`~email.message.EmailMessage` instance.
        """

        if message_id is None:
            message_id = f"<{uuid.uuid4()}@{self.as2_id}>"

        msg = EmailMessage()
        msg["AS2-Version"] = "1.2"
        msg["AS2-From"] = self.as2_id
        msg["AS2-To"] = as2_to
        msg["Message-ID"] = message_id
        msg["Subject"] = subject

        msg.set_content(payload)
        msg.replace_header("Content-Type", content_type)
        return message_id, msg

    # ------------------------------------------------------------------
    def send(
        self, as2_to: str, payload: bytes | str, *, subject: str = "AS2 Message"
    ) -> Tuple[str, "requests.Response"]:
        """Send a minimal AS2 message.

        The response returned by the remote server contains the raw MDN
        (Message Disposition Notification).  The caller is responsible for
        parsing it using :func:`as2.mdn.parse_mdn`.
        """

        import requests

        message_id, msg = self.build_message(as2_to, payload, subject=subject)
        body = self._serialize(msg)
        response = requests.post(
            self.url,
            data=body,
            headers={
                "Content-Type": msg["Content-Type"],
                "Content-Length": str(len(body)),
                "AS2-Version": msg["AS2-Version"],
                "AS2-From": msg["AS2-From"],
                "AS2-To": msg["AS2-To"],
                "Message-ID": msg["Message-ID"],
                "Subject": msg["Subject"],
                "MIME-Version": "1.0",
            },
        )
        return message_id, response
