from app.spider.yushu_book import YuShuBook
from app.models.wish import Wish

class Trade:
    def __init__(self):
        self.total = 0
        self.books = []
    def fill(self,*trades):
        self.total = len(trades)
        books = []
        for trade in trades:
            book = trade.book
            r = {
                'gid': trade.id,
                'image': book['image'],
                'title': book['title'],
                'author': '，'.join(book['author']),
                'publisher': book['publisher'],
                'price': book['price'],
                'isbn': book['isbn'],
                'count_wishes': trade.count_wishes
            }
            self.books.append(r)

class My_gift:
    def __init__(self):
        self.book = {}

    @property
    def json_view(self):
        return { 'title':self.book['title'],
                 'author':self.book['author'],
                 'price':self.book['price'],
                 'isbn':self.book['isbn'] ,
                 'wishes':self.book['wishes']
                 }

    def fill(self,isbn):
        yushu = YuShuBook()
        yushu.search_by_isbn(isbn)
        self.book = yushu.books[0]
        self.book['wishes'] = self.get_wish(isbn)

    def get_wish(self,isbn):
        wishes = Wish.query.filter_by(isbn=isbn).all()
        return len(wishes)

class My_gifts:
    def __init__(self):
        self.total= 0
        self.books = []

    def fill(self, *gifts):
        self.total = len(gifts)
        for gift in gifts:
            book = My_gift()
            book.fill(gift.isbn)
            self.books.append(book.json_view)

class Lates_gift:
    def __init__(self,**book):
        self.image = book['image']
        self.title = book['title']
        self.author = book['author']
        self.summary = book['summary']

    @property
    def json_view(self):
        return {'image':self.image, 'title':self.title, 'author':self.author, 'summary':self.summary}



class Latest_gifts_view:
    def __init__(self):
        self.total = 0
        self.books = []
    def parse(self, *books):
        self.total = len(books)
        for book in books:
            self.books.append(Lates_gift(**book).json_view)