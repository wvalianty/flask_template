from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import EqualTo, Length, NumberRange, DataRequired, Email, \
    ValidationError
from app.models.user import User

class RegisterForm(Form):
    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32), EqualTo('repassword', message='两次输入的密码不相同')])
    repassword = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])
    def validate_email(self, field):
        # db.session.
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')
    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')

class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])

class Password(Form):
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])

class ResetPasswdForm(Form):
    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'),
        Length(6, 32),
        EqualTo('repassword',message='两次输入的密码不一致')
    ])
    repassword = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])

class ChangePasswdForm(ResetPasswdForm):
    old_password = PasswordField(validators=[DataRequired(message='old_password密码不可以为空，请输入你的密码'), Length(6, 32)])
