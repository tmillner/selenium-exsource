from selenium import webdriver
from logger import log


class Driver(object):
    """Wrapper for common webdriver operations.
    Uses Firefox by default
    """
    CONTEXT = {}
    DRIVER = None

    def __init__(self):
        if Driver.DRIVER is None:
            self.driver = webdriver.Firefox()
            Driver.DRIVER = self.driver
            log.debug("Driver started with context: " + str(Driver.CONTEXT))
        else:
            self.driver = Driver.DRIVER

    def jump_to(self, relativePath=""):
        domain = Driver.CONTEXT.get("domain")
        port = Driver.CONTEXT.get("port")
        url = str.format("{}:{}/{}", domain, port, relativePath)
        self.get(url)

    def get(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()
