#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: testfile.py

import json
import os

from .error import RestTestError
from .colortext import ColorText
from .testrequest import TestRequest
from ..utils import utils


class TestFile():
    """docstring for TestFile"""

    REQUEST_KEYS = ('id', 'name', 'description', 'order', 'requests',)

    def __init__(self, filename):
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
                    tr = TestRequest(request)
                    tr.print_info()
                    tr.send_request()
                    tr.print_request()
                    tr.print_response()
                    utils.print_log('-'*50)
