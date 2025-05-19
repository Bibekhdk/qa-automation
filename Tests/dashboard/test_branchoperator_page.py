import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pages.login_page import LoginPage
from pages.dashboard.branchoperator_dashboard_page import BranchOperatorDashboardPage

@pytest.fixture
def driver():
    service = Service('/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.title("TC_015: Branch Operator Dashboard Access Verification")
@allure.description("""
Verify that a Branch Operator user can:
1. Log in successfully.
2. Access only the allowed dashboard menus:
   - Operation
   - Merchant
   - IPN
   - Profile
   - Logout
""")
def test_branch_operator_dashboard(driver):
    login_page = LoginPage(driver)
    dashboard = BranchOperatorDashboardPage(driver)

    with allure.step("Step 1: Open login page and login with branch operator credentials"):
        login_page.load()
        login_page.login("admin99", "min@2121A")  # Replace with real credentials

    with allure.step("Step 2: Verify access to branch operator-specific dashboard menus"):
        dashboard.verify_branch_operator_menus()

    allure.attach(driver.get_screenshot_as_png(), name="BranchOperatorDashboard", attachment_type=allure.attachment_type.PNG)
