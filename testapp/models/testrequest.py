#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: testrequest.py

import json
import requests

from .error import RestTestError
from .colortext import ColorText
from .expectation import Expectation
from ..utils import utils


class TestRequest():
    """docstring for TestRequest
          this class is for build a request using url, method, etc
          and then return a response
    """
    REQUEST_KEYS = ('id', 'name', 'description', 'method', 'url', 'data')
    SUPPORTED_HTTP_METHODS = ('get', 'post', 'put', 'delete')
    HTTP_PREFIX = ('http://', 'https://')

    def __init__(self, doc, http_prefix='http://'):
        ''' init method
            passing a json to form an objective
        '''
        if not isinstance(doc, dict):
            raise RestTestError('FORMAT_ERROR', correct_type='dict')
        if http_prefix not in self.HTTP_PREFIX:
            raise RestTestError('ILLEGAL_DATA',
                                param='http_prefix',
                                value=http_prefix)
        for key in self.REQUEST_KEYS:
            if key not in doc.keys():
                raise RestTestError('KEY_NOT_FOUND',
                                    key=key,
                                    collection='request')

        self.id = doc['id']
        self.name = doc['name']
        self.description = doc['description']
        self.method = str(doc['method']).lower()
        self.url = http_prefix + doc['url']
        self.data = {}
        for item in doc['data']:
            if item['enabled']:
                self.data[item['key']] = item['value']
        self.response = None
        self.expectations = None
        if 'expectations' in doc.keys():
            self.expectations = doc['expectations']

    def send_request(self):
        if self.method not in self.SUPPORTED_HTTP_METHODS:
            raise RestTestError('UNSUPPORT_METHOD', self.method)
        mtd = getattr(requests, self.method)
        if self.data:
            self.response = mtd(self.url, self.data)
        else:
            self.response = mtd(self.url)

    def check_expections(self):
        if not self.response:
            raise RestTestError('NO_RESPONSE')
        if not self.expectations:
            return

        for expectation in self.expectations:
            ep = Expectation(expectation)
            ep.check_expectation(self.response)

    def print_info(self):
        utils.print_log('testing {}'.format(ColorText(self.id, 'red')))
        utils.print_log(ColorText(self.name, 'blue'))
        utils.print_log(ColorText(self.description, 'blue'))

    def print_request(self):
        if not self.response:
            raise RestTestError('NO_RESPONSE')

        utils.print_log(
            ColorText(self.method.upper() + ' ' + self.response.url, 'yellow'))
        if self.data:
            utils.print_log(
                ColorText(
                    'committed data: {}'.format(repr(self.data)), 'yellow'))

    def print_response(self):
        if not self.response:
            raise RestTestError('NO_RESPONSE')

        utils.print_log('status code: {}'.format(self.response.status_code))
        r_text = json.dumps(self.response.json(),
                            ensure_ascii=False,
                            sort_keys=True,
                            indent=4)
        utils.print_log('response: {}'.format(r_text))
