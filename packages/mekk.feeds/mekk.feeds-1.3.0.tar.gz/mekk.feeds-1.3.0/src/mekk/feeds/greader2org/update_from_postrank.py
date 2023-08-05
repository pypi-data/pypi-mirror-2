#!/usr/bin/python
# -*- coding: utf-8 -*-

from mekk.feeds.orgfile import Folder, Feed
from collections import defaultdict
from base_command import BaseCommand
from helpers import true_categories
import logging

log = logging.getLogger("greader2org")

class UpdateFromPostrank(BaseCommand):
    """
    Uzupełnia plik feeds.org na bazie wpisów Postrank
    """

    def execute(self):
        if not self.org.exists():
            raise Exception("%s does not exist. Use\n  greader2org init\nto create initial version" % self.org.file_name)

        try:
            self.grab_postranks()
        finally:
            self.org.save_to()

    def grab_postranks(self):
        not_found = []
        for folder in self.org.folders:
            for feed in folder.feeds:
                if feed.postrank_feed:
                    continue
                if ('disabled' in feed.tags) or ('private' in feed.tags):
                    continue
                if feed.feed:
                    print "Checking postrank URL for %s" % feed.title
                    try:
                        info = self.postrank.feed_info(feed.feed)
                    except Exception, e:
                        print "... failure (%s)" % str(e)
                        continue
                    if info:
                        id = info.get('id')
                    else:
                        id = None
                    if id:
                        print "... found (adding)"
                        #http://feeds.postrank.com/bbb2cce1a12c1995b6b74f87c620d282?level=good
                        feed.postrank_feed = "http://feeds.postrank.com/%s" % id
                    else:
                        print "... not found"
                        not_found.append(feed.feed)
        
        self.org.save_to()

        if not_found:
            print
            print "The following feeds are missing:"
            print
            for f in not_found:
                print f
            print
            print "To ensure PostRank monitors them, login to http://postrank.com"
            print "visit MyFeeds, click Import, select Direct Input and paste there"
            print "the list of URLs printed above"
