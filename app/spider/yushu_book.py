from app.lib.httper import HTTP
from flask import current_app

# 鱼书的 search view_model，我认为写在这里也是可以的，而且会更方便一些
class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_key(self, key, page=1):
        url = self.keyword_url.format(key, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_multiple(result)

    def calculate_start(self, page):
        return (page - 1) * current_app.config['PER_PAGE']

    def __fill_single(self, data):
        self.total = 1
        self.books.append(data)

    def __fill_multiple(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None