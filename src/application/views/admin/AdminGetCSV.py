"""
AdminGetCSV.py

Handler for App Engine for /admin/csv

"""

from flask.views import View

from flask import make_response

from ...models import TicketModel


class AdminGetCSV(View):

    def dispatch_request(self):

        tickets = TicketModel.query().order(-TicketModel.created)

        lines = []
        columns = []

        columns.append("Ticket ID")
        columns.append("Email")
        columns.append("Payment method")
        columns.append("Price")
        columns.append("Paid")
        columns.append("Created")
        columns.append("Note")
        columns.append("Hidden")

        lines.append(self.add_line(columns))

        for ticket in tickets:

            columns = []

            columns.append(ticket.key.id())
            columns.append(ticket.email)
            columns.append(ticket.payment_method)
            columns.append(str(ticket.price))
            columns.append(str(ticket.paid))
            columns.append(ticket.created.strftime("%d.%m.%Y %H:%M"))
            columns.append(str(ticket.note))
            columns.append(str(ticket.hidden))

            lines.append(self.add_line(columns))

        csv_file = u"\n".join(lines)

        response = make_response(csv_file)

        response.headers["Content-Disposition"] = "attachment; filename=tickets.csv"

        return response

    def add_line(self, columns):

        return u";".join(columns)
