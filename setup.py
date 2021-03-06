#!/usr/bin/env python3

from setuptools import setup

setup(
    name='kandoman',
    version='0.1',
    description='UI for todoman in form of kanban board.',
    author='Josip Janzic',
    author_email='me@josip.dev',
    url='https://github.com/janza/kandoman',
    license='MIT',
    packages=['kandoman'],
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'todoman'
    ],
    entry_points={
        'console_scripts': [
            'kandoman = kandoman.kandoman:kandoman',
        ],
    },
)
