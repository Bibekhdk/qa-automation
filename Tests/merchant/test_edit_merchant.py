import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.merchant.edit_merchant_page import EditMerchantPage
from utils.config import TestData

@pytest.mark.usefixtures("init_driver")
class TestEditMerchant:

    def setup_method(self):
        self.wait = WebDriverWait(self.driver, 10)

    @allure.title("Test to edit a merchant's email and verify success")
    def test_edit_merchant_email(self):
        driver = self.driver

        # Step 1: Login
        driver.get(TestData.BASE_URL)
        login_page = LoginPage(driver)
        login_page.login(TestData.USERNAME, TestData.PASSWORD)

        # Step 2: Go to merchant page
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Merchant')]"))).click()

        time.sleep(3)  # Allow page to settle

        # Step 3: Edit Flow
        edit_page = EditMerchantPage(driver)
        edit_page.click_more_options()
        edit_page.click_edit_option()

        new_email = edit_page.generate_random_email()
        edit_page.update_email(new_email)
        edit_page.click_update_button()

        time.sleep(3)  # Wait for toast to appear

        # Step 4: Validate toast message
        try:
            toast_message = edit_page.get_toast_message()
            assert "merchant updated successfully" in toast_message.lower(), f"Unexpected toast: {toast_message}"
        except TimeoutException:
            raise AssertionError("Toast message did not appear within timeout.")

        # Step 5: Capture screenshot after the update
        edit_page.capture_screenshot_after_update()
