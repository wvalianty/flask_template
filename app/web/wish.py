from flask import jsonify

from . import web
from app.models.wish import Wish
from flask_login import current_user
from app.view_models.trade import Trade
from sqlalchemy import desc
from app.models.gift import Gift
from flask import render_template

class Trade_wish(Wish):
    @classmethod
    def get_user_wishes(cls):
        # uid = current_user.id
        uid = 6
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        for wish in wishes:
            wish.count_gift = len(Gift.query.filter_by(launched=False, isbn=wish.isbn).all())
        return wishes

@web.route('/my/wishes')
def my_wish():
    my_wishes = Trade_wish.get_user_wishes()
    my_wishes_view = Trade()
    my_wishes_view.fill_wish(*my_wishes)
    # return jsonify(books=my_wishes_view.books, total=my_wishes_view.total)
    return render_template('my_wishes.html', books=my_wishes_view.books, total=my_wishes_view.total)