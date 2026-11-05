import smtplib
from dataclasses import dataclass
from email.message import EmailMessage

from flask import Flask


@dataclass
class Message:
    subject: str
    to: str
    text: str


class Mailer:
    """Sends mail over SMTP with the credentials from app config.

    Gmail does not accept the account password here: GMAIL_PASSWORD must be an app password.
    """
    def init_app(self, app: Flask):
        self.username = app.config.get('GMAIL_USERNAME')
        self.password = app.config.get('GMAIL_PASSWORD')
        self.mail_from = app.config.get('MAIL_FROM')
        self.host = app.config.get('SMTP_HOST')
        self.port = app.config.get('SMTP_PORT')

    def send(self, message: Message):
        email = EmailMessage()
        email['Subject'] = message.subject
        email['From'] = f'{self.mail_from} <{self.username}>'
        email['To'] = message.to
        email.set_content(message.text)

        with smtplib.SMTP_SSL(self.host, self.port, timeout=10) as smtp:
            smtp.login(self.username, self.password)
            smtp.send_message(email)


Gmail = Mailer
