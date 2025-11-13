import threading
from flask import current_app
from flask_mail import Message

from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    # Build msg
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    # pass the actual app instance to the background thread
    app = current_app._get_current_object()
    threading.Thread(target=send_async_email, args=(app, msg)).start()
