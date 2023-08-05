#!/usr/bin/env python

##  Module obfuscate.py
##
##  Copyright (c) 2010 Steven D'Aprano.
##
##  Permission is hereby granted, free of charge, to any person obtaining
##  a copy of this software and associated documentation files (the
##  "Software"), to deal in the Software without restriction, including
##  without limitation the rights to use, copy, modify, merge, publish,
##  distribute, sublicense, and/or sell copies of the Software, and to
##  permit persons to whom the Software is furnished to do so, subject to
##  the following conditions:
##
##  The above copyright notice and this permission notice shall be
##  included in all copies or substantial portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
##  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
##  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
##  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
##  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
##  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
##  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



"""Obfuscate text using a variety of classical cryptographic ciphers and
simple obfuscation functions.


    **********************************************************
    **  DISCLAIMER:                                         **
    **  These routines are not cryptographically secure     **
    **  and should not be used for applications requiring   **
    **  security against adversarial attacks.               **
    **********************************************************


The Ciphers
===========

  Cipher        |  Description
----------------+----------------------------------------------------
  Affine        |  Map characters using a mathematical function
* atbash        |  Shift letters A <-> Z, B <-> Y, C <-> X, etc.
  Caesar        |  Shift letters by a constant amount
  Chaff         |  Reversably add random noise to message
* frob          |  XOR characters with characters from a password
  Keyword       |  Map letters using a password as key
  Playfair      |  Encrypt pairs of letters (digraphs)
  Playfair16    |  Encrypt digraphs of binary characters
  Playfair6     |  Encrypt digraphs of letters and numbers
  RailFence     |  Transpose characters
* rot13         |  Rotate letters A <-> N, B <-> O, C <-> P, etc.
* rot18         |  Combine rot13 and rot5 in one function
* rot47         |  Rotate chars between '!' and '~' (ASCII 33-126)
* rot5          |  Rotate numbers 0 <-> 5, 1 <-> 6, 2 <-> 7, etc.
  RowTranspose  |  Transpose characters
  Vigenere      |  Variable Caesar shift


* Self-inverting cipher.

Most ciphers fall into two general categories:
    (a) Substitution ciphers
    (b) Transposition ciphers

Substitution ciphers are more common. Given an unencrypted letter, they
replace the letter with another letter. Monoalphabetic ciphers always
make the same substitution for a given key, e.g. if A is replaced by X
with a particular key, all A's in the message will be replaced by X.
Polyalphabetic ciphers vary the substitution so that, e.g. A may be
replaced with X the first time, P the second time, then E, and so on.

Transposition ciphers don't change the letters in the message, they
shuffle them around into an anagram.


The Cipher APIs
===============

Unless otherwise stated, all ciphers use one of two APIs.

(1) Self-Inverting Cipher API.

    Obfuscation and unobfuscation are the same operation. To obfuscate
    or unobfuscate a message, call the cipher object with the message
    as argument. In general, no key is required. When one is needed, you
    pass it as the second argument.

    Calling these ciphers on their own output reverses the obfuscation:

        >>> rot13('Send help now.')
        'Fraq uryc abj.'
        >>> rot13('Fraq uryc abj.')
        'Send help now.'

    (Hence the joke about calling rot13 twice for extra security.)

    These ciphers are polymorphic and can operate on either strings or
    arbitrary iterables containing strings. If the message passed to the
    cipher is a string, it will return a string. For any other iterable,
    the result is an iterator:

        >>> it = rot13(['Send', ' help', ' now.'])
        >>> it.next()
        'Fraq'
        >>> it.next()
        ' uryc'
        >>> it.next()
        ' abj.'


(2) Non-Self-Inverting Cipher API ("the Regular API").

    Obfuscation and unobfuscation are different operations. To obfuscate
    a message, call the encrypt method. To unobfuscate it, call decrypt.
    A key (password or passphrase) is generally required.

    There are three ways of obfuscating a message:

        (a) Call the encrypt method on the cipher object, giving the
            message and key as arguments.
        (b) Instantiate the cipher object with a key, then call the
            encrypt method on the instance without passing a key.
        (c) Call the encrypt method on the instance as in (b), except
            passing an alternate key.

    To unobfuscate a message, use the decrypt method instead of encrypt.

    Examples using the cipher object directly:

        >>> Keyword.encrypt('Tuesday by the fountain.', 'python')
        'Fgoehpl yl fro nagzfpsz.'
        >>> Keyword.decrypt('Fgoehpl yl fro nagzfpsz.', 'python')
        'Tuesday by the fountain.'

    Alternatively, you can instantiate the cipher with a key:

        >>> instance = Keyword('python')
        >>> instance.encrypt('Wednesday behind the bakery')
        'Johzoehpl yorszh fro ypvodl'
        >>> instance.encrypt('Thursday in the library')
        'Frgdehpl sz fro wsydpdl'

    Passing a key to the instance overrides the original key:

        >>> instance.encrypt('Thursday in the library', 'salad days')
        'Qcropdsw ej qcy heaosow'

    These ciphers are polymorphic and can operate on non-string iterable
    arguments as well as strings, in which case they return an iterator.
    For example:

        >>> it = instance.decrypt(['Frgdehpl', 'sz fro', 'wsydpdl'])
        >>> it.next()
        'Thursday'
        >>> it.next()
        'in the'
        >>> it.next()
        'library'



The Self-test
=============

This module includes a self-test function that executes the doctests in all
classes and functions. To run the self-test, execute the module from the
shell, e.g.:

    $ python obfuscate.py

For verbose output, pass the -v switch after the module name.
"""

from __future__ import division


# Module metadata.
__version__ = "0.2.2"
__date__ = "2010-04-10"
__author__ = "Steven D'Aprano <steve+python@pearwood.info>"


__all__ = [
    # Self-inverting monoalphabetic substitution ciphers.
    'rot13', 'rot5', 'rot18', 'rot47', 'atbash',
    # Other monoalphabetic substitution ciphers.
    'Caesar', 'Keyword', 'Affine', 'Playfair', 'Playfair6', 'Playfair16',
    # Polyalphabetic substitution ciphers.
    'frob', 'Vigenere',
    # Transposition ciphers.
    'RowTranspose', 'RailFence',
    # Steganographic padding.
    'Chaff',
    ]


import functools
import hashlib
import itertools
import random
import string

BYTES = string.maketrans('', '')  # ASCII characters from 0 to 255.


## An implementation note about the APIs used in this module
## =========================================================
## Some classes in this module behave as callable function-like objects
## (in C++ terminology, "functors"), returning a calculated result rather
## than a new instance. This is a relatively unusual thing to do, although
## new-style classes explicitly support it. Why do we do this rather than
## the more common strategy of using a callable instance? E.g:
##
##   class Common(object):
##       def __init__(self, *args): ...
##       def __call__(self, arg): ...
##
##   f = Common(...)  # Define a callable instance.
##   g = Common(...)  # And another one.
##
## One disadvantage of the instance-based strategy is that functors f
## and g both inherit the same docstring, from Common. Although we can
## give each one its own instance __doc__, help(f) and help(g) ignore
## the instance docstrings and use the class docstring.
##
## Another disadvantage is that it requires keeping both the class and an
## instance alive (although the class could be deleted, after instantiation,
## in order to hide it from casual use). This is redundant: since there
## would only ever be a single instance, the usual OOP strategy would be to
## make the instance a singleton. But classes in Python are already first-
## class singleton objects, so why bother creating an instance?


# === Utility classes and functions ===

def is_string(obj):
    """Return True if obj is string-like, otherwise False.

    >>> is_string("hello world")
    True
    >>> is_string(iter("hello world"))
    False

    """
    # FIX ME -- is there a better way to do this?
    # How about UserString and MutableString?
    return isinstance(obj, basestring)


def isclass(obj):
    """isclass(obj) -> True|False

    Return True if obj is a class or type, otherwise False.

    >>> isclass(int)
    True
    >>> isclass(42)
    False

    """
    try:
        return issubclass(obj, (type, object))
    except TypeError:
        return False


def remove_duplicates(s):
    """Remove duplicate characters from string s.

    >>> remove_duplicates("visit australia now")
    'vist aurlnow'

    """
    t = []
    for c in s:
        if c not in t:
            t.append(c)
    assert len(t) == len(set(t))
    return ''.join(t)


def key2permutation(key):
    """Return a permutation of range(len(key)).

    >>> key2permutation("bcda")
    [1, 2, 3, 0]
    >>> key2permutation("PYTHON")
    [3, 5, 4, 0, 2, 1]

    Ties are decided by going left to right.

    >>> key2permutation("PYTPHON")
    [3, 6, 5, 4, 0, 2, 1]

    Keys are case-sensitive, and are ordered according to their ordinal value.
    """
    key = [(c, i) for (i, c) in enumerate(key)]
    tmp = sorted(key)
    return [tmp.index(x) for x in key]


