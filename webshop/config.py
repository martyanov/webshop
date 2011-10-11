# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import ConfigParser

class ConfigManager(object):
    #TODO: return bool parameters as bools, not strings

    def __init__(self, config_file='/etc/webshop.conf'):
        self._options = {}
        self._config_file = config_file

    def load_options(self):
        parser = ConfigParser.ConfigParser()
        try:
            parser.readfp(open(self._config_file))
        except IOError:
            return
        for section_name in parser.sections():
            section_options = {}
            for (name, value) in parser.items(section_name):
                section_options[name] = value
            self._options[section_name] = section_options


    def get_option(self, section_name, key, default=None):
        section = self._options.get(section_name, None)
        if section:
            return section.get(key, default)
        else:
            return default

    def get_options(self):
        if self._options:
            return self._options
        else:
            return {}

