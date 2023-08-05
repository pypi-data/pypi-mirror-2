# -*- coding: utf-8 -*-

import urllib, urllib2
import re
import simplejson
import time

import logging
log = logging.getLogger("postrank")

POSTRANK = 'http://api.postrank.com/v1/'

class PostRankClient(object):
    """
    PostRank (http://www.postrank.com) access client.

    At the moment only one function is implemented.
    """

    def __init__(self, appkey):
        """
        appkey - symbolic application identifier, for example domain name
        """
        self.appkey = appkey

    def feed_info(self, feed_url):
        """
        Returns PostRank information about given feed.

        Returns either dictionary with feed details, or None (that means
        that feed info is not currently available but may appear in the future.

        In case dictionary is returned, it consists of the following fields:
        - title  (blog/site/feed title)
        - description (subtitle)
        - link (blog - not feed - URL)
        - xml (feed URL)
        - id (some internal identifier)
        - tags (list of dictionaries, every dictionary consists of fields count and name)
        - topics (?),
        - ttl (?)

        Note those fields may change if PostRank API changes.
        """

        query = {
            'appkey' : self.appkey,
            'format' : 'json',
            'id' : feed_url,
            }
        enc_query = urllib.urlencode(query)

        url = "http://api.postrank.com/v2/feed/info?" + enc_query

        request = urllib2.Request(url.encode('utf-8'))

        log.info("Calling: %s" % request.get_full_url())
        try:
            f = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            if e.code == 202:
                log.info("HTTP:202 (accepted) - feed accepted for processing")
                return None
            else:
                raise
        result = f.read()
        log.debug("Result: %s" % result)

        return simplejson.loads(result)

