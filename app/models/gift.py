from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, desc
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.spider.yushu_book import YuShuBook
from flask_login import current_user
from app.models.wish import Wish
from flask import current_app


class Gift(Base):
    id = Column(Integer,primary_key=True)
    isbn = Column(String(15),nullable=False)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def owner(cls, gid):
        gift = Gift.query.filter_by(id=gid).first()
        user = gift.user
        user.gid = gid
        return user

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        a_book = yushu_book.books[0]
        if a_book["author"]:
            a_book["author"] = ("、").join(a_book["author"])
        return a_book

    @classmethod
    def my_gifts(cls):
        # uid = current_user.id
        uid = 6
        mygifts = Gift.query.filter_by(uid=uid, launched=False).all()
        for gift in mygifts:
            isbn = gift.isbn
            count_wishes = len(Wish.query.filter_by(launched=False, isbn=gift.isbn).all())
            gift.count_wishes = count_wishes
        return mygifts

    @classmethod
    def recent_gift(cls):
        recent_gifts = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)
           ).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gifts

    @classmethod
    def get_isbn(cls, gid):
        gift = Gift.query.filter_by(id=gid, launched=False).first()
        return gift.isbn
