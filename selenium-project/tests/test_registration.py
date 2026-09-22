"""
Automated tests for the Command Dashboard & Operative Registration Form (dashboard.html).
Covers form validation rules, data-driven registration, table updates, search filter, and logout.
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@pytest.fixture
def authenticated_dashboard(driver, base_url):
    """Fixture that logs in through the Login page to reach the authenticated Dashboard."""
    login_page = LoginPage(driver)
    login_page.open(base_url)
    login_page.click_demo_fill()
    login_page.click_submit()
    login_page.wait_for_redirect_to_dashboard(timeout=10)
    return RegistrationPage(driver)


class TestRegistration:

    def test_dashboard_elements_and_metrics_present(self, authenticated_dashboard):
        """Verify dashboard header, metric cards, and directory roster are loaded."""
        reg_page = authenticated_dashboard

        assert "Command" in reg_page.driver.title or "CyberTech" in reg_page.driver.title
        assert int(reg_page.get_stat_total_operatives()) >= 3
        assert int(reg_page.get_stat_departments_count()) >= 1
        assert reg_page.get_table_rows_count() >= 3

    def test_registration_empty_form_validation(self, authenticated_dashboard):
        """Verify submitting empty form triggers validation alerts on required fields."""
        reg_page = authenticated_dashboard

        reg_page.click_submit()

        alert_text = reg_page.get_form_alert_banner_text()
        assert "validation failed" in alert_text.lower()
        assert "cannot be empty" in reg_page.get_field_error_message("fullName").lower()
        assert "cannot be empty" in reg_page.get_field_error_message("empEmail").lower()

    def test_registration_invalid_email_validation(self, authenticated_dashboard):
        """Verify invalid email syntax triggers validation error."""
        reg_page = authenticated_dashboard

        reg_page.enter_text(RegistrationPage.EMAIL_INPUT, "bad-email-format")
        reg_page.click_submit()

        email_error = reg_page.get_field_error_message("empEmail")
        assert "invalid email format" in email_error.lower()

    def test_registration_numeric_validations(self, authenticated_dashboard):
        """Verify invalid numeric inputs (Phone, ID, Salary) trigger specific error rules."""
        reg_page = authenticated_dashboard

        # Invalid phone (< 10 digits or letters)
        reg_page.enter_text(RegistrationPage.PHONE_INPUT, "12345")
        reg_page.click_submit()
        phone_error = reg_page.get_field_error_message("empPhone")
        assert "invalid numeric input" in phone_error.lower()

        # Invalid salary (less than 20000)
        reg_page.enter_text(RegistrationPage.SALARY_INPUT, "5000")
        reg_page.click_submit()
        salary_error = reg_page.get_field_error_message("empSalary")
        assert "at least 20,000" in salary_error.lower()

    def test_registration_password_length_validation(self, authenticated_dashboard):
        """Verify passcode shorter than 8 characters is rejected."""
        reg_page = authenticated_dashboard

        reg_page.enter_text(RegistrationPage.PASSWORD_INPUT, "12345")
        reg_page.click_submit()

        pass_error = reg_page.get_field_error_message("empPassword")
        assert "minimum 8 characters" in pass_error.lower()

    def test_registration_required_dropdown_validation(self, authenticated_dashboard):
        """Verify leaving required dropdowns unselected triggers error."""
        reg_page = authenticated_dashboard

        # Reset selection to empty prompt
        reg_page.select_dropdown_by_value(RegistrationPage.DEPT_SELECT, "")
        reg_page.click_submit()

        dept_error = reg_page.get_field_error_message("empDept")
        assert "required dropdown selection" in dept_error.lower()

    def test_successful_registration_and_table_update(self, authenticated_dashboard):
        """Verify valid operative registration updates directory roster table and metrics."""
        reg_page = authenticated_dashboard

        initial_count = reg_page.get_table_rows_count()
        initial_stat = int(reg_page.get_stat_total_operatives())

        # Generate unique ID for test run
        unique_id = str(int(time.time()) % 900000 + 100000)
        test_name = f"Agent Omega-{unique_id[-4:]}"

        reg_page.fill_form(
            name=test_name,
            email=f"omega.{unique_id}@cybertech.net",
            emp_id=unique_id,
            password=f"MasterKey#{unique_id}",
            phone="5550198273",
            salary="165000",
            dept="Cybersecurity Operations",
            clearance="Tier 5 - Root Admin",
            work_mode="Hybrid",
            compliance=True
        )

        reg_page.click_submit()
        time.sleep(0.5)

        # Verify table count increment
        new_count = reg_page.get_table_rows_count()
        assert new_count == initial_count + 1

        # Verify stat count increment
        new_stat = int(reg_page.get_stat_total_operatives())
        assert new_stat == initial_stat + 1

        # Verify new record appears in roster
        page_source = reg_page.driver.page_source
        assert test_name in page_source
        assert unique_id in page_source

    def test_search_roster_filter(self, authenticated_dashboard):
        """Verify live search filters the directory table in real time."""
        reg_page = authenticated_dashboard

        # Search for known seed employee 'Elena'
        reg_page.search("Elena")
        time.sleep(0.3)
        assert reg_page.get_table_rows_count() == 1

        # Search for nonexistent operative
        reg_page.search("NonExistentOperativeQueryXYZ")
        time.sleep(0.3)
        assert reg_page.is_displayed(RegistrationPage.EMPTY_STATE)

        # Clear search
        reg_page.enter_text(RegistrationPage.SEARCH_INPUT, "")
        time.sleep(0.3)
        assert reg_page.get_table_rows_count() >= 3

    def test_logout_navigation(self, authenticated_dashboard):
        """Verify clicking disconnect logs out and redirects to index.html."""
        reg_page = authenticated_dashboard

        reg_page.click_logout(accept_alert=True)
        time.sleep(0.5)

        assert "index.html" in reg_page.driver.current_url
