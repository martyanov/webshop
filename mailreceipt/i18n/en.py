# -*- coding: utf-8 -*-

# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

_translations = {
    'Your receipt will be emailed shortly. Thank you for your patience!':
        'Your receipt will be emailed shortly. Thank you for your patience!',
    'Payment receipt, reference:': 'Payment receipt, reference:',
    'Malformed request': 'Malformed request',
    'Request was completed successfully': 'Request was completed successfully',
    'You should use POST request with Content-Type: application/x-www-form-urlencoded and appropriate parameters list.':
        'You should use POST request with Content-Type: application/x-www-form-urlencoded and appropriate parameters list.'
}

def translate(msgid):
    try:
        return _translations[msgid]
    except KeyError:
        return msgid

