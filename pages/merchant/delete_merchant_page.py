import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from datetime import datetime

class DeleteMerchantPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Search for merchant by account number: {account_number}")
    def search_merchant_by_account(self, account_number):
        try:
            # Locate the search input and clear it before entering the new account number
            search_input = self.wait.until(EC.visibility_of_element_located((By.ID, "merchant-search-textfield")))
            search_input.clear()  # Clear any existing text
            search_input.send_keys(account_number)  # Enter the new account number
        except (ElementNotInteractableException, TimeoutException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error Searching Merchant", attachment_type=allure.attachment_type.PNG)
            raise e

    @allure.step("Click more options for merchant")
    def click_more_options(self):
        try:
            more_icon = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='MoreHorizIcon']")))
            more_icon.click()
        except (ElementNotInteractableException, TimeoutException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error Clicking More Options", attachment_type=allure.attachment_type.PNG)
            raise e

    @allure.step("Click Delete option for merchant")
    def click_delete_option(self):
        try:
            delete_li = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[title='Delete']")))
            delete_li.click()
        except (ElementNotInteractableException, TimeoutException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error Clicking Delete Option", attachment_type=allure.attachment_type.PNG)
            raise e

    @allure.step("Confirm deletion of merchant")
    def confirm_delete(self):
        try:
            confirm_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']")))
            confirm_btn.click()
        except (ElementNotInteractableException, TimeoutException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error Confirming Delete", attachment_type=allure.attachment_type.PNG)
            raise e

    @allure.step("Capture screenshot after deletion")
    def capture_screenshot_after_deletion(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshot_after_deletion_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, name="Screenshot after Deletion", attachment_type=allure.attachment_type.PNG)

    @allure.step("Get toast message after deletion")
    def get_toast_message(self):
        try:
            toast = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast-body")))
            return toast.text
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error Fetching Toast Message", attachment_type=allure.attachment_type.PNG)
            raise

    @allure.step("Search for merchant again to verify not found")
    def search_merchant_again(self, account_number):
        try:
            # Clear the search bar before attempting the second search
            search_input = self.wait.until(EC.visibility_of_element_located((By.ID, "merchant-search-textfield")))
            search_input.clear()  # Clear any existing text in the search bar

            # After clearing, enter the account number again to validate deletion
            search_input.send_keys(account_number)  # Enter the account number to search for the deleted merchant

            # Save a screenshot after attempting the second search
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_after_search_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Screenshot after search", attachment_type=allure.attachment_type.PNG)
        except TimeoutException as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="Error Searching Merchant After Deletion", attachment_type=allure.attachment_type.PNG)
            raise e
