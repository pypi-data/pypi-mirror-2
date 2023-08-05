import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(
    name='drippy',
    version='0.1',
    description='Nose plugin for finding tempfile leaks',
    long_description='\n\n'.join([README, CHANGES]),
    platforms=['Unix', 'Windows'],
    keywords='nose tempfile leak',
    url='http://pypi.python.org/pypi/drippy/',
    author='Tres Seaver, Agendaless Consulting',
    author_email='tseaver@agendaless.com',
    license='Python',
    classifiers=[
      'Intended Audience :: Developers',
      'License :: OSI Approved :: Python Software Foundation License',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2',
      'Topic :: Software Development :: Testing',
    ],
    entry_points = {
        'nose.plugins': [
            'hack = drippy:Drippy',
        ]
    },
)
