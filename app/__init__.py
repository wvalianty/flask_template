from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from app.models.base import db

#可以简单初始化的
login_manager = LoginManager()
mail = Mail()


def register_blueprint(app):
    #
    from app.web import web
    app.register_blueprint(web)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'
    mail.init_app(app)

    with app.app_context():
        db.create_all()
    return app
