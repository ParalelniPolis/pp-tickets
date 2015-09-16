"""
AdminAddTicket.py

Handler for App Engine for /admin/newticket

"""

import logging

from flask.views import View

from flask import render_template, flash, request, redirect

from ...models import TicketModel, gen_new_ticket_id
from ...forms import TikcetAddForm


class AdminAddTicket(View):

    def dispatch_request(self):

        if request.method == "POST":

            form = TikcetAddForm()

            if form.validate_on_submit():

                ticket = TicketModel.get_by_id(form.ticket_id.data)

                if ticket:
                    flash("Ticket ID is not " + form.ticket_id.data + " unique", "error")
                    return redirect("/admin/newticket")

                ticket = TicketModel(id=form.ticket_id.data.upper())
                ticket.email = form.email.data
                ticket.payment_method = "BTC"
                ticket.put()

                flash("Ticket " + form.ticket_id.data + " was saved")
                return redirect("/admin/tickets")

            else:

                flash("Form is not valid", "error")

        form = TikcetAddForm()

        form.ticket_id.data = gen_new_ticket_id()

        return render_template(
            "admin_ticket_new.html",
            form=form
        )
