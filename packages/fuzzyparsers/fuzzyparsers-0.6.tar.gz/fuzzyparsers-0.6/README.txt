The intent of the fuzzyparsers library is to provide a central place for functions to sanitize free form user input.

The library has two main parsers.  The first is a prefix parser which compares a string to a list of strings 
and returns the unique element of the list which matches the prefix.  An exception is thrown if the match is 
not unique.

    >>> fuzzy_match(['aab','bba','abc'],'aa')
    'aab'
    >>> fuzzy_match(['aab','bba','abc'],'a')  # two strings starting with 'a'.
    ... 
    ValueError('ambiguous match',)

The second parser parses dates in various formats and returns a datetime.date object.  Accepted formats include 

    jan 12, 2003
    jan 5
    2004-3-5
    +34 -- 34 days in the future (relative to todays date)
    -4 -- 4 days in the past (relative to todays date)

Fuzzyparsers is written by Joel B. Mohler and distributed under the terms of the GPL v2 (or later).

The doc-tests provide fair code coverage.  Use the following command::

    python -m doctest fuzzyparsers/*.py

To install fuzzyparsers, do the normal python thing (probably as root)::

    python setup.py install

or 
    eazy_install fuzzyparsers
