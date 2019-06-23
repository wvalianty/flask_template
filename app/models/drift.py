from sqlalchemy import Integer, String, Column, SmallInteger
from app.models.base import Base
from app.lib.enum import PendingStatus
from flask_login import current_user
from sqlalchemy import or_, desc
from app.spider.yushu_book import YuShuBook


class Drift(Base):
    """
        一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    # 十一月

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value

    def save_drift(self, form, gift, book, gifter):
        self.recipient_name = form.recipient_name.data
        self.address = form.address.data
        self.message = form.message.data
        self.mobile = form.mobile.data
        self.isbn = book['isbn']
        self.book_title = book['title']
        self.book_author = book['author']
        self.book_img = book['image']
        self.requester_id = current_user.id
        self.requester_nickname = current_user.nickname
        self.gifter_id = gifter.id
        self.gift_id = gift.id
        self.gifter_nickname = gifter.nickname

    @classmethod
    def user_drifts(cls):
        id = current_user.id
        drifts = Drift.query.filter(or_(Drift.gifter_id==id, Drift.requester_id==id)).order_by((Drift.create_time)).all()
        return drifts

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        a_book = yushu_book.first
        if a_book["author"]:
            a_book["author"] = ("、").join(a_book["author"])
        return a_book
