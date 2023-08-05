
import doctest
import test_urlimport
doctest.testmod(test_urlimport, optionflags=doctest.NORMALIZE_WHITESPACE |
                                   doctest.ELLIPSIS |
                                   doctest.REPORT_ONLY_FIRST_FAILURE
                                   )
