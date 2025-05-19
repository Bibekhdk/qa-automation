from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AddMerchantPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def login(self, url, username, password):
        self.driver.get(url)
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@id='submit-button']").click()

    def go_to_add_merchant(self):
        # Navigate to the Merchant page (or Add Merchant section)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Merchant')]"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Merchant']"))).click()

    def fill_merchant_form(self, data):
        # Fill all required fields for adding a merchant
        self.driver.find_element(By.ID, "account_number").send_keys(data['accountnumber'])
        self.driver.find_element(By.ID, "pan").send_keys(data['merchantpan'])

        branch_input = self.driver.find_element(By.ID, "branch")
        branch_input.send_keys(data['branch'])
        branch_input.send_keys(Keys.DOWN)
        branch_input.send_keys(Keys.ENTER)

        scheme_input = self.driver.find_element(By.ID, "scheme-select-box")
        scheme_input.send_keys(data['scheme'])
        scheme_input.send_keys(Keys.DOWN)
        scheme_input.send_keys(Keys.ENTER)

        self.driver.find_element(By.NAME, "nchl_merchantCode").send_keys(data['nchl'])

        category_input = self.driver.find_element(By.ID, "category-code-search")
        category_input.send_keys(data['categorycode'])
        category_input.send_keys(Keys.DOWN)
        category_input.send_keys(Keys.ENTER())

        self.driver.find_element(By.ID, "name").send_keys(data['name'])
        self.driver.find_element(By.ID, "email").send_keys(data['email'])
        self.driver.find_element(By.ID, "address").send_keys(data['address'])
        self.driver.find_element(By.ID, "phone").send_keys(data['phone'])

    def submit_form(self):
        # Submit the form
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def get_toast_message(self):
        # Capture and return the success toast message
        try:
            toast = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast-body")))
            return toast.get_attribute("innerText")
        except:
            return ""
    