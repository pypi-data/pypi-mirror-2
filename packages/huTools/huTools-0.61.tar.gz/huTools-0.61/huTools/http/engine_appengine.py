#!/usr/bin/env python
# encoding: utf-8
"""
engine_appengine.py implements urlfetch based queries for huTools.http.

See http://code.google.com/appengine/docs/python/urlfetch/overview.html for the basics of the
AppEngine capabilities.

Created by Maximillian Dornseif on 2010-10-24.
Copyright (c) 2010 HUDORA. All rights reserved.
"""


from google.appengine.api import urlfetch
import logging


def request(url, method, content, headers, timeout=25):
    """Does a HTTP Request via Google Appengine urlfetch Service.

    Incereases the default appengine timeout from 5 seconds to 25.
    (For Web-Requests this is reduced to 10s by the GAE Infrastructure)"""

    # on appengine debuging is always post mortem, so better log what we arde doing
    logging.debug('fetching %s %s', method, url)
    if method == 'GET':
        method = urlfetch.GET
    elif method == 'POST':
        method = urlfetch.POST
    elif method == 'DELETE':
        method = urlfetch.DELETE
    elif method == 'PUT':
        method = urlfetch.PUT
    elif method == 'HEAD':
        method = urlfetch.HEAD
    headers['User-Agent'] = headers.get('User-Agent', '') + ' (urlfetch)'
    result = urlfetch.fetch(url=url, deadline=timeout, payload=content, method=method, headers=headers)
    return int(result.status_code), result.headers, result.content
