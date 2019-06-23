from . import web
from flask import render_template
from app.models.gift import Gift
from flask import current_app
from flask import request
from app.forms.drift import ReceiverForm
from app.models.drift import Drift
from flask_login import current_user
from app.models.base import db
from flask import redirect, url_for, flash, jsonify
from flask_login import login_required
from app.view_models.drift import DriftCollection


@web.route('/drift/<gid>', methods=['POST', 'GET'])
def send_drift(gid):
    gifter = Gift.owner(gid)
    if request.method == "POST":
        form = ReceiverForm(request.form)
        if form.validate():
            gift = Gift.query.filter_by(id=gid).first()
            book = gift.book
            if current_user.can_send_drift(book['isbn']):
                with db.auto_commit():
                    current_user.beans -= 1
                    current_user.receive_counter += 1
                    drift = Drift()
                    drift.save_drift(form, gift, book, gifter)
                    db.session.add(drift)
                return redirect(url_for('web.pending'))
            else:
                flash('您的鱼豆不够！')
        else:
            flash('表单提交错误！')
    return render_template('drift.html', gifter=gifter, beans_ask_one_book=current_app.config["BEANS_ASK_ONE_BOOK"])


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.user_drifts()
    drifts_view = DriftCollection()
    drifts_view.fill(drifts)
    return render_template('pending.html',total=drifts_view.total, drifts=drifts_view.drifts)