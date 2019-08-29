import smtplib

def send_email(to_addr_list, message="MOHID run has finished", cc_addr_list=[], from_addr="mailing.maretec@gmail.com", password="Maretec2004", subject="MOHID_RUN"):
    #To Addresses and Ccs have to come in the form of lists
    user = from_addr.split("@")[0]
    smtpserver = "smtp.gmail.com:587"
    msg = "\r\n".join(["From: " + from_addr, "To: " + ','.join(to_addr_list), "Cc: " + ','.join(cc_addr_list), "Subject: " + subject, message])
    try:
        server = smtplib.SMTP(smtpserver)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(from_addr, ','.join(to_addr_list), msg)
        server.close()
    except:
        raise ValueError("Failed to send message")

send_email(["tomasta2010@gmail.com"],"ok")