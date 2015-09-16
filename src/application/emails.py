"""
emails.py

This sends emails

"""

import logging

from application import app

from google.appengine.api import mail

from flask import render_template


class Emails(object):
    """docstring for Emails"""

    sender_address = "HCPP 2015 <" + app.config["SENDER_EMAIL"] + ">"

    @classmethod
    def order_paid(cls, ticket):

        subject = "HCPP 2015 ticket"
        content = render_template(
            "public_ticket_email.html",
            ticket=ticket
        )

        logging.info("Sending email " + subject + " to " + ticket.email)
        mail.send_mail(cls.sender_address, ticket.email, subject, content)

    @classmethod
    def order_waiting_bank(cls, ticket):

        subject = "Payment for ticket to HCPP 2015"
        content = render_template(
            "public_ticket_email_bank.html",
            ticket=ticket
        )

        logging.info("Sending email " + subject + " to " + ticket.email)
        mail.send_mail(cls.sender_address, ticket.email, subject, content)

    @classmethod
    def order_waiting_paypal(cls, ticket):

        subject = "Payment for ticket to HCPP 2015"
        content = render_template(
            "public_ticket_email_paypal.html",
            ticket=ticket
        )

        logging.info("Sending email " + subject + " to " + ticket.email)
        mail.send_mail(cls.sender_address, ticket.email, subject, content)
