"""
PublicWarmup.py

Handler for App Engine warmp up requests

"""

from flask.views import View


class PublicWarmup(View):

    def dispatch_request(self):

        return "I'm hot :)"
