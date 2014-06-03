import time

from core import PDU
from lib.log import setup_logging
from smtplib import SMTP, SMTPException


# Default email configs.
SENDER = 'ami@amilab.com'
SENDER_NAME = 'AmI Lab'
RECEIVER = 'diana.tatu@gmail.com'
RECEIVER_NAME = 'Diana Tatu'
TRACKED_PERSON_NAME = 'Andrei'
SUBJECT = '[IMPORTANT] %s may need help!' % TRACKED_PERSON_NAME
POST_CONTENT = 'Please checkout email attachments!'
CONTENT = {
    'HR_ASC': 'Sudden heart rate drop was detected! ',
    'HR_DESC': 'Sudden heart rate raise was detected! ',
}
MARKER = 'AUNIQUEMARKER'


DEFAULT_CONTENT = """From: %s <%s>
To: %s <%s>
Subject: %s

{body}
""" % (SENDER_NAME, SENDER, RECEIVER_NAME, RECEIVER, SUBJECT)


# Main headers.
PART1 = """From: %s <%s>
To: <%s>
Subject: %s
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (SENDER_NAME, SENDER, RECEIVER, SUBJECT, MARKER, MARKER)

# Message action
PART2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

{body}
--%s
""" % MARKER

# Attachment section
# TODO: add support for multiple images attached.
PART3 = """Content-Type: multipart/mixed;
Content-Transfer-Encoding:base64
Content-Disposition: attachment;

{image64}
--%s--
""" % MARKER


class EmailSender(PDU):
    QUEUE = 'email-sender'

    def process_message(self, message):
        """Send emails.

        Args:
            message: dict instance containing email info.
                     Fields:
                         type [REQUIRED]: HR_ASC / HR_DESC
                         attachments [OPTIONAL]: recorded images base64 encoded
        """
        self.logger.info("Sending email to %s" % RECEIVER)
        if not message.get('type'):
            self.logger.error('Received message has no type (it should have '
                              'been one of the following: HR_ASC/HR_DESC): %r')
            return

        if not message.get('attachments'):
            message = self.compose_message_without_attachments(message)
        else:
            message = self.compose_message_with_attachments(message)

        try:
            smtpObj = SMTP('localhost')
            smtpObj.sendmail(SENDER, RECEIVER, message)      
            self.logger.info("Successfully sent email to %s", RECEIVER)
        except SMTPException as e:
            self.logger.error("Unable to send email to %s: %r", RECEIVER, e)

    def compose_message_without_attachments(self, message):
        return DEFAULT_CONTENT.format(body=CONTENT[message['type']])

    def compose_message_with_attachments(self, message):
        body = CONTENT[message['type']] + POST_CONTENT
        image64 = message['attachments']
        return PART1 + PART2.format(body=body) + PART3.format(image64=image64)


if __name__ == "__main__":
    setup_logging()
    module = EmailSender()
    module.run()
