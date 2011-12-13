# ePoint WebShop
# Copyright (C) 2010 - 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import os
import imp
import re
import threading

from flask import request, current_app

from webshop import settings

language_re = re.compile(r'^[a-zA-Z]{2}$')


def get_language_from_request():
    return request.params.get('L', '')


class I18N(object):

    def __init__(self, translations_dir):
        self._translations_dir = translations_dir
        self._supported_languages = {}
        self._local = threading.local()
        self._local.current_language_tag = None
        
        # Set the language cookie upon each request
        self._register_set_language_cookie_func()
    
    def __del__(self):
        del self._local

    def _get_available_language_tags(self):
        """
        Return a list of two-letter tags based on file names of language
        files founded in the language_dir
        """
        return [name[:-3] for name in os.listdir(self._translations_dir) \
            if name.endswith('.py') and language_re.match(name[:-3])]

    def update_supported_languages(self):
        """
        Populate the supported languages dictionary with key-value pairs of
        language_tag and appropriate loaded language_module
        """
        available_language_tags = self._get_available_language_tags()
        for language_tag in available_language_tags:
            try:
                f, filepath, desc = imp.find_module(language_tag,
                    [self._translations_dir])
                try:
                    language_module = imp.load_module(language_tag, f,
                        filepath, desc)
                    self._supported_languages[language_tag] = language_module
                except:
                    pass
                finally:
                    if f:
                        f.close()
            except ImportError:
                pass

    def _get_best_matched_language_tag(self):
        """
        Return the current language tag for translation
        """
        lang_from_request = get_language_from_request()
        if lang_from_request in self._supported_languages:
            self._local.current_language_tag = lang_from_request
            return self._local.current_language_tag
        lang_from_cookie = request.cookies.get('wslang', '')
        if lang_from_cookie in self._supported_languages:
            self._local.current_language_tag = lang_from_cookie
            return self._local.current_language_tag
        lang_from_browser = request.accept_languages.best_match(
            self._supported_languages)
        if lang_from_browser is not None:
            self._local.current_language_tag = lang_from_browser
            return self._local.current_language_tag
        self._local.current_language_tag = settings.LANGUAGE
        return self._local.current_language_tag

    def _register_set_language_cookie_func(self):
        @current_app.after_request
        def _set_language_cookie(response):
            """
            Set the language cookie
            """
            response.set_cookie('wslang', self._local.current_language_tag)
            return response

    def get_current_language(self):
        """
        Return the current language module 
        """
        return self._supported_languages[self._get_current_language_tag()]