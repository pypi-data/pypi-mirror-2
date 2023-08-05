##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
r"""Regular expression pattern normalizing output checker

The pattern-normalizing output checker extends the default output checker with
an option to normalize expected and actual output.

You specify a sequence of patterns and replacements.  The replacements are
applied to the expected and actual outputs before calling the default outputs
checker.  Let's look at an example.  In this example, we have some times and
addresses:

    >>> want = '''\
    ... <object object at 0xb7f14438>
    ... completed in 1.234 seconds.
    ... <BLANKLINE>
    ... <object object at 0xb7f14440>
    ... completed in 123.234 seconds.
    ... <BLANKLINE>
    ... <object object at 0xb7f14448>
    ... completed in .234 seconds.
    ... <BLANKLINE>
    ... <object object at 0xb7f14450>
    ... completed in 1.234 seconds.
    ... <BLANKLINE>
    ... '''

    >>> got = '''\
    ... <object object at 0xb7f14458>
    ... completed in 1.235 seconds.
    ...
    ... <object object at 0xb7f14460>
    ... completed in 123.233 seconds.
    ...
    ... <object object at 0xb7f14468>
    ... completed in .231 seconds.
    ...
    ... <object object at 0xb7f14470>
    ... completed in 1.23 seconds.
    ...
    ... '''

We may wish to consider these two strings to match, even though they differ in
actual addresses and times.  The default output checker will consider them
different:

    >>> doctest.OutputChecker().check_output(want, got, 0)
    False

We'll use the RENormalizing to normalize both the wanted and gotten strings to
ignore differences in times and addresses:

    >>> import re
    >>> checker = RENormalizing([
    ...    (re.compile('[0-9]*[.][0-9]* seconds'), '<SOME NUMBER OF> seconds'),
    ...    (re.compile('at 0x[0-9a-f]+'), 'at <SOME ADDRESS>'),
    ...    ])

    >>> checker.check_output(want, got, 0)
    True

Usual OutputChecker options work as expected:

    >>> want_ellided = '''\
    ... <object object at 0xb7f14438>
    ... completed in 1.234 seconds.
    ... ...
    ... <object object at 0xb7f14450>
    ... completed in 1.234 seconds.
    ... <BLANKLINE>
    ... '''

    >>> checker.check_output(want_ellided, got, 0)
    False

    >>> checker.check_output(want_ellided, got, doctest.ELLIPSIS)
    True

When we get differencs, we output them with normalized text:

    >>> source = '''\
    ... >>> do_something()
    ... <object object at 0xb7f14438>
    ... completed in 1.234 seconds.
    ... ...
    ... <object object at 0xb7f14450>
    ... completed in 1.234 seconds.
    ... <BLANKLINE>
    ... '''

    >>> example = doctest.Example(source, want_ellided)

    >>> print checker.output_difference(example, got, 0)
    Expected:
        <object object at <SOME ADDRESS>>
        completed in <SOME NUMBER OF> seconds.
        ...
        <object object at <SOME ADDRESS>>
        completed in <SOME NUMBER OF> seconds.
        <BLANKLINE>
    Got:
        <object object at <SOME ADDRESS>>
        completed in <SOME NUMBER OF> seconds.
        <BLANKLINE>
        <object object at <SOME ADDRESS>>
        completed in <SOME NUMBER OF> seconds.
        <BLANKLINE>
        <object object at <SOME ADDRESS>>
        completed in <SOME NUMBER OF> seconds.
        <BLANKLINE>
        <object object at <SOME ADDRESS>>
        completed in <SOME NUMBER OF> seconds.
        <BLANKLINE>
    <BLANKLINE>

    >>> print checker.output_difference(example, got,
    ...                                 doctest.REPORT_NDIFF)
    Differences (ndiff with -expected +actual):
        - <object object at <SOME ADDRESS>>
        - completed in <SOME NUMBER OF> seconds.
        - ...
          <object object at <SOME ADDRESS>>
          completed in <SOME NUMBER OF> seconds.
          <BLANKLINE>
        + <object object at <SOME ADDRESS>>
        + completed in <SOME NUMBER OF> seconds.
        + <BLANKLINE>
        + <object object at <SOME ADDRESS>>
        + completed in <SOME NUMBER OF> seconds.
        + <BLANKLINE>
        + <object object at <SOME ADDRESS>>
        + completed in <SOME NUMBER OF> seconds.
        + <BLANKLINE>
    <BLANKLINE>

    If the wanted text is empty, however, we don't transform the actual output.
    This is usful when writing tests.  We leave the expected output empty, run
    the test, and use the actual output as expected, after reviewing it.

    >>> source = '''\
    ... >>> do_something()
    ... '''

    >>> example = doctest.Example(source, '\n')
    >>> print checker.output_difference(example, got, 0)
    Expected:
    <BLANKLINE>
    Got:
        <object object at 0xb7f14458>
        completed in 1.235 seconds.
        <BLANKLINE>
        <object object at 0xb7f14460>
        completed in 123.233 seconds.
        <BLANKLINE>
        <object object at 0xb7f14468>
        completed in .231 seconds.
        <BLANKLINE>
        <object object at 0xb7f14470>
        completed in 1.23 seconds.
        <BLANKLINE>
    <BLANKLINE>

If regular expressions aren't expressive enough, you can use arbitrary Python
callables to transform the text.  For example, suppose you want to ignore
case during comparison:

    >>> checker = RENormalizing([
    ...    lambda s: s.lower(),
    ...    lambda s: s.replace('<blankline>', '<BLANKLINE>'),
    ...    ])

    >>> want = '''\
    ... Usage: thundermonkey [options] [url]
    ... <BLANKLINE>
    ... Options:
    ...     -h    display this help message
    ... '''

    >>> got = '''\
    ... usage: thundermonkey [options] [URL]
    ...
    ... options:
    ...     -h    Display this help message
    ... '''

    >>> checker.check_output(want, got, 0)
    True

Suppose we forgot that <BLANKLINE> must be in upper case:

    >>> checker = RENormalizing([
    ...    lambda s: s.lower(),
    ...    ])

    >>> checker.check_output(want, got, 0)
    False

The difference would show us that:

    >>> source = '''\
    ... >>> print_help_message()
    ... ''' + want
    >>> example = doctest.Example(source, want)
    >>> print checker.output_difference(example, got,
    ...                                 doctest.REPORT_NDIFF),
    Differences (ndiff with -expected +actual):
          usage: thundermonkey [options] [url]
        - <blankline>
        + <BLANKLINE>
          options:
              -h    display this help message


It is possible to combine RENormalizing checkers for easy reuse:

    >>> address_and_time_checker = RENormalizing([
    ...    (re.compile('[0-9]*[.][0-9]* seconds'), '<SOME NUMBER OF> seconds'),
    ...    (re.compile('at 0x[0-9a-f]+'), 'at <SOME ADDRESS>'),
    ...    ])
    >>> lowercase_checker = RENormalizing([
    ...    lambda s: s.lower(),
    ...    ])
    >>> combined_checker = address_and_time_checker + lowercase_checker
    >>> len(combined_checker.transformers)
    3

Combining a checker with something else does not work:

    >>> lowercase_checker + 5
    Traceback (most recent call last):
        ...
    TypeError: unsupported operand type(s) for +: 'instance' and 'int'

"""

