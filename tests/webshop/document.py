# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import unittest

from webshop.gpg import GPG
from webshop.protocol import parse_message
from webshop.document import Document

PUB_KEY = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.2 (MingW32)

mQGiBEu16GoRBAC7YX76UukPV+2ZHFHPL/aVJ8yQ9k+ARHWe1F78o8l6Com8AHqu
MBHQGaDqeBAxq4Njr7SjQvgJlPftvowYc1a0KAT86w/ruppOiRwjIR4jz+ghfNt7
aQkeWsYhCW/kDKWg7GWn7sKe93rsBUY6d8vx4rSYk/lhFs1M350ksJ7FewCgxGoH
2pfZwuN8YC5kTkFWxxoxl1cD/2praroorf1+/k9I2QDzwev2NEdNXTCez+71hPDy
9dwt3lRonoUCAi7lJZNy/xJSS146BWWYDkyiN5kDkW0jDdm6iPJZ7MICN5rVoJ6S
736RcUdXRMKVcQbGiI29yvpBv5Sa6xZk2qpQV+rMlG3znRRPxcjYwrpjBpcZE4CE
CL/TA/9hJmJHqIRqJEbQBTyHjotcS3HpefZ8TDfhiifC0aui3wZRvJAinM4FK2S4
0SBrKKOoeCbz0bEqZhMoFzFaJ086S5eWG41nF5TaHrc2hJ5n79PtpIGppkzYfDeJ
RkRo3wK1tCRyGuIQdI7ROtWaEcY5vxXXiH/Nw+JXgZ62qQzygrQ1d3d3LmVwb2lu
dHN5c3RlbS5vcmcvaXNzdWVyIDxpc3N1ZXJAZXBvaW50c3lzdGVtLm9yZz6IXQQT
EQIAHQUCS7XoagYLCQgHAwIEFQIIAwQWAgMBAh4BAheAAAoJEM/Y4LwsPGxOlS4A
oMEDdztRu6W/NoR2SxGNblWHwxUOAKCp6350KRKYs7jb7fPGDyfaw2/rRLkBDQRL
tehrEAQA7z2ZVobf9PTu4JgS2/xXOnTTobyYWpNpR80Axw/PHvmgeQIT48/kHZCK
cLWk6Xs6IaNnKrvLwo5/6fnG/KoYopJ9POPxy/3CPeneZov9ZD+bo7R1uJY0VBei
4u/bZMd835+Yg1ZhupIUqag9t0LrsQr7XJksC9pjx5frGqMOu68AAwUD/R3NJQu0
BJ9eFqabzo6V3j2CVybgNbmu8diT/uHmMtmzMIib70TNIXknEM0UDnD5NKwUAkuN
n/6XXR3TYEzpZISLIdJEhwPJnR0JjOi9fwrB6GUbh4fplv11jeM22p8HCx0RVOm2
X4ytjte0NPj96hz5GT7y+/VxwlM/iz+VGkTDiEYEGBECAAYFAku16GsACgkQz9jg
vCw8bE5QPACgje2GMSBKI0wrw8W4IDgCwcBUdOQAn1a2+m/FvVwng45OiDKRjolE
GWvP
=qv0Y
-----END PGP PUBLIC KEY BLOCK-----
"""

CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE = """-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Content-type: text/plain.epoint.certificate; charset=utf-8
Document-template: https://www.epointsystem.org/issuer/template?ID=4B78EA23722649AF8C8A578BE3B08D6CB34680D7

CERTIFICATE OF VALUE


Value: 3 EPT

ID: 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF

SN: 0000000000000200


Issued by: FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
URL: https://www.epointsystem.org/issuer
Email: issuer@epointsystem.org
Date: 2009-01-14 23:16:36 UTC

Licensed by: N/A

Redemption:
 The issuer identified by the OpenPGP public key
 FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
 pursuant to the service contract as published at
 https://www.epointsystem.org/issuer/service
 (1) shall redeem the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 for newly issued certificates equal to 3 ePoints
 or for goods and services worth 3 ePoints to
 whoever reveals the sequence first and
 (2) shall accept the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 as tender of existing debt equal to 3 ePoints
 of the one who reveals the sequence first.

