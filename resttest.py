#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: resttest.py

import json
import os
import traceback

import arrow
import requests

from utils import colortext

YAML_DIR = 'testfiles'
REQUEST_KEYS = ('id', 'name', 'description', 'order', 'requests',)


def print_log(log_words):
    prefix = '[ {0} ]'.format(arrow.now('Asia/Shanghai')
                                   .format('YYYY-MM-DD HH:mm:ss:SSS'))
    print('{0} {1}'.format(prefix, log_words))


def test(json_info):
    for key in REQUEST_KEYS:
        if key not in json_info.keys():
            print_log('key "{0}" not in json, invalid format'.format(key))

    print_log('starting deal test {0}'.format(
                        colortext.output(json_info['name'], 'red')))

    for test_id in json_info['order']:
        print_log('dealing request {0}'.format(test_id))
        for request in json_info['requests']:
            if request['id'] == test_id:
                print_log('testing: {0}'.format(
                    colortext.output(request['name'], 'purple')))
                print_log('{0} {1}'.format(
                    colortext.output(request['method'], 'yellow'),
                    colortext.output(request['url'], 'yellow')))
                print_log('-'*50)


if __name__ == '__main__':
    try:
        if not os.path.isdir(YAML_DIR):
            raise RuntimeError('directory {0} not exists!'.format(YAML_DIR))

        for tfile in os.listdir(YAML_DIR):
            testfile = '{0}/{1}'.format(YAML_DIR, tfile)
            if os.path.isfile(testfile):
                with open(testfile, encoding='utf-8') as f:
                    try:
                        test_info = json.loads(f.read())
                        test(test_info)
                    except json.decoder.JSONDecodeError:
                        print_log('not a json file, passed: {0}'.format(tfile))
            print_log('='*80)
    except:
        traceback.print_exc()
