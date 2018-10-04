import manuel.codeblock
import manuel.doctest
import manuel.ignore
import manuel.testing
import unittest


DOCTEST_STREAM = None


def get_manuel_doctest():
    global DOCTEST_STREAM

    m = manuel.doctest.Manuel()
    DOCTEST_STREAM = m.runner._fakeout
    return m


def get_test_suite():
    m = manuel.ignore.Manuel()
    m += get_manuel_doctest()
    m += manuel.codeblock.Manuel()
    return manuel.testing.TestSuite(m, 'README.rst')


if __name__ == '__main__':
    import logging

    test_suite = get_test_suite()
    # Redirect logging output to doctest runner so we can test logging output.
    # See https://stackoverflow.com/a/22301726/260303
    logging.basicConfig(level=logging.DEBUG, stream=DOCTEST_STREAM,
                        format='%(levelname)s: %(message)s')

    unittest.TextTestRunner().run(test_suite)
