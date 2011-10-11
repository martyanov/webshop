# -*- coding: utf-8 -*-

# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

_translations = {
    # Template translations
    'WebShop Invoice': 'WebShop Invoice',
    'Enter ePoint RAND:': 'Enter ePoint RAND:',
    'Enter email address:': 'Enter email address:',
    'Enter pgp encyption key ID (optional):': 'Enter pgp encyption key ID (optional):',
    'Enable PGP/MIME:': 'Enable PGP/MIME:',
    'Total ePoints uploaded in this session:': 'Total ePoints uploaded in this session:',
    'Send': 'Send',
    
    # General translations
    'GET CERTIFICATE': 'GET CERTIFICATE',
    'The corresponding invoice has been paid': 'The corresponding invoice has been paid',
    'Missing parameter': 'Missing parameter',
    'Parameter D is missing': 'Parameter D is missing',
    'Internal error': 'Internal error',
    'Sorry for the inconvenience': 'Sorry for the inconvenience',
}

def translate(msgid):
    try:
        return _translations[msgid]
    except KeyError:
        return msgid
