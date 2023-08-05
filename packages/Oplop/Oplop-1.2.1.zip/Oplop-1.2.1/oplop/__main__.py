"Generate account passwords based on an account name and a master password."
from __future__ import print_function

import argparse
try:
    import win32clipboard
except ImportError:
    win32clipboard = None
from . import create
from getpass import getpass
import subprocess
import sys


# Python 2.6 compat along with ease of mocking.
try:
    from builtins import input
except ImportError:
    input = raw_input


def get_account_name():
    return input('Account name = ')


def get_master_password():
    return getpass('Master password (not echoed) ... ')


def set_account_password(account_password):
    if sys.platform == 'darwin':
        clipboard = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        out, err = clipboard.communicate(account_password.encode('utf-8'))
        if out or err:
            print("Unexpected output from pbcopy:")
            if out:
                print("stdout:\n", out, sep="    ")
            if err:
                print("stderr:\n", err, sep="    ")
        else:
            print("\nAccount password copied to the clipboard")
    elif sys.platform == 'win32' and win32clipboard is not None:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(account_password)
        win32clipboard.CloseClipboard()
        print("\nAccount password copied to the clipboard")
    else:
        print("\n", account_password, "\n", sep='')


def main(cmd_line_args=[]):
    parser = argparse.ArgumentParser(prog="oplop", description=__doc__)
    parser.add_argument("account_name", nargs='?', help="Account name")
    args = parser.parse_args(cmd_line_args)
    if args.account_name:
        label = args.account_name
    else:
        label = get_account_name()
    master = get_master_password()
    password = create(label, master)
    set_account_password(password)


if __name__ == '__main__':
    main(sys.argv[1:])
