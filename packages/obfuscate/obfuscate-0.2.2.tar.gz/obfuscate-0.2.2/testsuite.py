#!/usr/bin/env python
"""Test suite for obfuscate.py

Runs:
    doctests from the obfuscate module
    doctests from the examples text file
    unit tests in this module
    a limited test for uncollectable objects

"""

from __future__ import division

import doctest
import gc
import itertools
import string
import sys
import unittest


# Module being tested.
import obfuscate



# === Helper functions ===

def verify_ascii_only(list_of_strings):
    """Raise an exception if any string contains non-ASCII characters."""
    for i, s in enumerate(list_of_strings):
        try:
            t = s.encode('ascii')
        except UnicodeDecodeError, e:
            e.extra = "failure at item %d with string %s" % (i, s)
            raise
        if t != s:
            raise ValueError(
            'bad string %r encodes to %r (item %d)' % (s, t, i))


def verify_reusable(iterables):
    """Raise an exception if any iterable can't be reused."""
    for i, it in enumerate(iterables):
        x = list(it)  # Iterate over it once.
        y = list(it)  # And again.
        if x != y:
            raise ValueError(
            'item %d %r is not reusable, got %s' % (i, it, x))


class HelperTests(unittest.TestCase):
    """Test helper functions."""
    def testVerifyAsciiOnly(self):
        self.failUnlessRaises(UnicodeDecodeError, verify_ascii_only, '\xFA')
        self.assert_(verify_ascii_only('ab') is None)

    def testVerifyReusable(self):
        self.failUnlessRaises(ValueError, verify_reusable, [iter('abc')])
        self.assert_(verify_reusable(['abc', [1,2,3]]) is None)


def make_iterable_test_data(ascii_only=False):
    """Return a list of iterables and a list of the iterables as strings.

    Returns a tuple with two items. The first is a list of assorted iterables,
    the second is the same data converted to strings:
        ([a, b, c, ..., z], [''.join(a), ..., ''.join(z)])
    """
    # First do the reusable iterables.
    iterables = ASCII_TEST_ITERABLES if ascii_only else TEST_ITERABLES
    if not ascii_only:
        iterables = iterables + [[BYTES]]
    strings = [''.join(it) for it in iterables]
    # Test that all of these remain reusable as expected.
    if __debug__:
        verify_reusable(iterables)
    # Now add the use-once iterables.
    for s in ASCII_TEST_STRINGS if ascii_only else TEST_STRINGS:
        iterables.append(reversed(s))
        strings.append(s[::-1])
        iterables.append(iter(s))
        strings.append(s)
    if __debug__:
        if ascii_only:
            verify_ascii_only(strings)
    return (iterables, strings)


# === Data sets for testing ===

ASCII = ''.join([chr(i) for i in xrange(128)])
BYTES = ''.join([chr(i) for i in xrange(256)])


ASCII_TEST_STRINGS = [
    # These should all be strings.
    "", "    ", "\n", "\0", "\01\r\n",
    "abcdEFGH", "1234567890", "#!@*&^%()-<>+",
    "some text 1234 \t\v\f\r AND MORE",
    "NOBODY expects the Spanish Inquistition!!!",
    BYTES[:128]*20,
    ]

ASCII_TEST_ITERABLES = [
    # Make sure all of these are reusable. No iterators!
    # Lists:
    [], ['\0~'], ["a", "bb", "ccc", "DDDD"],
    # Tuples:
    (), ('alpha', 'beta', 'gamma', 'delta', 'epsilon'),
    (';@ab 35', '+%~1', '\n\t\v #', '*=$m\0\x01\x7a\x7b\x7f'),
    # Dicts and sets:
    {}, set(), set('z'), set(['', 'v']), frozenset(['A']),
    ]


if __debug__:
    verify_ascii_only(ASCII_TEST_STRINGS)
    verify_reusable(ASCII_TEST_ITERABLES)
    verify_ascii_only([''.join(x) for x in ASCII_TEST_ITERABLES])


# Now create non-ASCII tst data, that is to say, "extended ASCII" using
# characters in the full range 0...255 and not just 0...127.

TEST_STRINGS = ASCII_TEST_STRINGS + ["ABC\xc8 \xc9123", "\xa1\xfe\xff"]
TEST_ITERABLES = ASCII_TEST_ITERABLES + [
    ("ABC\xc8 ", "\xc9123"), ["\xa1\xfe", "\xff"]]

if __debug__:
    verify_reusable(TEST_ITERABLES)



# === Test suites ===

class GlobalTest(unittest.TestCase):
    def testState(self):
        """Test the state of globals."""
        self.assertEquals(len(obfuscate.BYTES), 256)
        self.assertEquals(obfuscate.BYTES, BYTES)
    def testMeta(self):
        """Test existence of metadata."""
        attrs = "__doc__  __version__  __date__  __author__  __all__".split()
        for meta in attrs:
            self.failUnless(hasattr(obfuscate, meta))


class DualMethodTest(unittest.TestCase):
    """Verify the dualmethod descriptor works correctly."""

    class K(object):
        @obfuscate.dualmethod
        def method(this, x):
            """This is a doc string."""
            return (this, type(this), x)

    def testDualMethodDoc(self):
        """Verify that dualmethods can have a doc string."""
        self.failUnlessEqual(self.K.method.__doc__, "This is a doc string.")

    def testDualMethodInstance(self):
        """Test calling the dualmethod on the instance."""
        instance = self.K()
        result = instance.method(123)
        self.failUnlessEqual(result, (instance, self.K, 123))

    def testDualMethodClass(self):
        """Test calling the dualmethod on the class."""
        result = self.K.method(123)
        self.failUnlessEqual(result, (self.K, type, 123))

    def testDualMethodDirect(self):
        """Test calling the descriptor directly."""
        instance = self.K()
        result = self.K.__dict__['method'].__get__(instance)(123)
        self.failUnlessEqual(result, (instance, self.K, 123))


