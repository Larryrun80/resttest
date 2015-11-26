#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: resttest.py

import os
import traceback

from testapp.utils import utils
from testapp.models.error import RestTestError
from testapp.models.testfile import TestFile

TEST_DIR = 'testfiles'

if __name__ == '__main__':
    try:
        if not os.path.isdir(TEST_DIR):
            raise RestTestError('DIR_NOT_FOUND', dir=TEST_DIR)

        for tfile in os.listdir(TEST_DIR):
            filename = '{0}/{1}'.format(TEST_DIR, tfile)
            try:
                tf = TestFile(filename)
                tf.print_file_info()
                tf.test_requests()
            except RestTestError as e:
                if e.code == 100003:
                    utils.print_log(e.message)
                    utils.print_log('skipped!')
            utils.print_log('='*80)
    except:
        traceback.print_exc()
