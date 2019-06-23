from app import mail
from threading import Thread
from flask_mail import Message
from flask import current_app, render_template

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    # Python email
    # msg = Message('测试邮件', sender='aaa@qq.com', body='Test',
    #               recipients=['user@qq.com'])
    msg = Message('[鱼书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # current_app  app = Flask()
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()