class StandAloneFunctionTests(unittest.TestCase):
    """Test stand-alone functions."""

    def test_abstract(self):
        abstract = obfuscate.abstract
        f = abstract(lambda: None)
        self.assertRaises(TypeError, f)

    def test_ceildiv(self):
        ceildiv = obfuscate.ceildiv
        self.assertEquals(ceildiv(10, 2), 5)
        self.assertEquals(ceildiv(11, 2), 6)
        self.assertEquals(ceildiv(12, 2), 6)
        self.assertEquals(ceildiv(11, -2), -5)

    def test_flatten(self):
        flatten = obfuscate.flatten
        data = [ ([], []),
            ([1, 2, 3], [1, 2, 3]),
            ([1, [2], 3], [1, 2, 3]),
            ([1, [2, 3], 4, [5, 6], 7], [1, 2, 3, 4, 5, 6, 7]),
            ]
        for a, b in data:
            self.assertEquals(flatten(a), b)

    def test_get_case_state(self):
        get_case_state = obfuscate.get_case_state
        self.assertEquals(get_case_state(''), [])
        self.assertEquals(get_case_state('a'), [False])
        self.assertEquals(get_case_state('A'), [True])
        self.assertEquals(get_case_state('ABC'), [True, True, True])
        self.assertEquals(get_case_state('1aA'), [False, False, True])

    def test_is_string(self):
        is_string = obfuscate.is_string
        for x in ['', 'abc', ' \n', '123']:
            self.failUnless(is_string(x))
        for x in [None, [], iter('abc'), 123, {}]:
            self.failIf(is_string(x))

    def test_isclass(self):
        isclass = obfuscate.isclass

        class K(object):
            pass

        class Meta(type):
            pass

        class Q(K):
            __metaclass__ = Meta

        # Types and metaclasses are a bit tricky. First verify we haven't
        # confused ourselves utterly:
        assert issubclass(K, object)
        assert not issubclass(K, type)
        assert isinstance(K, type)
        assert isinstance(K, object)  # Strange but true! Is this a bug?

        assert issubclass(Meta, type)
        assert type(Meta) is type

        assert issubclass(Q, K)
        assert issubclass(Q, object)
        assert isinstance(Q, Meta)
        assert isinstance(Q, type)
        assert type(Q) is not type

        # Now perform the real tests we care about.
        for obj in (int, bool, str, list, type, object, K, Meta, Q):
            self.failUnless(isclass(obj))
        for obj in (42, True, "a", [], object(), K(), Q()):
        # But don't include type or Meta!
            self.failIf(isclass(obj))

    def test_key2permutation(self):
        key2permutation = obfuscate.key2permutation
        testdata = [
            # Tests without duplicate entries.
            ('', []), ('G', [0]), ('ABCDEFGH', [0, 1, 2, 3, 4, 5, 6, 7]),
            ('spam', [3, 2, 0, 1]), ('zyxwabc', [6, 5, 4, 3, 0, 1, 2]),
            # Tests with duplicates.
            ('moon', [0, 2, 3, 1]),
            ('telephone', [8, 0, 4, 1, 7, 3, 6, 5, 2]),
            ]
        for arg, result in testdata:
            self.assertEquals(key2permutation(arg), result)

    def test_permuted(self):
        permuted = obfuscate.permuted
        for L in ([1, 2], [1, 2, 3, 4]):
            self.assertRaises(ValueError, permuted, L, [1,2,3])
            self.assertRaises(ValueError, permuted, L, 'cat')
        # Test the identity permutation.
        for n in range(5, 10):
            L = range(100, 100+n)
            id_permute = range(n)
            self.assertEquals(permuted(L, id_permute), L)
        # Check empty list.
        self.assertEquals(permuted([], []), [])

    def test_randchars(self):
        randchars = obfuscate.randchars

        # Fake choice function that returns each character in turn.
        # We use the default mutable trick to track the index.
        def mychoice(seq, i=[-1]):
            i[0] += 1
            return seq[i[0]]

        s = 'abc'
        it = randchars(s, mychoice)
        self.assertEquals(it.next(), 'a')
        self.assertEquals(it.next(), 'b')
        self.assertEquals(it.next(), 'c')
        self.assertRaises(IndexError, it.next)

    def test_remove_duplicates(self):
        remove_duplicates = obfuscate.remove_duplicates
        testdata = [
            ('', ''), ('A', 'A'), ('ABCDEF\n\n', 'ABCDEF\n'),
            ('spam 1231', 'spam 123'), ('aardvark', 'ardvk'),
            ('moon  river', 'mon rive'), ('TELEPHONE', 'TELPHON'),
            ('11223456543787', '12345678'), (BYTES+BYTES, BYTES),
            ]
        for arg, result in testdata:
            self.assertEquals(remove_duplicates(arg), result)

    def test_set_case_state(self):
        set_case_state = obfuscate.set_case_state
        for s in ('', 'A', 'a', 'Aa', '+', 'AbCdEfG', '123abcXYZ'):
            flags = obfuscate.get_case_state(s)
            s_lower = s.lower()
            self.assertEquals(s, obfuscate.set_case_state(s_lower, flags))


class AbstractClassTest(unittest.TestCase):
    """Test suite for the abstract base classes."""
    targets = [
        obfuscate._BaseCipher, obfuscate._PlayfairBase,
        obfuscate._TableCipher, obfuscate._SelfInvertingCipher,
        ]
    def testAbstractNoInstantiate(self):
        """Test that each abstract class cannot be instantiated."""
        for target in self.targets:
            self.assertRaises(TypeError, target, "")


class AbstractSelfInvertingCipherTest(unittest.TestCase):
    """Test the abstract behaviour of the _SelfInvertingCipher class."""
    target = obfuscate._SelfInvertingCipher

    def testCall(self):
        """Test that calling the abstract class fails."""
        self.assertRaises(TypeError, self.target, '')
        self.assertRaises(TypeError, self.target, [])

    def testTransform(self):
        """Test that calling the transform method fails."""
        self.assertRaises(TypeError, self.target.transform, '')


class ConcreteSelfInvertingCipherTest(unittest.TestCase):
    """Test the concrete behaviour of the _SelfInvertingCipher class."""

    # Since the class is an abstract class, we subclass it and work with that.
    class target(obfuscate._SelfInvertingCipher):
        @classmethod
        def transform(cls, msg):
            return msg

    def testConstructor(self):
        """Test that the constructor doesn't return a class instance."""
        cls = self.target
        self.failIf(isinstance(cls(''), cls))
        self.failIf(isinstance(cls([]), cls))

    def testCall(self):
        """Test that calling the class returns the correct object type."""
        self.failUnless(isinstance(self.target(''), basestring))
        self.failUnless(hasattr(self.target([]), 'next'))

    def testStringArgument(self):
        """Test the class with a string argument."""
        message = "Nobody expects the Spanish Inquisition!"
        s = self.target(message)
        self.assertEquals(s, message)

    def testIteratorArgument(self):
        """Test the class with an iterable argument."""
        message = "Nobody expects the Spanish Inquisition!".split()
        it = self.target(message)
        self.assertEquals(it.next(), 'Nobody')
        self.assertEquals(it.next(), 'expects')
        self.assertEquals(it.next(), 'the')
        self.assertEquals(it.next(), 'Spanish')
        self.assertEquals(it.next(), 'Inquisition!')
        self.assertRaises(StopIteration, it.next)


class BaseCipherTest(unittest.TestCase):
    """Test the _BaseCipher class."""

    target = obfuscate._BaseCipher

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        class Subclass(self.target):
            @staticmethod
            def encrypt_string(message, token):
                return token + message
            @staticmethod
            def decrypt_string(message, token):
                return message[len(token):]
        self.Subclass = Subclass

    def testAbstractClassMethodFails(self):
        """Test that calling encrypt/decrypt on the abstract class fails."""
        self.assertRaises(TypeError, self.target.encrypt, 'abc', 'key')
        self.assertRaises(TypeError, self.target.decrypt, 'abc', 'key')

    def testConstructor(self):
        """Test that we can instantiate the subclass."""
        inst = self.Subclass('key')
        self.failUnless(isinstance(inst, self.Subclass))

    def testTokens(self):
        """Test that instances have token attributes."""
        inst = self.Subclass('key')
        self.failUnless(hasattr(inst, 'ETOKEN'))
        self.failUnless(hasattr(inst, 'DTOKEN'))

    def getMethodResult(self, obj, methodname, *args, **kwargs):
        """Helper method to test methods."""
        return getattr(obj, methodname)(*args, **kwargs)

    def testInstanceMakeTokens(self):
        inst = self.Subclass('key')
        methods = ('make_encryption_token', 'make_decryption_token')
        for methodname in methods:
            result = self.getMethodResult(inst, methodname, 'key')
            self.assertEquals(result, 'key')

    def testGetTokens(self):
        """Test the get_encryption_token and get_decryption_token methods."""
        methods = ('get_encryption_token', 'get_decryption_token')
        for methodname in methods:
            # Test the instance.
            method = getattr(self.Subclass("key"), methodname)
            self.assertEquals(method(None), "key")
            self.assertEquals(method("altkey"), "altkey")
            # Test the class.
            method = getattr(self.Subclass, methodname)
            self.assertEquals(method("key"), "key")
            self.assertRaises(TypeError, method, None)
            self.assertRaises(TypeError, method)

    def testEncrypt(self):
        """Test the encrypt method."""
        self.assertEquals(self.Subclass.encrypt("spam", "key"), "keyspam")
        instance = self.Subclass("password")
        self.assertEquals(instance.encrypt("spam"), "passwordspam")
        self.assertEquals(instance.encrypt("spam", "KEEY"), "KEEYspam")

    def testDecrypt(self):
        """Test the decrypt method."""
        self.assertEquals(self.Subclass.decrypt("keyspam", "key"), "spam")
        instance = self.Subclass("password")
        self.assertEquals(instance.decrypt("passwordspam"), "spam")
        self.assertEquals(instance.decrypt("KEEYspam", "KEEY"), "spam")


class TableCipherAbstractTest(unittest.TestCase):
    """Test the abstract behaviour of the _TableCipher class."""
    target = obfuscate._TableCipher

    def testConstructorFail(self):
        """Test that the constructor fails."""
        self.failUnlessRaises(TypeError, self.target, '')

    def testMakeAlphabetFail(self):
        """Test that _TableCipher.make_alphabet fails appropriately."""
        self.failUnlessRaises(TypeError, self.target.make_alphabet)

    def testMakeCipherTableFail(self):
        """Test that _TableCipher.make_cipher_table fails appropriately."""
        self.failUnlessRaises(TypeError, self.target.make_cipher_table)

