# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import os.path

from webshop.i18n import I18N

_i18n = I18N(os.path.dirname(os.path.realpath(__file__)))
_i18n.update_supported_languages()

def translate(msgid):
    return _i18n.get_current_language().translate(msgid)
