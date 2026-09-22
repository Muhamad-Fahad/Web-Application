"""
Automated tests for the Terminal Access Login Page (index.html).
Covers layout verification, field validations, demo autofill, and authentication redirect.
"""

import time
import pytest
from pages.login_page import LoginPage


class TestLogin:

    def test_login_page_renders_elements(self, driver, base_url):
        """Verify presence of core header, inputs, and action buttons."""
        login_page = LoginPage(driver)
        login_page.open(base_url)

        assert "CyberTech" in driver.title
        assert login_page.get_heading_text() == "TERMINAL ACCESS"
        assert login_page.is_displayed(LoginPage.EMAIL_INPUT)
        assert login_page.is_displayed(LoginPage.PASSWORD_INPUT)
        assert login_page.is_displayed(LoginPage.SUBMIT_BTN)
        assert login_page.is_displayed(LoginPage.DEMO_BTN)

    def test_login_empty_fields_validation(self, driver, base_url):
        """Verify empty fields trigger validation alerts and prevent navigation."""
        login_page = LoginPage(driver)
        login_page.open(base_url)

        # Submit without entering data
        login_page.click_submit()

        assert login_page.is_alert_visible(), "Alert banner should be displayed on empty submission"
        assert "cannot be empty" in login_page.get_email_error_text().lower()
        assert "index.html" in driver.current_url

    def test_login_invalid_email_format(self, driver, base_url):
        """Verify that invalid email syntax triggers validation error."""
        login_page = LoginPage(driver)
        login_page.open(base_url)

        login_page.enter_email("notanemail")
        login_page.enter_password("CyberOps#2026")
        login_page.click_submit()

        assert login_page.is_alert_visible()
        assert "invalid email" in login_page.get_email_error_text().lower()
        assert "index.html" in driver.current_url

    def test_login_short_password_validation(self, driver, base_url):
        """Verify password less than 8 characters triggers length error."""
        login_page = LoginPage(driver)
        login_page.open(base_url)

        login_page.enter_email("operative@cybertech.net")
        login_page.enter_password("short")
        login_page.click_submit()

        assert login_page.is_alert_visible()
        assert "at least 8 characters" in login_page.get_password_error_text().lower()
        assert "index.html" in driver.current_url

    def test_demo_credentials_autofill(self, driver, base_url):
        """Verify demo button automatically populates valid credentials."""
        login_page = LoginPage(driver)
        login_page.open(base_url)

        login_page.click_demo_fill()

        email_val = login_page.get_email_value()
        pass_val = login_page.get_password_value()

        assert email_val == "alex.vance@cybertech.net"
        assert pass_val == "CyberOps#2026"

    def test_successful_login_and_redirect(self, driver, base_url):
        """Verify valid login triggers authorization and navigates to dashboard."""
        login_page = LoginPage(driver)
        login_page.open(base_url)

        login_page.click_demo_fill()
        login_page.click_submit()

        # Wait for redirect to dashboard
        assert login_page.wait_for_redirect_to_dashboard(timeout=10)
        assert "dashboard.html" in driver.current_url
