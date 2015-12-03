#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: testfile.py

from configparser import ConfigParser
import json
import os

import arrow

from .error import RestTestError
from .colortext import ColorText
from .testrequest import TestRequest
from ..utils import utils


class TestFile():
    """docstring for TestFile"""

    REQUEST_KEYS = ('id', 'name', 'description', 'order', 'requests',)
    CONFIG_FILE = os.path.abspath(os.path.dirname(__file__)) \
        + '/../settings.conf'

    def __init__(self, filename):
            # get config
            self.debug_mode = False
            try:
                config = ConfigParser()
                config.read(self.CONFIG_FILE)
                if config.has_section('GENERAL'):
                    self.debug_mode = \
                        'true' == config.get('GENERAL', 'Debug_mode').lower()
            except:
                utils.print_log('get config failed, debug mode closed')

            # search files
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, encoding='utf-8') as f:
                    try:
                        t_json = json.loads(f.read())
                        for key in self.REQUEST_KEYS:
                            if key not in t_json.keys():
                                raise RestTestError('KEY_NOT_FOUND',
                                                    key=key,
                                                    collection=t_json)
                        self.filename = filename
                        self.id = t_json['id']
                        self.name = t_json['name']
                        self.description = t_json['description']
                        self.order = t_json['order']
                        self.requests = t_json['requests']
                        self.context = None
                        if 'context' in t_json.keys():
                            self.context = t_json['context']
                    except json.decoder.JSONDecodeError:
                        raise RestTestError('ILLEGAL_JSON_FILE',
                                            filename=filename)
            else:
                raise RestTestError('FILE_NOT_FOUND', path=filename)

    def print_file_info(self):
        utils.print_log('DEALING FILE {0}'.format(
            ColorText(self.filename, 'red')))
        utils.print_log('DESCRIPTION: {0}'.format(
            ColorText(self.description, 'yellow')))

    def test_requests(self):
        for t_id in self.order:
            for request in self.requests:
                if t_id == request['id']:
                    tr = TestRequest(request, self.context)
                    # print general info and request info
                    tr.print_info()
                    tr.send_request()
                    tr.print_request()
                    utils.print_log('-'*50)

                    # start check expectations and print info
                    tr.check_expectations()

                    # print response for debug, if needs
                    if self.debug_mode:
                        tr.print_response()

                    # if tr's output is a context's value, update it
                    if tr.response:
                        for c in self.context:
                            if t_id in c['request_id']:
                                try:
                                    c['value'] = utils.get_json_with_path(
                                        tr.response.json(), c['path'])
                                    c['timestamp'] = arrow.now('Asia/Shanghai')
                                except:
                                    utils.print_log(
                                        'try to get context value {} failed'
                                        ''.format(c['name']))

                    utils.print_log('#'*50)
