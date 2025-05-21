from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import allure

class AddMerchantPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        self.toast_message = (By.CLASS_NAME, "Toastify__toast-body")

    @allure.step("Login to application")
    def login(self, url, username, password):
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@id='submit-button']").click()

    @allure.step("Navigate to Add Merchant page")
    def go_to_add_merchant(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Merchant')]"))).click()
        add_button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Add Merchant']")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)
        add_button.click()

    @allure.step("Fill merchant form")
    def fill_merchant_form(self, data):
        self.wait.until(EC.presence_of_element_located((By.ID, "account_number"))).send_keys(data['accountnumber'])
        self.wait.until(EC.presence_of_element_located((By.ID, "pan"))).send_keys(data['merchantpan'])

        branch_input = self.wait.until(EC.element_to_be_clickable((By.ID, "branch")))
        branch_input.click()
        branch_input.send_keys(data['branch'])
        time.sleep(1)
        branch_input.send_keys(Keys.DOWN)
        branch_input.send_keys(Keys.ENTER)

        scheme_input = self.wait.until(EC.element_to_be_clickable((By.ID, "scheme-select-box")))
        scheme_input.click()
        scheme_input.send_keys(data['scheme'])
        time.sleep(1)
        scheme_input.send_keys(Keys.DOWN)
        scheme_input.send_keys(Keys.DOWN)
        scheme_input.send_keys(Keys.ENTER)

        self.wait.until(EC.presence_of_element_located((By.ID, "nchl11_meckhi_ident"))).send_keys(data['nchl'])

        category_input = self.wait.until(EC.element_to_be_clickable((By.ID, "category-code-search")))
        category_input.click()
        time.sleep(1)
        category_input.send_keys(Keys.DOWN)
        category_input.send_keys(Keys.ENTER)
        time.sleep(2)

        self.wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys(data['name'])
        self.wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys(data['email'])
        self.wait.until(EC.presence_of_element_located((By.ID, "address"))).send_keys(data['address'])
        self.wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(data['phone'])
        time.sleep(1)

    @allure.step("Submit the merchant form")
    def submit_form(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        time.sleep(2)

    @allure.step("Get merchant toast message")
    def get_toast_message(self):
        try:
            toast = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.toast_message)
            )
            toast_text = toast.text.strip()
            # Optional wait for it to disappear (can remove if not needed)
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.toast_message)
            )
            return toast_text
        except:
            return ""
