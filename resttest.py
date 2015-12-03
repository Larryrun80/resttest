#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: resttest.py

from configparser import ConfigParser
import os
import traceback

from testapp.utils import utils
from testapp.models.error import RestTestError
from testapp.models.testfile import TestFile
from testapp.models.expectation import Expectation

TEST_DIR = os.path.abspath(os.path.dirname(__file__)) \
        + '/testfiles'
CONFIG_FILE = os.path.abspath(os.path.dirname(__file__)) \
        + '/settings.conf'


def read_config():
    # default settings
    config = {}
    config['debug_mode'] = False

    # read config settings from config file
    try:
        config = ConfigParser()
        config.read(CONFIG_FILE)
        if config.has_section('GENERAL'):
            config['debug_mode'] = \
                'true' == config.get('GENERAL', 'Debug_mode').lower()
    except:
        utils.print_log('get config failed, using default settings')

    return config


if __name__ == '__main__':
    try:
        if not os.path.isdir(TEST_DIR):
            raise RestTestError('DIR_NOT_FOUND', dir=TEST_DIR)

        config = read_config()
        utils.print_log('resttest now begin work!')
        utils.print_log('scaning folder {}'.format(
                TEST_DIR))

        for tfile in os.listdir(TEST_DIR):
            utils.print_separator()
            utils.print_log('trying to read file {}'.format(
                tfile))
            filename = '{0}/{1}'.format(TEST_DIR, tfile)
            try:
                tf = TestFile(filename, config)
                tf.print_file_info()
                tf.test_requests()
            except RestTestError as e:
                if e.code == 100003:
                    utils.print_log(e.message)
                else:
                    raise e
        Expectation.print_summary()
    except RestTestError as e:
        utils.print_log(e.message)
    except:
        traceback.print_exc()
