# -*- coding: utf-8 -*-

# ePoint WebShop
# Copyright (C) 2011 ePoint Systems Ltd
# Author: Andrey V. Martyanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

_translations = {
    'Your receipt will be emailed shortly. Thank you for your patience!':
        u'Ваш чек вскоре будет доставлен. Спасибо за понимание!',
    'Payment receipt, reference:': u'Платежный чек:',
    'Malformed request': u'Неверно сформирован запрос',
    'Request was completed successfully': u'Запрос был выполнен успешно',
    'You should use POST request with Content-Type: application/x-www-form-urlencoded and appropriate parameters list.':
        u'Вам следует использовать POST запрос с Content-Type: application/x-www-form-urlencoded и соответствующим списком параметров.'
}

def translate(msgid):
    try:
        return _translations[msgid]
    except KeyError:
        return msgid