class TableCipherTest(unittest.TestCase):
    """Test the concrete behaviour of the _TableCipher class."""

    plaintext =  "Nobody expects the Spanish Inquisition!"
    ciphertext = "No5oy2 x1pxzts thx Sp4nish Inquisition~"

    # As this is an abstract class, we need to subclass it, which we do
    # in the __init__ method.
    target = obfuscate._TableCipher

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        class Subclass(self.target):
            def make_cipher_table(self, key):
                return "45zyxabcdef123~?!"
            def make_alphabet(self, key):
                return "abcdef12345xyz!~?"
        self.Subclass = Subclass

    def testConstructor(self):
        """Test that the constructor does return a class instance."""
        self.failUnless(isinstance(self.Subclass(''), self.target))

    def testEncrypt(self):
        """Test encryption."""
        inst = self.Subclass('')
        self.assertEquals(inst.encrypt(self.plaintext), self.ciphertext)

    def testDecrypt(self):
        """Test encryption."""
        inst = self.Subclass('')
        self.assertEquals(inst.decrypt(self.ciphertext), self.plaintext)

    def testRoundTrip(self):
        inst = self.Subclass('')
        self.assertEquals(inst.decrypt(inst.encrypt(BYTES)), BYTES)
        self.assertEquals(inst.encrypt(inst.decrypt(BYTES)), BYTES)


class SelfInvertingTests(unittest.TestCase):
    """Test self-inverting ciphers."""

    ciphers = [
        obfuscate.rot13, obfuscate.rot5, obfuscate.rot18, obfuscate.rot47,
        obfuscate.atbash, obfuscate.frob
        ]

    def testInvertStrings(self):
        """Test ciphers self-invert correctly with string arguments."""
        for cipher in self.ciphers:
            for s in TEST_STRINGS + [BYTES]:
                self.failUnlessEqual(cipher(cipher(s)), s)

    def testInvertIter(self):
        """Test ciphers self-invert correctly with iterator arguments."""
        for cipher in self.ciphers:
            for it, s in zip(*make_iterable_test_data()):
                self.failUnlessEqual(''.join(cipher(cipher(it))), s)

    def testRot13AgainstBuiltin(self):
        """Compare rot13 against the Python version."""
        for s in ASCII_TEST_STRINGS + [ASCII]:
            self.failUnlessEqual(s.encode('rot13'), obfuscate.rot13(s))


class CaesarTest(unittest.TestCase):
    """Test suite for the Caesar cipher."""
    target = obfuscate.Caesar

    def test_null(self):
        """Test that a Caesar shift of zero is the null cipher."""
        caesar0 = self.target(0)
        for s in TEST_STRINGS + [BYTES]:
            self.assertEquals(caesar0.encrypt(s), s)
            self.assertEquals(caesar0.decrypt(s), s)

    def roundtrip(self, shift, message):
        """Verify that the given shift round-trips correctly."""
        inst = self.target(shift)
        self.assertEquals(inst.decrypt(inst.encrypt(message)), message)
        self.assertEquals(inst.encrypt(inst.decrypt(message)), message)

    def testRoundTrip(self):
        """Test that all Caesar shifts round-trip correctly."""
        for i in range(26):
            for s in TEST_STRINGS + [BYTES]:
                self.roundtrip(i, s)

    def testModulo(self):
        """Test that Caesar shifts are modulo 26."""
        for i in range(26):
            inst1 = self.target(i)
            inst2 = self.target(i+26)
            self.assertEquals(inst1.encrypt(BYTES), inst2.encrypt(BYTES))
            inst2 = self.target(i+26*11)
            self.assertEquals(inst1.encrypt(BYTES), inst2.encrypt(BYTES))

    def testRot13(self):
        """Test that a Caesar shift of 13 is the same as rot13."""
        caesar13 = self.target(13)
        for s in ASCII_TEST_STRINGS:
            self.failUnlessEqual(caesar13.encrypt(s), s.encode('rot13'))

    def testEmptyStr(self):
        """Test that the Caesar cipher works on empty strings."""
        for shift in xrange(26):
            caesar = self.target(shift)
            self.assertEquals(caesar.encrypt(''), '')

    def testEmptyIter(self):
        """Test that the Caesar cipher works on empty iterables."""
        for shift in xrange(26):
            caesar = self.target(shift)
            it = caesar.encrypt([])
            self.assertRaises(StopIteration, it.next)

    def testEmptyStringIter(self):
        """Test Caesar cipher on an iterable containing empty strings."""
        for shift in xrange(26):
            caesar = self.target(shift)
            it = caesar.encrypt(['', 'x', ''])
            self.assertEquals(it.next(), '')
            it.next() # Skip one.
            self.assertEquals(it.next(), '')

    def testWhitespace(self):
        """Test that the Caesar cipher works on whitespace."""
        for shift in xrange(26):
            caesar = self.target(shift)
            for ws in (' ', '    ', '\t\n\r\f\v'):
                self.assertEquals(caesar.encrypt(ws), ws)

    def testIter(self):
        """Test that Caesar works with interables other than strings."""
        caesar0 = self.target(0)  # Null cipher.
        for it, s in zip(*make_iterable_test_data()):
            self.assertEquals(''.join(caesar0.encrypt(it)), s)
        caesar13 = self.target(13)
        for it, s in zip(*make_iterable_test_data(ascii_only=True)):
            self.assertEquals(''.join(caesar13.encrypt(it)), s.encode('rot13'))


class KeywordTest(unittest.TestCase):
    """Test suite for the Keyword cipher."""
    target = obfuscate.Keyword

    def testMakeCipherTable(self):
        """Test the key table generation method."""
        data = [
            ('',    'abcdefghijklmnopqrstuvwxyz'),
            ('z',   'zabcdefghijklmnopqrstuvwxy'),
            ('zyx', 'zyxabcdefghijklmnopqrstuvw'),
            ("Nobody expects the Spanish Inquisition!",
                "nobdyexpctshaiquvwzfgjklmr"),
            ]
        data = [(key, tbl+tbl.upper()) for (key, tbl) in data]
        genkey = self.target.make_cipher_table
        for key, result in data:
            assert len(result) == 52
            self.assertEquals(genkey(key), result)

    # FIXME -- the next two tests are actually testing the null cipher.
    def testStrEncryption(self):
        """Test Keyword cipher works as expected with strings."""
        null_cipher = self.target('')
        for s in TEST_STRINGS + [BYTES]:
            self.assertEquals(null_cipher.encrypt(s), s)

    # FIXME -- see above.
    def testIterEncryption(self):
        """Test Keyword cipher works as expected with iterables."""
        null_cipher = self.target('')
        for it, s in zip(*make_iterable_test_data()):
            self.assertEquals(''.join(null_cipher.encrypt(it)), s)

    def testRoundTrip(self):
        """Test the Keyword cipher round-trips correctly."""
        for key in ('', 'cheeseshop', 'ethel the aardvark', 'norwegian blue',
        'monty python', 'spanish inquisition', 'something 1234 xyz'):
            cipher = self.target(key)
            for s in TEST_STRINGS + [BYTES]:
                self.assertEquals(cipher.decrypt(cipher.encrypt(s)), s)
            for it, s in zip(*make_iterable_test_data()):
                result = cipher.decrypt(cipher.encrypt(it))
                self.assertEquals(''.join(result), s)


