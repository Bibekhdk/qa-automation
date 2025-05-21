import pytest
import allure
import time
from pages.merchant.add_merchant_page import AddMerchantPage

@allure.title("TC_132 - Add Merchant with valid data")
@allure.description("This test adds a merchant with valid data and verifies toast message")
@pytest.mark.usefixtures("init_driver")
class TestAddMerchant:

    @pytest.fixture(autouse=True)
    def setup(self, init_driver):
        self.page = AddMerchantPage(self.driver)

    def test_add_valid_merchant(self):
        login_data = {
            'url': 'https://ipn-tms-staging.koilifin.com',
            'username': 'admin10',
            'password': 'Bibek2426@',
        }
    
        timestamp = str(int(time.time()))
        merchant_data = {
            'accountnumber': "0653434213",
            'merchantpan': '123332AA',
            'branch': 'NMB',
            'scheme': 'nchl',
            'nchl': f'TestNCHL{timestamp[-3:]}Code',
            'categorycode': 'scheme: nchl | code: 5311 | desc: Retail Outlets',
            'name': f'ram khanal  {timestamp[-4:]}',
            'email': f'khanalram{timestamp[-4:]}@example.com',
            'address': '123 Test St, Test City',
            'phone': '9876222222'
        }

        with allure.step("Step 1: Login to application"):
            self.page.login(login_data['url'], login_data['username'], login_data['password'])

        with allure.step("Step 2: Navigate to Add Merchant page"):
            self.page.go_to_add_merchant()

        with allure.step("Step 3: Fill merchant form"):
            self.page.fill_merchant_form(merchant_data)

        with allure.step("Step 4: Submit the form"):
            self.page.submit_form()

        with allure.step("Step 5: Capture toast and validate"):
            toast_msg = self.page.get_toast_message()

            allure.attach(toast_msg or "No toast captured", name="Toast Message", attachment_type=allure.attachment_type.TEXT)

           
            allure.attach(self.page.driver.get_screenshot_as_png(), name="Toast Screenshot", attachment_type=allure.attachment_type.PNG)

            assert toast_msg and ("success" in toast_msg.lower() or "added" in toast_msg.lower()), \
                f"Expected success or added toast, got: '{toast_msg}'"
