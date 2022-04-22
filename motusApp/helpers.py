import smtplib
import ssl

from motus.config import EMAIL_SENDER, EMAIL_PORT, EMAIL_SMTP_SERER_DOMAIN, EMAIL_PASSWORD


class GMail:

    def __init__(self):
        self.port = EMAIL_PORT
        self.smtp_server_domain_name = EMAIL_SMTP_SERER_DOMAIN
        self.sender_mail = EMAIL_SENDER
        self.password = EMAIL_PASSWORD

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        for email in emails:
            result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}".encode('utf-8'))

        service.quit()
