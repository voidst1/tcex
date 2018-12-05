#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module to test batch indicator creation using interface 2"""


def address_create(batch_job):
    """Test address creation"""
    address = batch_job.indicator('Address', '123.124.125.126', '5.0', '100')
    address.attribute('Description', 'Example Description', True)
    address.tag('Example Tag')
    address.security_label('TLP Green')


def email_address_create(batch_job):
    """Test email address creation"""
    email_address = batch_job.indicator('EmailAddress', 'bad@dfadsfaddsfa.com', '5.0', '100')
    email_address.attribute('Description', 'Example Description', True)
    email_address.tag('Example Tag')
    email_address.security_label('TLP Green')


def file_create(batch_job):
    """Test file creation"""
    file = batch_job.indicator(
        'File', '{} : {} : {}'.format('a' * 32, 'b' * 40, 'c' * 64), '5.0', '100'
    )
    file.attribute('Description', 'Example Description', True)
    file.tag('Example Tag')
    file.security_label('TLP Green')


def host_create(batch_job):
    """Test host creation"""
    host = batch_job.indicator('Host', 'dfadsfaddsfa.com', '5.0', '100')
    host.attribute('Description', 'Example Description', True)
    host.tag('Example Tag')
    host.security_label('TLP Green')


def url_create(batch_job):
    """Test url creation"""
    url = batch_job.indicator('Url', 'https://dfadsfaddsfa.com/index.html', '5.0', '100')
    url.attribute('Description', 'Example Description', True)
    url.tag('Example Tag')
    url.security_label('TLP Green')