#!/usr/bin/env python
# encoding: utf-8
"""
pypostal/sipgate.py - fax a PDF via the sipgate API

See http://www.live.sipgate.de/api/rest for further description of the sipgate REST API.

Created by Maximillian Dornseif on 2010-08-14.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


import httplib
import os
import urllib
import urlparse


def add_query(url, params):
    """
    Add GET parameters to a given URL
    
    >>> add_query('/sicrit/', {'passphrase': 'fiftyseveneleven'})
    '/sicrit/?passphrase=fiftyseveneleven'
    """
    
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(url_parts)


def send_fax_sipgate(uploadfiles, source, dest_numbers=[], guid='', username=None, password=None):
    if not username:
        username = os.environ.get('PYPOSTAL_SIPGATE_CRED', ':').split(':', 2)[0]
    if not password:
        password = os.environ.get('PYPOSTAL_SIPGATE_CRED', ':').split(':', 2)[1]
    
    sip = Sipgate(username, password)
    return sip.sendFax(uploadfiles, source, dest_numbers)


def clean_number(number):
    """Try to clean a phonenumber"""
    
    if number.startswith('0'):
        number = '49' + number[1:]
    number = number.replace(' ', '').replace('-', '').replace('+', '')
    return number


class Sipgate(object):
    def __init__(self, username, password):
        self.version = '2.17.0'
        self.username = username
        self.password = password
        
    @property
    def authheader(self):
        auth = '%s:%s' % (self.username, self.password)
        return "Basic %s" % auth.encode('base64').strip()
    
    def sendFax(self, uploadfiles, source, dest_numbers, guid=''):
        if len(uploadfiles) > 1:
            raise ValueError('Sipgate currently only supports single PDF uploading')
        if hasattr(uploadfiles[0], 'name'):
            filedata = uploadfiles[0].read()
        else:
            filedata = uploadfiles[0]
        
        params = {'version': self.version, 'source': 'tel:' + clean_number(source),
                  'targets': ",".join('tel:' + clean_number(dest) for dest in dest_numbers)}
        url = add_query("/my/events/faxes/", params)
        headers = {"Content-Type": "application/pdf", "Authorization": self.authheader}
        
        conn = httplib.HTTPSConnection("api.sipgate.net")
        conn.request("POST", url, headers=headers, body=filedata)
        
        response = conn.getresponse()
        
        # TODO: Error handling
        print response.status, response.reason
        data = response.read()
        print data
        
        conn.close()
        return guid


if __name__ == "__main__":
    import doctest
    doctest.testmod()