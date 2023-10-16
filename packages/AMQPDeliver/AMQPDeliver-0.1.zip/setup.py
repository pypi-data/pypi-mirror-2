#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 LShift
# All rights reserved.
#

from setuptools import setup, find_packages

setup(
    name = 'AMQPDeliver',
    version = '0.1',
    description = 'Asynchronous file transfer using AMQP',
    long_description = """
    A command line tool which sends AMQP messages whose body is anything
    read on stdin, and a deamon which executes a command for each message,
    which reads the message body on its stdin.

    There are some scripts which sign and encrypt the message using GnuPG,
    so you can use this as a mechanism for secure synchronization between
    two sites, neither of which accept incoming connections, via an
    AMQP server you don't want to trust.
    
    The idea is that you use this with a DCVS such as mercurial, passing
    changesets as messages.
    """,
    author = 'David Ireland',
    author_email = 'david@lshift.net',
    license = 'BSD',
    url = 'http://www.lshift.net/',
    download_url = 'http://www.lshift.net/',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Version Control',
        ],
    
    packages = find_packages(exclude=['*.tests']),

    install_requires = [
        'setuptools>=0.6b1',
        'amqplib>=1.0'
        ],

    entry_points = {
        'console_scripts': [
            'amqp-send = amqpdeliver.send:main',
            'amqp-receive-d = amqpdeliver.receive_d:main',
            'amqp-receive-hg = amqpdeliver.hg:main']
        }
,	zip_safe = False
)
