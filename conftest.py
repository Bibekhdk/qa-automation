import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import TestData

@pytest.fixture(params=["chrome"], scope="class")
def init_driver(request):
    browser = request.param

    if browser == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser == "firefox":
        service = FirefoxService(executable_path=TestData.FIREFOX_EXECUTABLE_PATH)
        driver = webdriver.Firefox(service=service)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver
    driver.quit()
