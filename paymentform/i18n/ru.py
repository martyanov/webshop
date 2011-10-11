# -*- coding: utf-8 -*-

# ePoint WebShop
# Copyright (C) 2010 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

_translations = {
    # Шаблонные
    'WebShop Invoice': u'WebShop Инвойс',
    'Enter ePoint RAND:': u'Введите рэнд ePoint:',
    'Enter email address:': u'Введите адрес электронной почты:',
    'Enter pgp encyption key ID (optional):': u'Введите ID ключа шифрования pgp (опционально):',
    'Enable PGP/MIME:': u'Включить PGP/MIME:',
    'Total ePoints uploaded in this session:': u'Общее количество ePoint-ов, потраченных за сессию:',
    'Send': u'Отправить',

    # Общие
    'GET CERTIFICATE': u'ПОЛУЧИТЬ СЕРТИФИКАТ',
    'The corresponding invoice has been paid': u'Текущий инвойс оплачен',
    'Missing parameter': u'Параметр не указан',
    'Parameter D is missing': u'Параметр D отсутствует',
    'Internal error': u'Внутренняя ошибка сервера',
    'Sorry for the inconvenience': u'Приносим извинения за неудобства',
}

def translate(msgid):
    try:
        return _translations[msgid]
    except KeyError:
        return msgid
