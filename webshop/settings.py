# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

from webshop import config

_config_manager = config.ConfigManager()
_config_manager.load_options()

LANGUAGE = _config_manager.get_option('webshop', 'language', 'en')
GNUPG_HOME = _config_manager.get_option('webshop', 'gnupg_home', None)
DEBUG = _config_manager.get_option('mailreceipt', 'debug', 'false')
