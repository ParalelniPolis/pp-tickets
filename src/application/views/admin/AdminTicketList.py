"""
AdminTicketList.py

Handler for App Engine for /admin

"""

from flask.views import View

from flask import render_template

from ...models import TicketModel


class AdminTicketList(View):

    def dispatch_request(self):

        tickets = TicketModel.query().order(-TicketModel.created)

        return render_template(
            "admin_ticket_list.html",
            tickets=tickets
        )
