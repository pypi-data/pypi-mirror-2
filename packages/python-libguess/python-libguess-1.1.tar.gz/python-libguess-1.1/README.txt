=====================
 python-libguess 1.1
=====================

python-libguess is a Python wrapper for libguess_.

libguess_ enables finding out in what encoding some text is for
given language. This library is especially useful for short text strings
that themselves don't carry reliable encoding information, like ID3 tags
in MP3 files. For example we can encode the same Japanese string in 3
different encodings (UTF-8, SHIFT-JIS, EUC-JP) and libguess_ will
hopefully guess the encoding correctly just by looking at the first
few bytes of the given string.

.. _libguess: http://www.atheme.org/project/libguess

You can also use this as a regular command line program by giving
region as the first parameter and possible target files after that::

  Usage: python -m guess REGION [INPUT_FILE]

  If input file name is not given, this program reads from the standard input.

Functions
=========

determine_encoding(in_string, region)
-------------------------------------

Determines encoding of a string for the given language region.

| Arguments:
| ``in_string`` -- a raw byte string for which encoding needs to be guessed.
| ``region`` -- one of the ``REGION_*`` constants for which encoding is guessed.

| Returns:
| String value indicating the guessed encoding of in_string argument for given region or ``None`` if error happened.

As an usage example we might see what happens when given Japanese
text in 2 different encodings::

  >>> import guess
  >>> guess.determine_encoding(u'\u3042'.encode('euc-jp'), guess.REGION_JP)
  'EUC-JP'
  >>> guess.determine_encoding(u'\u3042'.encode('utf-8'), guess.REGION_JP)
  'UTF-8'

The output string of this function can be given directly
to ``iconv_open()`` C function and the resulting names should be
compatible with the encoding string of ``str.decode()`` function::

  >>> encoded_value = u'\u3042'.encode('shift-jis')
  >>> encoding = guess.determine_encoding(encoded_value, guess.REGION_JP)
  >>> encoding
  'SJIS'
  >>> encoded_value.decode(encoding)
  u'\u3042'

In case the given region name is invalid or the underlying
``libguess_determine_encoding()`` call fails for any other reason,
None value is returned::

  >>> encoding = guess.determine_encoding("asdf", "UNKNOWN")
  >>> encoding is None
  True

Use ``REGION_*`` constants for region names.

validate_utf8(in_string)
------------------------

Checks if the given string is a valid UTF-8 byte sequence.

| Arguments:
| ``in_string`` -- a raw byte string to be inspected for UTF-8 validity.

| Return value:
| ``True`` if given string is a valid UTF-8 byte sequence, ``False`` otherwise.

This function is included here for the completeness with libguess
interface. It gives more precise results for UTF-8 validity than
for example functions in glib.

::

  >>> import guess
  >>> guess.validate_utf8(u'\u3042'.encode('EUC-JP'))
  False
  >>> guess.validate_utf8(u'\u3042'.encode('UTF-8'))
  True

Region names
============

| ``REGION_AR`` = 'arabic'
| ``REGION_BL`` = 'baltic'
| ``REGION_CN`` = 'chinese'
| ``REGION_GR`` = 'greek'
| ``REGION_HW`` = 'hebrew'
| ``REGION_JP`` = 'japanese'
| ``REGION_KR`` = 'korean'
| ``REGION_PL`` = 'polish'
| ``REGION_RU`` = 'russian'
| ``REGION_TR`` = 'turkish'
| ``REGION_TW`` = 'taiwanese'
