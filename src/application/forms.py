# -*- coding: utf-8 -*-
"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form
from application import app

from .models import TicketModel

# Main form
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
        ("PAYPAL", "PayPal"),
        ("WIRETRANSFER", "Bank Transfer")
    ]
)

TikcetForm.ticket_type = wtf.SelectField(
    choices=[
        ("NORMAL", u"Normal - {} Kč".format(app.config["TICKET_PRICE_NORMAL"])),
        ("VIP", u"VIP - {} Kč".format(app.config["TICKET_PRICE_VIP"]))
    ]
)


# Admin form
TikcetAdminForm = model_form(
    TicketModel,
    wtf.Form,
    only=[
        "email",
        "price",
        "paid",
        "note",
        "hidden",
    ],
    field_args={
        "email": dict(validators=[validators.Regexp(regex="^[A-Za-z0-9._%+\-\ ]+@[A-Za-z0-9.\-\ ]+\.[A-Za-z]{2,4}([\ ]+)?$")]),
        "price": dict(validators=[validators.NumberRange(min=1, max=10000)]),
        "paid": dict(validators=[]),
        "note": dict(validators=[]),
        "hidden": dict(validators=[]),
    }
)

TikcetAdminForm.payment_method = wtf.SelectField(
    choices=[
        ("BTC", "Bitcoin"),
        ("CASH", "Cash"),
        ("PAYPAL", "PayPal"),
        ("WIRETRANSFER", "Bank Transfer")
    ]
)

TikcetAdminForm.ticket_type = wtf.SelectField(
    choices=[
        ("NORMAL", u"Normal"),
        ("VIP", u"VIP")
    ]
)


# Add ticket
class TikcetAddForm(wtf.Form):

    ticket_id = wtf.TextField('Ticket ID', validators=[validators.Regexp(regex="^[A-Za-z0-9]{6}$")])
    email = wtf.TextField('Email', validators=[validators.Regexp(regex="^[A-Za-z0-9._%+\-\ ]+@[A-Za-z0-9.\-\ ]+\.[A-Za-z]{2,4}([\ ]+)?$")])
