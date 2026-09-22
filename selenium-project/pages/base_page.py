"""
Base Page Object providing core WebDriver interaction helpers,
explicit waits, and defensive element handling.
"""

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator, timeout=None):
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator, timeout=None):
        t = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def click(self, locator, timeout=None):
        t = timeout if timeout is not None else self.timeout
        element = WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def enter_text(self, locator, text, clear_first=True, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        if clear_first:
            element.clear()
        if str(text) != "":
            element.send_keys(str(text))
        else:
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true })); "
                "arguments[0].dispatchEvent(new Event('change', { bubbles: true }));",
                element
            )
        return element

    def get_text(self, locator, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        text = element.text.strip()
        if not text and element.is_displayed():
            text = (element.get_attribute("textContent") or "").strip()
        return text

    def get_attribute(self, locator, attr_name, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        return element.get_attribute(attr_name)

    def is_displayed(self, locator, timeout=4):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def select_dropdown_by_text(self, locator, visible_text, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        select = Select(element)
        select.select_by_visible_text(visible_text)

    def select_dropdown_by_value(self, locator, value, timeout=None):
        element = self.find_element(locator, timeout=timeout)
        select = Select(element)
        select.select_by_value(value)

    def wait_for_url_contains(self, fragment, timeout=None):
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.url_contains(fragment)
        )

    def scroll_into_view(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        return element

    def get_current_url(self):
        return self.driver.current_url
