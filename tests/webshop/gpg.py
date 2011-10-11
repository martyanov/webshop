# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import os
import unittest

from webshop.gpg import GPG

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

CERT = open(os.path.join(TEST_DATA_PATH, 'certificate'), 'r').read()
CERT_RFC1991_LITERAL_DATA_PACKET = open(os.path.join(TEST_DATA_PATH, 'certificate_rfc1991'), 'r').read()


def null_date(data):
    """
    To pass the tests we should set the bytes indicating a date to zero
    """
    dat = list(data)
    dat[4] = dat[5] = dat[6] = dat[7] = chr(0)
    return ''.join(dat)


class GPGTestCase(unittest.TestCase):
    def setUp(self):
        self.gpg = GPG()

    def testCorrectnessOfRFC1991LiteralDataPacket(self):
        "Test correctness of RFC1991 literal data packet generation"
        self.assertEquals(null_date(self.gpg.store(CERT).data), null_date(CERT_RFC1991_LITERAL_DATA_PACKET))

