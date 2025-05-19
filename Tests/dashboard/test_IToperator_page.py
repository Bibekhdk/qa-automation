import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pages.login_page import LoginPage
from pages.dashboard.IToperator_dashboard_page import ITOperatorDashboardPage

@pytest.fixture
def driver():
    service = Service('/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.title("TC_017: IT Operator Dashboard Access Verification")
@allure.description("""
Verify that an IT Operator user can:
1. Log in successfully.
2. Access the following menus:
   - User
   - Audit Log
   - Profile
   - Logout
""")
def test_it_operator_dashboard(driver):
    login_page = LoginPage(driver)
    dashboard = ITOperatorDashboardPage(driver)

    with allure.step("Step 1: Log in as IT Operator"):
        login_page.load()
        login_page.login("itoperator", "@dmin2929A")  # Replace with actual IT operator credentials

    with allure.step("Step 2: Verify IT Operator dashboard menus"):
        dashboard.verify_it_operator_menus()

    allure.attach(driver.get_screenshot_as_png(), name="ITOperatorDashboard", attachment_type=allure.attachment_type.PNG)
