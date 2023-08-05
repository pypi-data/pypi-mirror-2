from distutils.core import setup
import os

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name = 'onlinepayment',
    packages = ['onlinepayment'],
    version = '1.0.0',
    description = 'a generic Python API for making online payments',
    long_description=_read('README.txt'),
    author='Sam Tregar',
    author_email = "sam@wawd.com",
    license = "GPL 3",
    keywords = "credit card authorize.net CC AIM paypal payflow payment",
    url='http://code.google.com/p/python-onlinepayment/',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'Topic :: Office/Business :: Financial',
                 'Topic :: Software Development :: Libraries',
                 'Programming Language :: Python',
                 'Operating System :: OS Independent']
)
