#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow

from ..models.error import RestTestError


def print_log(log_words):
    prefix = '[ {0} ]'.format(arrow.now('Asia/Shanghai')
                                   .format('YYYY-MM-DD HH:mm:ss:SSS'))
    print('{0} {1}'.format(prefix, log_words))


def get_json_with_path(json_obj, path):
    if not str(path).startswith('.'):
        raise RestTestError('FORMAT_ERROR',
                            correct_type='string start with "."')

    if path == '.':
        return json_obj

    elements = path[1:].split('.')
    try:
        for element in elements:
            json_obj = json_obj[element]
    except:
        raise RestTestError('KEY_NOT_FOUND',
                            key=element,
                            collection=json_obj)
    return json_obj
