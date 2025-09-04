import unittest

from as2.client import AS2Client
from as2.mdn import parse_mdn


class AS2Tests(unittest.TestCase):
    def test_build_message_sets_headers(self):
        client = AS2Client("SENDER", "https://example.com/as2")
        message_id, msg = client.build_message("RECEIVER", "TEST")
        self.assertIn("AS2-From", msg)
        self.assertIn("AS2-To", msg)
        self.assertEqual(msg["AS2-From"], "SENDER")
        self.assertEqual(msg["AS2-To"], "RECEIVER")
        self.assertEqual(msg["Message-ID"], message_id)

    def test_parse_successful_mdn(self):
        raw = (
            b"Content-Type: multipart/report; report-type=disposition-notification; boundary=foo\r\n"
            b"\r\n--foo\r\n"
            b"Content-Type: text/plain\r\n\r\n"
            b"Your message was successfully received\r\n"
            b"--foo\r\n"
            b"Content-Type: message/disposition-notification\r\n\r\n"
            b"Disposition: automatic-action/MDN-sent-automatically; processed\r\n"
            b"--foo--\r\n"
        )
        mdn = parse_mdn(raw)
        self.assertTrue(mdn.is_success())


if __name__ == "__main__":
    unittest.main()
