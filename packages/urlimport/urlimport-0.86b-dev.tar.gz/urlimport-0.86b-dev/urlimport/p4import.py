# -*- coding: utf-8 -*-

"""enables to import modules from perforce, by adding p4:// urls to the python 
   path.
"""
#authors: Jure Vrscaj <jure@codeshift.net> (copyright (c) 2006-10),
#         송영진(MyEvan) <myevan_net@naver.com> (copyright (c) 2010), 
#         Alex Bodnaru <alexbodn@012.net.il> (copyright (c) 2010)

# This is free software; you may use, copy, modify and/or distribute this work
# under the terms of the MIT License.


from urlimport import UrlFinder, debug
import sys, re
from P4 import P4
from datetime import datetime

class PerforceFinder(UrlFinder):

    re_url_ok = re.compile(r'^p4://')

    connection_cache = dict()

    def get_file_data(self, url, cached_last_modified, cached_etag):
        """Download the file data from given url.
        """
        p4conn = self.connection_cache.get(self.path, None)
        if p4conn is None:
            p4conn = P4()
            p4conn.connect()
            self.connection_cache[self.path] = p4conn
            debug("p4 connect", lvl=1)

        fstats = p4conn.run_fstat(url[3:])
        for fstat in fstats:
            last_modified = datetime.fromtimestamp(int(fstat["headModTime"]))
            keep_cached = last_modified <= self.parse_date(cached_last_modified) \
                if cached_last_modified else False
            last_modified = last_modified.strftime(self.date_format)
            if not keep_cached:
                try:
                    fileData = open(fstat["clientFile"]).read()
                except IOError:
                    p4conn.run_sync(url[3:])
                    fileData = open(fstat["clientFile"]).read()
            else:
                fileData = None

            return fileData, \
                   None,\
                   last_modified,\
                   keep_cached,\
                   None, \
                   url

    def split_url(self, url):
        return ("",) * 8


# register The Hook
sys.path_hooks = \
    [x for x in sys.path_hooks if x.__name__ != 'PerforceFinder'] + [PerforceFinder]

