import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://ipn-tms-staging.koilifin.com/auth"

        # Locators
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.signin_button = (By.ID, "submit-button")
        self.toast_message = (By.CLASS_NAME, "Toastify__toast-body")
        self.inline_user_error = (By.ID, "username-helper-text")
        self.inline_pass_error = (By.XPATH, "//span[text()='Password is required']")

    @allure.step("Load login page")
    def load(self):
        if self.driver.current_url != self.url:
            self.driver.get(self.url)
        else:
            self.driver.refresh()

    @allure.step("Login with username: {1}, password: {2}")
    def login(self, username, password):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.username_input)).clear()
        self.driver.find_element(*self.username_input).send_keys(username)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.password_input)).clear()
        self.driver.find_element(*self.password_input).send_keys(password)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.signin_button)).click()

    @allure.step("Get toast message if exists")
    def get_toast_message(self):
        try:
            toast = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.toast_message)
            )
            return toast.get_attribute("innerText") or toast.get_attribute("textContent")
        except:
            return None

    @allure.step("Check for inline error messages")
    def get_inline_errors(self):
        errors = {}
        try:
            user_error = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(self.inline_user_error)
            )
            errors["username"] = user_error.text
        except:
            pass

        try:
            pass_error = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(self.inline_pass_error)
            )
            errors["password"] = pass_error.text
        except:
            pass

        return errors

    @allure.step("Check if login is successful")
    def is_login_successful(self):
        return self.driver.current_url == "https://ipn-tms-staging.koilifin.com/dashboard"
