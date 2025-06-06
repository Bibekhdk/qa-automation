import pytest
import allure
from pages.login_page import LoginPage

@allure.epic("Login Functionality")
@allure.feature("Login Page Tests")
@pytest.mark.usefixtures("init_driver")
class TestLogin:

    @pytest.mark.parametrize("username, password", [
        ("ram", "ram1234"),
        ("dibash", "@dmin2929A"),
        ("admin1", "dibash11"),
        ("admin1", ""),
        ("", "@dmin2929A"),
        ("", ""),
        ("admin10", "Bibek2426@")  # valid
    ])
    def test_login_functionality(self, username, password):
        login_page = LoginPage(self.driver)

        with allure.step("Load login page"):
            login_page.load()

        with allure.step("Try login"):
            login_page.login(username, password)

        toast = login_page.get_toast_message()
        errors = login_page.get_inline_errors()

        if login_page.is_login_successful():
            allure.attach(self.driver.get_screenshot_as_png(), name="Login Success", attachment_type=allure.attachment_type.PNG)
            assert True
        else:
            if toast:
                allure.attach(self.driver.get_screenshot_as_png(), name="Toast", attachment_type=allure.attachment_type.PNG)
                allure.attach(toast, name="Toast Text", attachment_type=allure.attachment_type.TEXT)
            if errors:
                allure.attach(str(errors), name="Inline Errors", attachment_type=allure.attachment_type.TEXT)
            assert False, f"Login failed for username='{username}', password='{password}'"  
