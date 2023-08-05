from setuptools import setup
from webdepcompress import __doc__


setup(
    name='WebDepCompress',
    version='0.2',
    url='http://dev.pocoo.org/hg/webdepcompress/',
    license='BSD',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    description='JavaScript and CSS Compression Package',
    long_description=__doc__,
    packages=['webdepcompress', 'webdepcompress.compressors'],
    namespace_packages=['webdepcompress', 'webdepcompress.compressors'],
    platforms='any'
)
