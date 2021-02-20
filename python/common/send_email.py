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

    def send_ok_email(self, log_file):
        self.yag.send(
            to=self.receivers,
            subject="ART: RUN on " + socket.gethostname() + " SUCCESSFUL",
            contents=ok_body,
            attachments=log_file
        )

    def send_not_ok_email(self, log_file):
        self.yag.send(
            to=self.receivers,
            subject="ART: RUN on " + socket.gethostname() + " NOT SUCCESSFUL",
            contents=not_ok_body,
            attachments=log_file
        )