import doctest

class RENormalizing(doctest.OutputChecker):
    """Pattern-normalizing outout checker
    """

    def __init__(self, patterns):
        self.transformers = map(self._cook, patterns)

    def __add__(self, other):
        if not isinstance(other, RENormalizing):
            return NotImplemented
        return RENormalizing(self.transformers + other.transformers)

    def _cook(self, pattern):
        if callable(pattern):
            return pattern
        regexp, replacement = pattern
        return lambda text: regexp.sub(replacement, text)

    def check_output(self, want, got, optionflags):
        if got == want:
            return True

        for transformer in self.transformers:
            want = transformer(want)
            got = transformer(got)

        return doctest.OutputChecker.check_output(self, want, got, optionflags)

    def output_difference(self, example, got, optionflags):

        want = example.want

        # If want is empty, use original outputter. This is useful
        # when setting up tests for the first time.  In that case, we
        # generally use the differencer to display output, which we evaluate
        # by hand.
        if not want.strip():
            return doctest.OutputChecker.output_difference(
                self, example, got, optionflags)

        # Dang, this isn't as easy to override as we might wish
        original = want

        for transformer in self.transformers:
            want = transformer(want)
            got = transformer(got)

        # temporarily hack example with normalized want:
        example.want = want
        result = doctest.OutputChecker.output_difference(
            self, example, got, optionflags)
        example.want = original

        return result
