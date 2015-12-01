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
    SUPPORTED_OPERATORS = {
        '=': 'eq',
        '!=': 'ne',
        '>': 'gt',
        '>=': 'ge',
        '<': 'lt',
        '<=': 'le',
        'in': 'in'
    }

    def __init__(self, doc, response):
        if not isinstance(doc, dict):
            raise RestTestError('FORMAT_ERROR', correct_type='dict')
        if 'type' not in doc.keys():
            raise RestTestError('KEY_NOT_FOUND', key='type', collection=doc)
        if doc['type'] not in self.SUPPORTED_TYPE:
            raise RestTestError('UNSUPPORT_METHOD', method=doc['type'])
        if not response:
            raise RestTestError('NO_RESPONSE')

        self.type = doc['type']
        for attr in self.ATTRIBUTES:
            if attr in doc.keys():
                setattr(self, attr, doc[attr])
            else:
                setattr(self, attr, None)

        self.response = response

    def check_expectation(self):
        method_name = 'check_' + self.type
        mtd = getattr(self, method_name)
        return mtd()

    def check_status_code(self):
        if not self.value:
            raise RestTestError('SOMETHING_MISSING', sth='expect value')

        if str(self.response.status_code) == str(self.value):
            self.print_result('SUCCESS')
        else:
            self.print_result('FAIL', 'get status code {0}'.format(
                            self.response.status_code))

    def check_include_keys(self):
        if not self.value or not self.obj:
            raise RestTestError('SOMETHING_MISSING',
                                sth='value or obj')

        for key in self.value:
            json_value = self.get_json()
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

    def check_include_words(self):
        if not self.value or not self.obj:
            raise RestTestError('SOMETHING_MISSING',
                                sth='value or obj')

        for word in self.value:
            json_value = self.get_json()
            text = json.dumps(json_value, ensure_ascii=False)
            if word in text:
                self.print_result('SUCCESS', word=word)
            else:
                self.print_result('FAIL', word=word)

    def check_value(self):
        if self.left is None or self.right is None or not self.op \
                or not self.obj:
            raise RestTestError('SOMETHING_MISSING',
                                sth='left, right, obj or op')
        if self.op not in self.SUPPORTED_OPERATORS.keys():
            raise RestTestError('UNSUPPORT_OPERATOR',
                                operator=self.op)

        if self.pass_expression():
            self.print_result('SUCCESS')
        else:
            self.print_result('FAIL')

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
        if self.type == 'include_words':
            e_type = ColorText(params['word'], 'yellow')
            e_value = ColorText('in ' + str(self.obj), 'yellow')
        if self.type == 'value':
            e_type = ColorText(str(self.left), 'yellow')
            e_value = ColorText(str(self.op) + ' ' + str(self.right), 'yellow')
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

    def get_json(self):
        path = str(self.obj)
        if not path.startswith('.'):
            raise RestTestError('FORMAT_ERROR',
                                correct_type='string start with "."')

        json_value = self.response.json()
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

    def pass_expression(self):
        oprands = self.deal_operands()
        return self.campare_operands(oprands)

    def deal_operands(self):
        '''get data from response and generate oprands to campare
        '''
        to_deal = (self.left, self.right)
        values = [None, None]
        # deal left and right, result kept in value[0], value[1]
        for i, item in enumerate(to_deal, 0):
            if isinstance(item, str) and str(item).startswith('.'):
                key = str(item)[1:]
                json_data = self.get_json()
                # if what we want is a value of key
                if not isinstance(json_data, list):
                    if key in json_data.keys():
                        values[i] = json_data[key]
                    else:
                        raise RestTestError('KEY_NOT_FOUND',
                                            key=key,
                                            collection=json_data)
                # if we got a list, get all value in list
                else:
                    v_list = []
                    for data in json_data:
                        if key in data.keys():
                            v_list.append(data[key])
                        else:
                            raise RestTestError('KEY_NOT_FOUND',
                                                key=key,
                                                collection=data)
                    values[i] = v_list
            # if not a sign to get data from response, just reutrn value
            else:
                values[i] = item

        return values

    def campare_operands(self, oprands):
        if not isinstance(oprands, list) or len(oprands) != 2:
            raise RestTestError('OPRANDS_ERROR')

        # if 'in' comparation
        if self.op == 'in':
            for item in oprands[0]:
                if item not in oprands[1]:
                    return False
            return True

        # if not 'in' comparation
        operator = '__{}__'.format(self.SUPPORTED_OPERATORS[str(self.op)])
        list_ops = []
        sole_ops = []
        for oprand in oprands:
            if isinstance(oprand, list):
                list_ops.append(oprand)
            else:
                sole_ops.append(oprand)

        # if campare in 2 list
        if len(list_ops) == 2 and len(sole_ops) == 0:
            for i, op in enumerate(list_ops[0], 0):
                mtd = getattr(op, operator)
                if not mtd(list_ops[1][i]):
                    return False

        # if campare in 2 operands, no list operand
        if len(sole_ops) == 2 and len(list_ops) == 0:
            mtd = getattr(sole_ops[0], operator)
            return mtd(sole_ops[1])

        # campare with an operand and a list oprand
        if len(sole_ops) == len(list_ops) == 1:
            for list_op in list_ops[0]:
                mtd = getattr(list_op, operator)
                if not mtd(sole_ops[0]):
                    return False

        return True
