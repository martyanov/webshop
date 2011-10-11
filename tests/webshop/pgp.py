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

from webshop.pgp import extract_signature_packet, make_document

TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

GOOD_SIGNATURE = open(os.path.join(TEST_DATA_PATH, 'good_signature'), 'r').read()
BAD_SIGNATURE = open(os.path.join(TEST_DATA_PATH, 'bad_signature'), 'r').read()
DECODED_SIGNATURE = open(os.path.join(TEST_DATA_PATH, 'decoded_signature'), 'r').read()

CERTIFICATE_ASC = open(os.path.join(TEST_DATA_PATH, 'document.asc'), 'r').read()
CERTIFICATE_GPG = open(os.path.join(TEST_DATA_PATH, 'document.gpg'), 'r').read()

def null_date(data):
    """
    To pass the tests we should set the bytes indicating a date to zero
    """
    dat = list(data)
    dat[19] = dat[20] = dat[21] = dat[22] = chr(0)
    return ''.join(dat)

class PGPTestCase(unittest.TestCase):
    def testExtractionOfGoodSignaturePacket(self):
        "Test the validity of good signature data extracted from the document signature"
        self.assertEquals(extract_signature_packet(GOOD_SIGNATURE), DECODED_SIGNATURE)

    def testExtractionOfBadSignaturePacket(self):
        "Test the invalidity of bad signature data extracted from the document signature"
        self.assertNotEquals(extract_signature_packet(BAD_SIGNATURE), DECODED_SIGNATURE)

    def testMakingOpenPGPDocumentFromCertificate(self):
        "Test the validity of making OpenPGP document from certificate"
        self.assertEquals(null_date(make_document(CERTIFICATE_ASC)), null_date(CERTIFICATE_GPG))
