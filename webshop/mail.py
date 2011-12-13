# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import socket
import smtplib
from email.mime.text import MIMEText

from mailreceipt.settings import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, USE_SSL, USE_TLS

from flask import current_app

class MailerException(Exception):
    pass

class MailTransport(object):
    """
    Base class for all transport implementations
    """

    def send(self, message):
        raise NotImplementedError


class SMTPTransport(MailTransport):
    """
    SMTP transport implementation
    """

    def __init__(self, host=SMTP_HOST, port=SMTP_PORT, username=SMTP_USERNAME,
                 password=SMTP_PASSWORD, use_ssl=USE_SSL, use_tls=USE_TLS,
                 suppress_exceptions=True):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = True if use_ssl == 'true' else False
        self.use_tls = True if use_tls == 'true' else False
        self.suppress_exceptions = suppress_exceptions

    def _connect(self):
        """
        Open a connection to the mail host
        """
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        if self.use_tls:
            server.starttls()
        if self.username and self.password:
            server.login(self.username, self.password)

        return server

    def send(self, message):
        """
        Send a message
        """
        try:
            server = self._connect()
        except (smtplib.SMTPException, socket.error), err:
            current_app.logger.error('Connection failure %s' % err)
            if self.suppress_exceptions:
                return
            else:
                raise MailerException('Connection failure %s' % err)

        try:
            server.sendmail(message.from_address, message.to_address,
                            message.as_string())
        except smtplib.SMTPException, err:
            current_app.logger.error('Sending failure: %s' % err)
            if not self.suppress_exceptions:
                raise MailerException('Sending failure %s' % err)
        finally:
            server.quit()
            server = None

            
class Mailer(object):
    """
    Base class for sending messages
    """

    def __init__(self, transport=SMTPTransport, suppress_exceptions=True):
            self.transport = transport(suppress_exceptions=suppress_exceptions)

    def send(self, message):
        self.transport.send(message)