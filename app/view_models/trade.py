from app.models.wish import Wish
from app.models.gift import Gift

class Trade_wish():
    def __init__(self):
        self.wishes = []
        self.total = 0
    def fill(self, trade_wishes):
        for wish in trade_wishes:
            self.wishes.append({'user': wish.user.nickname, 'time':wish.create_datetime, 'id':wish.id})
        self.total = len(self.wishes)

class Trade_gift():
    def __init__(self):
        self.gifts = []
        self.total = 0

    def fill(self, trade_gifts):
        for gift in trade_gifts:
            self.gifts.append({'user': gift.user.nickname, 'create_datetime': gift.create_datetime.strftime('%Y-%m-%d'), 'id':gift.id})
        self.total = len(self.gifts)

# class Trade():
#     def __init__(self):
#         self.total = 0
#         self.books = []
#     def fill(self, objs):
#         isbns = [obj.isbn for obj in objs]


class Trade:
    def __init__(self):
        self.total = 0
        self.books = []
    def fill(self,*trades):
        self.total = len(trades)
        for trade in trades:
            book = trade.book
            r = {
                'title': book['title'],
                'author': '，'.join(book['author']),
                'publisher': book['publisher'],
                'price': book['price'],
                'isbn': book['isbn'],
                'count_wishes': trade.count_wishes
            }
            self.books.append(r)

    def fill_wish(self,*trades):
        self.total = len(trades)
        for trade in trades:
            book = trade.book
            r = {
                'wid': trade.id,
                'image': book['image'],
                'title': book['title'],
                'author': '，'.join(book['author']),
                'publisher': book['publisher'],
                'price': book['price'],
                'isbn': book['isbn'],
                'count_gift': trade.count_gift
            }
            self.books.append(r)