class AffineTest(unittest.TestCase):
    """Test suite for the Affine cipher."""
    target = obfuscate.Affine

    goodm = (10, 26, 52, 62, 94, 256)
    keys = [ # Known good key parameters, with arbitrary values of b.
        # Valid values of a for m=10 are 1, 3, 7, 9.
        (1, 6, 10),     (3, 1, 10),     (7, 9, 10),     (9, 4, 10),
        # Valid a for m=26 are 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.
        (1, 3, 26),     (3, 7, 26),     (5, 0, 26),     (7, 2, 26),
        (9, 17, 26),    (11, 21, 26),   (15, 8, 26),    (17, 3, 26),
        (19, 19, 26),   (21, 9, 26),    (23, 14, 26),   (25, 16, 26),
        # Arbitrarily selected values of a for m=52, 62, 94 and 256.
        (1, 17, 52),    (17, 11, 52),   (33, 0, 52),    (51, 42, 52),
        (1, 38, 62),    (13, 20, 62),   (45, 12, 62),   (61, 59, 62),
        (1, 87, 94),    (23, 72, 94),   (55, 80, 94),   (93, 36, 94),
        (1, 101, 256),  (29, 200, 256), (193, 11, 256), (255, 142, 256),
        ]

    def testBadAlphabetSize(self):
        """Fail instantiation with invalid alphabet sizes."""
        for m in range(-10, 300):
            if m in self.goodm: continue
            self.assertRaises(ValueError, self.target, 1, 1, m)

    def testBadParams(self):
        """Fail instantiation with bad key parameters."""
        bad = [  # Selected values of a that are not coprime with m.
            (0, 1, 10),     (2, 1, 10),     (6, 1, 10),     (8, 1, 10),
            (0, 1, 26),     (4, 1, 26),     (12, 1, 26),    (20, 1, 26),
            (0, 1, 52),     (8, 1, 52),     (28, 1, 52),    (42, 1, 52),
            (0, 1, 62),     (14, 1, 62),    (31, 1, 62),    (60, 1, 62),
            (0, 1, 94),     (47, 1, 94),    (68, 1, 94),    (92, 1, 94),
            (0, 1, 256),    (14, 1, 256),   (60, 1, 256),   (100, 1, 256),
            ]
        for a, b, m in bad:
            self.assertRaises(ValueError, self.target, a, b, m)

    def testGoodParams(self):
        """Test instantiating Affine with good key parameters."""
        for a, b, m in self.keys:
            self.failUnless(isinstance(self.target(a, b, m), self.target))

    def testCaesar(self):
        """Test that the Affine class can implement a Caesar shift."""
        for shift in range(26):
            affine = self.target(1, shift, 26)
            caesar = obfuscate.Caesar(shift)
            self.assertEquals(affine.encrypt(BYTES), caesar.encrypt(BYTES))

    def testAtbash(self):
        """Test that the Affine class can implement the Atbash cipher."""
        affine = self.target(25, 25, 26)
        self.assertEquals(affine.encrypt(BYTES), obfuscate.atbash(BYTES))

    # FIXME -- the next two methods actually test the null cipher.
    def testStrEncryption(self):
        """Test the Affine cipher works as expected with strings."""
        for m in self.goodm:
            null_cipher = self.target(1, 0, m)
            for s in TEST_STRINGS + [BYTES]:
                self.assertEquals(null_cipher.encrypt(s), s)

    # FIXME -- see above.
    def testIterEncryption(self):
        """Test the Affine cipher works as expected with iterables."""
        for m in self.goodm:
            null_cipher = self.target(1, 0, m)
            for it, s in zip(*make_iterable_test_data()):
                self.assertEquals(''.join(null_cipher.encrypt(it)), s)

    def testRoundTrip(self):
        """Test the Affine cipher round-trips correctly."""
        for key in self.keys:
            cipher = self.target(*key)
            for s in TEST_STRINGS + [BYTES]:
                self.assertEquals(cipher.decrypt(cipher.encrypt(s)), s)
            for it, s in zip(*make_iterable_test_data()):
                result = cipher.decrypt(cipher.encrypt(it))
                self.assertEquals(''.join(result), s)


class RowTransposeTest(unittest.TestCase):
    """Test suite for the row transposition cipher."""
    target = obfuscate.RowTranspose
    testdata = [("zoology\n", 4, "zooyolg\n"),
        ("Nobody expects the Spanish Inquisition!", 3,
            "Ns o Ibtnohqdeuy i Ssepixatpnieiocsnth!"),
        ("Nobody expects the Spanish Inquisition!!", 4,
            "Nepuocaibtnsosiid stythi h oeeInx n!pSq!"),
        ("hidden files", 2, "h ifdidleens"),
        ("hidden files", 6, "hde ieidnfls"),
        ]

    def test_null(self):
        """Test the Row Transpose null cipher."""
        for msg in TEST_STRINGS:
            self.assertEquals(self.target.encrypt(msg, 1), msg)

    def test_empty(self):
        """Test the Row Transpose cipher works with the empty string."""
        for rows in xrange(1, 11):
            self.assertEquals(self.target.encrypt('', rows), '')
            self.assertEquals(self.target.decrypt('', rows), '')

    def testPadding(self):
        """Test that the class has the appropriate PADDING attribute."""
        self.assert_(hasattr(self.target, 'PADDING'))
        self.assertEquals(len(self.target.PADDING), 1)

    def get_tester(self, get):
        """Testing method for the provided get method."""
        text = "abcde"  "fghij"  "klmno"  # Consider as three rows.
        width = 5
        self.assertEquals(get(text, 0, 0, width), 'a')
        self.assertEquals(get(text, 0, 4, width), 'e')
        self.assertEquals(get(text, 1, 3, width), 'i')
        self.assertEquals(get(text, 2, 4, width), 'o')

    def testInstanceGet(self):
        """Test the get method called from an instance."""
        self.get_tester(self.target(5).get)

    def testClassGet(self):
        """Test the get method called from the class."""
        self.get_tester(self.target.get)

    def get_tester_with_string_padding(self, get, pad):
        """Testing method for the provided get method, with string padding."""
        assert isinstance(pad, str)
        self.assertEquals(get('', 999, 999, 1), pad)

    def testInstanceGetWithStringPadding(self):
        """Test the get method called from an instance with string padding."""
        obj = self.target(5)
        self.get_tester_with_string_padding(obj.get, obj.PADDING)

    def testClassGetWithStringPadding(self):
        """Test the get method called from the class with string padding."""
        obj = self.target
        self.get_tester_with_string_padding(obj.get, obj.PADDING)

    def testIteratorPadding(self):
        """Test get method with iterator padding."""
        save = self.target.PADDING
        try:
            for obj in (self.target(5), self.target):
                obj.PADDING = iter('abc')
                self.assertEquals(obj.get('', 999, 999, 1), 'a')
                self.assertEquals(obj.get('', 999, 999, 1), 'b')
                self.assertEquals(obj.get('', 999, 999, 1), 'c')
        finally:
            self.target.PADDING = save

    def testValidation(self):
        """Test the private method _validate"""
        validator = self.target._validate
        # Too few rows.
        self.assertRaises(ValueError, validator, 0, 99)
        # Too few characters (width too small).
        self.assertRaises(ValueError, validator, 99, 0)
        self.assertRaises(ValueError, validator, 2, -1)
        # Allow at least one row.
        self.assert_(validator(1, 99) is None)
        self.assert_(validator(2, 1) is None)

    def testRoundTrip(self):
        """Test encryption and decryption round-trip correctly."""
        msg = "this is the secret message which is very secret okay thanks"
        for rows in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
            # Pad the text.
            n = rows - (len(msg) % rows)
            plaintext = "x"*n + msg
            assert len(plaintext) % rows == 0
            # Test the round-trip.
            ciphertext = self.target.encrypt(plaintext, rows)
            self.failIf(ciphertext == plaintext)
            self.failUnless(self.target.decrypt(ciphertext, rows) == plaintext)

    def testEncrypt(self):
        """Test the encrypt method."""
        # Test that calling on both the class and the instance works.
        for obj in (self.target, self.target(5)):
            encrypt = obj.encrypt
            for plaintext, rows, ciphertext in self.testdata:
                self.assertEquals(encrypt(plaintext, rows), ciphertext)

    def testDecrypt(self):
        """Test the decrypt method."""
        # Test that calling on both the class and the instance works.
        for obj in (self.target, self.target(5)):
            decrypt = obj.decrypt
            for plaintext, rows, ciphertext in self.testdata:
                self.assertEquals(decrypt(ciphertext, rows), plaintext)


