import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SystemAdminDashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Click menu item: {menu_name}")
    def click_menu(self, menu_name):
        xpath = f"//span[text()='{menu_name}']"
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    @allure.step("Verify all expected admin menus")
    def verify_all_admin_menus(self):
        menu_items = [
            "Dashboard", "Operation", "Branch", "User", "Scheme", "Partner",
            "Merchant", "IPN", "Settings", "Audit Log", "Bill",
            "Bill History", "Lead", "Profile", "Logout"
        ]
        for item in menu_items:
            self.click_menu(item)
