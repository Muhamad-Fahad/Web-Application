"""
Pytest configuration and shared fixtures for Selenium test execution.
Includes automatic driver initialization, failure screenshots, and logging.
"""

import os
import sys
import logging
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create required artifact directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

for directory in [SCREENSHOTS_DIR, REPORTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Configure logging
log_file = os.path.join(LOGS_DIR, 'test_execution.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('SeleniumTestRunner')


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://localhost:8080",
        help="Base URL for application under test"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or edge"
    )
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run browser in headless mode: true or false"
    )


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope="function")
def driver(request):
    browser_type = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless").lower() == "true"

    logger.info(f"Initializing WebDriver for browser: {browser_type}, headless: {headless}")

    driver = None
    if browser_type == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
    elif browser_type == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")

    driver.implicitly_wait(3)

    yield driver

    # Teardown
    logger.info("Terminating WebDriver session")
    try:
        driver.quit()
    except Exception as e:
        logger.warning(f"Error during driver quit: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_name = item.name.replace("/", "_").replace("\\", "_")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{sanitized_name}_{timestamp}.png")
            try:
                driver.save_screenshot(screenshot_path)
                logger.error(f"Test failed: {item.name}. Screenshot saved to: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to capture screenshot for {item.name}: {e}")
