import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils import attach
from dotenv import load_dotenv

load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--browser", default=os.getenv("BROWSER", "chrome"), choices=["chrome", "firefox"], help="Browser")
    parser.addoption("--browser_version", default=os.getenv("BROWSER_VERSION", "128.0"), help="Browser version")
    parser.addoption("--headless", default=os.getenv("HEADLESS", "False"), help="Headless mode True/False")
    parser.addoption("--width", default=os.getenv("SCREEN_WIDTH", "1920"), help="Window width")
    parser.addoption("--height", default=os.getenv("SCREEN_HEIGHT", "1080"), help="Window height")
    parser.addoption("--base_url", default=os.getenv("BASE_URL", "https://demoqa.com"), help="Base URL")
    parser.addoption("--selenoid_url", default=os.getenv("SELENOID_URL", "selenoid.autotests.cloud/wd/hub"), help="Selenoid URL")


@pytest.fixture(scope='function')
def setup_browser(request):
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    headless = request.config.getoption("--headless") == "True"
    width = request.config.getoption("--width")
    height = request.config.getoption("--height")
    base_url = request.config.getoption("--base_url")
    selenoid_url = request.config.getoption("--selenoid_url")

    if selenoid_url and not selenoid_url.startswith(('http://', 'https://')):
        selenoid_url = f"https://{selenoid_url}"

    user = os.getenv("SELENOID_USER", "")
    password = os.getenv("SELENOID_PASSWORD", "")

    if user and password:
        remote_url = selenoid_url.replace("://", f"://{user}:{password}@")
    else:
        remote_url = selenoid_url

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")
    else:
        raise ValueError(f"Browser {browser_name} not supported")

    selenoid_capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )

    driver.base_url = base_url

    yield driver

    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_console_logs(driver)
    attach.add_video(driver)

    driver.quit()