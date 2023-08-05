from .. import __main__
from . import testdata
import contextlib
import subprocess
import sys
import unittest


@contextlib.contextmanager
def temp_setattr(ob, attr, new_value):
    sentinel = object()
    old_value = getattr(ob, attr, sentinel)
    setattr(ob, attr, new_value)
    yield old_value
    if old_value is sentinel:
        delattr(ob, attr)
    else:
        setattr(ob, attr, old_value)


class CLITests(unittest.TestCase):

    """Test that the CLI works properly."""

    tester = testdata[0]

    def capture_args(self):
        args = []
        def capture(*arguments):
            nonlocal args
            args[:] = arguments

        return args, capture

    def test_algorithm(self):
        # Make sure that everything is properly calculated.
        for data in testdata:
            account_name = temp_setattr(__main__, 'get_account_name',
                                        lambda: data['label'])
            master_password = temp_setattr(__main__, 'get_master_password',
                                            lambda: data['master'])
            account_password, capture = self.capture_args()
            account_password_context = temp_setattr(__main__,
                                                    'set_account_password',
                                                    capture)
            with account_name, master_password, account_password_context:
                __main__.main()
            self.assertEquals(data['password'], account_password[0])
            account_password = None

    def test_account_name_from_terminal(self):
        # Make sure that the account name is taken from the terminal.
        account_name = temp_setattr(__main__, 'input',
                                    lambda *args: self.tester['label'])
        master_password = temp_setattr(__main__, 'get_master_password',
                                        lambda: self.tester['master'])
        arg, capture = self.capture_args()
        account_password = temp_setattr(__main__, 'set_account_password',
                                        capture)
        with account_name, master_password, account_password:
            __main__.main()
        self.assertEquals(arg[0], self.tester['password'])

    def test_command_line(self):
        # Make sure that the account name can be taken from the command-line.
        def error():
            raise Exception
        account_name = temp_setattr(__main__, 'get_account_name', error)
        master_password = temp_setattr(__main__, 'get_master_password',
                                        lambda: self.tester['master'])
        args, capture = self.capture_args()
        account_password = temp_setattr(__main__, 'set_account_password',
                                        capture)
        with account_name, master_password, account_password:
            __main__.main([self.tester['label']])
        self.assertEquals(args[0], self.tester['password'])
        with self.assertRaises(BaseException):
            __main__.main([0,1])

    def test_master_password(self):
        # The master password should be grabbed using getpass.getpass().
        account_name = temp_setattr(__main__, 'get_account_name',
                                    lambda: self.tester['label'])
        master_password = temp_setattr(__main__, 'getpass',
                                        lambda *args: self.tester['master'])
        args, capture = self.capture_args()
        account_password = temp_setattr(__main__, 'set_account_password',
                                        capture)
        with account_name, master_password, account_password:
            __main__.main()
        self.assertEquals(args[0], self.tester['password'])

    @unittest.skipIf(sys.platform != "darwin", "requires OS X")
    def test_account_password_copied(self):
        # Under OS X, the account password should be copied to the clipboard.
        account_name = temp_setattr(__main__, 'get_account_name',
                                    lambda: self.tester['label'])
        master_password = temp_setattr(__main__, 'get_master_password',
                                        lambda: self.tester['master'])
        silence_print = temp_setattr(__main__, 'print', lambda *args, **kwargs:
                                        None)
        with account_name, master_password, silence_print:
            __main__.main()
        pasteboard = subprocess.check_output('pbpaste')
        self.assertEquals(pasteboard, self.tester['password'].encode('ascii'))




def test_main():
    from test.support import run_unittest
    run_unittest(CLITests)



if __name__ == '__main__':
    test_main()
