"""
Page Object Model for the Command Dashboard & Operative Registration Form (dashboard.html).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    # Metric Stat Locators
    STAT_TOTAL = (By.ID, "statTotalEmployees")
    STAT_DEPTS = (By.ID, "statTotalDepts")
    STAT_CLEARANCE = (By.ID, "statTopClearance")
    STAT_AVG_SALARY = (By.ID, "statAvgSalary")
    USER_EMAIL = (By.ID, "userDisplayEmail")

    # Form Input Locators
    NAME_INPUT = (By.ID, "fullName")
    EMAIL_INPUT = (By.ID, "empEmail")
    ID_INPUT = (By.ID, "empId")
    PASSWORD_INPUT = (By.ID, "empPassword")
    PHONE_INPUT = (By.ID, "empPhone")
    SALARY_INPUT = (By.ID, "empSalary")
    DEPT_SELECT = (By.ID, "empDept")
    CLEARANCE_SELECT = (By.ID, "empClearance")
    COMPLIANCE_CHECKBOX = (By.ID, "complianceCheck")

    # Buttons
    SUBMIT_BTN = (By.ID, "btnSubmitEmployee")
    CLEAR_BTN = (By.ID, "btnClearForm")
    SAMPLE_BTN = (By.ID, "btnSampleEmployee")
    LOGOUT_BTN = (By.ID, "btnLogout")

    # Feedback Locators
    FORM_ALERT = (By.ID, "formAlertBanner")
    FORM_ALERT_TEXT = (By.ID, "formAlertText")
    TOAST = (By.CSS_SELECTOR, ".toast")

    # Table & Search Locators
    SEARCH_INPUT = (By.ID, "searchRecords")
    TABLE_ROWS = (By.CSS_SELECTOR, "#recordsTableBody tr")
    EMPTY_STATE = (By.ID, "tableEmptyState")

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def open(self, base_url):
        url = f"{base_url.rstrip('/')}/dashboard.html"
        self.driver.get(url)
        return self

    def fill_form(self, name=None, email=None, emp_id=None, password=None,
                  phone=None, salary=None, dept=None, clearance=None,
                  work_mode=None, compliance=None):
        if name is not None:
            self.enter_text(self.NAME_INPUT, name)
        if email is not None:
            self.enter_text(self.EMAIL_INPUT, email)
        if emp_id is not None:
            self.enter_text(self.ID_INPUT, emp_id)
        if password is not None:
            self.enter_text(self.PASSWORD_INPUT, password)
        if phone is not None:
            self.enter_text(self.PHONE_INPUT, phone)
        if salary is not None:
            self.enter_text(self.SALARY_INPUT, salary)
        if dept:
            self.select_dropdown_by_value(self.DEPT_SELECT, dept)
        if clearance:
            self.select_dropdown_by_value(self.CLEARANCE_SELECT, clearance)
        if work_mode:
            radio_locator = (By.CSS_SELECTOR, f"input[name='workMode'][value='{work_mode}']")
            self.click(radio_locator)
        if compliance is not None:
            checkbox = self.find_element(self.COMPLIANCE_CHECKBOX)
            if checkbox.is_selected() != compliance:
                self.click(self.COMPLIANCE_CHECKBOX)
        return self

    def click_submit(self):
        self.scroll_into_view(self.SUBMIT_BTN)
        self.click(self.SUBMIT_BTN)
        return self

    def click_clear(self):
        self.scroll_into_view(self.CLEAR_BTN)
        self.click(self.CLEAR_BTN)
        return self

    def click_sample_data(self):
        self.click(self.SAMPLE_BTN)
        return self

    def click_logout(self, accept_alert=True):
        self.click(self.LOGOUT_BTN)
        try:
            alert = self.driver.switch_to.alert
            if accept_alert:
                alert.accept()
            else:
                alert.dismiss()
        except Exception:
            pass
        return self

    def search(self, query):
        self.enter_text(self.SEARCH_INPUT, query)
        return self

    def get_table_rows_count(self):
        return len(self.find_elements(self.TABLE_ROWS, timeout=3))

    def get_field_error_message(self, field_id):
        error_locator = (By.ID, f"error-{field_id}")
        group_locator = (By.ID, f"group-{field_id}")
        try:
            group = self.find_element(group_locator, timeout=1)
            if "has-error" in (group.get_attribute("class") or ""):
                WebDriverWait(self.driver, 2).until(
                    lambda d: d.find_element(*error_locator).is_displayed() or d.find_element(*error_locator).text.strip() != ""
                )
        except Exception:
            pass
        return self.get_text(error_locator)

    def get_form_alert_banner_text(self):
        if self.is_displayed(self.FORM_ALERT):
            return self.get_text(self.FORM_ALERT_TEXT)
        return ""

    def get_stat_total_operatives(self):
        return self.get_text(self.STAT_TOTAL)

    def get_stat_departments_count(self):
        return self.get_text(self.STAT_DEPTS)

    def get_stat_high_clearance_count(self):
        return self.get_text(self.STAT_CLEARANCE)

    def get_stat_avg_salary(self):
        return self.get_text(self.STAT_AVG_SALARY)

    def get_user_display_email(self):
        return self.get_text(self.USER_EMAIL)

    def delete_operative_by_id(self, emp_id, accept_alert=True):
        delete_btn = (By.CSS_SELECTOR, f"button[data-id='{emp_id}']")
        self.click(delete_btn)
        try:
            alert = self.driver.switch_to.alert
            if accept_alert:
                alert.accept()
            else:
                alert.dismiss()
        except Exception:
            pass
        return self
