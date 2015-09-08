"""
AdminTicketDetail.py

Handler for App Engine for /admin/ticket/<ticket_id>

"""

from flask.views import View

from flask import render_template

from ...models import TicketModel


class AdminTicketDetail(View):

    def dispatch_request(self, ticket_id):

        ticket = TicketModel.get_by_id(ticket_id)

        assert ticket is not None

        return render_template(
            "admin_index.html",
            ticket=ticket
        )
