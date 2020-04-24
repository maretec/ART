import smtplib

def send_email(smtpserver, to_addr_list, message, cc_addr_list, from_addr, password, subject):
    #To Addresses and CCs have to come in the form of lists (e.g. ['email1@email.com', 'email2@gmail.com'])
    user = from_addr.split("@")[0]
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