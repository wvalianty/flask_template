from flask import jsonify
from . import web
from app.models.gift import Gift
from flask_login import current_user
from app.models.wish import Wish
from app.view_models.gift import My_gifts
from app.view_models.gift import Trade
from app.models.base import db
from flask import current_app
from flask import flash
from flask_login import login_required
from flask import render_template


@web.route('/my/gifts')
@login_required
def my_gifts():
    # gifts = Gift.query.filter_by(uid=current_user.id).all()
    # gifts = Gift.query.filter_by(uid=6).all()
    # print(gifts)
    # gifts_view = My_gifts()
    # gifts_view.fill(*gifts)
    # return jsonify(books=gifts_view.books,total=gifts_view.total)

    mygifts = Gift.my_gifts()
    mygifts_view = Trade()
    mygifts_view.fill(*mygifts)
    # return jsonify(books=mygifts_view.books, total=mygifts_view.total)
    return render_template('my_gifts.html', books=mygifts_view.books, total=mygifts_view.total)


@web.route('/gift/book/<isbn>')
@login_required
def save_gift(isbn):
    if current_user.can_save_to_gift:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        return jsonify(saved=0)
    return jsonify(saved=1)