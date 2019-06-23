from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp, ValidationError
from app.lib.helper import is_isbn_or_key

class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)

class IsbnForm(Form):
    isbn = IntegerField(validators=[DataRequired()])
    def validate_isbn(self,field):
        is_isbn = is_isbn_or_key(field.data)
        if is_isbn != "isbn":
            raise ValidationError("isbn不合规")