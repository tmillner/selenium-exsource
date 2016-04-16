#!/usr/bin/python


class Page(object):
    """Base Page for inherting by application pages"""

    def __init__(self):
        self.pageInfo = {
                         "path": "relative/path/of/page.html",
                         "meta": {
                                "createsResources": False,
                                "apiCalls": []
                          }
        }
