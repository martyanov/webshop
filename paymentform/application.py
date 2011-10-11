# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import os.path
import sys

sys.stdout = sys.stderr

import cherrypy

from webshop.document import DocumentSource, Document
from webshop.cookie import get_cookie_value, set_cookie_value

from paymentform import settings
from paymentform.templates import *
from paymentform.i18n import translate as _

class Invoice(object):
    def __init__(self, D, B='', F=0, issuer=settings.ISSUER):
        self.certificate_link = ''
        self.message = ''
        self.issuer = issuer
        self.value = 0
        self.D = D
        self.B =  B
        self.F = F


class InvoiceApp(object):

    def _render_error_page(self, error_title, error_details, status=500):
        cherrypy.response.status = status
        error_page = [render_header()]
        error_page.append(render_error(error_title, error_details))
        error_page.append(render_footer())
        return error_page

    @cherrypy.expose
    def index(self, D=None, B=None, F=None, E=None, K=None, L=None, **params):
        cherrypy.response.headers['Content-Type'] = "text/html"
        if F is not None:
            try:
                F = int(F)
            except ValueError:
                F = 0
        else:
            F = 0
        page = [render_header()]
        if D is None:
            return self._render_error_page(_('Missing parameter'),
                _('Parameter D is missing'))
        if B is None:
            B = ''
        if L is None:
            L = ''
        invoice = Invoice(D, B=B, F=F)
        document_source = DocumentSource(settings.ISSUER, docid=invoice.D)
        document = Document(document_source)
        value = None
        verified = document.verify()
        # document.verify() returns False if verification failed
        # and None upon another error
        if verified != False:
            value = document.get_value()
        if value is not None:
            invoice.value = value
            if value > 0:
                invoice.certificate_link = '<a href="%s/info?ID=%s">%s</a>' % (settings.ISSUER,
                    invoice.D, _('GET CERTIFICATE'))
            if (value >= F) and (F is not None) and (F > 0):
                invoice.message = _('The corresponding invoice has been paid')
                cherrypy.response.status = 200
                page.append(render_invoce(invoice))
                # Email address
                email = ''
                if E is not None:
                    set_cookie_value('pfemail', E)
                    email = E
                else:
                    email = get_cookie_value('pfemail')
                # PGP encryption key ID
                pgpkey = ''
                if K is not None:
                    set_cookie_value('pfpgpkey', K)
                    pgpkey = K
                else:
                    pgpkey = get_cookie_value('pfpgpkey')
                # If mailreceipt application is configured render the email form
                if settings.MAILRECEIPT_URL:
                    page.append(render_email_form(email, pgpkey, document.get_sn(),
                        settings.MAILRECEIPT_URL, L))
            else:
                if F > 0:
                    cherrypy.response.headers['Content-Price'] = "%s EPT" % str(F - value)
                cherrypy.response.status = 402
                invoice.G = '%s/?D=%s&F=%s' % (settings.REDIRECTION_TARGET, invoice.D,
                    str(invoice.F))
                page.append(render_invoce_form(invoice))

        else:
            return self._render_error_page(_('Internal error'),
                _('Sorry for the inconvenience'))

        page.append(render_footer())

        return page

def run():
    # Cherrypy configuration settings
    application_conf = {
        'environment': 'embedded',
    }

    debug = True if settings.DEBUG == 'true' else False
    if debug:
        application_conf['request.show_tracebacks'] = True

    # Update CherryPy configuration
    cherrypy.config.update(application_conf)

    # Create an instance of the application
    invoice_app = InvoiceApp()

    return cherrypy.Application(invoice_app, script_name=None, config=None)

