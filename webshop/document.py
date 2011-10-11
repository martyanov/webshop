# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

from webshop.gpg import GPG
from webshop.http import urlfetch, HTTPError
from webshop.protocol import parse_message, strip_signature, extract_signature
from webshop.protocol import TemplateError

class DocumentSource(object):
    
    def __init__(self, issuer, docid=None, sn=None):
        if docid:
            self.url = '%s/info?ID=%s' % (issuer, docid)
        elif sn:
            self.url = '%s/%s' % (issuer, sn)
    
    def fetch(self):
        try:
            data = urlfetch(self.url)
        except HTTPError:
            return None
    
        return data
        

class Document(object):
    """TODO: cache all the values to eliminate computation overhead"""    
    
    def __init__(self, source):
        self.source = source
        self.data = source.fetch()
    
    def verify(self):
        if self.data is None:
            return False
        if self.data[0] != 200:
            return None
        gpg = GPG()
        try:
            verified = gpg.verify(self.data[1])
        except Exception:
            return False
        return verified
        
    def get_value(self, parser_func=parse_message):
        if self.data is not None:
            code = self.data[0]
            body = self.data[1]
            if code == 404:
                return 0
            elif code == 200:
                try:
                    values = parser_func(body)
                except TemplateError:
                    return None
                return int(values['VALUE'])
            else:
                return None
        else:
            return None

    def get_id(self):
        try:
            values = parse_message(self.data[1])
            _id = values['ID']
        except TemplateError:
            return None
        return _id

    def get_sn(self):
        try:
            values = parse_message(self.data[1])
            sn = values['SN']
        except TemplateError:
            return None
        return sn

    def get_signature(self):
        try:
            signature = extract_signature(self.data[1])
        except TemplateError:
            return None
        return signature

    def get_body(self):
        body = strip_signature(self.data[1])
        return body[0:len(body) - 1]

    def get_raw_data(self):
        return self.data[1]