def permuted(alist, key=None):
    """Return a copy of alist permuted according to key.

    If key is None (the default), return a copy of alist. If key is a string,
    it is converted into a permutation list using key2permutation. Otherwise
    key should be a permutation of [0, 1, 2, ..., len(alist)-1], and items of
    alist are returned in that order.

    >>> permuted([10, 20, 30, 40], [3, 2, 0, 1])
    [40, 30, 10, 20]
    >>> permuted([10, 20, 30, 40], "code")
    [10, 40, 20, 30]

    """
    if key is None:
        return alist[:]
    if isinstance(key, str):
        if len(key) != len(alist):
            raise ValueError('key must have length %d' % len(key))
        key = key2permutation(key)
    elif sorted(key) != range(len(alist)):
        raise ValueError(
        'key must be permutation of [0,1,...%d]' % (len(alist)-1))
    return [alist[i] for i in key]


# FIXME? This is a very naive implementation of flatten.
def flatten(alist):
    """Return alist with sublists flattened.

    >>> flatten([0, [1, 2, 3], 4, [5, 6]])
    [0, 1, 2, 3, 4, 5, 6]

    """
    tmp = []
    for item in alist:
        try:
            tmp.extend(item)
        except TypeError:
            tmp.append(item)
    return tmp


def ceildiv(x, y):
    """Return x/y rounded up to the nearest integer.

    >>> ceildiv(10, 2)
    5
    >>> ceildiv(11, 2)
    6
    >>> ceildiv(-11, 2)
    -5

    """
    return x//y + bool(x%y)


class dualmethod(object):
    """Descriptor implementing dualmethods (combination class/instance method).

    Returns a method which takes either an instance or a class as the first
    argument. When called on an instance, the instance is passed as the first
    argument. When called as a class, the class itself is passed instead.

    >>> class Example(object):
    ...     @dualmethod
    ...     def method(this):
    ...         if type(this) is type:
    ...             print "I am the class '%s'." % this.__name__
    ...         else:
    ...             print (
    ...                 "I am an instance of the class '%s'." %
    ...                 this.__class__.__name__)
    ...
    >>> Example.method()
    I am the class 'Example'.
    >>> Example().method()
    I am an instance of the class 'Example'.

    """
    def __init__(self, func):
        self.func = func
    def __get__(self, obj, cls=None):
        if cls is None:  cls = type(obj)
        if obj is None:  obj = cls
        @functools.wraps(self.func)
        def newfunc(*args, **kwargs):
            return self.func(obj, *args, **kwargs)
        return newfunc


def abstract(func):
    """Decorate method func to make it abstract. func itself is never called."""
    @functools.wraps(func)
    def inner(*args, **kwargs):
        raise TypeError('abstract method <%s> must be overridden' % func.__name__)
    return inner


def get_case_state(s):
    """Return a list of flags stating which characters in s are uppercase.

    >>> get_case_state('SpaM')
    [True, False, False, True]

    """
    return [c.isupper() for c in s]


def set_case_state(s, flags):
    """Return string s converted to uppercase according to flags.

    >>> set_case_state('spam', [True, False, False, True])
    'SpaM'

    """
    if len(flags) != len(s):
        raise ValueError('too few or too many flags for string')
    t = zip(s, flags)
    return ''.join([(c.upper() if flag else c) for (c, flag) in t])


# === Substitution ciphers: abstract base classes ===


class _SelfInvertingCipher(object):
    """Abstract base class for self-inverting ciphers.

    This class should be used for classes where encryption and decryption
    are the same operation. Call the class itself to perform encryption or
    decryption.

    This class provides polymorphic encryption: both string and non-string
    iterable messages are supported. If the argument is a string, the return
    result is the encrypted (or decrypted) string. If the argument is some
    other iterable, the return result is an iterator which yields each item
    from the input argument after encryption.

    Subclasses of this cannot be instantiated: the subclass object itself is
    used as a callable function-like object. Calling the subclass performs
    encryption/decryption of the argument.

    To subclass this, you must override the transform method.
    """
    # The __new__ method is called when instantiating the class. Rather than
    # return an instance, we use __new__ instead of __call__ to return the
    # result we want (in this case, encrypt/decryption). This makes the class
    # object itself (rather than an instance of it) a callable (or functor in
    # C++ terminology). Furthermore, we get singleton behaviour for free.
    def __new__(cls, message, *args, **kwargs):
        cls._failIfAbstract()
        if is_string(message):
            return cls.transform(message, *args, **kwargs)
        else:
            def func():
                for block in message:
                    yield cls.transform(block, *args, **kwargs)
            return func()

    @classmethod
    def _failIfAbstract(cls, errmsg="abstract base class cannot be called"):
        """Raise TypeError if the current class is the abstract base class."""
        if cls is _SelfInvertingCipher:
            raise TypeError(errmsg)

    @classmethod
    @abstract
    def transform(cls, s, *args, **kwargs):
        """Return string s encrypted/decrypted.

        This method must be overridden in subclasses.
        """


class _BaseCipher(object):
    """Abstract base class for non-self-inverting ciphers.

    This class should be used for classes where encryption and decryption are
    different operations, which you perform using the encrypt and decrypt
    methods.

    This class provides polymorphic encryption: both string and non-string
    iterable messages are supported. If the message argument to the encrypt
    message is a string, the return result is the encrypted string. If the
    argument is some other iterable, the return result is an iterator which
    yields each item from the input argument after encryption.

    Subclasses of this class can be instantiated, but doing so is optional.
    To encrypt a message, you can call the encrypt method on either the class
    or an instance. If Cipher is a subclass, then any of:

    (1) Cipher.encrypt(message, key)

    (2) instance = Cipher(key)
        instance.encrypt(message)

    (3) instance = Cipher(key)
        instance.encrypt(message, altkey)

    are valid. In the third case, the key supplied to the method overrides the
    key used to instantiate the instance.

    To subclass this, you must override the encrypt_string and decrypt_string
    abstract methods. You may also override the make_encryption_token and
    make_decryption_token methods, which are no-ops by default, and __init__.
    """

    def __init__(self, key):
        self._failIfAbstract()
        # Convert key to suitable internal states for encryption and
        # decryption (tokens).
        self.ETOKEN = self.make_encryption_token(key)
        self.DTOKEN = self.make_decryption_token(key)

    # Input validation:

    @dualmethod
    def _verifykey(this, key):
        """Raise TypeError unless a key is given and not None.

        Keys can be given either explicitly in the key argument, or implicitly
        if this is an instance.
        """
        if isclass(this) and key is None:
                raise TypeError("no key specified")

    @dualmethod
    def _failIfAbstract(this, errmsg="abstract base class"):
        """Raise TypeError if the current class is the abstract base class."""
        cls = this if isclass(this) else type(this)
        if cls is _BaseCipher:
            raise TypeError(errmsg)

    # Manage decryption and encryption tokens:
    # Tokens are an abstract object used by the cipher. They could be the
    # key itself, or some data derived from the key. E.g. if the key is a
    # password, the token might be a translation table derived from that
    # password.

    @dualmethod
    def get_decryption_token(this, key):
        """Return a token used for decrypting, derived from key (which may be
        None) or the instance default key."""
        this._verifykey(key)
        if key is None:
            # Return the existing instance token.
            assert not isclass(this)
            return this.DTOKEN
        else:
            # Return a new token.
            return this.make_decryption_token(key)

    @dualmethod
    def get_encryption_token(this, key):
        """Return a token used for encrypting, derived from key (which may be
        None) or the instance default key."""
        this._verifykey(key)
        if key is None:
            # Return the existing instance token.
            assert not isclass(this)
            return this.ETOKEN
        else:
            # Return a new token.
            return this.make_encryption_token(key)

    # Decryption and encryption:

    @dualmethod
    def decrypt(this, ciphertext, key=None):
        """Unobfuscate ciphertext using a cipher and optional key."""
        this._failIfAbstract()
        token = this.get_decryption_token(key)
        if is_string(ciphertext):
            return this.decrypt_string(ciphertext, token)
        else:
            def inner():
                for s in ciphertext:
                    yield this.decrypt_string(s, token)
            return inner()

    @dualmethod
    def encrypt(this, plaintext, key=None):
        """Obfuscate plaintext using a cipher and optional key."""
        this._failIfAbstract()
        token = this.get_encryption_token(key)
        if is_string(plaintext):
            return this.encrypt_string(plaintext, token)
        else:
            def inner():
                for s in plaintext:
                    yield this.encrypt_string(s, token)
            return inner()

    # Abstract and other methods needing to be overridden:

    @dualmethod
    def make_encryption_token(this, key):
        """Return key converted to an encryption token."""
        # The default is a null-op. Optionally override this.
        return key

    @dualmethod
    def make_decryption_token(this, key):
        """Return key converted to an decryption token."""
        # The default is a null-op. Optionally override this.
        return key

    @dualmethod
    @abstract
    def encrypt_string(this, message, token):
        """Obfuscate a string message. This must be overridden in subclasses."""

    @dualmethod
    @abstract
    def decrypt_string(this, message, token):
        """Unobfuscate a string message. This must be overridden in subclasses."""


