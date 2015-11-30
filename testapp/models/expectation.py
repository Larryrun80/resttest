#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: expectation.py
import json

from .error import RestTestError
from .colortext import ColorText
from ..utils import utils


class Expectation():
    """docstring for Expectation"""

    SUPPORTED_TYPE = \
        ('status_code', 'include_keys', 'include_words', 'value')
    ATTRIBUTES = ('value', 'obj', 'left', 'op', 'right')

    def __init__(self, doc):
        if not isinstance(doc, dict):
            raise RestTestError('FORMAT_ERROR', correct_type='dict')
        if 'type' not in doc.keys():
            raise RestTestError('KEY_NOT_FOUND', key='type', collection=doc)
        if doc['type'] not in self.SUPPORTED_TYPE:
            raise RestTestError('UNSUPPORT_METHOD', method=doc['type'])

        self.type = doc['type']
        for attr in self.ATTRIBUTES:
            if attr in doc.keys():
                setattr(self, attr, doc[attr])
            else:
                setattr(self, attr, None)

    def check_expectation(self, response):
        method_name = 'check_' + self.type
        mtd = getattr(self, method_name)
        return mtd(response)

    def check_status_code(self, response):
        if not self.value:
            raise RestTestError('SOMETHING_MISSING', sth='expect value')

        if str(response.status_code) == str(self.value):
            self.print_result('SUCCESS')
        else:
            self.print_result('FAIL', 'get status code {0}'.format(
                            response.status_code))

    def check_include_keys(self, response):
        print(self.value)
        print(self.obj)
        if not self.value or not self.obj:
            raise RestTestError('SOMETHING_MISSING',
                                sth='ecpect value or expect obj')

        for key in self.value:
            json_value = self.get_json(response)
            if isinstance(json_value, dict) and key in json_value.keys():
                self.print_result('SUCCESS', key=key)
            elif isinstance(json_value, list):
                has_key = True
                for item in json_value:
                    if key not in item.keys():
                        has_key = False
                        break
                if has_key:
                    self.print_result('SUCCESS', key=key)
            else:
                self.print_result('FAIL', key=key)

    def check_include_words(self, response):
        pass

    def check_value(self, response):
        pass

    def print_result(self, result, msg=None, **params):
        ''' print_result
            this function is to print suitable result for expectation check
            pass 'SUCCESS' OR 'FAIL' as result
            pass fail message as msg
            msg only work in 'FAIL' type
            params used to print statement info
        '''
        result_type = ('SUCCESS', 'FAIL')
        if result not in result_type:
            raise RestTestError('UNSUPPORT_TYPE', type=result,
                                whenclause='print expectation result')

        # print expectation statement
        m_statement = 'checking expectation:  {} should {}'

        e_type = e_value = None
        if self.type == 'status_code':
            e_type = ColorText('status code', 'yellow')
            e_value = ColorText('be ' + str(self.value), 'yellow')
        if self.type == 'include_keys':
            e_type = ColorText(params['key'], 'yellow')
            e_value = ColorText('in ' + str(self.obj), 'yellow')
        utils.print_log(m_statement.format(e_type, e_value))

        # print result
        m_result = 'expectation check {}!'
        if result == 'SUCCESS':
            e_result = ColorText('successed', 'green')
        else:
            if msg:
                m_result += ' {}'
            e_result = ColorText('failed', 'red')
        utils.print_log(m_result.format(e_result, msg))

    def get_json(self, response):
        path = str(self.obj)
        if not path.startswith('.'):
            raise RestTestError('FORMAT_ERROR',
                                correct_type='string start with "."')

        json_value = response.json()
        if path == '.':
            return json_value

        elements = path[1:].split('.')
        try:
            for element in elements:
                json_value = json_value[element]
        except:
            raise RestTestError('KEY_NOT_FOUND',
                                key=element,
                                collection=json_value)
        return json_value
