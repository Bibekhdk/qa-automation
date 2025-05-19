import pytest
import allure
from pages.merchant.add_merchant_page import AddMerchantPage

@allure.title("TC_132 - Add Merchant with valid data")
@allure.description("This test adds a merchant with valid data and verifies toast message")
@pytest.mark.usefixtures("init_driver")
class TestAddMerchant:

    @pytest.fixture(autouse=True)
    def setup(self, init_driver):
        # Initialize the AddMerchantPage with the driver
        self.page = AddMerchantPage(self.driver)

    def test_add_valid_merchant(self):
        # Assuming data for adding the merchant
        data = {
            'url': 'http://example.com',  # Replace with actual URL
            'username': 'testuser',
            'password': 'testpassword',
            'accountnumber': '1234567890',
            'merchantpan': 'ABCDE12345',
            'branch': 'Test Branch',
            'scheme': 'Test Scheme',
            'nchl': 'TestNCHLCode',
            'categorycode': 'Category123',
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'address': '123 Test St, Test City',
            'phone': '9876543210'
        }

        with allure.step("Login to application"):
            self.page.login(data['url'], data['username'], data['password'])

        with allure.step("Navigate to Add Merchant page"):
            self.page.go_to_add_merchant()

        with allure.step("Fill merchant form"):
            self.page.fill_merchant_form(data)

        with allure.step("Submit the form and capture toast message"):
            self.page.submit_form()
            toast_msg = self.page.get_toast_message()

        with allure.step("Verify success toast message"):
            assert "success" in toast_msg.lower() or "added" in toast_msg.lower(), f"Unexpected toast: {toast_msg}"
