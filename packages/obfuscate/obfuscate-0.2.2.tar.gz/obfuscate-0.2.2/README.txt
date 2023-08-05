============================================
obfuscate -- classical encryption algorithms
============================================

Introduction
------------

obfuscate provides classical encryption algorithms suitable for obfuscating
and unobfuscating text.

Includes:

- rot13, rot5, rot18, rot47
- atbash
- Caesar cipher
- Keyword
- Affine
- Playfair, Playfair6, Playfair16
- frob (xor)
- Vigenere
- RailFence
- plus others.


Requires Python 2.5 or 2.6.

DISCLAIMER: obfuscate is not cryptographically strong, and should not be used
in high-security applications where state of the art encryption is required.
The ciphers provided in obfuscate may have been state of the art in the past,
but should not be considered secure against modern attacks.

See also the file examples.txt for more information.


Installation
------------

obfuscate requires Python 2.5 or 2.6. To install, do the usual:

    python setup.py install


Licence
-------

obfuscate is licenced under the MIT Licence. See the LICENCE.txt file
and the header of obfuscate.py.


Self-test and unit-tests
------------------------

You can run the module's doctests by executing the file from the commandline.
On most Linux or UNIX systems:

    $ chmod u+x obfuscate.py  # this is only needed once
    $ ./obfuscate.py

or:

    $ python obfuscate.py

If all the doctests pass, no output will be printed. To get verbose output,
run with the -v switch:

    $ python obfuscate.py -v

To run obfuscate's unit tests, execute the test suite from the commandline:

    $ python testsuite.py

The test suite also takes an optional -v switch for verbose output.


Known Issues
------------

See the CHANGES.txt file for a list of known issues.