class RailFenceTest(unittest.TestCase):
    """Rail Fence cipher test suite."""

    target = obfuscate.RailFence

    def test_null(self):
        """Test the Rail Fence null cipher."""
        for msg in TEST_STRINGS:
            self.assertEquals(self.target.encrypt(msg, 1), msg)

    def test_empty(self):
        """Test the Rail Fence cipher works with the empty string."""
        for rows in xrange(1, 11):
            self.assertEquals(self.target.encrypt('', rows), '')

    def test_iter_rails(self):
        """Test iter_rails method."""
        it = self.target.iter_rails(7)
        self.assert_(hasattr(it, 'next'))
        self.assertEquals([it.next() for _ in xrange(15)],
            [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 1, 2])

    def test_make_fence(self):
        """Test the make_fence method."""
        msg = "this is the message"
        result = self.target.make_fence(msg, 4)
        result1 = self.target.make_fence(msg, 4)
        self.assertEquals(result, result1)
        self.assertEquals(result,
            [list('tsme'), list('hi  eg'), list('i tesa'), list('shs')])

    def testEncrypt(self):
        """Test encryption with RailFence."""
        # Test that calling on both the class and the instance works.
        for obj in (self.target, self.target(5)):
            encrypt = obj.encrypt
            msg = "secret-message"
            self.assertEquals(encrypt(msg, 2), "sce-esgertmsae")
            self.assertEquals(encrypt(msg, 5), "seemsc-srtaeeg")

    def testEncryptWithKeys(self):
        """Test key-based encryption with RailFence."""
        encrypt = self.target.encrypt
        msg = "secret-message"
        for key in ('AB', [0, 1], 'mq', 'ex', '23'):
            self.assertEquals(encrypt(msg, 2, key), "sce-esgertmsae")
        for key in ('BA', [1, 0], 'qm', 'xe', '42'):
            self.assertEquals(encrypt(msg, 2, key), "ertmsaesce-esg")
        self.assertEquals(encrypt(msg, 3, [0, 1, 2]), "seegertmsaec-s")
        self.assertEquals(encrypt(msg, 3, [0, 2, 1]), "seegc-sertmsae")
        self.assertEquals(encrypt(msg, 3, [1, 0, 2]), "ertmsaeseegc-s")
        self.assertEquals(encrypt(msg, 3, [1, 2, 0]), "ertmsaec-sseeg")
        self.assertEquals(encrypt(msg, 3, [2, 0, 1]), "c-sseegertmsae")
        self.assertEquals(encrypt(msg, 3, [2, 1, 0]), "c-sertmsaeseeg")
        self.assertEquals(encrypt(msg, 3, "HAL"), "ertmsaeseegc-s")

    def testBadNumericKeys(self):
        """Test key-based encryption fails for bad numeric keys."""
        encrypt = self.target.encrypt
        # Test key which is too short, too long, invalid.
        for key in (range(6), range(8), range(1, 9)):
            self.assertRaises(ValueError, encrypt, "message", 4, key)

    def testBadStringKeys(self):
        """Test key-based encryption fails for bad string keys."""
        encrypt = self.target.encrypt
        # Test key which is too short, too long.
        for key in ("AB", "ABCDEFG"):
            self.assertRaises(ValueError, encrypt, "message", 4, key)


class randcharsTest(unittest.TestCase):
    """Test suite for the randchars function."""

    def __init__(self, *args, **kwargs):
        super(randcharsTest, self).__init__(*args, **kwargs)
        self.reset()

    def reset(self):
        """Reset the seed."""
        self.seed = -1  # Used by mychoice method.

    def mychoice(self, alist):
        """Non-random choice function for testing purposes."""
        self.seed = (self.seed + 1) % len(alist)
        return alist[self.seed]

    def test_randchars(self):
        """Test the randchars function with a supplied alphabet."""
        self.reset()
        alphabet = "0123456789"
        it = obfuscate.randchars(alphabet, self.mychoice)
        x = [it.next() for _ in xrange(20)]
        self.assertEquals(''.join(x), "01234567890123456789")

    def test_randchars_default(self):
        """Test the randchars function with the default alphabet."""
        self.reset()
        it = obfuscate.randchars(None, self.mychoice)
        x = [it.next() for _ in xrange(256)]
        self.assertEquals(''.join(x), BYTES)

    def test_randchars_choice(self):
        """Test the randchars function with the default choice function."""
        import random
        save = random.getstate()
        try:
            random.seed(14562)
            self.reset()
            it = obfuscate.randchars('abcdefgh')
            x = [it.next() for _ in xrange(20)]
            self.assertEquals(''.join(x), "chgabhhgabhcgbhffecc")
        finally:
            random.setstate(save)


class ChaffTest(unittest.TestCase):
    """Test suite for the Chaff class."""
    target = obfuscate.Chaff

    def test_hash_exists(self):
        """Test the Chaff class has a private hash attribute."""
        self.assert_(hasattr(self.target, '_hash'))
        self.assert_(hasattr(self.target._hash(''), 'digest'))

    def test_init(self):
        """Test Chaff class can be instantiated."""
        self.assert_(isinstance(self.target(2), self.target))
        self.assert_(isinstance(self.target(2, 'abcd'), self.target))

    def test_stream(self):
        """Test the default stream is correct."""
        inst = self.target(1)
        # This is a bit ugly...
        self.assert_(inst.stream.gi_frame.f_code is
            obfuscate.randchars.func_code)

    def test_hash(self):
        """Test the Chaff hash function."""
        self.assert_(isinstance(self.target(0, '').hash('something'), long))

    def test_get_chars_exact(self):
        """Test the Chaff get_chars staticmethod returns the right number of characters."""
        get_chars = self.target.get_chars
        def stream():
            while 1:
                yield 'a'
        stream = stream()
        for n in xrange(100):
            s = get_chars(n, stream)
            self.assertEquals(s, 'a'*n)

    def test_get_chars_short(self):
        """Test that Chaff.get_chars copes with a too short stream."""
        get_chars = self.target.get_chars
        def stream():
            for _ in xrange(10):
                yield 'a'
        stream = stream()
        s = get_chars(100, stream)
        self.assertEquals(s, 'a'*10)

    def test_pad_with_empty_key(self):
        """Test that the Chaff.pad method fails with an empty key."""
        self.assertRaises(ValueError, self.target(2).pad, "message", "")

    def test_unpad_with_empty_key(self):
        """Test that the Chaff.unpad method fails with an empty key."""
        self.assertRaises(ValueError, self.target(2).unpad, "message", "")

    def test_mod_key(self):
        """Test the mod_key method of the Chaff class."""
        self.assertEquals(self.target.mod_key("password"), "asswordq")
        self.assertEquals(self.target.mod_key("12345"), "23452")
        self.assertEquals(self.target.mod_key("\x02\x03\x04"), "\x03\x04\x03")
        self.assertEquals(self.target.mod_key("\xffab"), "ab\0")
        self.assertEquals(self.target.mod_key("R"), "S")

    def test_mod_empty_key(self):
        """Test that Chaff.mod_key fails with an empty key."""
        self.assertRaises(ValueError, self.target.mod_key, "")

    def test_padstr_two_strings(self):
        """Test that Chaff._padstr returns two strings."""
        self.check_two_strings('pad')
    def test_unpadstr_two_strings(self):
        """Test that Chaff._unpadstr returns two strings."""
        self.check_two_strings('unpad')

    def test_padstr_length(self):
        """Test that the 2nd string from _padstr has the right length."""
        self.check_string_length('pad')
    def test_unpadstr_length(self):
        """Test that the 2nd string from _unpadstr has the right length."""
        self.check_string_length('unpad')

    def test_paditer_no_strings(self):
        """Test Chaff._paditer method fails if passed a string message."""
        self.check_iter_no_strings('pad')
    def test_unpaditer_no_strings(self):
        """Test Chaff._unpaditer method fails if passed a string message."""
        self.check_iter_no_strings('unpad')

    def test_paditer(self):
        """Test Chaff._paditer method returns an iterable of strings."""
        self.check_iter('pad')
    def test_unpaditer(self):
        """Test Chaff._unpaditer method returns an iterable of strings."""
        self.check_iter('unpad')

    # FIXME: need explicit tests of pad and unpad, or are the doctests enough?

    # === Generator methods for producing test data ===

    def pad_gen(self):
        """Generate test data for the _[un]pad* test functions."""
        for size in xrange(1, 6):
            for key in ('x', 'abcd', 'something else 1248', '$x%6df^'):
                yield (size, key)

    def padstr_gen(self):
        """Generate test data for the _[un]padstr test functions."""
        for (size, key) in self.pad_gen():
            for msg in ('123', 'text', 'this is a message\n'):
                yield (size, key, msg)

    def paditer_gen(self):
        """Generate test data for the _[un]paditer test functions."""
        for (size, key) in self.pad_gen():
            for blocks in (
                ['123', 'text', 'this is a message\n'],
                [iter('xyz'), reversed('abcde')],
                (word for word in "hello world what happens now?".split()),
                ):
                yield (size, key, blocks)

    # === Check methods called by various test functions ===
    # (Check common behaviour for the assorted _[un]pad* methods)

    def verify_methodname_prefix(self, prefix):
        if prefix not in ('pad', 'unpad'):
            raise ValueError('bad method prefix %r' % prefix)

    def check_two_strings(self, prefix):
        """Check that Chaff._[un]padstr returns two strings."""
        self.verify_methodname_prefix(prefix)
        methodname = '_%sstr' % prefix
        for size, key, msg in self.padstr_gen():
            instance = self.target(size)
            method = getattr(instance, methodname)
            result = method(msg, key)
            self.failUnless(isinstance(result, tuple))
            self.failUnless(len(result) == 2)
            self.failUnless(isinstance(result[0], str))
            self.failUnless(isinstance(result[1], str))

    def check_string_length(self, prefix):
        """Check the length of the second string from Chaff._[un]padstr."""
        self.verify_methodname_prefix(prefix)
        methodname = '_%sstr' % prefix
        for size, key, msg in self.padstr_gen():
            instance = self.target(size)
            method = getattr(instance, methodname)
            result = method(msg, key)
            self.failUnless(len(result[1]) == len(key))

    def check_iter_no_strings(self, prefix):
        """Test Chaff._[un]paditer fails if passed a string message."""
        self.verify_methodname_prefix(prefix)
        methodname = '_%siter' % prefix
        instance = self.target(5)
        method = getattr(instance, methodname)
        self.assertRaises(TypeError, method, "message", "key")

    def check_iter(self, prefix):
        """Test Chaff._[un]paditer method returns an iterable of strings."""
        self.verify_methodname_prefix(prefix)
        methodname = '_%siter' % prefix
        for size, key, blocks in self.paditer_gen():
            instance = self.target(size)
            method = getattr(instance, methodname)
            result = method(blocks, key)
            self.failIf(isinstance(result, str))
            for x in result:
                self.failUnless(isinstance(x, str))


