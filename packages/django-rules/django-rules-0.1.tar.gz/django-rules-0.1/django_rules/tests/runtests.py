#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

from django.test.simple import run_tests
from django.conf import settings

def runtests():
    failures = run_tests([
        'django_rules.BackendTest',
        'django_rules.RulePermissionTest',
        'django_rules.UtilsTest',
        'django_rules.DecoratorsTest'
        ], verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()

