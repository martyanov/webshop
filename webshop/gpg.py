# -*- coding: utf-8 -*

# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

import re

from gnupg import GPG, ImportResult, Crypt, logger
from gnupg import _is_sequence, _make_binary_stream

key_id_re = re.compile(r'^(0x)*([0-9a-fA-F]{8})$')


def monkeypatch_method(cls):
    """
    Simple decorator that helps to add or to overrride a method
    in an existing class
    """
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


@monkeypatch_method(GPG)
def receive_keys(self, fingerprints, keyserver=None, always_trust=False):
    """
    Receive keys from public key servers
    """
    if _is_sequence(fingerprints):
        fingerprints = ' '.join(fingerprints)
    args = []
    if always_trust:
        args.append('--always-trust')
    args.append('--recv-keys %s' % fingerprints)
    if keyserver:
        args.append('--keyserver %s' % keyserver)
    result = ImportResult()
    logger.debug('receive_keys: %r', fingerprints)
    p = self._open_subprocess(args)
    self._collect_output(p, result, stdin=p.stdin)
    logger.debug('receive_keys: %r', result.__dict__)
    return result


@monkeypatch_method(GPG)
def store(self, data, **kwargs):
    """
    Process the message contained in the string 'data'
    """
    data = _make_binary_stream(data, self.encoding)
    result = self.store_file(data, **kwargs)
    data.close()
    return result


@monkeypatch_method(GPG)
def store_file(self, file, compress_algo=None):
    """
    Make a simple RFC1991 literal data packet

    Process the message read from the file-like object 'file'
    """
    args = ['-t']
    if compress_algo:
        args.append('--compress-algo %s' % compress_algo)
    else:
        args.append('--compress-algo none')
    args.append('--store')
    result = StoreResult(self.encoding)
    self._handle_io(args, file, result)
    logger.debug('store: %s', result.data, binary=False)
    return result


@monkeypatch_method(GPG)
def encrypt_file(self, file, recipients, sign=None,
                 always_trust=False, passphrase=None,
                 armor=True, output=None, no_literal=False):
    """
    Encrypt the message read from the file-like object 'file'

    We patch the original version to add an optional --no-literal parameter
    """
    args = []
    if no_literal:
        args.append('--no-literal --encrypt')
    else:
        args.append('--encrypt')
    if armor:   # create ascii-armored output - set to False for binary output
        args.append('--armor')
    if output:  # write the output to a file with the specified name
        if os.path.exists(output):
            os.remove(output) # to avoid overwrite confirmation message
        args.append('--output %s' % output)
    if not _is_sequence(recipients):
        recipients = (recipients,)
    for recipient in recipients:
        args.append('--recipient %s' % recipient)
    if sign:
        args.append("--sign --default-key %s" % sign)
    if always_trust:
        args.append("--always-trust")
    result = Crypt(self.encoding)
    self._handle_io(args, file, result, passphrase=passphrase, binary=True)
    logger.debug('encrypt result: %r', result.data)
    return result


class StoreResult(object):
    """
    Handle store result
    """
    def __init__(self, encoding):
        self.data = ''
        self.encoding = encoding

    #def __str__(self):
    #    return self.data.decode(self.encoding)

    def handle_status(self, key, value):
        pass
