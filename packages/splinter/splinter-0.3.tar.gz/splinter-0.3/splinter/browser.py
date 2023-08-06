from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.exceptions import DriverNotFoundError

_DRIVERS = {
    'webdriver.firefox': FirefoxWebDriver,
    'webdriver.chrome': ChromeWebDriver
}

try:
    from splinter.driver.zopetestbrowser import ZopeTestBrowser
    _DRIVERS['zope.testbrowser'] = ZopeTestBrowser
except ImportError:
    pass


def Browser(driver_name='webdriver.firefox', profile=None, extensions=[]):
    """
    Returns a driver instance for the given name.

    When working with ``webdriver.firefox``, it's possible to provide a profile name and a
    list of extensions.

    If you don't provide any driver_name, then ``webdriver.firefox`` will be used.

    If there is no driver registered with the provided ``driver_name``, this function
    will raise a :class:`splinter.exceptions.DriverNotFoundError` exception.
    """

    try:
        driver = _DRIVERS[driver_name]
        if driver_name == 'webdriver.firefox':
            return driver(profile, extensions)
        else:
            return driver()
    except KeyError:
        raise DriverNotFoundError("No driver for %s" % driver_name)
