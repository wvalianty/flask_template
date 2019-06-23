from app.models.gift import Gift
from . import web
from flask import jsonify, render_template
from flask_login import login_required


@web.route("/", methods=['GET'])
def main():
    recent_gifts = Gift.recent_gift()
    recent_gifts_books = [gift.book for gift in recent_gifts]
    # return jsonify(total=len(recent_gifts_books), books=recent_gifts_books)
    return render_template("index.html", books=recent_gifts_books)


@web.route("/abc")
def abc():
    count = 62
    per_page = 10
    return render_template("search.html", count=count, per_page=per_page)