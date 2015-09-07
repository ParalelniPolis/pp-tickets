"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import TicketModel

TikcetForm = model_form(
    TicketModel,
    wtf.Form,
    only=[
        "email"
    ],
    field_args={
        "email": dict(validators=[validators.Regexp(regex="^[A-Za-z0-9._%+\-\ ]+@[A-Za-z0-9.\-\ ]+\.[A-Za-z]{2,4}([\ ]+)?$")]),
    }
)

TikcetForm.payment_method = wtf.SelectField(
    choices=[
        ("BTC", "Bitcoin"),
        # ("PAYPAL", "PayPal"),
        # ("WIRETRANSFER", "Bank Transfer")
    ]
)