class _TableCipher(_BaseCipher):
    """Abstract base class for ciphers based on translation tables.

    To subclass this, you must override the methods make_cipher_table and
    make_alphabet.
    """

    @dualmethod
    def _failIfAbstract(this, errmsg="abstract base class"):
        """Raise TypeError if the current class is the abstract base class."""
        cls = this if isclass(this) else type(this)
        if cls is _TableCipher:
            raise TypeError(errmsg)

    @dualmethod
    def encrypt_string(this, message, table):
        """Encrypt string message using translation table."""
        return string.translate(message, table)

    decrypt_string = encrypt_string

    @dualmethod
    def make_encryption_token(this, key):
        alphabet = this.make_alphabet(key)
        cipherbet = this.make_cipher_table(key)
        return string.maketrans(alphabet, cipherbet)

    @dualmethod
    def make_decryption_token(this, key):
        alphabet = this.make_alphabet(key)
        cipherbet = this.make_cipher_table(key)
        return string.maketrans(cipherbet, alphabet)

    @dualmethod
    @abstract
    def make_cipher_table(this, key):
        """Return the character table used by the cipher.
        This method must be overridden.
        """

    @dualmethod
    @abstract
    def make_alphabet(this, key):
        """Return the plaintext character table used by the cipher.
        This method must be overridden.
        """


# === Monoalphabetic substitution ciphers ===


class rot13(_SelfInvertingCipher):
    """Obfuscate and unobfuscate text using rot13.

    rot13 is the Usenet standard for obfuscating spoilers, punchlines of jokes
    and other sensitive but unimportant information. It obfuscates the letters
    a...z and A...Z, shifting each letter by 13. Other characters are left
    unchanged. It is equivalent to a Caesar cipher with a shift of 13.

    rot13 is self-inverting: calling it again reverses the cipher:

    >>> rot13("Colonel Mering in the library with the candlestick")
    'Pbybary Zrevat va gur yvoenel jvgu gur pnaqyrfgvpx'
    >>> rot13('Pbybary Zrevat va gur yvoenel jvgu gur pnaqyrfgvpx')
    'Colonel Mering in the library with the candlestick'

    """
    tmp = string.ascii_lowercase
    tmp = tmp[13:] + tmp[:13]
    tmp += tmp.upper()
    TABLE = string.maketrans(string.ascii_letters, tmp)
    del tmp

    @classmethod
    def transform(cls, message):
        return string.translate(message, cls.TABLE)


class rot5(rot13):
    """Obfuscate and unobfuscate text using rot5.

    rot5 is the equivalent of rot13 for the digits 0...9, equivalent to a
    Caesar shift of 5 applied to digits.

    >>> rot5('Phone +079 2136-4568.')
    'Phone +524 7681-9013.'

    """
    TABLE = string.maketrans("0123456789", "5678901234")


class rot18(rot13):
    """Obfuscate and unobfuscate text using rot18.

    rot18 combines rot13 and rot5 in one cipher. The name is somewhat
    misleading, as it does not implement a Caesar shift of 18. It shifts
    letters by 13 and digits by 5.

    >>> rot18('Send 23 men to sector 42.')
    'Fraq 78 zra gb frpgbe 97.'

    """
    tmp = string.ascii_lowercase
    tmp = tmp[13:] + tmp[:13]
    tmp = tmp + tmp.upper() + "5678901234"
    TABLE = string.maketrans(string.ascii_letters + string.digits, tmp)
    del tmp


class rot47(rot13):
    """Obfuscate and unobfuscate text using rot47.

    rot47 is the equivalent of rot13 extended to the 94 characters between
    ASCII 33 and 126 inclusive. Is is a self-inverting Caesar shift of 47.

    >>> rot47("Shhh... this is a secret message")
    '$999]]] E9:D :D 2 D64C6E >6DD286'
    >>> rot47('$999]]] E9:D :D 2 D64C6E >6DD286')
    'Shhh... this is a secret message'

    """
    TABLE = string.maketrans(BYTES[33:127], BYTES[80:127] + BYTES[33:80])


class atbash(rot13):
    """Obfuscate and unobfuscate text using the ancient Hebrew atbash method.

    Letters are swapped A <-> Z, B <-> Y, C <-> X and so forth. atbash is
    self-inverting and case-preserving.

    >>> atbash('LET THERE BE LIGHT')
    'OVG GSVIV YV ORTSG'
    >>> atbash('OVG GSVIV YV ORTSG')
    'LET THERE BE LIGHT'

    """
    TABLE = string.maketrans(string.ascii_letters,
        string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1])


class Caesar(_TableCipher):
    """Caesar substitution cipher.

    The Caesar cipher is a case-preserving cipher that shifts each letter by a
    fixed amount. Julius Caesar himself used a shift of 3, that is A->D, B->E,
    C->F and so forth.

    The key for Caesar ciphers is an integer taken modulo 26. Obfuscate and
    unobfuscate by calling the encrypt and decrypt methods:

    >>> Caesar.encrypt('Invade Gaul on Wednesday.', 3)
    'Lqydgh Jdxo rq Zhgqhvgdb.'
    >>> Caesar.decrypt('Lqydgh Jdxo rq Zhgqhvgdb.', 3)
    'Invade Gaul on Wednesday.'

    Shifts are taken module 26, so that shifts of 27, 53, etc. are equivalent
    to a shift of 1. A shift of 0, 26, 52... is equivalent to the null cipher:

    >>> Caesar.encrypt('BEWARE THE TREACHERY OF BRUTUS', 0)
    'BEWARE THE TREACHERY OF BRUTUS'

    Hence there are only 25 substitutions possible with the Caesar cipher.
    """

    @staticmethod
    def make_alphabet(key):  # key is not actually used here.
        return string.ascii_letters

    @staticmethod
    def make_cipher_table(key):
        """Return a 52-character translation table for a Caesar shift.

        >>> Caesar.make_cipher_table(5)
        'fghijklmnopqrstuvwxyzabcdeFGHIJKLMNOPQRSTUVWXYZABCDE'

        """
        shift = key % 26
        shifted = string.ascii_lowercase
        shifted = shifted[shift:] + shifted[:shift]
        shifted += shifted.upper()
        assert len(shifted) == 52
        return shifted


class Keyword(_TableCipher):
    """Simple case-preserving keyword cipher.

    The Keyword cipher is a case-preserving cipher that uses an alphabetical
    password to shift each letter in the message.

    Obfuscate and unobfuscate by calling the encrypt and decrypt methods:

    >>> key = 'mary queen of scots'
    >>> Keyword.encrypt('Death to all Tyrants!', key)
    'Yqmgn gw mcc Glbmvgd!'
    >>> Keyword.decrypt('Yqmgn gw mcc Glbmvgd!', key)
    'Death to all Tyrants!'

    """

    @staticmethod
    def make_alphabet(key):  # key is not actually used here.
        return string.ascii_letters

    @staticmethod
    def make_cipher_table(key):
        """Generate a 52 character table from a key phrase.

        >>> Keyword.make_cipher_table('SWORDFISH')
        'swordfihjklmnpqtuvxyzabcegSWORDFIHJKLMNPQTUVXYZABCEG'
        >>> Keyword.make_cipher_table('Catherine the Great')
        'catheringjklmopqsuvwxyzbdfCATHERINGJKLMOPQSUVWXYZBDF'

        """
        lowercase = string.ascii_lowercase
        # Remove anything that isn't a letter, and duplicates.
        key = filter(lambda c: c in lowercase, key.lower())
        key = remove_duplicates(key)
        # Add the rest of the letters, starting after the last character
        # in the key and wrapping around.
        if key:
            p = lowercase.index(key[-1])
            key += lowercase[p+1:] + lowercase[:p+1]
        else:
            key = lowercase
        # Remove duplicates again.
        key = remove_duplicates(key)
        assert set(key) == set(lowercase)
        return key + key.upper()


