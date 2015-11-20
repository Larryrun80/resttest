#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: resttest.py

import os
import traceback

import arrow
import requests
import yaml

from utils import colortext

YAML_DIR = 'testfiles'


def print_log(log_words):
    prefix = '[ {0} ]'.format(arrow.now('Asia/Shanghai')
                                   .format('YYYY-MM-DD HH:mm:ss:SSS'))
    print('{0} {1}'.format(prefix, log_words))


def do_test(test_list, settings):
    base_items = ('test_id', 'description', 'route')
    if not isinstance(test_list, dict):
        print_log('wrong format test item found')
        return

    for base_item in base_items:
        if base_item not in test_list.keys():
            print_log('{0} not found in test item'.format(base_item))
            return

    # starting do test
    test_info = {
        'method': 'GET',
        'expected_status': 200,
        'expected_include': None,
        }

    for key in test_info:
        if key in test_list.keys():
            test_info[key] = test_list[key]

    request_url = settings['base_url'] + test_list['route']
    print_log('dealing {0}'.format(colortext.output(test_list['test_id'],  'yellow')))
    print_log('desc: {0}'.format(test_list['description']))
    print_log('trying to {0} {1}'.format(test_info['method'], request_url))
    r = requests.get(request_url)

    result = colortext.output('FAILED', 'red')
    extra_info = 'http status is ' + str(r.status_code)
    success = True

    if r.status_code != test_info['expected_status']:
        success = False

    if test_info['expected_include']:
        if test_info['expected_include'] not in r.text:
            success = False
            extra_info +=\
                ', without string {0}'.format(test_info['expected_include'])
        else:
            extra_info +=\
                    ', with string {0}'.format(test_info['expected_include'])

    if success:
        result = colortext.output('SUCCESSED', 'blue')

    print_log('test {0}! {1}'.format(result, extra_info))
    return success


def get_base_settings(yaml_data):
    base_settings = {
                        'test_set': '',
                        'base_url': '',
                        'headers': {},
                    }
    for key in base_settings.keys():
        if key in yaml_data.keys():
            base_settings[key] = yaml_data[key]

    return base_settings


if __name__ == '__main__':
    try:
        if not os.path.isdir(YAML_DIR):
            raise RuntimeError('yaml directory {0} not exists!'.format(YAML_DIR))

        for yfile in os.listdir(YAML_DIR):
            testfile = '{0}/{1}'.format(YAML_DIR, yfile)
            if os.path.isfile(testfile) and yfile.endswith('.yaml'):
                with open(testfile, encoding='utf-8') as f:
                    test_info = yaml.load(f)
                    if not isinstance(test_info, list):
                        break

                    # filling base settings
                    for yaml_conf in test_info:
                        if 'base_settings' in yaml_conf.keys():
                            base_settings = get_base_settings(yaml_conf['base_settings'])

                    if not base_settings:
                        raise RuntimeError('failed to get base settings')

                    header = '-'*15 + ' TESTING SET {0} '.format(base_settings['test_set']) + '-'*15
                    print_log(colortext.output(header, 'white'))

                    # starting test
                    success_count = 0
                    for yaml_conf in test_info:
                        if 'rest_tests' in yaml_conf.keys():
                            for item in yaml_conf['rest_tests']:
                                if do_test(item, base_settings):
                                    success_count += 1
                            print_log('-' * 40)
                            summary = 'tested {0} items, {1} success and {2} failed'.format(len(yaml_conf['rest_tests']), success_count, len(yaml_conf['rest_tests']) - success_count)
                            print_log(colortext.output(summary, 'white'))
    except:
        traceback.print_exc()
