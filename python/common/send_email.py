import smtplib

def send_email(to_addr, message, from_addr="mailing.maretec@gmail.com", password="Maretec2004", subject="MOHID_RUN"):
    user = from_addr.split("@")[0]
    smtpserver = "smtp.gmail.com:587"
    msg = "\r\n".join(["From: " + from_addr, "To: " + to_addr, "Subject: " + subject, "", message])
    try:
        server = smtplib.SMTP(smtpserver)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(from_addr, to_addr, msg)
        server.close()
    except:
        raise ValueError("Failed to send message")