class Affine(_TableCipher):
    """Generalisation of a large class of monoalphabetic substitution ciphers.

    The affine cipher generalises most monoalphabetic substitution ciphers
    with a pair of transformation functions and a key consisting of three
    integer parameters a, b and m. The letters of the alphabet are mapped to
    integers in the range 0...(m-1), then transformed to a different value
    using modular arithmetic with multiplicative parameter a and additive
    factor (shift) b. The transformed integer is then mapped back to a letter.

    The encryption function E(x) and decryption function D(x) for a single
    letter x are given by:

        E(x) = (a*x + b) % m
        D(x) = q*(x - b) % m

    where x is the ordinal value of each letter (e.g. 'A'=0, 'B'=1, etc.) and
    q is the multiplicative inverse of a modulo m. That is, q satisfies the
    equation 1 = (a*q) % m, implying that a and m are coprime.

    To use the Affine cipher, call the encrypt and decrypt methods with a
    tuple (a, b) or (a, b, m). If m is not specified, the default value is 26
    and the cipher will operate on case-preserving letters A...Z.

    >>> key = (5, 17, 26)
    >>> Affine.encrypt('Bury the gold behind the roses.', key)
    'Wnyh ial vjug wlafeg ial yjdld.'
    >>> Affine.decrypt('Wnyh ial vjug wlafeg ial yjdld.', key)
    'Bury the gold behind the roses.'

    For the cipher to be reversable, there are restrictions on the values of
    a and m allowed. a and m must be coprime, otherwise encryption is not 1:1
    and decryption is not possible. That is, the greatest common denominator
    (gcd) of a and m must equal 1. There are no restrictions on the shift
    parameter b apart from needing to be an integer.

    Only certain values for m are permitted in this implemention:

        m    |  Alphabet transformed
        -----+------------------------------------------
        10   |  digits 0...9 only
        26   |  case-preserving letters A...Z
        52   |  case-sensitive letters
        62   |  case-sensitive letters plus digits
        94   |  ASCII characters 33 to 126
        256  |  all extended ASCII characters 0 to 255

    "Case-preserving" means that upper and lowercase letters will map
    the same way, e.g. 'A' <-> 'G' and 'a' <-> 'g'.

    "Case-sensitive" means that upper and lowercase letters may map
    differently, e.g. 'A' <-> 'G' but 'a' <-> 'W'.

    If m is an invalid values, or if a and m are not coprime, ValueError
    is raised.
    """
    def __init__(self, a, b, m=26):
        key = (a, b, m)
        self.validate_key(key)
        super(Affine, self).__init__(key)

    @staticmethod
    def validate_key(key):
        """Raise TypeError or ValueError if key (a, b, m) is not valid.

        Note that this does not check that the inverse exists, that is, that
        a is coprime to m. That is checked during the generation of the
        translation table (see get_inverse method).
        """
        if type(key) is not tuple:
            raise TypeError('key must be a three-tuple')
        if len(key) != 3:
            raise ValueError('key must be a three-tuple')
        if not all(isinstance(i, int) for i in key):
            raise TypeError('key values must be integers')
        a, b, m = key
        if m not in (10, 26, 52, 62, 94, 256):
            raise ValueError('bad alphabet size m=%s' % m)

    @dualmethod  # FIXME -- should this be a static method?
    def make_alphabet(this, key):
        """Generate a variable-sized table of the plaintext alphabet.

        >>> Affine.make_alphabet((1, 0, 10))
        '0123456789'
        >>> Affine.make_alphabet((1, 0, 26))
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        """
        m = key[2]
        if m == 10:
            alphabet = string.digits
        elif m in (26, 52):
            alphabet = string.ascii_letters
        elif m == 62:
            alphabet = string.ascii_letters + string.digits
        elif m == 94:
            alphabet = BYTES[33:127]
        else:
            assert m == 256
            alphabet = BYTES
        assert m == 26 or len(alphabet) == m
        return alphabet

    @dualmethod
    def make_cipher_table(this, key):
        """Generate a variable-sized character table from a key (a, b, m).

        >>> Affine.make_cipher_table((1, 0, 10))
        '0123456789'
        >>> Affine.make_cipher_table((3, 1, 10))
        '1470369258'

        """
        a, b, m = key
        # Generate the inverse of a and the affine transformation function.
        q = this.get_inverse(a, m)
        assert q > 0
        assert (q*a) % m == 1
        # The affine transformation function for encryption:
        e = lambda x: (a*x+b) % m
        # Generate the plaintext alphabet.
        if m == 26:
            # We have to treat this case as a special case, due to
            # case-preserving properties.
            alphabet = string.ascii_lowercase
        else:
            alphabet = this.make_alphabet(key)
        assert len(alphabet) == m
        # Generate the transformed integer values.
        cipherbet = [e(x) for x in range(len(alphabet))]
        if __debug__:
            # Check the affine transformation function for decryption.
            d = lambda x: q*(x-b) % m
            assert [d(x) for x in cipherbet] == range(len(alphabet))
        # And convert integers back to letters.
        cipherbet = ''.join([alphabet[i] for i in cipherbet])
        # Now handle the special case where we preserve case.
        if m == 26:
            cipherbet += cipherbet.upper()
            assert len(cipherbet) == 2*len(alphabet)
        return cipherbet

    @staticmethod
    def get_inverse(a, m):
        """Return the multiplicative inverse of a modulo m.

        >>> Affine.get_inverse(3, 7)
        5
        >>> (5*3) % 7
        1

        Raises ValueError if a is not coprime to m.
        """
        # Calculate the extended GCD of a and m.
        xx, x = 0, 1
        yy, y = 1, 0
        mm = m
        while mm:
            quotient = a//mm
            a, mm = mm, a%mm
            xx, x = x - quotient*xx, xx
            yy, y = y - quotient*yy, yy
        # a is now the GCD.
        if a != 1:
            raise ValueError('bad a for given m (a and m must be coprime)')
        # x is the inverse, but be sure to return a positive number.
        return x % m


class PlayfairTable(object):
    """Helper class for the Playfair family of ciphers."""

    def __init__(self, table):
        size = int(len(table)**0.5)
        if size**2 != len(table):
            raise ValueError('table is not square')
        self.TABLE = table
        self._TABLE_SIZE = size

    @property
    def size(self):
        return self._TABLE_SIZE

    def find(self, digraph):
        """Return a pair of coordinates for the letters in the given digraph.

        >>> table = PlayfairTable('abcdefghijklmnop')
        >>> table.find("fo")
        ((1, 1), (3, 2))

        """
        a, b = digraph
        return self.cfind(a), self.cfind(b)

    def cfind(self, c):
        """Return the (row, column) where letter c is found in the table.

        >>> table = PlayfairTable('abcdefghi')
        >>> table.cfind('c')
        (0, 2)
        >>> table.cfind('h')
        (2, 1)

        """
        i = self.TABLE.index(c)
        return divmod(i, self.size)

    def get(self, a, b):
        """Return the digraph specified by the pair of coordinates a, b.

        >>> table = PlayfairTable('abcdefghijklmnop')
        >>> table.get((1, 1), (3, 2))
        'fo'

        """
        return self.cget(a) + self.cget(b)

    def cget(self, coord):
        """Return the single letter at the given coordinate in the table.

        >>> table = PlayfairTable('abcdefghi')
        >>> table.cget((0, 2))
        'c'
        >>> table.cget((2, 1))
        'h'

        """
        return self.TABLE[coord[0]*self.size + coord[1]]

    def __str__(self):
        """Return the string representation of the instance.

        >>> table = PlayfairTable('abcdefghi')
        >>> print table
        a b c
        d e f
        g h i

        """
        L = []
        size = self.size
        for i in range(size):
            L.append(' '.join(self.TABLE[i*size: i*size+size]))
        return '\n'.join(L)


