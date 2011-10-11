# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import cherrypy

COOKIE_MAX_AGE = 316224000 #60 * 60 * 24 * 366 * 10 = 10 years


def get_cookie_value(key):
    try:
        return cherrypy.request.cookie[key].value
    except KeyError, e:
        return ''


def set_cookie_value(key, value, max_age=COOKIE_MAX_AGE):
    cookie = cherrypy.response.cookie
    cookie[key] = value
    cookie[key]['max-age'] = max_age
