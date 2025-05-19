import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pages.login_page import LoginPage
from pages.dashboard.checker_dashboard_page import CheckerDashboardPage

@pytest.fixture
def driver():
    service = Service('/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.title("TC_012: Checker Dashboard Access Verification")
@allure.description("""
Verify that a Checker user can:
1. Log in successfully.
2. Access only the allowed dashboard menus:
   - Approval
   - Merchant
   - IPN
   - Profile
   - Logout
""")
def test_checker_dashboard(driver):
    login_page = LoginPage(driver)
    checker_dashboard = CheckerDashboardPage(driver)

    with allure.step("Step 1: Open login page and login with checker credentials"):
        login_page.load()
        login_page.login("ashu11", "@dmin2929A")  # Update with actual checker credentials if different

    with allure.step("Step 2: Verify access to specific dashboard menus"):
        checker_dashboard.verify_checker_menus()

    allure.attach(driver.get_screenshot_as_png(), name="CheckerDashboardFinalState", attachment_type=allure.attachment_type.PNG)
