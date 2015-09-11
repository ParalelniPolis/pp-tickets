"""
PublicTicket.py

Handler for App Engine for /ticket

"""

from flask.views import View

from flask import render_template

from ...models import TicketModel


class PublicTicket(View):

    def dispatch_request(self, ticket_id):

        ticket = TicketModel.get_by_id(ticket_id)

        assert ticket is not None

        return render_template(
            "public_ticket.html",
            ticketid=ticket.key.id(),
            ticket=ticket
        )
