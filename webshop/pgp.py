# -*- coding: utf-8 -*

# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import base64

from webshop.gpg import GPG
from webshop.protocol import extract_signature, strip_signature
from webshop import settings

def extract_signature_packet(data):
    """
    Extract signature packet from the document pgp signature
    """
    begin = data.find("\n\n")
    end = data.find("-----END")
    signature_in_b64 = data[begin+2:end-7]
    return base64.b64decode(signature_in_b64)


def make_one_pass_signature_packet(signature):
    """
    Extract information from the signature packet and
    compile an OpenPGP one-pass signature packet

    See details in RFC4880
    """
    ver = signature[2]
    sig_type = signature[4]
    hash_algo = signature[18]
    pub_key_algo = signature[17]
    key_id = signature[9:17]
    nested = chr(1)

    return "%s%s%s%s%s%s" % (
        ver,
        sig_type,
        hash_algo,
        pub_key_algo,
        key_id,
        nested
    )


def make_document(data):
    """
    Make OpenPGP document containing one-pass signature packet,
    literal packet and binary signature packet

    See details in RFC4880
    """
    g = GPG(gnupghome=settings.GNUPG_HOME)
    header = "%s%s" % (chr(144), chr(13)) #0x90 0x0D
    signature_packet = extract_signature_packet(extract_signature(data))
    body = strip_signature(data).rstrip()
    literal_packet = g.store(body).data
    one_pass_signature_packet = make_one_pass_signature_packet(signature_packet)
    return "%s%s%s%s" % (
        header,
        one_pass_signature_packet,
        literal_packet,
        signature_packet
    )