from wtforms import Form, StringField
from wtforms.validators import Length, DataRequired

class ReceiverForm(Form):
    recipient_name = StringField(validators=[DataRequired(message='收件人姓名不能为空！'), Length(2,30)])
    address = StringField(validators=[DataRequired(message='收件人地址不能为空！'), Length(2,100)])
    mobile = StringField(validators=[DataRequired(message='收件人手机号不能为空！'), Length(8, 64)])
    message = StringField()