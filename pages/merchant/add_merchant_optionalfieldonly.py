import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AddMerchantOptionalFieldOnly:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Navigate to Add Merchant page")
    def go_to_add_merchant(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Merchant')]"))).click()
        add_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add Merchant']")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        add_button.click()

    @allure.step("Fill optional merchant form fields")
    def fill_optional_fields(self, data):
        time.sleep(2)
        self.wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(data["name"])
        self.wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(data["email"])
        self.wait.until(EC.presence_of_element_located((By.ID, "address"))).send_keys(data["address"])
        self.wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(data["phone"])
        time.sleep(1)

    @allure.step("Submit merchant form")
    def submit_form(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_btn.click()
        time.sleep(2)

    @allure.step("Check for required field validation messages")
    def is_validation_error_present(self):
        try:
            account_error = self.driver.find_element(By.ID, "account_number-helper-text")
            branch_error = self.driver.find_element(By.ID, "branch-helper-text")
            scheme_error = self.driver.find_element(By.ID, "scheme-select-box-helper-text")

            if (account_error.is_displayed() and 
                branch_error.is_displayed() and 
                scheme_error.is_displayed()):
                allure.attach(self.driver.get_screenshot_as_png(), name="Validation Errors",
                              attachment_type=allure.attachment_type.PNG)
                return True
        except Exception as e:
            print(f"Error validation not found: {e}")
        return False
