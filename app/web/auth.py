from app.models.user import User
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.auth import RegisterForm, LoginForm, EmailForm,Password, ResetPasswdForm, ChangePasswdForm
from . import web
from app.models.base import db
from app.lib.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)

# @web.route('/login',methods=['GET','POST'])
# def login():
#     form = LoginForm(request.form)
#     if request.method == 'POST' and form.validate():
#         #密码前端不加密
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user,remember=True)
#             next = request.args.get('next')
#             if not next or not next.startswith('/'):
#                 next = url_for('web.index')
#                 return redirect(next)
#             return redirect(next)
#         flash("账号不存在或密码错误")
#     return render_template('auth/login.html',form=form)


@web.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next = request.args.get('next')
            if not next or next.startswith('/'):
                next = url_for('web.main')
            return redirect(next)
        else:
            flash("密码错误！")
    return render_template('auth/login.html', form=form)


@web.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.main'))


#
# @web.route('/forget_passswd', methods=['GET','POST'])
# def forget_password_request():
#     form = EmailForm(request.form)
#     if request.method == 'POST':
#         if form.validate():
#             user = User.query.filter_by(email=form.email.data).first_or_404()
#             send_mail(form.email.data,
#                         '重置你的密码',
#                         'tmplate/forget.html',
#                         token=user.generate_token())
#             flash('一封邮件已发送到邮箱' + form.email.data + '，请及时查收')
#         else:
#             flash('邮箱格式不正确')
#     return render_template('')


@web.route('/forget_passswd', methods=['GET','POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.generate_token()
            send_mail(email, "【重置密码】", 'email/reset_passwd.html', user=user, token=token)
            flash('一封邮件已发送到邮箱' + email + '，请及时查收')
        else:
            flash("输入的邮箱有误，请重新输入")
    return render_template('auth/forget_password_request.html',form=form)


@web.route('/reset_passswd/<token>', methods=['GET','POST'])
def reset_passwd(token):
    form = ResetPasswdForm(request.form)
    if request.method == "POST" and form.validate():
        passwd = form.password.data
        if User.reset_passwd(token, passwd):
            return redirect(url_for("web.main"))
        else:
            flash("重置密码失败")
    return render_template('auth/reset_password.html', form=form)


@web.route('/change_passwd', methods=["GET", "POST"])
@login_required
def change_passwd():
    form = ChangePasswdForm(request.form)
    if request.method == "POST" and form.validate():
        with db.auto_commit():
            current_user.password = form.password.data
        flash("重置密码成功")
        return redirect(url_for('web.main'))
    return render_template('auth/change_password.html', form=form)

@web.route("/personal")
def personal_center():
    return render_template("auth/personal.html")