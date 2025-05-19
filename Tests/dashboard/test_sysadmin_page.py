import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from pages.login_page import LoginPage
from pages.dashboard.systemadmin_dashboard_page import SystemAdminDashboardPage

@pytest.fixture
def driver():
    service = Service('/snap/bin/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@allure.title("TC_011: System Admin Dashboard Access Verification")
@allure.description("""
Verify that a System Admin user can:
1. Log in successfully.
2. Access all expected dashboard menus.
""")
def test_system_admin_dashboard(driver):
    login_page = LoginPage(driver)
    dashboard = SystemAdminDashboardPage(driver)

    with allure.step("Step 1: Open login page and login with admin credentials"):
        login_page.load()
        login_page.login("testuser1", "@dmin2929A")

    with allure.step("Step 2: Verify access to all dashboard menus"):
        dashboard.verify_all_admin_menus()

    allure.attach(driver.get_screenshot_as_png(), name="Final State", attachment_type=allure.attachment_type.PNG)
