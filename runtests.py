#!/usr/bin/env python
import sys
from optparse import OptionParser
from os.path import abspath, dirname
from django.test.simple import DjangoTestSuiteRunner
from django.test.utils import setup_test_environment

from south.management.commands import patch_for_test_db_setup

def runtests(*test_args, **kwargs):
    # setup_test_environment()

    # This is needed because tables doesn't get created by south
    # http://blogs.terrorware.com/geoff/2012/03/05/making-sure-south-migrations-get-run-when-using-djangos-create_test_db/
    patch_for_test_db_setup()

    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    test_runner = DjangoTestSuiteRunner(
        verbosity=kwargs.get('verbosity', 1),
        interactive=kwargs.get('interactive', False),
        failfast=kwargs.get('failfast')
    )
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)
