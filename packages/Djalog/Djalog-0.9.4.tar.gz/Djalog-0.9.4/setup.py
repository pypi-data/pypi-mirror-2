import sys
from setuptools import setup, find_packages

djalog = __import__('djalog')
VERSION = djalog.get_version()
LONG_DESCRIPTION_FILE = 'README.rst'

try:
    long_description = open(LONG_DESCRIPTION_FILE).read()
except IOError:
    sys.stderr.write("ERROR: Cannot open readme file ('%s')\n"
        % LONG_DESCRIPTION_FILE)
    sys.exit(1)

setup(
    name = 'Djalog',
    version = VERSION,
    url = 'http://code.google.com/p/djalog',
    author = 'Lukasz Balcerzak',
    author_email = 'lukaszbalcerzak@gmail.com',
    description = djalog.__doc__,
    long_description = long_description,
    packages = find_packages(),
    zip_safe = True,
    include_package_data = True,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
)
