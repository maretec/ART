import yagmail
import socket

ok_body = "RUN WAS SUCCESSFUL"
not_ok_body = "RUN WAS NOT SUCCESSFUL"


class MailClient:
    def __init__(self, email, password, receivers):
        self.email = email
        self.password = password
        self.receivers = receivers
        print(self.email)
        print(self.password)
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
        print("entrei send_not_ok_email 2")
        self.yag.send(
            to=self.receivers,
            subject="ART: RUN on " + str(socket.gethostname()) + " NOT SUCCESSFUL\n" + str(message),
            contents=not_ok_body,
            attachments=str(self.attachment)
        )
