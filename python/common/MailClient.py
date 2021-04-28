import yagmail
import socket

ok_body = "RUN WAS SUCCESSFUL"
not_ok_body = "RUN WAS NOT SUCCESSFUL"


class MailClient:
    def __init__(self, email, password, receivers):
        self.email = email
        self.password = password
        self.receivers = receivers
        self.yag = yagmail.SMTP(self.email, self.password)
        self.attachment = None

    def send_ok_email(self):
        self.yag.send(
            to=self.receivers,
            subject="ART: RUN on " + socket.gethostname() + " SUCCESSFUL",
            contents=ok_body,
            attachments=self.attachment
        )

    def send_not_ok_email(self, message):
        self.yag.send(
            to=self.receivers,
            subject="ART: RUN on " + socket.gethostname() + " NOT SUCCESSFUL\n" + message,
            contents=not_ok_body,
            attachments=self.attachment
        )
