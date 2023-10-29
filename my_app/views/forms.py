import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, DateField, FieldList, FormField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from datetime import date


def validate_phone_number(form, phone_number):
    if not phone_number.data.isdigit():
        raise ValidationError('Phone number should consist only digits')


class AddClientForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(min=5, max=45)])
    phone_number = StringField("Phone number: ", validators=[DataRequired(), Length(min=10, max=10),
                                                             validate_phone_number])
    email = StringField("Email: ", validators=[DataRequired(), Length(min=7, max=30)])


class AddServiceForm(FlaskForm):

    name = StringField("Name: ", validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField("Description: ", render_kw={'style': 'width: 400px; height:100px;'},
                                validators=[DataRequired(), Length(min=5, max=1000)])
    unit = StringField("Unit: ", validators=[DataRequired(), Length(min=3, max=20)])
    price = IntegerField("Price: ", validators=[DataRequired(), NumberRange(min=1)])


def filter_date(x):
    if isinstance(x, datetime.date):
        return x.strftime('%Y-%m-%d')
    elif isinstance(x, str):
        return datetime.datetime.strptime(x, "%Y-%m-%d")


class AddOrderForm(FlaskForm):
    class Meta:
        csrf = False


    service_id = SelectField("Goods")
    quantity = IntegerField("Number: ", default=1, validators=[DataRequired(), NumberRange(min=1)])
    unit = StringField("Unit", render_kw={'readonly': True})
    price = IntegerField("Price", render_kw={'readonly': True})
    order_line_price = IntegerField("Total price")
    event_date = DateField("Event_date: ", default=date.today(), format='%Y-%m-%d', validators=[DataRequired()])

    def validate_event_date(form, field):
        if field.data < form.meta.created_date:
            raise ValidationError("Event date must not be earlier than created date.")


class OrderFormSet(FlaskForm):
    created_date = DateField('Date', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()])
    client_id = SelectField("Clients", validators=[DataRequired()])
    order_line = FieldList(FormField(AddOrderForm), min_entries=1)







