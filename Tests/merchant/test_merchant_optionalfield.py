import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.merchant.add_merchant_optionalfieldonly import AddMerchantOptionalFieldOnly  # Correct import

@allure.epic("Merchant Functionality")
@allure.feature("Add Merchant Required Field Validations")
@pytest.mark.usefixtures("init_driver")
class TestAddMerchantValidation:

    def test_required_field_validations(self):
        driver = self.driver

        with allure.step("Login with valid credentials"):
            driver.get("https://ipn-tms-staging.koilifin.com")
            driver.find_element(By.NAME, "username").send_keys("admin1")
            driver.find_element(By.NAME, "password").send_keys("@dmin2929A")
            driver.find_element(By.ID,"submit-button").click()

            # Wait for URL to confirm dashboard load
            WebDriverWait(driver, 10).until(
                EC.url_contains("dashboard")
            )
            assert "dashboard" in driver.current_url, "Login failed with valid credentials"

        # Create an instance of the AddMerchantOptionalFieldOnly class
        merchant = AddMerchantOptionalFieldOnly(driver)

        with allure.step("Navigate to Add Merchant and fill optional fields"):
            merchant.go_to_add_merchant()
            merchant.fill_optional_fields({
                "name": "Auto Test Merchant",
                "email": "merchant@test.com",
                "address": "Test City",
                "phone": "9800000000"
            })
            merchant.submit_form()

        with allure.step("Check if required field errors are shown"):
            assert merchant.is_validation_error_present(), "Required field validation messages NOT shown!"
