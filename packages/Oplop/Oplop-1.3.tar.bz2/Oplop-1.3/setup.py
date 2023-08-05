from distutils.core import setup
import sys


if sys.version_info[:2] < (2, 6):
    raise SystemExit("Oplop requires Python 3.1 or newer "
                        "(or Python 2.6 or newer)")


# Only install argparse if necessary.
try:
    import argparse
except ImportError:
    py_modules = ['argparse']
else:
    py_modules = None


packages = ['oplop']
# Tests run under Python 3 only.
if sys.version_info[:2] >= (3, 1):
    packages.append('oplop.tests')


setup(name="Oplop",
        version='1.3',
        description="Generate account passwords based on an account name and "
                    "a master password",
        author="Brett Cannon",
        author_email="brett@python.org",
        url="http://oplop.googlecode.com",
        download_url="http://code.google.com/p/oplop/downloads/list",
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Security',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 3',
            # Python 3.0 probably works, but it's untested.
            'Programming Language :: Python :: 3.1',
        ],

        packages=packages,
        py_modules=py_modules,
        scripts=['bin/oplop'] if sys.platform != 'win32' else None,
)
