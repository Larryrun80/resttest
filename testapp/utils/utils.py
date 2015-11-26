#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow


def print_log(log_words):
    prefix = '[ {0} ]'.format(arrow.now('Asia/Shanghai')
                                   .format('YYYY-MM-DD HH:mm:ss:SSS'))
    print('{0} {1}'.format(prefix, log_words))
