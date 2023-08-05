from setuptools import setup, find_packages

setup(
    name         = 'xmodem',
    version      = '0.1',
    author       = 'Wijnand Modderman',
    author_email = 'maze@pyth0n.org',
    description  = ('XMODEM protocol implementation.'),
    license      = 'MIT',
    keywords     = 'xmodem protocol',
    packages     = ['xmodem'],
    package_data = {'': ['doc/*.TXT']},
)

