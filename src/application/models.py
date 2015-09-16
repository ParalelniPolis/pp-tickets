"""
models.py

App Engine datastore models

"""

import random

import logging

from google.appengine.ext import ndb

from emails import Emails


class TicketModel(ndb.Model):

    email = ndb.StringProperty(required=True)

    payment_method = ndb.StringProperty(required=True)

    price = ndb.IntegerProperty(default=0)

    paid = ndb.BooleanProperty(default=False)

    created = ndb.DateTimeProperty(auto_now_add=True)

    note = ndb.TextProperty(required=False, default="")

    hidden = ndb.BooleanProperty(default=False)

    ticket_type = ndb.StringProperty(required=False)

    def set_paid(self, value):
        if self.paid is False and value is True:
            logging.info("Order " + self.key.id() + " has been paid")

            Emails.order_paid(self)

        self.paid = value


def gen_alnum_string():
    return ''.join(random.choice('123456789ABCDEFGHIJKLMNPQRSTUVWXYZ') for i in range(6))


def gen_new_ticket_id():

    ticket_id = gen_alnum_string()

    while TicketModel.get_by_id(ticket_id) is not None:
        ticket_id = gen_alnum_string()

    return ticket_id
