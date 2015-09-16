"""
PublicTicketPaypal.py

Handler for App Engine for /ticket/paypal

"""

from flask.views import View

from flask import render_template


class PublicTicketPaypal(View):

    def dispatch_request(self):

        return render_template(
            "public_ticket_paypal.html"
        )
