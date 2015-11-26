#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: testrequest.py

import requests

from .error import RestTestError
from .colortext import ColorText
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

    def send_request(self):
        if self.method not in self.SUPPORTED_HTTP_METHODS:
            raise RestTestError('UNSUPPORT_METHOD', self.method)
        mtd = getattr(requests, self.method)
        if self.data:
            self.response = mtd(self.url, self.data)
        else:
            self.response = mtd(self.url)

    def print_info(self):
        utils.print_log('testing {0}'.format(ColorText(self.id, 'red')))
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
                    'committed data: {0}'.format(repr(self.data)), 'yellow'))

    def print_response(self):
        if not self.response:
            raise RestTestError('NO_RESPONSE')

        utils.print_log('status code: {0}'.format(self.response.status_code))
        utils.print_log('response: {0}'.format(self.response.json()))
