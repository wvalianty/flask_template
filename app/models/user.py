from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import current_user
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.lib.helper import is_isbn_or_key
from app.models.gift import Gift
from math import floor


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def get_id(self):
        return self.id

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_passwd(token, new_passwd):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
            uid = data.get('id')
            user = User.query.get(uid)
            with db.auto_commit():
                user.password = new_passwd
            return True
        except Exception as e:
            return False

    @classmethod
    def latest_gift(self,uid):
        # id = current_user.id
        id = uid
        gift_list = Gift.query.filter_by(launched=False, uid=id).all()
        return gift_list

    def can_save_to_gift(self, isbn):
        uid = current_user.id
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        if Gift.query.filter_by(isbn=isbn, launched=False, uid=uid).all():
            return False
        if Wish.query.filter_by(isbn=isbn, launched=False, uid=uid).all():
            return False
        yushu = YuShuBook()
        yushu.search_by_isbn(isbn)
        if not yushu.first:
            return False
        return True

    def can_send_drift(self, isbn):
        if current_user.beans < 1:
            return False
        if Gift.query.filter_by(launched=False, isbn=isbn, uid=current_user.id).first():
            return False
        if floor(current_user.send_counter / 2) <= floor(current_user.receive_counter):
            return False
        return True

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))