"""
models.py

App Engine datastore models

"""

import random

from google.appengine.ext import ndb


class TicketModel(ndb.Model):

    email = ndb.StringProperty(required=True)

    payment_method = ndb.StringProperty(required=True)

    price = ndb.IntegerProperty(default=0)

    paid = ndb.BooleanProperty(default=False)

    created = ndb.DateTimeProperty(auto_now_add=True)

    note = ndb.TextProperty(required=False, default="")

    hidden = ndb.BooleanProperty(default=False)


def gen_alnum_string():
    return ''.join(random.choice('123456789ABCDEFGHIJKLMNPQRSTUVWXYZ') for i in range(6))


def gen_new_ticket_id():

    ticket_id = gen_alnum_string()

    while TicketModel.get_by_id(ticket_id) is not None:
        ticket_id = gen_alnum_string()

    return ticket_id