class _PlayfairBase(_BaseCipher):
    """Abstract base class for Playfair family of ciphers.

    Playfair ciphers operate on digraphs (pairs of letters) rather than
    single characters, making frequency analysis far more difficult, and
    requiring a much longer sample of ciphertext.
    """

    # We need two distinct characters for padding: one is used to break up
    # double letters, the other is used if the double letter is the pad
    # character itself. We also use these same pad characters for adding to
    # the end of the string if it doesn't end with a diagraph.
    #
    # By default, we want these to be lowercase letters other than 'j',
    # although subclasses can weaken these restrictions.
    PADDING = 'xq'
    if __debug__:  # So I can indent the following code.
        assert len(PADDING) == 2
        assert PADDING[0] != PADDING[1]
        assert PADDING[0] in string.ascii_lowercase
        assert PADDING[1] in string.ascii_lowercase
        assert 'j' not in PADDING

    # This is a mapping of letters to letters.
    SUBSTITUTIONS = {}

    # This is a string of the characters used by the ciphertext.
    # Subclasses MUST override this, or bad things will happen.
    ALPHABET = None  # Force an exception if not overridden.

    @classmethod
    def _failIfAbstract(cls, errmsg="abstract base class cannot be called"):
        """Raise TypeError if cls is the abstract base class."""
        if cls is _PlayfairBase:
            raise TypeError(errmsg)

    @dualmethod
    def make_encryption_token(this, key):
        """Generate the key table used for encryptions."""
        for k,v in this.SUBSTITUTIONS.items():
            key = key.replace(k, v)
        alphabet = this.ALPHABET
        key = filter(lambda c: c in alphabet, key)
        key = remove_duplicates(key + alphabet)
        assert set(key) == set(alphabet)
        assert len(key) == len(alphabet)
        return key

    @dualmethod
    def make_decryption_token(this, key):
        """Generate the key table used for decryptions."""
        return this.make_encryption_token(key)[::-1]

    @dualmethod
    def encrypt_string(this, message, key):
        table = PlayfairTable(key)
        accumulator = []
        translate = this.translate_digraph
        for digraph in this.digraphs(message):
            accumulator.append(translate(digraph, table))
        return ''.join(accumulator)

    decrypt_string = encrypt_string

    @dualmethod
    def char_filter(this, c):
        """Return char c filtered and processed.

        Returns c (possibly modified) if it is permitted in the plaintext
        stream, otherwise return None.
        """
        c = this.SUBSTITUTIONS.get(c, c)
        if c in this.ALPHABET:
            return c
        else:
            return None

    @dualmethod
    def preprocess(this, stream):
        """Yield characters in stream after pre-processing.

        Performs replacements according to optional dict substitutions,
        and filters out any illegal characters.
        """
        for c in stream:
            c = this.char_filter(c)
            if c is not None:
                yield c

    @dualmethod
    def digraphs(this, stream):
        """Yield digraphs from stream.

        Double letters are broken up, and the stream is padded if necessary.
        """
        X, Q = this.PADDING
        assert X != Q
        stream = this.preprocess(stream)
        prev = ''
        for c in stream:
            if prev:
                if c == prev:
                    yield prev + (Q if prev==X else X)
                    prev = c
                else:
                    yield prev + c
                    prev = ''
            else:
                prev = c
        if prev:
            yield prev + (Q if prev==X else X)

    @dualmethod
    def translate_digraph(this, d, table):
        """Return translated digraph d using table.

        >>> table = PlayfairTable('abcdefghi')
        >>> translate = _PlayfairBase.translate_digraph
        >>> translate('ab', table)  # Digraph in the same row.
        'bc'
        >>> translate('be', table)  # Digraph in the same column.
        'eh'
        >>> translate('gf', table)  # Opposite corners.
        'id'

        """
        if len(d) != 2:
            raise ValueError('expected a digraph but got: %s' % d)
        size = table.size
        a, b = table.find(d)  # Get the coordinates of both letters.
        assert a != b
        if a[0] == b[0]:
            # Letters are in the same row. Move each one position to the
            # right (or left), wrapping around if needed.
            a = a[0], (a[1] + 1)%size
            b = b[0], (b[1] + 1)%size
        elif a[1] == b[1]:
            # Letters are in the same column. Move each one position down
            # (or above), wrapping if necessary.
            a = (a[0] + 1)%size, a[1]
            b = (b[0] + 1)%size, b[1]
        else:
            # Neither the same column nor row. Move to the opposite corner
            # of the rectangle defined by a and b by changing the column
            # and keeping the row unchanged.
            a, b = (a[0], b[1]), (b[0], a[1])
        # Get the translated and lowercased digraph.
        d = table.get(a, b)
        return d


class Playfair(_PlayfairBase):
    """Obfuscate or unobfuscate messages using the Playfair cipher.

    The Playfair cipher operates on digraphs (pairs of letters) rather than
    single characters. The advantage of Playfair is that frequency analysis
    is far more difficult and generally requires a much longer sample of
    ciphertext. However, as the key is limited to letters A-Z, Playfair is
    still a weak cipher by modern standards.

    Playfair is a lossy cipher:

    - characters other than letters are deleted;
    - the letter J is converted to I;
      (historically, some people kept J and I distinct, but dropped Q)
    - repeated characters may be separated by padding;
    - and the message is padded to an even length.

    Obfuscate and unobfuscate messages by calling the encrypt and decrypt
    methods:

    >>> key = 'playfair example'
    >>> Playfair.encrypt('Hide the gold in the tree stump', key)
    'Bmodzbxdnabekudmuixmmouvif'
    >>> Playfair.decrypt('Bmodzbxdnabekudmuixmmouvif', key)
    'Hidethegoldinthetrexestump'

    """

    SUBSTITUTIONS = {'j': 'i'}
    ALPHABET = "abcdefghiklmnopqrstuvwxyz"
    assert "j" not in ALPHABET

    @dualmethod
    def make_encryption_token(this, key):
        """Generate the 25 character key table used for encryptions.

        >>> Playfair.make_encryption_token('')
        'abcdefghiklmnopqrstuvwxyz'
        >>> Playfair.make_encryption_token('swordfish')
        'swordfihabcegklmnpqtuvxyz'

        Note that although this implementation of Playfair preserves case,
        the table generated is lowercase.
        """
        return super(Playfair, this).make_encryption_token(key.lower())

    @dualmethod
    def make_decryption_token(this, key):
        """Generate the 25 character key table used for decryptions.

        >>> Playfair.make_decryption_token('swordfish')
        'zyxvutqpnmlkgecbahifdrows'

        """
        return super(Playfair, this).make_decryption_token(key)

    @dualmethod
    def char_filter(this, c):
        """Return char c filtered and processed.

        Returns c (possibly modified) if it is permitted in the plaintext
        stream, otherwise return None.

        >>> Playfair.char_filter('a')
        'a'
        >>> Playfair.char_filter('j')
        'i'
        >>> Playfair.char_filter('?') is None
        True

        """
        flag = c.isupper()
        c = super(Playfair, this).char_filter(c.lower())
        if c:
            return c.upper() if flag else c
        else:
            return None

    @dualmethod
    def preprocess(this, stream):
        """Yield case-preserving characters in stream after pre-processing.

        Performs replacements according to optional dict substitutions,
        and filters out any illegal characters.

        >>> ''.join(Playfair.preprocess('Jumping Jack Flash!'))
        'IumpingIackFlash'

        """
        return super(Playfair, this).preprocess(stream)

    @dualmethod
    def digraphs(this, stream):
        """Yield digraphs from stream.

        Double letters are broken up, and the stream is padded if necessary.

        >>> list(Playfair.digraphs('Simon says jump'))
        ['Si', 'mo', 'ns', 'ay', 'si', 'um', 'px']
        >>> list(Playfair.digraphs('abbc ddex xy aabc'))
        ['ab', 'bc', 'dx', 'de', 'xq', 'xy', 'ax', 'ab', 'cx']

        """
        return super(Playfair, this).digraphs(stream)

    @dualmethod
    def translate_digraph(this, d, table):
        """Return translated digraph d using table, preserving case.

        >>> table = PlayfairTable('abcdefghi')
        >>> Playfair.translate_digraph('gF', table)
        'iD'

        """
        upper_flags = get_case_state(d)
        d = d.lower()
        d = super(Playfair, this).translate_digraph(d, table)
        d = set_case_state(d, upper_flags)
        return d


class Playfair6(Playfair):
    """Variant of the Playfair cipher extended to letters and numbers.

    Named "Playfair6" as the translation table is 6*6.

    Like the original Playfair cipher, this is lossy:
        - characters other than letters and digits are lost;
        - repeated characters may be separated by a pad character;
        - and the message is padded to an even length.

    >>> Playfair6.encrypt('Meet at 3pm', 'playfair7')
    'Ndcvysprh1'
    >>> Playfair6.decrypt('Ndcvysprh1', 'playfair7')
    'Meetat3pmx'

    Unlike the original Playfair, J is allowed as a letter.
    """
    SUBSTITUTIONS = {}
    ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"


class Playfair16(_PlayfairBase):
    """Variant of Playfair using all 256 extended ASCII characters.

    Named "Playfair16" as the translation table is 16*16.

    Like the original Playfair cipher, this is lossy:
        - repeated characters may be separated by a pad character;
        - and the message is padded to an even length.

    Otherwise there are no restrictions on characters, and case is
    significant.
    """

    PADDING = '\xa0\xa1'  # This must be exactly two distinct characters.
    assert len(PADDING) == 2
    assert PADDING[0] != PADDING[1]

    SUBSTITUTIONS = {}
    ALPHABET = BYTES

    @dualmethod
    def preprocess(this, stream):
        """Yield characters in stream.

        >>> ''.join(Playfair16.preprocess('Jumping Jack Flash!'))
        'Jumping Jack Flash!'

        """
        return super(Playfair16, this).preprocess(stream)