class PlayfairTest(unittest.TestCase):
    """Test suite for the Playfair cipher."""

    target = obfuscate.Playfair
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    assert len(alphabet) == 25

    # Note that not all characters in these keys are significant.
    testkeys = ['cherry pie', 'king george', 'PLAYFAIRCIPHER',
        'yellow-green', 'xyz1234%^&cba', 'UVW+-*/9876mnopq']
    testdata = [ # Caution here! This implementation of Platfair is lossy.
        # (plaintext before and after encryption/decryption)
        ('Jumping Jack Flash', 'IumpingIackFlash'),
        ('Beware the Jabberwock', 'BewaretheIabberwockx'),
        ('abcd1234\nxyz', 'abcdxyzx'),
        ('Nobody expects the Spanish Inquisition!',
         'NobodyexpectstheSpanishInquisition'),
        ('Lions and tigers and bears, oh my!', 'Lionsandtigersandbearsohmy'),
        ('Trip to the Moon', 'TriptotheMoxon'),
        ('Double xx', 'Doublexqxq'),
        ]

    def testPadding(self):
        """Test the PADDING attribute."""
        padding = self.target.PADDING
        self.failUnlessEqual(len(padding), 2)
        self.failIfEqual(padding[0], padding[1])
        self.failUnless(padding[0] in self.alphabet)
        self.failUnless(padding[1] in self.alphabet)

    def testInstantiate(self):
        """Test that Playfair can be instantiated."""
        self.assert_(isinstance(self.target(''), self.target))

    def testRoundTrip(self):
        """Test round-tripping of the Playfair cipher."""
        # Caution here: this implementation of Playfair is lossy!
        for key in self.testkeys:
            inst = self.target(key)
            for pretext, posttext in self.testdata:
                result = '????'
                errmsg = ('key="%s"; before="%s"; after="%s";'
                    ' actual="%s"; cipher="%s"' )
                try:
                    ciphertext = inst.encrypt(pretext)
                    result = inst.decrypt(ciphertext)
                    self.assertEquals(result, posttext, errmsg %
                        (key, pretext, posttext, result, ciphertext))
                except Exception:
                    print errmsg % \
                        (key, pretext, posttext, result, ciphertext)
                    raise

    def notestDoubleX(self):
        """Test strings with double X using Playfair."""
        inst = self.target("fix me")
        self.assertEquals(inst.encrypt('xx'), 'irir')
        self.assertEquals(inst.encrypt('xxa'), 'irfc')
        self.assertEquals(inst.encrypt('XX'), 'IrIr')
        self.assertEquals(inst.encrypt('Xxa'), 'Irfc')

    def testPreprocess(self):
        """Test Playfair preprocess method."""
        it = self.target.preprocess('ajk12z\n')
        self.assertEquals(it.next(), 'a')
        self.assertEquals(it.next(), 'i')
        self.assertEquals(it.next(), 'k')
        self.assertEquals(it.next(), 'z')
        self.assertRaises(StopIteration, it.next)


class Playfair6Test(PlayfairTest):
    """Playfair6 cipher test suite."""

    target = obfuscate.Playfair6
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    assert len(alphabet) == 36

    testdata = PlayfairTest.testdata[3:] + [
        ('Jumping Jack Flash', 'JumpingJackFlash'),
        ('123 Jumping Jack Flash', '123JumpingJackFlashx'),
        ('Beware the Jabberwock', 'BewaretheJabberwockx'),
        ('abcd1234\nxyz', 'abcd1234xyzx'),
        ]

    def testPreprocess(self):
        """Test Playfair6 preprocess method."""
        it = self.target.preprocess('ajk12z\n')
        self.assertEquals(it.next(), 'a')
        self.assertEquals(it.next(), 'j')
        self.assertEquals(it.next(), 'k')
        self.assertEquals(it.next(), '1')
        self.assertEquals(it.next(), '2')
        self.assertEquals(it.next(), 'z')
        self.assertRaises(StopIteration, it.next)

    def notestDoubleX(self):
        """Test strings with double X using Playfair6."""
        inst = self.target("fix me")
        self.assertEquals(inst.encrypt('xx'), 'anan')
        self.assertEquals(inst.encrypt('xxa'), 'anmf')
        self.assertEquals(inst.encrypt('XX'), 'AnAn')
        self.assertEquals(inst.encrypt('Xxa'), 'Anmf')


class Playfair16Test(PlayfairTest):
    """Playfair16 cipher test suite."""

    target = obfuscate.Playfair16
    alphabet = BYTES
    assert len(alphabet) == 256

    testdata = [
        ('Jumping Jack Flash', 'Jumping Jack Flash'),
        ('Beware the Jabberwock', 'Beware the Jabberwock\xa0'),
        ('abcd1234\nxyz', 'abcd1234\nxyz'),
        ('Nobody expects the Spanish Inquisition!',
            'Nobody expects the Spanish Inquisition!\xa0'),
        ('Lions and tigers and bears, oh my!',
            'Lions and tigers and bears, oh my!'),
        ('Trip to the moon', 'Trip to the moon'),
        ('Double XX', 'Double XX\xa0'),
        ('XXY\xa0\xa0X', 'X\xa0XY\xa0\xa1\xa0X'),
        ]

    def testPreprocess(self):
        """Test Playfair preprocess method."""
        it = self.target.preprocess(BYTES)
        for i in range(len(BYTES)):
            self.assertEquals(it.next(), BYTES[i])
        self.assertRaises(StopIteration, it.next)

    def testDoubleX(self):
        """Test strings with double X using Playfair16."""
        inst = self.target("")
        row1, col1 = divmod(ord('x') , 16)
        row2, col2 = divmod(ord('\xa0') , 16)
        assert row1 != row2 and col1 != col2
        r1, c1 = row1, col2
        r2, c2 = row2, col1
        c1 = chr(16*r1 + c1)
        c2 = chr(16*r2 + c2)
        self.assertEquals(inst.encrypt('xx'), (c1+c2)*2)


