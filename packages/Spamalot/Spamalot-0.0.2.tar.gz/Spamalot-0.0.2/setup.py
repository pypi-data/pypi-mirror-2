#!/usr/bin/env python

from setuptools import setup

setup(
    name='Spamalot',
    version='0.0.2',
    description='Python simple mailer',
    author='Alberto Granzotto (vrde)',
    author_email='agranzot@gmail.com',
    url='http://hg.tastybra.in/spamalot',

    packages=['spamalot'],

    package_data = {
        'spamalot': ['conf/*']
    },

    install_requires=[
        'ConfigObj',
        'setuptools'
    ]
)

