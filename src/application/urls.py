"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app
from decorators import login_required_user

# Public
from application.views.public.PublicWarmup import PublicWarmup
from application.views.public.PublicIndex import PublicIndex
from application.views.public.PublicSale import PublicSale
from application.views.public.PublicTicket import PublicTicket
from application.views.public.PublicTicketPaypal import PublicTicketPaypal
from application.views.public.PublicNotification import PublicNotification

# Admin
from application.views.admin.AdminIndex import AdminIndex
from application.views.admin.AdminTicketList import AdminTicketList
from application.views.admin.AdminTicketDetail import AdminTicketDetail
from application.views.admin.AdminGetCSV import AdminGetCSV
from application.views.admin.AdminAddTicket import AdminAddTicket

app.add_url_rule('/_ah/warmup', 'PublicWarmup', view_func=PublicWarmup.as_view('PublicWarmup'))

# Public
app.add_url_rule('/', 'PublicIndex', view_func=PublicIndex.as_view('PublicIndex'))
app.add_url_rule('/sale', 'PublicSale', view_func=PublicSale.as_view('PublicSale'), methods=["GET", "POST"])
app.add_url_rule('/ticket/<ticket_id>', 'PublicTicket', view_func=PublicTicket.as_view('PublicTicket'))
app.add_url_rule('/ticket/paypal', 'PublicTicketPaypal', view_func=PublicTicketPaypal.as_view('PublicTicketPaypal'))
app.add_url_rule('/notification', 'PublicNotification', view_func=PublicNotification.as_view('PublicNotification'), methods=["GET", "POST"])

# Admin
app.add_url_rule('/admin', 'AdminIndex', view_func=login_required_user(AdminIndex.as_view('AdminIndex')))
app.add_url_rule('/admin/tickets', 'AdminTicketList', view_func=login_required_user(AdminTicketList.as_view('AdminTicketList')))
app.add_url_rule('/admin/ticket/<ticket_id>', 'AdminTicketDetail', view_func=login_required_user(AdminTicketDetail.as_view('AdminTicketDetail')), methods=["GET", "POST"])
app.add_url_rule('/admin/csv', 'AdminGetCSV', view_func=login_required_user(AdminGetCSV.as_view('AdminGetCSV')))
app.add_url_rule('/admin/newticket', 'AdminAddTicket', view_func=login_required_user(AdminAddTicket.as_view('AdminAddTicket')), methods=["GET", "POST"])


# Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
