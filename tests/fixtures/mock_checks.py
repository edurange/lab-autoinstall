#!/usr/bin/env python3

"""
Mock checks for testing preflight.py.
"""

# pylint: disable=duplicate-code
__author__ = "Joe Granville"
__date__ = "20260119"
__license__ = "MIT"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"
# pylint: enable=duplicate-code


def _alwayspassnone():
    return None


def _alwayspasstuple():
    return tuple()


def _alwayspassnonetuple():
    return (None, "MOCK PASS")


def _alwaysfailstring():
    return "MOCK FAIL"


def _alwaysfailint():
    return 1


def _alwaysfailtrue():
    return True


def _alwaysfailfalse():
    return False


MOCK_SUCCEED_CHECKS = (_alwayspassnone, _alwayspasstuple, _alwayspassnonetuple)
MOCK_FAIL_CHECKS = (
    _alwaysfailstring,
    _alwaysfailint,
    _alwaysfailtrue,
    _alwaysfailfalse,
)

INSTALL_CHECKS = (_alwayspassnone, _alwaysfailstring)
SETUP_CHECKS = (_alwayspasstuple, _alwaysfailint)
USER_CHECKS = (_alwayspassnonetuple, _alwaysfailtrue, _alwaysfailfalse)
