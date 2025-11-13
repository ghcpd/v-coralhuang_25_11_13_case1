import threading

from flask import current_app
from flask_mail import Mail, Message

mail = Mail()


def send_async_email(app, msg):
    """Send mail within the provided application context."""

    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """Fire off an email in a background thread without leaking proxy objects."""

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    thread = threading.Thread(
        target=send_async_email, args=(current_app._get_current_object(), msg)
    )
    thread.daemon = True
    thread.start()
