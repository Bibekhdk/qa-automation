import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage
from pages.merchant.delete_merchant_page import DeleteMerchantPage
from utils.config import TestData

@pytest.mark.usefixtures("init_driver")
class TestDeleteMerchant:

    def setup_method(self):
        self.wait = WebDriverWait(self.driver, 10)

    @allure.step("Test to delete a merchant and verify deletion")
    def test_delete_merchant(self):
        driver = self.driver

        # Step 1: Login
        driver.get(TestData.BASE_URL)
        login_page = LoginPage(driver)
        login_page.login(TestData.USERNAME, TestData.PASSWORD)

        # Step 2: Navigate to merchant page
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Merchant')]"))).click()

        # Step 3: Wait a bit for merchant list to load
        time.sleep(3)

        # Step 4: Delete merchant
        delete_page = DeleteMerchantPage(driver)
        delete_page.click_more_options()
        delete_page.click_delete_option()
        delete_page.confirm_delete()

        # Step 5: Wait briefly for toast to appear
        time.sleep(2)  # Let UI animation play

        # Step 6: Capture screenshot after deletion
        delete_page.capture_screenshot_after_deletion()

        # Step 7: Verify toast message
        try:
            toast = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Toastify__toast-body"))
            )
            toast_text = toast.text
            print(f"Toast message: {toast_text}")
            assert "deleted successfully" in toast_text.lower(), f"Unexpected toast text: {toast_text}"
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="toast_missing", attachment_type=allure.attachment_type.PNG)
            raise AssertionError("Toast message did not appear within timeout.")