class VigenereTest(unittest.TestCase):
    """Test suite for Vigenere cipher."""
    target = obfuscate.Vigenere

    def test_alpha_ord_letters(self):
        """Test alpha_ord method of Vigenere with letters."""
        ao = self.target.alpha_ord
        for i, c in enumerate(string.ascii_uppercase):
            self.assertEquals(i, ao(c))
            self.assertEquals(i, ao(c.lower()))

    def test_alpha_ord_all(self):
        """Test alpha_ord method of Vigenere."""
        ao = self.target.alpha_ord
        r = range(26)
        for i, c in enumerate(BYTES):
            self.assert_(ao(c) in r)

    def test_shift_char(self):
        """Test that Vigenere.shift method always returns a char."""
        shift = self.target.shift
        # Test with an arbitrary selection of shift amounts.
        shifts = [1, 2, 5, 11, 17, 21, 28, 30, 45, 52, 175, 300, 457]
        shifts.extend([-(3+i) for i in shifts])
        shifts.extend([0, -1, -2])
        for c in BYTES:
            for n in shifts:
                s = shift(c, n)
                self.assert_(isinstance(s, basestring) and len(s) == 1)

    def test_shift_letters(self):
        """Test Vigenere.shift on letters."""
        shift = self.target.shift
        # Test with an arbitrary selection of shift amounts.
        shifts = [-4, -2, -1, 0, 1, 2, 3, 4, 10, 35, 66, 87, 156, 356]
        for c in string.ascii_uppercase:
            for n in shifts:
                self.assert_(shift(c, n) in string.ascii_uppercase)
                self.assert_(shift(c.lower(), n) in string.ascii_lowercase)

    def test_shift_case_letters(self):
        """Test that Vigenere.shift works the same on upper/lowercase."""
        shift = self.target.shift
        # Test with an arbitrary selection of shift amounts.
        shifts = [-7, -2, -1, 0, 1, 2, 3, 5, 12, 23, 42, 90, 187, 400]
        for C,c in zip(string.ascii_uppercase, string.ascii_lowercase):
            for n in shifts:
                self.assertEquals(shift(c, n), shift(C, n).lower())

    def test_shift_nonletters(self):
        """Test that Vigenere.shift on nonletters is a no-op."""
        shift = self.target.shift
        # Test with an arbitrary selection of shift amounts.
        shifts = [-5, -2, -1, 0, 1, 2, 3, 4, 11, 28, 55, 73, 179, 299]
        for c in BYTES:
            if c in string.ascii_letters:
                continue
            for n in shifts:
                self.assertEquals(shift(c, n), c)

    def testMakeTokenLen(self):
        """Test that the shifts produced by Vigenere have the right length."""
        for methodname in ("make_encryption_token", "make_decryption_token"):
            f = getattr(self.target, methodname)
            for key in ('ABC', 'secret', 'The Great & Terrible Oz!'):
                self.assertEquals(len(f(key)), len(key))

    def testMakeTokenRange(self):
        """Test that the Vigenere shifts are in the correct range."""
        for methodname in ("make_encryption_token", "make_decryption_token"):
            f = getattr(self.target, methodname)
            for key in ('ABC', 'secret', 'The Great & Terrible Oz!', BYTES):
                shifts = f(key)
                for shift in shifts:
                    self.failUnless(0 <= shift < 26)

    def testIter(self):
        """Test that Vigenere.encrypt and decrypt can return iterators."""
        for method in ("encrypt", "decrypt"):
            func = getattr(self.target, method)
            it = func(list('abc'), 'key')
            self.assert_(iter(it) is it)

    def testStr(self):
        """Test that Vigenere.encrypt and decrypt can return strings."""
        for method in ("encrypt", "decrypt"):
            func = getattr(self.target, method)
            s = func('abc', 'key')
            self.assert_(isinstance(s, str))

    def testMonoEncrypt(self):
        """Test Vigenere with a single char password (i.e. a Caesar shift)."""
        self.assertEquals(self.target.encrypt('abcABC', 'a'), 'bcdBCD')
        self.assertEquals(self.target.encrypt('abcABC', 'bb'), 'cdeCDE')

    def compare_dualmethods(self, name):
        """Compare method name when called on the class and instance."""
        f1 = getattr(self.target, name)  # Call on the class.
        f2 = getattr(self.target(''), name)  # Call on the instance.
        for msg in ("", "\n", "advance at dawn 12\n", "This Is The Message."):
            for key in ("", "c", "secret", "guess me", "1-2-3-spaghetti!"):
                self.assertEquals(f1(msg, key), f2(msg, key))

    def testDualEncrypt(self):
        """Test calling Vigenere on the class and instance."""
        self.compare_dualmethods('encrypt')
        self.compare_dualmethods('decrypt')

    def testNull(self):
        """Test that an empty password is the null cipher for Vigenere."""
        self.assertEquals(self.target.encrypt('abc', ''), 'abc')
        self.assertEquals(self.target.decrypt('abc', ''), 'abc')

    def testZNull(self):
        """Test that a key of 'Z' is a null cipher for Vigenere."""
        self.assertEquals(self.target.encrypt('abc', 'z'), 'abc')
        self.assertEquals(self.target.decrypt('abc', 'z'), 'abc')


class BaseFrob(unittest.TestCase):
    """Base class for frob testers."""
    messages = ('', 'something secret', '12345\\nabcdEFGH\\0\\01\\xFFz')

    @staticmethod
    def myfrob(s, key):
        """Independent implementation of frob for strings."""
        assert isinstance(s, str)
        buffer = []
        for n in map(ord, s):
            k = ord(key.next())
            buffer.append(chr(n^k))
        return ''.join(buffer)


class MonoFrobCommonTest(BaseFrob):
    """Common test suite for _MonoFrob and frob."""
    target = obfuscate._MonoFrob  # Override this in the subclass.

    def testNotInstantiable(self):
        """Test that the class cannot be instantiated."""
        self.failIf(isinstance(self.target('',''), self.target))

    def testStringMessage(self):
        """Test that the class returns a string with string messages."""
        self.assert_(isinstance(self.target('message', 'a'), str))

    def testNonStringMessage(self):
        """Test that the class returns an iterator with non-string messages."""
        for func in (list, tuple, iter):
            x = self.target(func('message'), 'a')
            self.assert_(iter(x) is x)

    def testNullCipher(self):
        """Test the null ciphers for the class."""
        for key in ('', '\0'):
            msg  = "message"
            x = self.target(msg, key)
            self.failUnlessEqual(x, msg)
            msg = list("message")
            x = self.target(msg, key)
            self.failUnlessEqual(list(x), msg)

    def testIsNull(self):
        """Test isnull method."""
        self.assert_(self.target.isnull(''))
        self.assert_(self.target.isnull('\0'))
        for c in BYTES[1:]:
            self.failIf(self.target.isnull(c))

    def testRoundtripStr(self):
        """Test that string messages roundtrip correctly."""
        frob = self.target
        for key in BYTES[23:89]:  # Keep the test reasonably fast.
            for s in TEST_STRINGS:
                self.assertEquals(frob(frob(s, key), key), s)

    def testRoundtripIter(self):
        """Test that iterable messages roundtrip correctly."""
        frob = self.target
        for key in BYTES[46:112]:  # Keep the test reasonably fast.
            for it, s in zip(*make_iterable_test_data()):
                t = ''.join(frob(frob(it, key), key))
                self.assertEquals(s, t)

    def testShortKeyStr(self):
        """Test that strings are encrypted correctly with a short key."""
        message = "And now for something completely different..."
        for key in BYTES:
            expected = self.myfrob(message, itertools.cycle(key))
            self.assertEquals(self.target(message, key), expected)

    def testShortKeyIter(self):
        """Test that iterables are encrypted correctly with a short key."""
        messages = "And now for something completely different...".split()
        for key in BYTES:
            keyit = itertools.cycle(key)
            expected = [self.myfrob(msg, keyit) for msg in messages]
            results = list(self.target(messages, key))
            self.assertEquals(results, expected)


class FrobCommonTest(MonoFrobCommonTest):
    target = obfuscate.frob
    keys = ('password', 'secret key', 'th1s i5 a_ "\\0+COMPLICATED-" paSsworD\\n;')

    def testRoundtripStr(self):
        """Test that string messages roundtrip correctly."""
        super(FrobCommonTest, self).testRoundtripStr()
        frob = self.target
        for key in self.keys:
            for s in TEST_STRINGS:
                self.assertEquals(frob(frob(s, key), key), s)

    def testRoundtripIter(self):
        """Test that iterable messages roundtrip correctly."""
        super(FrobCommonTest, self).testRoundtripIter()
        frob = self.target
        for key in self.keys:
            for s in TEST_STRINGS:
                self.assertEquals(frob(frob(s, key), key), s)

    def testLongKeyStr(self):
        """Test that string messages are encrypted correctly with a long key."""
        message = "And now for something completely different..."
        for key in self.keys:
            expected = self.myfrob(message, itertools.cycle(key))
            self.assertEquals(self.target(message, key), expected)

    def testShortKeyIter(self):
        """Test that iterable messages are encrypted correctly with a short key."""
        messages = "And now for something completely different...".split()
        for key in self.keys:
            keyit = itertools.cycle(key)
            expected = [self.myfrob(msg, keyit) for msg in messages]
            results = list(self.target(messages, key))
            self.assertEquals(results, expected)


