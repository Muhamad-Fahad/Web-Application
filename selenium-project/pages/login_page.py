"""
Page Object Model for the Terminal Access Login Page (index.html).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.ID, "loginEmail")
    PASSWORD_INPUT = (By.ID, "loginPassword")
    SUBMIT_BTN = (By.ID, "btnLoginSubmit")
    DEMO_BTN = (By.ID, "btnDemoLogin")
    ALERT_BANNER = (By.ID, "loginAlert")
    ALERT_TEXT = (By.ID, "loginAlertText")
    EMAIL_ERROR = (By.ID, "error-loginEmail")
    PASSWORD_ERROR = (By.ID, "error-loginPassword")
    PAGE_HEADING = (By.CSS_SELECTOR, ".auth-title")
    BRAND_BADGE = (By.CSS_SELECTOR, ".cyber-badge")
    TOAST = (By.CSS_SELECTOR, ".toast")

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def open(self, base_url):
        url = f"{base_url.rstrip('/')}/index.html"
        self.driver.get(url)
        return self

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)
        return self

    def click_submit(self):
        self.click(self.SUBMIT_BTN)
        return self

    def click_demo_fill(self):
        self.click(self.DEMO_BTN)
        return self

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        return self

    def get_email_value(self):
        return self.get_attribute(self.EMAIL_INPUT, "value")

    def get_password_value(self):
        return self.get_attribute(self.PASSWORD_INPUT, "value")

    def get_heading_text(self):
        return self.get_text(self.PAGE_HEADING)

    def get_alert_banner_text(self):
        if self.is_displayed(self.ALERT_BANNER):
            return self.get_text(self.ALERT_TEXT)
        return ""

    def get_email_error_text(self):
        return self.get_text(self.EMAIL_ERROR)

    def get_password_error_text(self):
        return self.get_text(self.PASSWORD_ERROR)

    def is_alert_visible(self):
        return self.is_displayed(self.ALERT_BANNER)

    def is_toast_visible(self):
        return self.is_displayed(self.TOAST)

    def wait_for_redirect_to_dashboard(self, timeout=10):
        return self.wait_for_url_contains("dashboard.html", timeout=timeout)
