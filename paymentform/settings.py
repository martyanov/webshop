# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

from webshop import config

_config_manager = config.ConfigManager()
_config_manager.load_options()

REDIRECTION_TARGET = _config_manager.get_option('paymentform', 'redirection_target', 'http://127.0.0.1:8080')
ISSUER = _config_manager.get_option('paymentform', 'issuer', 'https://www.epointsystem.org/issuer')
MAILRECEIPT_URL = _config_manager.get_option('paymentform', 'mailreceipt_url', 'http://127.0.0.1:8080')
DEBUG = _config_manager.get_option('paymentform', 'debug', 'false')

