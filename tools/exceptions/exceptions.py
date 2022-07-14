from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    ElementClickInterceptedException,
    )


class TimeoutException(TimeoutException):
    pass

class WebDriverException(WebDriverException):
    pass

class EmailOuLoginIncorretoElawException(Exception):
    pass

class ElementClickInterceptedException(ElementClickInterceptedException):
    pass

