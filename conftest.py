import pytest
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import TestData


@pytest.fixture(params=["chrome"], scope="class")
def init_driver(request):
    browser = request.param
    user_data_dir = None  # Initialize here for scope access

    if browser == "chrome":
        # Create a temporary user data directory to avoid session conflicts
        user_data_dir = tempfile.mkdtemp()

        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        #options.add_argument("--headless=new")  # Important for CI environments
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # Reduce resource usage in CI
        options.add_argument("--remote-debugging-port=9222")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

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

    # Clean up temporary user data directory (only for Chrome)
    if browser == "chrome" and user_data_dir:
        shutil.rmtree(user_data_dir, ignore_errors=True)