class _MonoFrob(object):
    """Private class _MonoFrob(msg[, key]) -> decoded/encoded message

    Obfuscate or unobfuscate a message by XORing with a single character key.
    This is a self-inverting monoalphabetic cipher, using a default key of
    chr(42) = '*', equivalent to the GNU C utility memfrob.

    If key is the empty string, or '\\0', _MonoFrob behaves as the null
    cipher and msg is not encoded or decoded.

    >>> _MonoFrob('magic')
    'GKMCI'
    >>> _MonoFrob('GKMCI')  # Reverse the cipher.
    'magic'

    Do not use this class directly. Instead, use frob(msg[, key]).
    """
    # We have a choice of algorithms for frobbing messages: a string.translate
    # based algorithm, and a naive list comp based algorith. The translate
    # algorithm is faster, but has a fairly hefty overhead making it slow for
    # short strings. We choose to cutover from the list comp algorithm to the
    # translate algorithm according to the value of _cutover:
    _cutover = 250
        # Set _cutover to 0 to never use translate, or a negative number
        # to always use it.

    # To get an even larger speedup, we cache the translation table:
    _cache = {}
        # Set _cache to None to disable the use of the cache.
    _maxcache = 100

    def __new__(cls, msg, key='*'):
        if len(key) > 1:
            raise ValueError('key must be empty or a single character')
        if is_string(msg):
            return cls.frob_string(msg, key)
        else:
            return cls.frob_iterable(msg, key)

    @classmethod
    def frob_string(cls, msg, key):
        """Frob string messages with a single-character or empty key.

        >>> frob = _MonoFrob.frob_string
        >>> frob('Abc\\x87', 'c')
        '"\\x01\\x00\\xe4'

        """
        assert is_string(msg)
        if cls.isnull(key):
            return msg
        else:
            k = ord(key)
            assert 0 <= k < 256
            return cls._optimized_monofrob(msg, k)

    @classmethod
    def frob_iterable(cls, msg, key):
        """Frob non-string messages with a single-character or empty key.

        >>> frob = _MonoFrob.frob_iterable
        >>> it = frob(list('"\\x01\\x00\\xe4'), 'c')
        >>> it.next()
        'A'
        >>> list(it)
        ['b', 'c', '\\x87']

        """
        if cls.isnull(key):
            return iter(msg)
        else:
            k = ord(key)
            assert 0 <= k < 256
            return itertools.imap(cls._optimized_monofrob, msg,
                itertools.cycle([k]))

    @classmethod
    def _optimized_monofrob(cls, s, k):
        """Return str s XORed with int k using some tricks for speed."""
        assert 0 <= k < 256
        cutover = cls._cutover
        if cutover == 0 or len(s) < cutover:
            return cls._comp(s, k)
        elif cutover < 0 or len(s) >= cutover:
            return cls._trans(s, k)
        assert False, 'no dispatch occurred - this should never happen'

    @classmethod
    def _comp(cls, s, k):
        """Return string s XORed with integer key k."""
        # Due to the overhead of the list comp, this is likely
        # to be slow for large strings.
        assert 0 <= k < 256
        ord_, chr_ = ord, chr  # Local copies for speed.
        return ''.join([chr_(ord_(c)^k) for c in s])

    @classmethod
    def _trans(cls, s, k):
        """Return str s XORed with int key k using a translation table."""
        # Due to the overhead of generating a 256 character table, this
        # is likely to be slow for small strings.
        assert 0 <= k < 256
        table = cls._get_table(k)
        return string.translate(s, table)

    @classmethod
    def _get_table(cls, k):
        """Return a translation table for integer key k.

        The table may be returned from the cache.
        """
        # The overhead of generating a table is fairly costly, so we only
        # call this for sufficiently large strings, and we cache the table.
        # Set the _cache attribute to None to disable caching.
        assert 0 <= k < 256
        cache = cls._cache
        if cache is None:
            # Don't use the cache at all, make a fresh table.
            return cls._make_table(k)
        assert isinstance(cache, dict)
        if k in cache:
            return cache[k]
        else:
            table = cls._make_table(k)
            # Don't let the cache get too big.
            if len(cache) >= cls._maxcache:
                cls._purge()
            cache[k] = table
            return table

    @classmethod
    def _make_table(cls, k):
        """Return a fresh translation table for integer key k."""
        assert 0 <= k < 256
        tmp = ''.join([chr(n^k) for n in xrange(256)])
        table = string.maketrans(BYTES, tmp)
        assert string.maketrans(tmp, BYTES) == table
        return table

    @classmethod
    def _purge(cls):
        """Purge unwanted entries in the cache."""
        # I'd prefer a proper LRU cache, but will settle for merely clearing
        # the entire cache. (If it's good enough for the re module, it's
        # good enough for me.)
        try:
            cls._cache.clear()
        except AttributeError:
            if cls._cache is None: pass
            else: raise

    @staticmethod
    def isnull(key):
        """Returns true for null cipher keys, otherwise false."""
        return key in ('', '\0')


# === Polyalphabetic substitution ciphers ===

class frob(object):
    """frob(message[, key]) -> ciphertext

    Obfuscate or unobfuscate a message by XORing with the characters of key.

    frob is a self-inverting polyalphabetic cipher. The default key is
    chr(42) = '*', equivalent to the GNU C utility memfrob.

    (Note that if key is a single character, frob is polyalphabetic in name
    only, and in practical terms becomes monoalphabetic.)

    >>> frob('magic')
    'GKMCI'
    >>> frob('GKMCI')  # Reverse the cipher.
    'magic'
    >>> frob('ADVANCE AT DAWN', 'xyz')
    '9=,979=Y;,Y>9.4'

    """

    def __new__(cls, msg, key='*'):
        if is_string(msg):
            return cls.frob_string(msg, key)
        else:
            return cls.frob_iterable(msg, key)

    @classmethod
    def frob_string(cls, msg, key):
        """Frob string messages with key.

        >>> frob.frob_string('mxymxy', 'AB')
        ',:8/9;'

        """
        assert is_string(msg)
        if cls.isnull(key):
            return msg
        elif len(key) == 1:
            return _MonoFrob(msg, key)
        else:
            assert key
            key = itertools.cycle(map(ord, key))
            msg = map(ord, msg)
            return ''.join([chr(c^k) for (c,k) in itertools.izip(msg, key)])

    @classmethod
    def frob_iterable(cls, msg, key):
        """Frob non-string messages with key.

        >>> it = frob.frob_iterable(iter('aaaa'), '&sT')
        >>> it.next()
        'G'
        >>> list(it)
        ['\\x12', '5', 'G']

        """
        if cls.isnull(key):
            return iter(msg)
        elif len(key) == 1:
            return _MonoFrob(msg, key)
        else:
            assert key
            key = itertools.cycle(map(ord, key))
            def inner():
                for block in msg:
                    block = itertools.imap(ord, block)
                    yield ''.join(
                        [chr(c^k) for (c,k) in itertools.izip(block, key)])
            return inner()

    @staticmethod
    def isnull(key):
        """Returns true for null cipher keys, otherwise false."""
        return key in ('', '\0')


