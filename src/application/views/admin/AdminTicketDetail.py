"""
AdminTicketDetail.py

Handler for App Engine for /admin/ticket/<ticket_id>

"""

import logging

from flask.views import View

from flask import render_template, request, flash, redirect

from ...models import TicketModel
from ...forms import TikcetAdminForm


class AdminTicketDetail(View):

    def dispatch_request(self, ticket_id):

        ticket = TicketModel.get_by_id(ticket_id)

        if request.method == "POST":

            form = TikcetAdminForm()

            if form.validate_on_submit():

                ticket.email = form.email.data
                ticket.price = form.price.data
                ticket.paid = form.paid.data
                ticket.payment_method = form.payment_method.data
                ticket.note = form.note.data
                ticket.hidden = form.hidden.data

                ticket.put()

                logging.info("Ticket " + ticket.key.id() + " has been updated")

                flash("Ticket has been saved")

                return redirect("/admin/ticket/" + ticket.key.id())

            else:

                logging.warning("Ticket form is not valid")

                flash("Form is not valid", "error")

        else:

            form = TikcetAdminForm(obj=ticket)

        assert ticket is not None

        return render_template(
            "admin_ticket_detail.html",
            ticket=ticket,
            form=form
        )
