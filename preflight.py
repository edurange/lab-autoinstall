#!/usr/bin/env python3

"""
A preflight/sanity check script for subiquity/cloud-init installations.
"""

# pylint: disable=duplicate-code
__author__ = "Joe Granville"
__date__ = "20260118"
__license__ = "MIT"
__version__ = "0.1.0"
__email__ = "jwgranville@gmail.com"
__status__ = "Proof-of-concept"
# pylint: enable=duplicate-code

import argparse
import shutil
import textwrap

import preflight_checks

ARGPARSE_DESCRPITION = __doc__.splitlines()[0]
ARGPARSE_EPILOG = (
    "%(prog)s is a read-only diagnostic tool for verifying installer outputs"
    " and per-user setup steps. Run in one of the following modes:" + """

    validate-install  Verify installed packages, files, and services
    setup-steps       Check minimum global post-install actions
    user [NAME]       Check minimum per-user setup (git config, SSH keys)

""" + "This tool does not modify the system. If a build fails, %(prog)s output"
    " can be used to determine what diagnostic information to collect."
)


def geterror(result):
    """
    Interpret a check result for errors.

    A non-None scalar, or a non-None value in the first element of a
    tuple, indicates an error. Success is indicated by None, an empty
    tuple, or a tuple with None in the first position.

    Returns None if there is no error. A non-None return value
    indicates the error code associated with a failed check.
    """
    if not isinstance(result, tuple):
        errorcode = result
    elif result:
        errorcode = result[0]
    else:
        errorcode = None
    return errorcode


def runchecks(checks):
    """
    Evaluate a collection of checks.
    """
    results = tuple(check() for check in checks)
    errorcodes = (geterror(result) for result in results)
    success = all(errorcode is None for errorcode in errorcodes)
    return success, results


def loadchecks(module):
    """
    Load a collection of checks from a check module.
    """
    checks = {
        "validate-install": getattr(module, "INSTALL_CHECKS", tuple()),
        "setup-steps": getattr(module, "SETUP_CHECKS", tuple()),
        "user": getattr(module, "USER_CHECKS", tuple()),
    }
    return checks


def _argparsesetup():
    parser = argparse.ArgumentParser(
        description=ARGPARSE_DESCRPITION, epilog=ARGPARSE_EPILOG
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    installhelp = "Run checks on results of installation and OS build"
    subparsers.add_parser("validate-install", help=installhelp)

    setuphelp = "Run checks on manual configuration the user must perform"
    subparsers.add_parser("setup-steps", help=setuphelp)

    userhelp = "Run checks on setup particular to specific user accounts"
    userparser = subparsers.add_parser("user", help=userhelp)
    userparser.add_argument(
        "username",
        nargs="?",
        default=None,
        help="User to check (defaults to current user)",
    )

    return parser


def _modeoutput(parser, args):
    output = f"{parser.prog} {args.mode}"
    if args.mode == "user" and args.username is not None:
        output = output + f" {args.username}"
    return output


def _resultindicator(result):
    if geterror(result) is not None:
        output = "FAIL"
    else:
        output = "PASS"
    return output


def _resultoutput(checks, results):
    terminalwidth = max(40, min(shutil.get_terminal_size().columns, 72))
    wrapper = textwrap.TextWrapper(
        width=terminalwidth,
        tabsize=4,
        initial_indent="\t- ",
        subsequent_indent="\t\t",
    )
    output = ""
    for check, result in zip(checks, results):
        output = output + f"[{_resultindicator(result)}] {check.__name__}()"
        if (errorcode := geterror(result)) is not None:
            output = output + f": {errorcode}"
        output = output + "\n"
        # Print result annotation messages
    return output


def _successoutput(success):
    if success:
        output = "Checks passed"
    else:
        output = "One or more checks failed - see results"
    return output


if __name__ == "__main__":
    mainparser = _argparsesetup()
    mainargs = mainparser.parse_args()
    print(_modeoutput(mainparser, mainargs))

    checkprofile = loadchecks(preflight_checks)
    mainchecks = checkprofile.get(mainargs.mode, default=tuple())
    if not mainchecks:
        print(f"{_modeoutput(mainparser, mainargs)}: no checks found")

    mainsuccess, mainresults = runchecks(mainchecks)

    print(_resultoutput(mainchecks, mainresults))
    print(_successoutput(mainsuccess))
