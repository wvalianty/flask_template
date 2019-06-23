from flask import jsonify, request, flash, render_template
from . import web
from app.spider.yushu_book import YuShuBook
from app.forms.book import SearchForm
from app.view_models.book import BookCollection
from app.lib.helper import is_isbn_or_key
from flask_login import current_user
from app.models.wish import Wish
from app.models.gift import Gift
from app.view_models.trade import Trade_gift, Trade_wish
from app.models.user import User
from flask import current_app


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = {}
    page = 0
    total = 0
    q = ''
    if form.validate():
        q = form.q.data
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu = YuShuBook()
        if isbn_or_key == 'key':
            yushu.search_by_key(q, page)
        if isbn_or_key == 'isbn':
            yushu.search_by_isbn(q)
        yushu_view = BookCollection(yushu)
        books = yushu_view.books
        total = yushu_view.total
        page = page
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search.html',q=q, books=books, total=total, per_page=current_app.config['PER_PAGE'], current_page=page)

   # return jsonify(books=yushu_view.books, total=yushu_view.total, per_page=current_app.config['PER_PAGE'])


# @web.route('/book/<isbn>/detail')
# def detail(isbn):
#     if is_isbn_or_key(isbn) == "isbn":
#         yushu = YuShuBook()
#         yushu.search_by_isbn(isbn)
#         yushu_view = BookCollection(yushu)
#         return jsonify(book=yushu_view.books)
#     else:
#         flash("isbn不合规")


@web.route('/book/<isbn>/detail')
def detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu = YuShuBook()
    yushu.search_by_isbn(isbn)
    yushu_view = BookCollection(yushu)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()

    trade_gift_view = Trade_gift()
    trade_gift_view.fill(trade_gifts)

    trade_wish_view = Trade_wish()
    trade_wish_view.fill(trade_wishes)

    print(trade_gift_view.gifts)
    return render_template("book_detail.html",book=yushu_view.books[0],wishes=trade_wish_view.wishes,gifts=trade_gift_view.gifts,has_in_wishes=has_in_wishes,has_in_gifts=has_in_gifts)

    # return jsonify(book=yushu_view.books,wishes=trade_wish_view.wishes,gifts=trade_gift_view.gifts,
    #                has_in_wishes=has_in_wishes,has_in_gifts=has_in_gifts)

# @web.route('/')
# def book_latest():
#     uid = 6
#     gift_list = User.latest_gift(uid)
#     books = []
#     for gift in gift_list:
#         books.append(gift.book)
#     from app.view_models.gift import Latest_gifts_view
#     latest_gifts = Latest_gifts_view()
#     latest_gifts.parse(*books)
#     return jsonify(books=latest_gifts.books, total=latest_gifts.total)
