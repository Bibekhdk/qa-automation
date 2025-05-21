import allure
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class EditMerchantPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Clicking 'More Options' for merchant")
    def click_more_options(self):
        more_button = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-testid='MoreHorizIcon']")))
        more_button.click()

    @allure.step("Clicking 'Edit' option from dropdown")
    def click_edit_option(self):
        edit_option = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "li[title='Edit']")))
        edit_option.click()

    @allure.step("Generate a random email address")
    def generate_random_email(self):
        # Generate a random email address
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        email = f"{prefix}@test.com"
        
        # Attach generated email to Allure report
        allure.attach(email, name="Generated Email", attachment_type=allure.attachment_type.TEXT)
        
        return email

    @allure.step("Updating email to: {1}")
    def update_email(self, new_email):
        # Find the email field and update its value
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.click()
        email_field.send_keys(Keys.CONTROL + "a")  # Select all text
        email_field.send_keys(Keys.DELETE)  # Delete selected text
        email_field.send_keys(new_email)  # Enter the new email

    @allure.step("Clicking 'Update' button")
    def click_update_button(self):
        # Find and click the 'Update' button
        update_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Update']")))
        update_button.click()

    @allure.step("Capturing screenshot after update")
    def capture_screenshot_after_update(self):
        # Capture screenshot as bytes and attach to Allure report
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name="After Update Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.step("Get toast message after update")
    def get_toast_message(self):
        try:
            # Wait for the toast message to be visible
            toast = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Toastify__toast-body")))
            toast_text = toast.text
            print(f"Toast message: {toast_text}")  # Print the toast message
            return toast_text
        except TimeoutException:
            raise AssertionError("Toast message did not appear within timeout.")