Validity:
 This certificate is valid only with a valid digital signature
 of the issuer.

Notes:
+giWAB5CiYP8F
~
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.2 (MingW32)

iD8DBQFLtgGQz9jgvCw8bE4RAlTnAJ9cvYDyNUigFmtVHWFng7HH+amU6QCgiErl
F0hLGp/9AR5dW5/h8ogP1tw=
=Wnq2
-----END PGP SIGNATURE-----
"""

VALID_SIGNATURE = """-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.2 (MingW32)

iD8DBQFLtgGQz9jgvCw8bE4RAlTnAJ9cvYDyNUigFmtVHWFng7HH+amU6QCgiErl
F0hLGp/9AR5dW5/h8ogP1tw=
=Wnq2
-----END PGP SIGNATURE-----
"""

VALID_BODY = """Content-type: text/plain.epoint.certificate; charset=utf-8
Document-template: https://www.epointsystem.org/issuer/template?ID=4B78EA23722649AF8C8A578BE3B08D6CB34680D7

CERTIFICATE OF VALUE


Value: 3 EPT

ID: 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF

SN: 0000000000000200


Issued by: FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
URL: https://www.epointsystem.org/issuer
Email: issuer@epointsystem.org
Date: 2009-01-14 23:16:36 UTC

Licensed by: N/A

Redemption:
 The issuer identified by the OpenPGP public key
 FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
 pursuant to the service contract as published at
 https://www.epointsystem.org/issuer/service
 (1) shall redeem the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 for newly issued certificates equal to 3 ePoints
 or for goods and services worth 3 ePoints to
 whoever reveals the sequence first and
 (2) shall accept the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 as tender of existing debt equal to 3 ePoints
 of the one who reveals the sequence first.

Validity:
 This certificate is valid only with a valid digital signature
 of the issuer.

Notes:
+giWAB5CiYP8F
~"""

# The same as CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE, but Value is equal to 30
CORRECT_CERTIFICATE_WITH_INVALID_SIGNATURE = """-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Content-type: text/plain.epoint.certificate; charset=utf-8
Document-template: https://www.epointsystem.org/issuer/template?ID=4B78EA23722649AF8C8A578BE3B08D6CB34680D7

CERTIFICATE OF VALUE


Value: 30 EPT

ID: 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF

SN: 0000000000000200


Issued by: FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
URL: https://www.epointsystem.org/issuer
Email: issuer@epointsystem.org
Date: 2009-01-14 23:16:36 UTC

Licensed by: N/A

Redemption:
 The issuer identified by the OpenPGP public key
 FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
 pursuant to the service contract as published at
 https://www.epointsystem.org/issuer/service
 (1) shall redeem the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 for newly issued certificates equal to 3 ePoints
 or for goods and services worth 3 ePoints to
 whoever reveals the sequence first and
 (2) shall accept the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 as tender of existing debt equal to 3 ePoints
 of the one who reveals the sequence first.

Validity:
 This certificate is valid only with a valid digital signature
 of the issuer.

Notes:
+giWAB5CiYP8F
~
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.2 (MingW32)

iD8DBQFLtgGQz9jgvCw8bE4RAlTnAJ9cvYDyNUigFmtVHWFng7HH+amU6QCgiErl
F0hLGp/9AR5dW5/h8ogP1tw=
=Wnq2
-----END PGP SIGNATURE-----
"""

INCORRECT_CERTIFICATE_WITH_VALID_SIGNATURE = """-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

Content-type: text/plain.epoint.certificate; charset=utf-8
Document-template: https://www.epointsystem.org/issuer/template?ID=4B78EA23722649AF8C8A578BE3B08D6CB34680D7

CERTIFICATE OF VALUE


Va: 3 EPT

ID: 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF

SN: 0000000000000200


