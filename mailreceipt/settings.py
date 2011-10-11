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

ISSUER = _config_manager.get_option('mailreceipt', 'issuer', 'https://www.epointsystem.org/issuer')
SMTP_HOST = _config_manager.get_option('mailreceipt', 'smtp_host', 'localhost')
SMTP_PORT = _config_manager.get_option('mailreceipt', 'smtp_port', '25')
SMTP_USERNAME = _config_manager.get_option('mailreceipt', 'smtp_username', '')
SMTP_PASSWORD = _config_manager.get_option('mailreceipt', 'smtp_password', '')
USE_SSL = _config_manager.get_option('mailreceipt', 'use_ssl', 'false')
USE_TLS = _config_manager.get_option('mailreceipt', 'use_tls', 'false')
DEBUG = _config_manager.get_option('mailreceipt', 'debug', 'false')

