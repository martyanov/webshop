# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import re
import urllib2

import cherrypy

accept_language_tag_re = re.compile(r'^[a-zA-Z]{1,8}(-[a-zA-Z]{1,8})?$')

class HTTPError(Exception):
    pass

def urlfetch(url):
    """
    Fetch a document at the URL given in url.
    """

    opener = urllib2.build_opener()
    try:
        response = opener.open(url)
    except IOError, e:
        if hasattr(e, 'code'):
            if e.code == 404:
                return (e.code, e.read())
            else:
                raise HTTPError('Network error: %s' % e.code)
        elif hasattr(e, 'reason'):
                raise HTTPError('Network error: %s' % e.reason)
    return (response.code, response.read())

def get_language_from_request():
    return cherrypy.request.params.get('L', '')

def get_accept_language():
    return cherrypy.request.headers.get('Accept-Language')

def parse_accept_language_header(accept_language_string):
    """
    Parse the Accept-Language header.

    The grammar is described in RFC 2616 section 14.4
    Return a list of unique two-letter tags sorted by their quality values
    Example: en,en-us;q=0.6,da;q=0.4,es;q=0.5
    Result: ['en', 'es', 'da']
    """
    parsed_language_tags = []
    languages = accept_language_string.lower().replace(' ', '').split(',')
    for language in languages:
        language_tag, sep, quality = language.partition(';')
        if accept_language_tag_re.match(language_tag):
            q, sep, value = quality.partition('=')
            if q == 'q':
                try:
                    value = float(value)
                except ValueError:
                    pass
            else:
                value = 1.0
            parsed_language_tags.append((language_tag[0:2], value))
    parsed_language_tags.sort(lambda a, b: -cmp(a[1], b[1]))
    sorted_language_tags = []
    [sorted_language_tags.append(l) for (l, q) in parsed_language_tags \
        if l not in sorted_language_tags]
    return sorted_language_tags

