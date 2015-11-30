#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: expectation.py

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
        if self.type == 'status_code':
            return self.check_status_code(response)
        pass

    def check_status_code(self, response):
        if not self.value:
            raise RestTestError('SOMETHING_MISSING', sth='ecpect value')

        if str(response.status_code) == str(self.value):
            self.print_result('SUCCESS')
        else:
            self.print_result('FAIL', 'get status code {0}'.format(
                            response.status_code))
        pass

    def check_include_keys(self, response):
        pass

    def check_include_words(self, response):
        pass

    def check_value(self, response):
        pass

    def print_result(self, result, msg=None):
        ''' print_result
            this function is to print suitable result for expectation check
            pass 'SUCCESS' OR 'FAIL' as result
            pass fail message as msg
            msg only work in 'FAIL' type
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
        utils.print_log(m_statement.format(e_type, e_value))

        # print result
        m_result = 'expectation check {}!'
        if result == 'SUCCESS':
            e_result = ColorText('successed', 'green')
        else:
            m_result += ' {}'
            e_result = ColorText('failed', 'red')
        utils.print_log(m_result.format(e_result, msg))
