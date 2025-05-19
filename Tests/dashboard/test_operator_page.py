import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pages.login_page import LoginPage
from pages.dashboard.operator_dashboard_page import OperatorDashboardPage

@pytest.fixture
def driver():
    service = Service('/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.title("TC_013: Operator Dashboard Access Verification")
@allure.description("""
Verify that an Operator user can:
1. Log in successfully.
2. Access only the allowed dashboard menus:
   - Operation
   - Merchant
   - IPN
   - Profile
   - Logout
""")
def test_operator_dashboard(driver):
    login_page = LoginPage(driver)
    operator_dashboard = OperatorDashboardPage(driver)

    with allure.step("Step 1: Open login page and login with operator credentials"):
        login_page.load()
        login_page.login("bibek10", "@dmin2929A")  # Replace with valid operator credentials

    with allure.step("Step 2: Verify access to operator-specific dashboard menus"):
        operator_dashboard.verify_operator_menus()

    allure.attach(driver.get_screenshot_as_png(), name="OperatorDashboardFinalState", attachment_type=allure.attachment_type.PNG)
