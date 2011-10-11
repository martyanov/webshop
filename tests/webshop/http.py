# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import unittest

from webshop.http import parse_accept_language_header


class HTTPTestCase(unittest.TestCase):
    
    def testAcceptHeaderWithQualityValuesWithoutWhitespacesLowerCase(self):
        "Test accept language header parsing input 1"
        self.assertEqual(parse_accept_language_header('en,en-us;q=0.6,da;q=0.4,es;q=0.5'), ['en', 'es', 'da'])

    def testAcceptHeaderWithQualityValuesWithWhitespacesLowerCase(self):
        "Test accept language header parsing input 2"
        self.assertEqual(parse_accept_language_header(' en, en-us;q=0.6,da ;q=0.4 ,es;q=0.5 '), ['en', 'es', 'da'])

    def testAcceptHeaderWithQualityValuesWithWhitespacesLowerAndUpperCase(self):
        "Test accept language header parsing input 3"
        self.assertEqual(parse_accept_language_header(' en, en-US;q=0.6,DA ;q=0.4 ,ES;q=0.5 '), ['en', 'es', 'da'])

    def testAcceptHeaderWithoutQualityValuesWithWhitespacesLowerAndUpperCase(self):
        "Test accept language header parsing input 4"
        self.assertEqual(parse_accept_language_header(' en, en-US ,DA, ES '), ['en', 'da', 'es'])
        
if __name__ == '__main__':
    unittest.main()
