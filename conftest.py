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

    if browser == "chrome":
        # Create a temporary user data directory to avoid session conflicts
        user_data_dir = tempfile.mkdtemp()
        
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        #options.add_argument("--headless")  # Run Chrome in headless mode for CI
        options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--no-sandbox")  # Disable sandbox for CI environments
        options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging

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
    
    # Clean up temporary user data directory for Chrome after test execution
    if browser == "chrome":
        shutil.rmtree(user_data_dir)
        
    driver.quit()
