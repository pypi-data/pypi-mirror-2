##############################################################################
#
# Copyright (c) 2004-2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Test runner

$Id: __init__.py 102626 2009-08-10 13:44:36Z gotcha $
"""

import sys
import unittest


import zope.testing.testrunner.interfaces


def run(defaults=None, args=None, script_parts=None):
    """Main runner function which can be and is being used from main programs.

    Will execute the tests and exit the process according to the test result.

    """
    failed = run_internal(defaults, args, script_parts=script_parts)
    sys.exit(int(failed))


def run_internal(defaults=None, args=None, script_parts=None):
    """Execute tests.

    Returns whether errors or failures occured during testing.

    """
    # XXX Bah. Lazy import to avoid circular/early import problems
    from zope.testing.testrunner.runner import Runner
    runner = Runner(defaults, args, script_parts=script_parts)
    runner.run()
    return runner.failed


###############################################################################
# Install 2.4 TestSuite __iter__ into earlier versions

if sys.version_info < (2, 4):
    def __iter__(suite):
        return iter(suite._tests)
    unittest.TestSuite.__iter__ = __iter__
    del __iter__

# Install 2.4 TestSuite __iter__ into earlier versions
###############################################################################

if __name__ == '__main__':
    # allow people to try out the test runner with
    # python -m zope.testing.testrunner --test-path .
    run()
