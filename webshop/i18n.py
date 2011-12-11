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

from flask import request

from webshop.config import ConfigManager
from webshop.http import get_language_from_request, get_accept_language
from webshop.http import parse_accept_language_header
from webshop import settings

language_re = re.compile(r'^[a-zA-Z]{2}$')


class I18N(object):

    def __init__(self, translations_dir):
        self._translations_dir = translations_dir
        self._supported_languages = {}

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
        Return the best matched language tag if available,
        otherwise return None
        """
        accept_language = get_accept_language()
        if accept_language is not None:
            try:
                language_tags = parse_accept_language_header(accept_language)
                for language_tag in language_tags:
                    if language_tag in self._supported_languages:
                        return language_tag
            except:
                return None
        return None

    def get_current_language_tag(self):
        """
        Return the current language tag for translation

        WARNING: function modifies the language cookie value in some conditions,
                 bad practice, needs refactoring
        """
        lang_from_request = get_language_from_request()
        if lang_from_request in self._supported_languages:
            self._set_language_tag(lang_from_request)
            return lang_from_request
        lang_from_cookie = request.cookies.get('wslang', '')
        if lang_from_cookie in self._supported_languages:
            return lang_from_cookie
        lang_from_browser = self._get_best_matched_language_tag()
        if lang_from_browser is not None:
            self._set_language_tag(lang_from_browser)
            return lang_from_browser
        return settings.LANGUAGE

    def _set_language_tag(self, language_tag):
        """
        Set the language cookie
        """
        if language_re.match(language_tag) and \
            language_tag in self._supported_languages:
            response.set_cookie('wslang', language_tag)

    def get_current_language(self):
        return self._supported_languages[self.get_current_language_tag()]
