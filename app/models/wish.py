from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, desc
from app.models.base import Base
from sqlalchemy.orm import relationship
from flask_login import current_user
from app.spider.yushu_book import YuShuBook
# from app.models.gift import Gift

class Wish(Base):
    id = Column(Integer,primary_key=True)
    isbn = Column(String,nullable=False)
    user = relationship('User')
    uid = Column(Integer,ForeignKey('user.id'))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first


    # sender

#与其他之间的关系
#前端展示要哪些信息launched