Issued by: FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
URL: https://www.epointsystem.org/issuer
Email: issuer@epointsystem.org
Date: 2009-01-14 23:16:36 UTC

Licensed by: N/A

Redemption:
 The issuer identified by the OpenPGP public key
 FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58
 pursuant to the service contract as published at
 https://www.epointsystem.org/issuer/service
 (1) shall redeem the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 for newly issued certificates equal to 3 ePoints
 or for goods and services worth 3 ePoints to
 whoever reveals the sequence first and
 (2) shall accept the binary sequence with the message
 digest 64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF (SHA1)
 as tender of existing debt equal to 3 ePoints
 of the one who reveals the sequence first.

Validity:
 This certificate is valid only with a valid digital signature
 of the issuer.

Notes:
+giWAB5CiYP8F
~
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.2 (MingW32)

iD8DBQFLtgIHz9jgvCw8bE4RAlsMAJ4pYjAx9bwF5upaqIrmI3nvJSLvWgCgikyO
1bUIA2LLhgEzOghijvlE2uQ=
=xGrB
-----END PGP SIGNATURE-----
"""

def parser_stub_func(data):
    return {
        'LICENSORS': 'N/A',
        'URL': 'https://www.epointsystem.org/issuer',
        'VALUE': '3',
        'ID': '64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF',
        'MD_ALGO': 'SHA1',
        'SN': '0000000000000200',
        'ISSUER_NOTES': 'SOME NOTES...',
        'DATE': '2009-01-14 23:16:36 UTC',
        'EMAIL': 'issuer@epointsystem.org',
        'ISSUER': 'FF55 B81E 2F9B 6E12 C65D  6153 BFB2 2A21 0DC8 3F58'
    }


class DocumentSourceMock(object):

    def __init__(self, data):
        self.data = data

    def fetch(self):
        return self.data

class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.gpg = GPG()
        self.gpg.import_keys(PUB_KEY)

    def testGetCertificateID(self):
        "Test result value of document ID"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertTrue(document.verify())
        self.assertEquals(document.get_id(), '64D0 F8CA 822B BDF0 FF59  42F6 A363 ED80 D8A5 CEFF')

    def testGetSignature(self):
        "Test result value of document signature"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertTrue(document.verify())
        self.assertEquals(document.get_signature(), VALID_SIGNATURE)

    def testGetBody(self):
        "Test result value of document body"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertTrue(document.verify())
        self.assertEquals(document.get_body(), VALID_BODY)

    def testGetRawData(self):
        "Test result value of document raw data"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertTrue(document.verify())
        self.assertEquals(document.get_raw_data(), CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE)


class DocumentVerificationTestCase(unittest.TestCase):

    def setUp(self):
        self.gpg = GPG()
        self.gpg.import_keys(PUB_KEY)

    def testCorrectCertificateWithValidSignature(self):
        "Test correct certificate with valid signature"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertTrue(document.verify())

    def testCorrectCertificateWithInvalidSignature(self):
        "Test correct certificate with invalid signature"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_INVALID_SIGNATURE))
        document = Document(source)
        self.assertFalse(document.verify())

    def testIncorrectCertificateWithValidSignature(self):
        "Test incorrect certificate with valid signature"
        source = DocumentSourceMock((200, INCORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertTrue(document.verify())


class DocumentValueTestCase(unittest.TestCase):

    def testGetValueUponStatus200(self):
        "Test result value upon status 200"
        source = DocumentSourceMock((200, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertEquals(document.get_value(parser_func=parser_stub_func), 3)

    def testGetValueUponStatus404(self):
        "Test result value upon status 404"
        source = DocumentSourceMock((404, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertEquals(document.get_value(parser_func=parser_stub_func), 0)

    def testGetValueUponWrongStatus(self):
        "Test result value upon wrong status"
        source = DocumentSourceMock((405, CORRECT_CERTIFICATE_WITH_VALID_SIGNATURE))
        document = Document(source)
        self.assertEquals(document.get_value(parser_func=parser_stub_func), None)

if __name__ == '__main__':
    unittest.main()

