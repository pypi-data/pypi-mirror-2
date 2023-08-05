from setuptools import setup

setup(
    name='wsdl2interface',
    version='1.0b2',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='http://pypi.python.org/pypi/wsdl2interface',
    description='Create zope.interface style interfaces from a WSDL file',
    long_description=open('README.txt').read(),
    py_modules = ['wsdl2interface'],
    license='ZPL',
    install_requires=[
        'suds',
    ],
    entry_points = {'console_scripts': ['wsdl2interface = wsdl2interface:main',]},
)