class MonoFrobTest(BaseFrob):
    """Additional test suite for _MonoFrob."""
    target = obfuscate._MonoFrob

    def testAttrExists(self):
        """Test the _MonoFrob class has the correct attributes."""
        self.assert_(hasattr(self.target, '_cutover'))
        self.assert_(hasattr(self.target, '_cache'))
        self.assert_(hasattr(self.target, '_maxcache'))

    def testAttrValues(self):
        """Test the _MonoFrob class attributes have valid values."""
        self.assert_(isinstance(self.target._cutover, int))
        self.assert_(isinstance(self.target._cache, dict) or
            self.target._cache is None)
        self.assert_(isinstance(self.target._maxcache, int))

    def testBadKey(self):
        """Test that _MonoFrob does not accept long keys."""
        self.failUnlessRaises(ValueError, self.target, 'message', 'ab')

    def testCompareCompTrans(self):
        """Test that _MonoFrob gives the same result with both algorithms."""
        comp = self.target._comp
        trans = self.target._trans
        for key in xrange(256):
            for msg in self.messages:
                self.assertEquals(comp(msg, key), trans(msg, key))


class MonoFrobCacheTest(BaseFrob):
    """Test suite for the _MonoFrob caching."""
    target = obfuscate._MonoFrob

    def setUp(self):
        cache = self.target._cache
        if cache is not None:
            self.save_cache = cache.copy()
        else:
            self.save_cache = None

    def tearDown(self):
        if self.save_cache is None:
            self.target._cache = None
        else:
            if self.target._cache is not None:
                self.target._cache.clear()
                self.target._cache.update(self.save_cache)
            else:
                self.target._cache = self.save_cache

    def testPurging(self):
        """Test that purging works correctly with a cache."""
        self.target._cache = {'x': None, 'y': None}
        self.target._purge()
        self.assert_(self.target._cache == {})

    def testPurgingNone(self):
        """Test that purging works correctly with _cache set to None."""
        self.target._cache = None
        self.target._purge()
        self.assert_(self.target._cache is None)

    def testAutoPurge(self):
        """Test that the cache is purged automatically."""
        self.target._purge()
        assert self.target._cache == {}
        n = self.target._maxcache
        for i in xrange(n):
            _ = self.target._get_table(i)
            self.assert_(len(self.target._cache) == i+1)
        for i in xrange(n, 256):
            _ = self.target._get_table(i)
            self.assert_(len(self.target._cache) <= n)

    def testNoCache(self):
        """Test that caching can be disabled in _MonoFrob."""
        self.target._cache = None
        _ = self.target._get_table(45)
        self.assert_(self.target._cache is None)

    def testCompareCompTransCached(self):
        """Compare _MonoFrob._comp and ._trans with caching on."""
        comp = self.target._comp
        trans = self.target._trans
        self.target._purge()
        for k in xrange(32, 88):
            # Populate the cache.
            _ = self.target._get_table(k)
            for msg in self.messages:
                x = comp(msg, k)
                # Now call trans and let it fetch the result from the cache.
                self.assertEquals(x, trans(msg, k))
                self.assert_(len(self.target._cache) == k-31)

    def testCompareCompTransUncached(self):
        """Compare _MonoFrob._comp and ._trans with caching off."""
        comp = self.target._comp
        trans = self.target._trans
        self.target._cache = None
        for k in xrange(32, 88):
            _ = self.target._get_table(k)
            self.assert_(self.target._cache is None)
            for msg in self.messages:
                x = comp(msg, k)
                self.assertEquals(x, trans(msg, k))
                self.assert_(self.target._cache is None)


class MonoFrobTableTest(BaseFrob):
    """Test suite for _MonoFrob table methods."""
    target = obfuscate._MonoFrob

    def setUp(self):
        self.target._purge()

    def testMakeTable(self):
        """Test that _MonoFrob._make_table returns an appropriate string."""
        for key in BYTES:
            tbl = self.myfrob(BYTES, itertools.cycle(key))
            self.assertEquals(self.target._make_table(ord(key)), tbl)

    def testGetTable(self):
        """Test that _MonoFrob._get_table returns an appropriate string."""
        self.assert_(self.target._cache == {})
        for key in BYTES:
            k = ord(key)
            tbl = self.target._get_table(k)
            self.assertEquals(tbl, self.target._make_table(k))
            self.assert_(self.target._cache[k] == tbl)


class MonoFrobCutoverTest(unittest.TestCase):
    """Test suite for the cutover from one MonoFrob algorithm to the other."""

    class SignallingMonoFrob(obfuscate._MonoFrob):
        @classmethod
        def _comp(cls, *args, **kwargs):
            return "Calling _comp"
        @classmethod
        def _trans(cls, *args, **kwargs):
            return "Calling _trans"

    target = SignallingMonoFrob

    def setUp(self):
        self.save = self.target._cutover
    def tearDown(self):
        self.target._cutover = self.save

    def testAlwaysTrans(self):
        """Test that _MonoFrob can be forced to always call _trans."""
        for cut in (-1, -2, -99):
            self.target._cutover = cut
            self.assertEquals(self.target("x"), "Calling _trans")
            self.assertEquals(self.target("x"*10000), "Calling _trans")

    def testNeverTrans(self):
        """Test that _MonoFrob can be forced to never call _trans."""
        self.target._cutover = 0
        self.assertEquals(self.target("x"), "Calling _comp")
        self.assertEquals(self.target("x"*10000), "Calling _comp")

    def testSometimesTrans(self):
        """Test that _MonoFrob chooses the correct method to call."""
        self.target._cutover = 100
        for n in (1, 10, 50, 99):
            self.assertEquals(self.target("x"*n), "Calling _comp")
        for n in (100, 101, 200, 300):
            self.assertEquals(self.target("x"*n), "Calling _trans")


class IterableSupportTest(unittest.TestCase):
    """Test that the public API functions can all operate on iterables."""

    items = ( # (Test object, additional arguments)
        (obfuscate.rot13, ),                (obfuscate.rot5, ),
        (obfuscate.rot18, ),                (obfuscate.rot47, ),
        (obfuscate.atbash, ),               (obfuscate.Caesar, 12),
        (obfuscate.Keyword, 'password'),    (obfuscate.Affine, (3, 1, 10)),
        (obfuscate.Playfair, 'password'),   (obfuscate.Playfair6, 'password'),
        (obfuscate.Playfair16, 'password'), (obfuscate.Vigenere, 'password'),
        (obfuscate.RowTranspose, 5),        (obfuscate.RailFence, 5),
        (obfuscate.frob, 'password'),
        )

    message = "this is a string".split()

    def condition(self, result):
        return result is iter(result)

    def testResults(self):
        for item in self.items:
            obj = item[0]
            args = item[1:]
            if hasattr(obj, 'encrypt'):
                msg = "encrypt test failed for %s"
                x = obj.encrypt(self.message, *args)
                # x = obj.decrypt(self.message, *args)
                # self.failUnless(self.condition(x), msg % obj)
            else:
                msg = "test failed for %s"
                x = obj(self.message, *args)
            self.failUnless(self.condition(x), "test failed for %s" % obj)


class StringSupportTest(IterableSupportTest):
    """Test that the public API functions can all operate on strings."""
    message = ''.join(IterableSupportTest.message)
    def condition(self, result):
        return isinstance(result, basestring)







# ============================================================================

if __name__ == '__main__':
    gc.collect()
    assert not gc.garbage
    # Run doctests in the obfuscate module.
    failures, tests = obfuscate.selftest(obfuscate)
    if failures:
        print "Skipping further tests while doctests failing."
        sys.exit(1)
    else:
        print "Module doc tests: failed %d, attempted %d" % (failures, tests)
    # Run doctests in the example text file.
    failures, tests = doctest.testfile('examples.txt')
    if failures:
        print "Skipping further tests while doctests failing."
        sys.exit(1)
    else:
        print "Example doc tests: failed %d, attempted %d" % (failures, tests)
    # Run unit tests.
    print "Running unit tests:"
    try:
        unittest.main()
    except SystemExit:
        pass
    # Check for reference leaks.
    gc.collect()
    if gc.garbage:
        print "List of uncollectable garbage:"
        print gc.garbage
    else:
        print "No garbage found."

