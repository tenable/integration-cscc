from setuptools import setup, find_packages
import os

long_description = '''
Tenable -> Google Cloud Security Command Center Bridge
For usage documentation, please refer to the github repository at
https://github.com/tenable/integrations-cscc
'''

setup(
    name='tenable-cscc',
    version='1.0.2',
    description='',
    author='Tenable, Inc.',
    long_description=long_description,
    author_email='smcgrath@tenable.com',
    url='https://github.com/tenable/integrations-cscc',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking',
        'Topic :: Other/Nonlisted Topic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tenable tenable_io securitycenter containersecurity',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pytenable>=0.3.15',
        'arrow>=0.13.0',
        'google-auth>=1.6.3',
        'Click>=7.0'
    ],
    entry_points={
        'console_scripts': [
            'tenable-cscc=tenable_cscc.cli:cli',
        ],
    },
)