import threading
from flask import current_app
from . import mail



def send_async_email(app, msg):
    # 'app' should be a real Flask app instance, not the proxy
    with app.app_context():
        mail.send(msg)



def send_email(subject, sender, recipients, text_body, html_body):
    from flask_mail import Message
    from flask import _app_ctx_stack

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    # pass real app instance to thread
    app = current_app._get_current_object()
    threading.Thread(target=send_async_email, args=(app, msg)).start()