class Vigenere(_BaseCipher):
    """Vigenere polyalphabetic substitution cipher.

    The Vigenere cipher shifts each letter in the message by a variable
    amount specified by a key, leaving non-letters untouched. It is
    equivalent to using the key to select between multiple Caesar ciphers,
    with "A" in the key equivalent to a Caesar shift of 1, "B" to a shift
    of 2, and so forth, up to "Z". This implies that plaintext characters
    will, in general, be encrypted into a different ciphertext character
    each time it is seen.

    This implementation treats the key as case insensitive ("A" is equivalent
    to "a") and the message as case-preserving. Non-letters in the key
    produce an arbitrary but consistent shift.

    Obfuscate and unobfuscate text by calling the encrypt and decrypt
    methods:

    >>> Vigenere.encrypt('All is NOT what it seems!', 'paranoia')
    'Qmd jg CXU misu wi bfunk!'
    >>> Vigenere.decrypt('Qmd jg CXU misu wi bfunk!', 'paranoia')
    'All is NOT what it seems!'

    If the key is chosen at random and as long as the message, then Vigenere
    is equivalent to a one-time pad cipher.

    WARNING: if key is made up of a single character (e.g. 'a' or 'bbbb')
    then the cipher will be equivalent to a single Caesar shift and will be
    very weak.

    Note: reversing the Vigenere cipher (using decrypt on the plaintext to
    generate the ciphertext, and encrypt on the ciphertext to generate the
    plaintext) is known as the "variant Beaufort cipher".
    """

    @dualmethod
    def make_encryption_token(this, key):
        """Return a non-empty list of encryption shifts calculated from key.

        >>> Vigenere.make_encryption_token('ample')
        [1, 13, 16, 12, 5]
        >>> Vigenere.make_encryption_token('Aardvark')
        [1, 1, 18, 4, 22, 1, 18, 11]
        >>> Vigenere.make_encryption_token('Wild Zero!')
        [23, 9, 12, 4, 7, 0, 5, 18, 15, 8]

        """
        if key:
            ord = this.alpha_ord
            result = [(ord(c)+1) % 26 for c in key]
        else:
            result = [0]
        if __debug__:
            for x in result:
                assert 0 <= x < 26
        return result

    @dualmethod
    def make_decryption_token(this, key):
        """Return a non-empty list of encryption shifts calculated from key.

        >>> Vigenere.make_decryption_token('ample')
        [25, 13, 10, 14, 21]

        """
        return [(26-n)%26 for n in this.make_encryption_token(key)]

    @dualmethod
    def encrypt_string(this, message, shifts):
        """

        >>> shifts = [2, 0, 1]
        >>> Vigenere.encrypt_string("AAA+BBBbbb + ccc", shifts)
        'CAB+DBCdbc + ecd'

        """
        assert shifts
        numshifts = len(shifts)
        i = -1  # Handle the index ourselves, rather than use enumerate.
        # This is necessary because we do not wish to increment i unless
        # the message character is a letter.
        letters = string.ascii_letters
        accumulator = []
        for c in message:
            if c in letters:
                i += 1
            # Note that although we pass a shift to the shift method, if
            # c is a non-letter it returns c unchanged without consuming
            # the shift value.
            accumulator.append(this.shift(c, shifts[i % numshifts]))
        return ''.join(accumulator)

    decrypt_string = encrypt_string

    @staticmethod
    def alpha_ord(c):
        """Static method alpha_ord(c) -> int

        Returns the ordinal value of case-insensitive letter c relative to
        'A', starting from 1, i.e. 'A' -> 0, 'B' -> 1, ... 'Z' -> 25. All
        other characters return some arbitrary value between 0 and 25.

        >>> alpha_ord = Vigenere.alpha_ord
        >>> alpha_ord('d')
        3
        >>> alpha_ord('x')
        23
        >>> alpha_ord('$')
        10

        """
        i = (string.ascii_lowercase.find(c) + 1) or \
            (string.ascii_uppercase.find(c) + 1)
        if i:
            i -= 1
        else:  # Non-letter.
            i = ord(c) % 26
        assert 0 <= i < 26
        return i

    @dualmethod
    def shift(this, c, n):
        """Method shift(c, n) -> char

        Shifts letters A-Za-z by n positions, e.g. n=4 gives:
        'A' -> 'E', 'B' -> 'F', ... 'Z' -> 'D'.

        Non-letters are returned unchanged.

        >>> shift = Vigenere.shift
        >>> shift('b', 3)
        'e'
        >>> shift('x', 5)
        'c'
        >>> shift('D', -4)
        'Z'
        >>> shift('$', 5)
        '$'

        """
        if c in string.ascii_lowercase:
            base = 97  # ord('a')
        elif c in string.ascii_uppercase:
            base = 65  # ord('A')
        else:
            # Non-letter, bail out early.
            return c
        # If we get here, c is an letter.
        o = this.alpha_ord(c)
        return chr(base + (o + n) % 26)


# === Transposition ciphers ===

class RowTranspose(_BaseCipher):
    """Basic transposition cipher.

    Obfuscates a message by transposing characters in the message as if it
    were written in a rectangular array, then reading in the opposite
    direction (down instead of across). The key used by the cipher is the
    number of rows. For example, the plaintext "ATTACK.AT.DAWN.SEND.FLOWERS"
    with three rows is written as:

        ATTACK.AT
        .DAWN.SEN
        D.FLOWERS

    The ciphertext is generated by reading down the columns instead of across
    the rows, giving "A.DTD.TAFAWLCNOK.W.SEAERTNS".

    >>> RowTranspose.encrypt('attack at dawn send flowers', 3)
    'a dtd tafawlcnok w seaertns'
    >>> RowTranspose.decrypt('a dtd tafawlcnok w seaertns', 3)
    'attack at dawn send flowers'

    Unless the length of the message is an exact multiple of the number of
    rows, the ciphertext will be padded with extra characters. By default
    spaces are used for such padding. In general, such padding is not
    reversable unless you choose a character which is recognisable as not
    part of the plaintext, but doing may give away the number of rows. You
    can set the padding character by assigning to the PADDING attribute: if
    it is a single character, it is used repeatedly, otherwise it should be
    an iterator whose next method yields the character.
    """
    PADDING = ' '
    assert len(PADDING) == 1

    @dualmethod
    def encrypt_string(this, message, numrows):
        if message:
            width = ceildiv(len(message), numrows)
            this._validate(numrows, width)
            return ''.join(this.transpose(message, numrows, width))
        else:
            return ''

    @dualmethod
    def decrypt_string(this, message, numrows):
        if message:
            width = ceildiv(len(message), numrows)
            this._validate(numrows, width)
            # Swap order of row/column relative to encryption.
            return ''.join(this.transpose(message, width, numrows))
        else:
            return ''

    @dualmethod
    def get(this, text, row, col, width):
        """Return the character in text at (row,col).

        If there is no such character, returns an appropriate
        padding character.
        """

        # Consider text 'abcdefgh' as a 4x2 array:
        #   abcd
        #   efgh
        #
        # The character at (row, col) is found at (row*width + col).
        try:
            return text[row*width + col]
        except IndexError:
            pad = this.PADDING
            if isinstance(pad, str):
                assert len(pad) == 1
                return pad
            else:
                return pad.next()

    @dualmethod  # Should this be a staticmethod?
    def _validate(this, rows, width):
        if rows < 1:
            raise ValueError("you must use at least one row")
        if width < 1:
            raise ValueError("too few characters for %d rows" % rows)

    @dualmethod
    def transpose(this, text, numrows, numcols):
        """Yield values from a transposed text block."""
        for col in xrange(numcols):
            for row in xrange(numrows):
                yield (this.get(text, row, col, numcols))


class RailFence(_BaseCipher):
    """Transposition cipher using the RailFence method.

    The message is transposed by writing it out as if on a rail fence,
    with the number of rails being the key. E.g. to encrypt the word
    "TRANSPOSITION" using three rails, first write it out on a railfence:

        T...S...I...N
        .R.N.P.S.T.O.
        ..A...O...I..

    (note that the pattern of writing the letters goes down, then up, then
    down, and repeats in this fashion). Then read across the rows, from top
    to bottom:

        TSINRNPSTOAOI

    >>> RailFence.encrypt('TRANSPOSITION', 3)
    'TSINRNPSTOAOI'

    The key is the number of rails, and a second optional key specifying the
    order to read the rows. This second key can be either a permutation of
    the ints [0, 1, ..., (rails-1)], or a string, which is then converted to
    a permutation by taking the letters in order:

    >>> RailFence.encrypt('TRANSPOSITION', 3, 'bca')  # Like [1, 2, 0].
    'RNPSTOAOITSIN'

    """
    def __init__(self, rails, key=None):
        super(RailFence, self).__init__((rails, key))

    @dualmethod
    def encrypt(this, plaintext, rails=None, key=None):
        if rails is key is None:
            key = None
        else:
            key = (rails, key)
        return super(RailFence, this).encrypt(plaintext, key)

    @dualmethod
    def encrypt_string(this, message, key):
        rails, extra_key = key
        if message:
            fence = this.make_fence(message, rails)
            fence = permuted(fence, extra_key)
            return ''.join(flatten(fence))
        else:
            return ''

    @dualmethod
    def decrypt_string(this, message, key):
        # FIX ME -- currently unimplemented.
        raise NotImplementedError

    @staticmethod
    def iter_rails(n):
        """Yield 0, 1, ..., n-2, n-1, n-2, n-3, ..., 1, 0, 1, 2, ...

        Count up through range(n), then down back to 0, then up, and so forth.

        >>> it = RailFence.iter_rails(5)
        >>> [it.next() for _ in range(20)]
        [0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0, 1, 2, 3]
        >>> it = RailFence.iter_rails(8)
        >>> [it.next() for _ in range(20)]
        [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5]

        """
        while 1:
            for i in xrange(n):
                yield i
            for i in xrange(n-2, 0, -1):
                yield i

    @dualmethod
    def make_fence(this, msg, rails):
        fence = [[] for _ in range(rails)]
        it = this.iter_rails(rails)
        for c in msg:
            rail = it.next()  # The rail we add to.
            assert 0 <= rail < rails
            fence[rail].append(c)
        return fence


# === Steganographic padding ===

def randchars(alpha=None, choice=random.choice):
    """Yield an infinite string of randomly selected characters.

    The characters are chosen randomly from alpha. By default, the full range
    of extended ASCII characters (bytes 0 through 255) are used.

    This is not guaranteed to be cryptographically strong.

    The optional second argument, choice, should be a function which takes a
    single non-empty sequence and returns a random item from that sequence.
    By default, random.choice is used. Note that random.choice uses the
    Mersenne Twister PRNG, which makes no attempt to stand up to adversarial
    attack.
    """
    if alpha is None:
        alpha = BYTES
    while 1:
        yield choice(alpha)


