"""
PublicNotification.py

Handler for App Engine for /notification

"""

from flask.views import View
from flask import request, render_template

import hashlib
import json
import logging

from ...models import TicketModel

from google.appengine.api import mail

from ... import app


class PublicNotification(View):

    def dispatch_request(self):

        if str(request.headers.get('BPSignature')) == self.get_hash(request.data):
            request_data = json.loads(request.data)
            logging.info("Payment notification " + str(request_data))

            self.ticket = TicketModel.get_by_id(request_data["reference"])

            assert self.ticket is not None

            self.ticket.paid = True
            self.ticket.put()

            logging.info("Ticket " + str(self.ticket.key.id()) + " has been paid")

            self.send_email()

        else:
            logging.warning("Incorrect callback password")
            logging.warning(str(request.data))

        return "OK"

    def get_hash(self, raw_string):
        m = hashlib.sha256()
        m.update(raw_string)
        m.update(app.config["BITCOINPAY_CALLBACK_PASS"])
        return m.hexdigest()

    def send_email(self):

        sender_address = "HCPP 2015 <" + app.config["SENDER_EMAIL"] + ">"
        subject = "HCPP 2015 ticket"
        content = render_template(
            "public_ticket_email.html",
            ticket=self.ticket
        )

        mail.send_mail(sender_address, self.ticket.email, subject, content)
