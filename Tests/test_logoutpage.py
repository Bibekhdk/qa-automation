import pytest
import allure
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("IPN App")
@allure.feature("Logout Functionality")
@pytest.mark.usefixtures("init_driver")
class TestLogout:

    @allure.title("TS_001_01: Cancel logout then confirm logout")
    @allure.description("Login → Cancel Logout → Confirm Logout → Verify redirect and toast.")
    def test_logout_cancel_then_confirm(self, init_driver):
        driver = init_driver
        login = LoginPage(driver)
        logout = LogoutPage(driver)

        with allure.step("Step 1: Login with valid credentials"):
            login.load()
            login.login("bibek1", "@dmin2929A")
            WebDriverWait(driver, 10).until(
                EC.url_to_be("https://ipn-tms-staging.koilifin.com/dashboard")
            )
            assert login.is_login_successful(), "Login not successful"
            allure.attach(driver.get_screenshot_as_png(), name="Logged In", attachment_type=allure.attachment_type.PNG)

        with allure.step("Step 2: Cancel logout"):
            logout.click_profile_icon()
            logout.click_logout_option()
            logout.click_cancel_logout()
            WebDriverWait(driver, 5).until(
                EC.url_to_be("https://ipn-tms-staging.koilifin.com/dashboard")
            )
            assert driver.current_url.endswith("/dashboard"), "User should stay on dashboard after cancel"
            allure.attach(driver.get_screenshot_as_png(), name="After Cancel Logout", attachment_type=allure.attachment_type.PNG)

        with allure.step("Step 3: Logout and confirm"):
            logout.click_profile_icon()
            logout.click_logout_option()
            logout.click_confirm_logout()

        with allure.step("Step 4: Verify logout toast and redirect"):
            WebDriverWait(driver, 10).until(
                EC.url_to_be("https://ipn-tms-staging.koilifin.com/auth")
            )
            toast_msg = logout.get_toast_message()
            allure.attach(driver.get_screenshot_as_png(), name="After Logout", attachment_type=allure.attachment_type.PNG)

            assert toast_msg is not None and "logged out" in toast_msg.lower(), f"Expected logout toast, got: {toast_msg}"
            assert driver.current_url.endswith("/auth"), "User was not redirected to login page after logout"
