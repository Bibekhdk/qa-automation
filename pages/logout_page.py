import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.profile_icon = (By.ID, "demo-positioned-button")
        self.logout_option = (By.XPATH, "//li[contains(text(), 'Logout')]")
        self.confirm_button = (By.XPATH, "//button[normalize-space()='Logout']")
        self.cancel_button = (By.XPATH, "//button[normalize-space()='Cancel']")
        self.toast_message = (By.CLASS_NAME, "Toastify__toast-body")

    @allure.step("Click profile icon")
    def click_profile_icon(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.profile_icon)
        ).click()

    @allure.step("Click logout option")
    def click_logout_option(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.logout_option)
        ).click()

    @allure.step("Click cancel logout button")
    def click_cancel_logout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cancel_button)
        ).click()

    @allure.step("Click confirm logout button")
    def click_confirm_logout(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.confirm_button)
        ).click()

    @allure.step("Get logout toast message")
    def get_toast_message(self):
        try:
            toast = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.toast_message)
            )
            return toast.text.strip()
        except:
            return None
