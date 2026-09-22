# CyberTech Web Application — Selenium Automation Framework

A production-grade test automation suite built with **Python**, **Selenium WebDriver**, and **Pytest** using the **Page Object Model (POM)** architectural pattern.

---

## 📁 Project Structure

```
selenium-project/
│
├── pages/                          # Page Object Model layer
│   ├── __init__.py
│   ├── base_page.py                # Reusable driver actions & explicit waits
│   ├── login_page.py               # Page object for Terminal Login (index.html)
│   └── registration_page.py        # Page object for Dashboard & Registration (dashboard.html)
│
├── tests/                          # Automated test suites
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures, driver management, and failure screenshots
│   ├── test_login.py               # 6 test cases for authentication & login validations
│   └── test_registration.py        # 9 test cases for form validations, roster CRUD, and search
│
├── test_data/
│   └── users.csv                   # CSV datasets for positive and negative scenario testing
│
├── screenshots/                    # Automatically saved screenshots for any failed test runs
├── reports/                        # Generated HTML execution reports
├── logs/                           # Execution logs (logs/test_execution.log)
├── requirements.txt                # Python package dependencies
└── README.md                       # Comprehensive setup and run documentation
```

---

## ⚡ Prerequisites

1. **Python 3.8+** installed (`python --version`)
2. **Google Chrome** or **Microsoft Edge** browser installed
3. **Web Application Server** running on `http://localhost:8080`:
   ```bash
   # In the root Web-Application directory:
   python -m http.server 8080
   ```

---

## 🛠️ Installation & Setup

### 1. Navigate to the project directory:
```bash
cd selenium-project
```

### 2. Create and activate a Python virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Tests

### 1. Run all tests in headless mode (default):
```bash
pytest
```

### 2. Run all tests in visible (headed) browser mode:
```bash
pytest --headless=false
```

### 3. Run a specific test suite:
```bash
# Run Login test suite only
pytest tests/test_login.py -v

# Run Registration & Dashboard test suite only
pytest tests/test_registration.py -v
```

### 4. Run a specific individual test:
```bash
pytest tests/test_login.py::TestLogin::test_demo_credentials_autofill -v
```

### 5. Generate a rich HTML test report:
```bash
pytest --html=reports/report.html --self-contained-html
```
The resulting report will be created inside the `reports/` folder.

### 6. Run on Microsoft Edge instead of Chrome:
```bash
pytest --browser=edge --headless=false
```

### 7. Custom Base URL (if running on a different port or host):
```bash
pytest --base-url=http://localhost:3000
```

---

## 🧪 Test Coverage Breakdown

### `tests/test_login.py`
| Test Case | Objective |
|---|---|
| `test_login_page_renders_elements` | Validates page title, header, inputs, and action buttons. |
| `test_login_empty_fields_validation` | Verifies rejection of empty inputs and display of error alerts. |
| `test_login_invalid_email_format` | Verifies standard corporate email format validation. |
| `test_login_short_password_validation` | Verifies rejection of passcodes under 8 characters. |
| `test_demo_credentials_autofill` | Verifies one-click demo credentials autofill feature. |
| `test_successful_login_and_redirect` | Validates valid login and automatic redirect to `dashboard.html`. |

### `tests/test_registration.py`
| Test Case | Objective |
|---|---|
| `test_dashboard_elements_and_metrics_present` | Validates dashboard header, 4 metric cards, and roster table. |
| `test_registration_empty_form_validation` | Validates rejection when submitting empty required fields. |
| `test_registration_invalid_email_validation` | Validates strict email regex in registration form. |
| `test_registration_numeric_validations` | Verifies numeric rules on ID, Phone line, and Salary. |
| `test_registration_password_length_validation` | Validates 8-character passcode rule. |
| `test_registration_required_dropdown_validation` | Validates mandatory sector department selection. |
| `test_successful_registration_and_table_update` | Enrolls new operative and verifies table insertion & stats increment. |
| `test_search_roster_filter` | Validates live search filtering by name and empty state display. |
| `test_logout_navigation` | Verifies Disconnect button session teardown and return to login. |

---

## 📸 Automated Failure Screenshots

If any test step fails, Pytest automatically captures a full-page browser screenshot and saves it into the `screenshots/` directory with a timestamped filename:
`screenshots/<test_name>_<YYYYMMDD_HHMMSS>.png`

Execution logs are concurrently streamed to `logs/test_execution.log`.
