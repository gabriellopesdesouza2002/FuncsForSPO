from selenium.common.exceptions import *

# --- Exceptions Selenium Base ---- #
class TimeoutException(TimeoutException):
    pass


class WebDriverException(WebDriverException):
    pass


class ElementClickInterceptedException(ElementClickInterceptedException):
    pass
# --- Exceptions Selenium Base ---- #


# --- Exceptions Python Base ---- #
class EmailOuLoginIncorretoElawException(Exception):
    pass

class EmailOuLoginIncorretoGmailException(Exception):
    pass
# --- Exceptions Python Base ---- #