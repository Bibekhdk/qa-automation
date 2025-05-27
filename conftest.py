import pytest
import tempfile
import shutil
import os  # Needed to get environment variable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import TestData


@pytest.fixture(params=["chrome", "firefox"], scope="class")
def init_driver(request):
    browser = request.param
    user_data_dir = None  # Initialize here for scope access

   
    hub_host = os.getenv("SELENIUM_HUB_HOST", "localhost")
    hub_url = f"http://{hub_host}:4444/wd/hub"

    if browser == "chrome":
        # Create a temporary user data directory to avoid session conflicts
        user_data_dir = tempfile.mkdtemp()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        # chrome_options.add_argument("--headless")  # Important for CI environments
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")

        driver = webdriver.Remote(
            command_executor=hub_url,
            options=chrome_options
        )

    elif browser == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = True

        driver = webdriver.Remote(
            command_executor=hub_url,
            options=firefox_options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(10)
    request.cls.driver = driver
    yield driver

    driver.quit()

    # Clean up temporary user data directory (only for Chrome)
    if browser == "chrome" and user_data_dir:
        shutil.rmtree(user_data_dir, ignore_errors=True)
