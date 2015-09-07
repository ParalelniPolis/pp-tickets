"""
AdminIndex.py

Handler for App Engine for /admin

"""

from flask.views import View

from flask import render_template, redirect

from ...models import TicketModel


class AdminIndex(View):

    def dispatch_request(self):

        return redirect("/admin/tickets")

        # last_tickets = TicketModel.query().fetch(10)

        # return render_template(
        #     "admin_index.html",
        #     last_tickets=last_tickets
        # )
