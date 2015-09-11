"""
AdminIndex.py

Handler for App Engine for /admin

"""

from flask.views import View

from flask import render_template

from ...models import TicketModel


class AdminIndex(View):

    def dispatch_request(self):

        tickets = TicketModel.query().order(-TicketModel.created).fetch(10)

        tickets_count_all = TicketModel.query(TicketModel.paid == True)

        return render_template(
            "admin_index.html",
            tickets=tickets,
            tickets_all=self.count_all(tickets_count_all),
            tickets_btc=self.count_by_method(tickets_count_all, "BTC"),
            tickets_bank=self.count_by_method(tickets_count_all, "WIRETRANSFER"),
            tickets_paypal=self.count_by_method(tickets_count_all, "PAYPAL")
        )

    def count_by_method(self, tickets, method):

        tickets_sum = 0

        for ticket in tickets:

            if ticket.payment_method == method and not ticket.hidden:

                tickets_sum += 1

        return tickets_sum

    def count_all(self, tickets):

        tickets_sum = 0

        for ticket in tickets:

            if not ticket.hidden:

                tickets_sum += 1

        return tickets_sum
