#!/usr/bin/env python3

"""
Tests for preflight.py.
"""

# pylint: disable=duplicate-code
__author__ = "Joe Granville"
__date__ = "20260119"
__license__ = "MIT"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"
# pylint: enable=duplicate-code

from preflight import geterror, runchecks
from tests.fixtures import mock_checks


def test_geterror_success_cases():
    assert geterror(None) is None
    assert geterror(()) is None
    assert geterror((None, "MOCK PASS")) is None


def test_geterror_failure_cases():
    assert geterror("MOCK FAIL") == "MOCK FAIL"
    assert geterror(1) == 1
    assert geterror(True) is True
    assert geterror(False) is False
    assert geterror(("MOCK FAIL", None))


def test_runchecks_all_pass():
    success, _ = runchecks(mock_checks.MOCK_SUCCEED_CHECKS)
    assert success is True


def test_runchecks_any_fail():
    successes = (
        runchecks((check,))[0] for check in mock_checks.MOCK_FAIL_CHECKS
    )
    assert all(successes) is False
