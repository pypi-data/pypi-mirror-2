from distutils.core import setup

setup(
    name = 'AutoRecalcDict',
    version = '0.1.1',
    author='Steven W. Orr',
    author_email='steveo@syslang.net',
    packages = ['autorecalcdict'],
    url='http://pypi.python.org/pypi/AutoRecalcDict/',
    description = 'dict that allows dependency definition.',
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
)
