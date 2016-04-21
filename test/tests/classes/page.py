from driver import Driver


class Page(Driver):
    """Base Page for inherting by application pages"""

    def __init__(self):
        super(Page, self).__init__()
        self.pageInfo = {
                         "path": "relative/path/of/page.html",
                         "meta": {
                                "createsResources": False,
                                "apiCalls": []
                          }
        }
