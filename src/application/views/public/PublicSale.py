"""
PublicSale.py

Handler for App Engine for /sale

"""

import logging
import json

from flask.views import View

from flask import request, redirect, flash, abort

from ...forms import TikcetForm
from ...models import TicketModel, gen_new_ticket_id

from google.appengine.api import urlfetch

from ... import app

from ...emails import Emails


class PublicSale(View):

    def dispatch_request(self):

        if request.method == "POST":

            form = TikcetForm()

            if form.validate_on_submit():

                self.save_ticket(form)

                if form.payment_method.data == "BTC":
                    # Payment with Bitcoin

                    payment_url = self.get_payment_url()

                    return redirect(payment_url)

                elif form.payment_method.data == "WIRETRANSFER":
                    # Bank transfer

                    Emails.order_waiting_bank(self.ticket)

                    return redirect("/ticket/" + self.ticket.key.id())

                elif form.payment_method.data == "PAYPAL":
                    # Bank transfer

                    Emails.order_waiting_paypal(self.ticket)

                    return redirect(app.config["PAYPAL_BUTTON"])

                else:

                    logging.error("Unknown payment method " + form.payment_method.data)

                    abort(500)

            else:
                flash("Email is not valid, please try it again.", "error")
                return redirect("/")

    def save_ticket(self, form):

        ticket_id = gen_new_ticket_id()

        self.ticket = TicketModel(id=ticket_id)
        self.ticket.email = form.email.data
        self.ticket.payment_method = form.payment_method.data

        if form.ticket_type.data == "NORMAL":
            self.ticket.price = app.config["TICKET_PRICE_NORMAL"]

        if form.ticket_type.data == "VIP":
            self.ticket.price = app.config["TICKET_PRICE_VIP"]

        self.ticket.ticket_type = form.ticket_type.data

        self.ticket.put()

        logging.info("Ticket ID " + ticket_id + " saved")

    def get_payment_url(self):

        payment_data = {}
        payment_data["settled_currency"] = "CZK"
        payment_data["return_url"] = "http://" + request.host + "/ticket/" + self.ticket.key.id()
        payment_data["notify_url"] = "http://" + request.host + "/notification"
        payment_data["notify_email"] = app.config["NOTIFY_EMAIL"]
        payment_data["price"] = self.ticket.price
        payment_data["currency"] = "CZK"

        payment_data["reference"] = self.ticket.key.id()

        logging.info("Payment data : " + str(payment_data))

        payment_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + app.config["BITCOINPAY_API_PRODUCTION"]
        }

        logging.info("Payment headers : " + str(payment_headers))

        result = urlfetch.fetch(
            url='https://www.bitcoinpay.com/api/v1/payment/btc',
            payload=json.dumps(payment_data),
            method=urlfetch.POST,
            headers=payment_headers
        )

        logging.info("BitcoinPay response : " + str(result.content))

        payment_response = json.loads(result.content)["data"]

        payment_url = payment_response["payment_url"]

        assert payment_url.startswith("https")

        return payment_url
