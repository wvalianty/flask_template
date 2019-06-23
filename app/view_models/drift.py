from app.lib.enum import PendingStatus
from flask_login import current_user


class Drift:
    def __init__(self, drift):
        self.id = drift.id
        self.book_title = drift.book_title
        self.book_author = drift.book_author
        self.create_time = drift.create_time
        self.requester_nickname = drift.requester_nickname
        self.address = drift.address
        self.mobile = drift.mobile
        self.message = drift.message
        self.pending = drift.pending.value
        self.pending_str = PendingStatus.pending_str(drift.pending, drift.ident)
        self.book_image = drift.book_image
        self.ident = drift.ident


def distinguish_user(drifts):
    uid = current_user.id
    for drift in drifts:
        if drift.gifter_id == uid:
            drift.ident = 'gifter'
        if drift.requester_id == uid:
            drift.ident = 'requester'
        drift.book_image = drift.book['image']
        drift.create_time = drift.create_datetime.strftime('%Y-%m-%d')
    return drifts
# 一个class添加属性，一个for in 修改原来的对象
# 这里误打误撞的，前后一起的写法，前后分开调试，后端先调试数据就对了，和界面分开调试


class DriftCollection:
    def __init__(self):
        self.total = 0
        self.drifts = []

    def fill(self,drifts):
        drifts = distinguish_user(drifts)
        self.drifts = [Drift(drift).__dict__ for drift in drifts]
        self.total = len(drifts)