import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pages.login_page import LoginPage
from pages.dashboard.auditor_dashboard_page import AuditorDashboardPage

@pytest.fixture
def driver():
    service = Service('/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.title("TC_014: Auditor Dashboard Access Verification")
@allure.description("""
Verify that an Auditor user can:
1. Log in successfully.
2. Access only the allowed dashboard menus:
   - Branch
   - User
   - Scheme
   - Partner
   - Merchant
   - IPN
   - Audit Log
   - Profile
   - Logout
""")
def test_auditor_dashboard(driver):
    login_page = LoginPage(driver)
    auditor_dashboard = AuditorDashboardPage(driver)

    with allure.step("Step 1: Open login page and login with auditor credentials"):
        login_page.load()
        login_page.login("admin12", "@@min2929A")  # Replace with valid auditor credentials

    with allure.step("Step 2: Verify access to auditor-specific dashboard menus"):
        auditor_dashboard.verify_auditor_menus()

    allure.attach(driver.get_screenshot_as_png(), name="AuditorDashboardFinalState", attachment_type=allure.attachment_type.PNG)