class Chaff(object):
    """Reversably pad a message with chaff (insignificant characters).

    (This should not to be confused with Ron Rivest's strong cryptographic
    technique known as "chaffing and winnowing".)

    Chaff, otherwise known as cryptographic nulls, are insignificant letters
    added to a message with the aim of confounding frequency analysis.

    The amount and type of chaff added is controlled by the arguments given
    when initialising the Chaff instance. You give two arguments: an integer
    width, and optionally a stream of random characters. The width controls
    the amount of chaff added before and after each character in the message.
    Each character gets an amount of chaff added before and after it, varying
    between zero and 2*width with average approximately equal to width.

    In other words, each character in the plaintext ends up separated by
    approximately width junk characters, on average. If x represents a
    random chaff character, and A an arbitrary plaintext character, then a
    message like AAAAA might be padded to xAxxxAxxAAxxxxAxxx.

    If no stream is provided, the default uses characters from the full
    extended ASCII range (bytes 0 through 255).

    To add chaff to a message, call the pad method with a key. The key
    determines how many chaff characters are actually added: on average, this
    will tend towards the width argument given above, but will vary from
    character to character according to the key:

    >>> chaff = Chaff(width=5, stream='.'*1000)
    >>> chaff.pad('message', key='ROSEBUD')
    '........m....e...s........s...a....g..e.........'

    The key is case-sensitive:

    >>> chaff.pad('message', key='rosebud')
    '....m.........e....s.s.....ag.....e...'

    The pad method can take either a single string, or an iterable of strings.
    If given a string, it returns a string. If given an iterable, it returns
    an iterator:

    >>> it = chaff.pad('flee to south'.split(), key='george')
    >>> it.next()
    '...f..l.......e......e.........'
    >>> it.next()
    't..o......'
    >>> it.next()
    '........s......o........ut........h.........'

    To reverse the padding, use the unpad method:

    >>> blocks = chaff.pad('flee to south'.split(), key='george')
    >>> it = chaff.unpad(blocks, 'george')
    >>> list(it)
    ['flee', 'to', 'south']

    """

    # We default to md5 for the internal hash function. Change this to
    # hashlib.sha1 or sha512 for extra strength, at the cost of speed.
    # Note that md5 is no longer considered cryptographically secure.
    _hash = hashlib.md5

    def __init__(self, width, stream=None):
        # Apply width characters of chaff to each plaintext character,
        # on average.
        self.factor = width*2
        self.exact = None  # Was the last unpad operation exact?
        if stream is None:
            self.stream = randchars()
        else:
            self.stream = iter(stream)

    def hash(self, s):
        """Return the hash of string s as a long integer.

        >>> Chaff(0, '').hash('librarian')
        71747721734195069858424710002407141750L

        """
        s = self._hash(s).hexdigest()
        return long(s, 16)

    @staticmethod
    def get_chars(n, stream):
        """Return up to n characters from iterable stream.

        >>> Chaff.get_chars(10, (chr(n) for n in xrange(40, 100)))
        '()*+,-./01'

        If the stream becomes empty before n characters are taken,
        return as many as are available:

        >>> Chaff.get_chars(10, iter("abcd"))
        'abcd'

        """
        stream = iter(stream)
        buffer = []
        try:
            for _ in xrange(n):
                buffer.append(stream.next())
        except StopIteration:
            pass
        return ''.join(buffer)

    @staticmethod
    def mod_key(key):
        """Return key after modification. key must be a non-empty string.

        >>> Chaff.mod_key("swordfish")
        'wordfisht'
        >>> Chaff.mod_key("wordfisht")
        'ordfishtx'
        >>> Chaff.mod_key("ordfishtx")
        'rdfishtxp'

        """
        if not key:
            raise ValueError('key must not be empty')
        return key[1:] + chr((ord(key[0])+1) & 0xFF)

    def _padstr(self, s, key):
        """Return tuple of (string s padded by key, updated key).

        See pad method for further details.
        """
        assert key
        buffer = []
        for c in s:
            # Calculate how much chaff to use. We hash the key to produce an
            # integer checksum which is approximately uniformly distributed
            # between 0 and (factor-1), with an average of very approximately
            # factor//2.
            n = self.hash(key) % self.factor
            # Add that many characters of chaff to the buffer.
            buffer.append(self.get_chars(n, self.stream))
            # Add one non-chaff character.
            buffer.append(c)
            # Update the key to make the next amount of chaff be different.
            key = self.mod_key(key)
        # Append one more lot of chaff to the buffer and return.
        n = self.hash(key) % self.factor
        buffer.append(self.get_chars(n, self.stream))
        return (''.join(buffer), self.mod_key(key))

    def _paditer(self, msg, key):
        """Yield padded blocks from msg.

        See pad method for further details.
        """
        assert key
        if isinstance(msg, basestring):
            raise TypeError('string passed to _paditer')
        def inner(msg, key):
            for block in msg:
                s, key = self._padstr(block, key)
                yield s
        return inner(msg, key)

    def pad(self, msg, key):
        """Pad msg with junk characters (chaff).

        Add an unpredicable amount of chaff to each character in msg. The
        amount of chaff added is approximately self.factor//2 per character
        in the message, and the distribution of chaff depends on the key,
        a non-empty string.

        >>> chaff = Chaff(3, '*'*1000)
        >>> chaff.pad('Secret Message', 'parrot')
        '**S****e****c***re****t** *M**es****s*****a****g****e*****'

        """
        if not key:
            raise ValueError('key must not be empty')
        if is_string(msg):
            return self._padstr(msg, key)[0]
        else:
            return self._paditer(msg, key)

    def _unpadstr(self, s, key):
        """Return two-tuple (unpadded string s, updated key).

        See unpad method for further details.
        """
        assert key
        buffer = []
        s = iter(s)
        while 1:
            # Throw away some chaff.
            n = self.hash(key) % self.factor
            key = self.mod_key(key)
            junk = self.get_chars(n, s)
            # Save one non-chaff character.
            try:
                buffer.append(s.next())
            except StopIteration:
                break
        return (''.join(buffer), key)

    def _unpaditer(self, msg, key):
        """Yield unpadded blocks from msg.

        See unpad method for further details.
        """
        assert key
        if isinstance(msg, basestring):
            raise TypeError('string passed to _unpaditer')
        def inner(msg, key):
            for block in msg:
                s, key = self._unpadstr(block, key)
                yield s
        return inner(msg, key)

    def unpad(self, msg, key):
        """Remove chaff from msg using non-empty key.

        >>> chaff = Chaff(3, '')
        >>> s = '**S****e****c***re****t** *M**es****s*****a****g****e*****'
        >>> chaff.unpad(s, 'parrot')
        'Secret Message'

        If the message has been truncated, unpad will return as much of the
        unpadded message that is available:

        >>> chaff.unpad('**S****e****c***re**', 'parrot')
        'Secre'

        If the message is extended with extra junk characters, unpad has no
        way of recognising the end of the real message and may return some
        junk:

        >>> msg = s + '$'*10
        >>> chaff.unpad(msg, 'parrot')
        'Secret Message$$'

        """
        if not key:
            raise ValueError('key must not be empty')
        self.exact = None  # Clear the exact flag.
        if is_string(msg):
            return self._unpadstr(msg, key)[0]
        else:
            return self._unpaditer(msg, key)



# === Command-line utilities: run doctests ===

def setup_extra_tests(module):
    global __test__
    import inspect
    t = {}
    if module is None:
        module_names = ('__main__',)
        __test__ = t
    else:
        module_names = ('__main__', module.__name__)
        module.__test__ = t
    for nm, obj in globals().items():
        if inspect.isclass(obj) and obj.__module__ in module_names:
            # Careful here! Not all classes have a __dict__!
            adict = getattr(obj, '__dict__', {})
            for name, attr in adict.items():
                if type(attr) in (classmethod, staticmethod):
                    # No need to include this as doctest already handles it.
                    continue
                if inspect.ismethoddescriptor(attr):
                    t[nm + '.' + name] = attr.__get__(obj)

def teardown_extra_tests(module):
    global __test__
    if module is None:  del __test__
    else:  del module.__test__

def selftest(module=None):
    import doctest
    # Unfortunately, as of Python 2.6.4, doctest.testmod doesn't find tests
    # in method descriptors, so we have to get them ourselves.
    setup_extra_tests(module)
    result = doctest.testmod(module)
    teardown_extra_tests(module)
    return result



# From the command line, run doctests.
if __name__ == '__main__':
    print selftest()


