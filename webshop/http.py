# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import urllib2

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