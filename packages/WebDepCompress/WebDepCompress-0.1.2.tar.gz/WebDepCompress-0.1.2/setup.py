from setuptools import setup


setup(
    name='WebDepCompress',
    version='0.1.2',
    url='http://dev.pocoo.org/hg/webdepcompress/',
    license='BSD',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    description='JavaScript and CSS Compression Package',
    long_description=__doc__,
    packages=['webdepcompress', 'webdepcompress.compressors'],
    namespace_packages=['webdepcompress.compressors'],
    platforms='any'
)
