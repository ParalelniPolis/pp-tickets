"""
PublicNotification.py

Handler for App Engine for /notification

"""

from flask.views import View
from flask import request

import hashlib
import json
import logging

from ...models import TicketModel

from ... import app


class PublicNotification(View):

    def dispatch_request(self):

        if str(request.headers.get('BPSignature')) == self.get_hash(request.data):
            request_data = json.loads(request.data)

            if request_data["status"] == "confirmed":
                logging.info("Payment notification " + str(request_data))

                self.ticket = TicketModel.get_by_id(request_data["reference"])

                assert self.ticket is not None

                self.ticket.set_paid(True)
                self.ticket.put()

        else:
            logging.warning("Incorrect callback password")
            logging.warning(str(request.data))

        return "OK"

    def get_hash(self, raw_string):
        m = hashlib.sha256()
        m.update(raw_string)
        m.update(app.config["BITCOINPAY_CALLBACK_PASS"])
        return m.hexdigest()
