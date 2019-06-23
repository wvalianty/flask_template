class Book:
    def __init__(self, book):
        self.image = book['image']
        self.title = book['title']
        self.author = book['author']
        self.publisher = book['publisher']
        self.pubdate = book['pubdate']
        self.pages = book['pages']
        self.price = book['price']
        self.binding = book['binding']
        self.isbn = book['isbn']
        self.summary = book['summary']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(intros)


class _Book:
    def __init__(self, book):
        self.title = book['title']
        self.image = book['image']
        self.summary = book['summary']
        self.author = book['author']
        self.publisher = book['publisher']
        self.price = book['price']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.pages = book['pages']
        self.binding = book['binding']
    @property
    def authors(self):
        return "、".join(self.author)
    @property
    def intro(self):
        introduce = filter(lambda x:True if x else False, [self.authors, self.publisher, self.price])
        return '/'.join(introduce)
    @property
    def view(self):
        return {'title':self.title,'image':self.image,'author':self.authors,'publisher':self.publisher,'price':self.price,'intro':self.intro, 'summary':self.summary, 'isbn':self.isbn, 'pubdate':self.pubdate, 'pages':self.pages,'price':self.price, 'binding':self.binding, 'isbn':self.isbn }

class BookCollection:
    def __init__(self, yushu):
        self.total = yushu.total
        self.books = [ _Book(book).view for book in yushu.books]