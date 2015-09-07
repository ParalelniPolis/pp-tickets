"""
PublicIndex.py

Handler for App Engine for /

"""

from flask.views import View

from flask import render_template

from ...forms import TikcetForm


class PublicIndex(View):

    def dispatch_request(self):

        form = TikcetForm()

        return render_template(
            "public_index.html",
            form=form
        )
