"""
Email utilities for asynchronous email sending.
"""

import threading
from flask import current_app
from flask_mail import Mail, Message


mail = Mail()


def send_async_email(app, msg):
    """
    Send email asynchronously in a background thread.
    
    Args:
        app: Flask application instance (real instance, not proxy)
        msg: Message object to send
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Send an email asynchronously.
    
    Uses a background thread to avoid blocking the request handler.
    Properly passes the real app instance to the thread.
    
    Args:
        subject: Email subject
        sender: Sender email address
        recipients: List of recipient email addresses
        text_body: Plain text body
        html_body: HTML body
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    # Get the real app instance via _get_current_object()
    # This ensures the background thread receives a real app instance,
    # not the LocalProxy, which would fail in the new context.
    app = current_app._get_current_object()
    threading.Thread(target=send_async_email, args=(app, msg)).start()
