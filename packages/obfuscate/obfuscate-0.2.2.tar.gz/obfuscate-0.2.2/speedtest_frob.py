#!/usr/bin/env python
"""Speed tests for obfuscate._MonoFrob.

Output:

    (1) the near-optimum string size to switch algorithms from the _comp
        method to the _trans method in _MonoFrob. This should be considered
        approximate.

    (2) the approximate speedup gained by using a cache in _MonoFrob.

Options (accepts only short options):

    -V  (verbose) print extra output
    -F  (fast) run a smaller number of tests
    -S  (slow) run a larger number of tests

These tests are reasonably time consuming. Without either -F or -S, it takes
1-5 minutes depending on your computer speed.
"""

from __future__ import division

from timeit import Timer
from obfuscate import _MonoFrob as monofrob

F = T = K = None  # Placeholders for the function to be timed, the text
# to run the timing tests on, and the keys to use.


lorem = (
    "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do "
    "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad "
    "minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip "
    "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in "
    "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
    "sint occaecat cupidatat non proident, sunt in culpa qui officia "
    "deserunt mollit anim id est laborum.\n")

DEFAULT_NUMBER = 100
DEFAULT_REPEAT = 5

def print_(msg, verbose=True):
    if verbose:
        print msg


def timer(func, text, keys, number, repeat):
    global F, T, K
    F, T, K = func, text, keys
    setup = "from %s import F, T, K" % __name__
    timer = Timer('for key in K: x = F(T, key)', setup)
    return min(timer.repeat(repeat, number))


def time_with_cache(text, keys, number, repeat):
    assert monofrob._cache is not None
    return timer(monofrob, text, keys, number, repeat)


def time_without_cache(text, keys, number, repeat):
    save = monofrob._cache
    monofrob._cache = None
    try:
        t = timer(monofrob, text, keys, number, repeat)
        assert monofrob._cache is None
        return t
    finally:
        monofrob._cache = save


def cache_test(number=DEFAULT_NUMBER, repeat=DEFAULT_REPEAT, verbose=False):
    """Compare the speed of monofrob with and without a cache."""
    text = lorem*10
    keys = [chr(n) for n in xrange(23, 123)]
    print_("*** Comparing speed with and without cache ***", verbose)
    print_("    (%d iterations, best of %d)" % (number, repeat), verbose)
    t_with = time_with_cache(text, keys, number, repeat)
    print_("Time with cache: %f" % t_with, verbose)
    t_without = time_without_cache(text, keys, number, repeat)
    print_("Time without cache: %f" % t_without, verbose)
    speedup = t_without/t_with
    print_("Speed increase due to cache: %f" % speedup, verbose)
    return speedup


def mono_test(number=DEFAULT_NUMBER, repeat=DEFAULT_REPEAT, verbose=False,
        delta=5, tol=1e-6):
    print_(
        "*** Searching for cutover size for _optimized_monofrob ***",
        verbose)
    print_("    (testing with disabled cache)", verbose)
    save = monofrob._cache
    monofrob._cache = None
    try:
        trans = monofrob._trans
        comp = monofrob._comp
        keys = range(256)
        bigtext = lorem*20
        size = 0
        print_("Testing: hunt phase...", verbose)
        print_(
            "string length, time using trans, time using comp, "
            "rel difference", verbose)
        # Advance forward doubling each time.
        for i in xrange(0, len(bigtext)):  # Upper limit is arbitrarily large.
            prev = size
            size = 2**i
            if size > len(bigtext):
                bracket = prev, len(bigtext)
                break
            # Do the timing measurements.
            text = bigtext[:size]
            t_trans = timer(trans, text, keys, number, repeat)/number
            t_comp = timer(comp, text, keys, number, repeat)/number
            diff = (t_trans-t_comp)/t_comp
            print_(
                "%d %.4f %.4f %.1f%%" % (size, t_trans, t_comp, diff*100),
                verbose)
            if diff <= 0:
                bracket = prev, size
                break
        # Search between the bracketed values.
        print_("Switching to bisection phase...", verbose)
        left, right = bracket
        while True:
            # Cutover point occurs between left and right.
            if abs(left-right) <= delta:
                # Eh, close enough. Timings aren't exact, so we can't expect
                # high precision. Split the difference and be done.
                cutover = (left + right + 1)//2
                break
            # Search between the points.
            size = (left + right)//2
            text = bigtext[:size]
            t_trans = timer(trans, text, keys, number, repeat)/number
            t_comp = timer(comp, text, keys, number, repeat)/number
            diff = (t_trans-t_comp)/t_comp
            print_(
                "%d %.4f %.4f %.1f%%" % (size, t_trans, t_comp, diff*100),
                verbose)
            if abs(diff) <= tol:
                # Close enough to zero. Consider this equal.
                cutover = (left + right + 1)//2
                break
            elif diff > 0:
                # Table searching still too slow, so bracket to the right.
                left = size
            else:
                # Table searching now faster, so bracket to the left.
                right = size
        print_(
            "Cutover position occurs close to len = %d characters."
            % cutover,
            verbose)
    finally:
        monofrob._cache = save
    if verbose:
        # No need to do this at all if we're not printing!
        # Verify this is a plausible cutover.
        print "*** Time deltas for cutover set to %d ***" % cutover
        print "    expect [+0 +0 ... 0 ... -0 -0] in the ideal case"
        deltas = []
        save = monofrob._cutover
        monofrob._cutover = cutover
        try:
            for i in range(cutover-5, cutover+5):
                t_trans = timer(monofrob, bigtext[:i], ['*'], number, repeat)
                t_comp = timer(monofrob, bigtext[:i], ['*'], number, repeat)
                deltas.append('%.4f' % (t_trans-t_comp))
        finally:
            monofrob._cutover = save
        for s in deltas:
            print s,
        print
    return cutover


if __name__ == '__main__':
    import sys
    fast = '-F' in sys.argv
    slow = '-S' in sys.argv
    verbose = '-V' in sys.argv
    if fast and slow:
        raise TypeError('do not use both -F and -S switches together')
    if fast:
        number, repeat = DEFAULT_NUMBER//10, DEFAULT_REPEAT//2
    elif slow:
        number, repeat = 3*DEFAULT_NUMBER, DEFAULT_REPEAT
    else:
        number, repeat = DEFAULT_NUMBER, DEFAULT_REPEAT
    kw = dict(number=number, repeat=repeat, verbose=verbose)
    x = mono_test(**kw)
    if not verbose:
        print 'Approximate cutover size:', x
    x = cache_test(**kw)
    if not verbose:
        print 'Approximately speedup from cache:', x

