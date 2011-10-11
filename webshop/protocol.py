# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Authors: Rooslan S. Khayrov, Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import re
import hashlib

from webshop.http import urlfetch

template_cache = {}

class TemplateError(Exception):
    pass

def template_matcher(message, delims):
    result = {}
    pos = 0
    for var, delim in delims:
        i = message.find(delim, pos)
        if i < 0:
            raise TemplateError('Template mismatch')
        if var:
            value = message[pos:i]
            oldvalue = result.get(var)
            if oldvalue is None:
                result[var] = value
            elif value != oldvalue:
                raise TemplateError('Variable mismatch')
        pos = i + len(delim)
    return result

def varname(s):
    if s is None:
        return s
    if s.startswith('{$'):
        if s.find('$', 2) < 0:
            return s[2:-1]
        else:
            raise TemplateError('Invalid variable expression')
    elif s.startswith('${') and s.endswith('}'):
        return s[2:-1]
    elif s.startswith('$') and not s.endswith('}'):
        return s[1:]
    else:
        raise TemplateError('Invalid variable name')

var_re = re.compile(r'((?:(?<!\\)\${?[A-Za-z_][A-Za-z0-9_]*}?)|' \
                    r'(?:{\$[A-Za-z_][A-Za-z0-9_]*.*?}))')

def compile_template(template):
    tokens = [None] + var_re.split(template)
    delims = zip(map(varname, tokens[::2]), tokens[1::2])
    return lambda msg: template_matcher(msg, delims)

dash_escape_re = re.compile(r'^- ', re.MULTILINE)

def strip_signature(message):
    start = message.find('\n\n') + 2
    end = message.find('\n-----BEGIN PGP SIGNATURE-----') + 1
    if start < 0 or end <= 0:
        return message
    else:
        return dash_escape_re.sub('', message[start:end])

header_re = re.compile('^([\x21-\x7E^:]+):\s+(.*)$', re.MULTILINE)

def parse_headers(headers):
    return dict(header_re.findall(headers))

unfoldws_re = re.compile('\n\s+')

def extract_headers(message):
    eol = message.find('\n\n')
    if eol < 0:
        raise TemplateError('No headers found')
    raw_headers = unfoldws_re.sub('', message[:eol])
    return parse_headers(raw_headers), message[eol+2:]

def extract_signature(message):
    start = message.find('~\n-----BEGIN PGP SIGNATURE-----') + 2
    end = len(message)
    if start < 0:
        raise TemplateError('No signature found')
    return message[start:end]

template_url_re = re.compile('/template\?ID=([0-9A-Fa-f]+)$')

def fetch_template(url):
    m = template_url_re.search(url)
    if m:
        digest = m.groups()[0].upper()
        matcher = template_cache.get(digest)
    if not matcher:
        try:
            code, template = urlfetch(url)
        except:
            raise TemplateError('Cannot fetch template')
        if code != 200:
            raise TemplateError('Cannot fetch template')
        matcher = compile_template(template)
        calc_digest = hashlib.sha1(template).hexdigest().upper()
        if digest and calc_digest != digest:
            raise TemplateError('Template digest mismatch at URL %s' % url)
        template_cache[calc_digest] = matcher
    return matcher

def parse_message(message):
    message = strip_signature(message)
    headers, body = extract_headers(message)
    try:
        content_type = headers['Content-type']
        template_url = headers['Document-template']
    except KeyError, e:
        raise TemplateError('Required header "%s" is missing' % str(e))
    varmap = fetch_template(template_url)(body)
    return varmap

