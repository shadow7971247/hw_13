import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils import attach


load_dotenv()


def pytest_addoption(parser):
    parser.addoption("--browser", default=os.getenv("BROWSER", "chrome"), help="Browser to use")
    parser.addoption("--browser_version", default=os.getenv("BROWSER_VERSION", "128.0"), help="Browser version")
    parser.addoption("--headless", default=os.getenv("HEADLESS", "False"), help="Headless mode True/False")
    parser.addoption("--resolution", default=os.getenv("RESOLUTION", "1920x1080"), help="Screen resolution")
    parser.addoption("--url", default=os.getenv("URL", "https://demoqa.com/automation-practice-form"), help="Base URL")
    parser.addoption("--selenoid_url", default=os.getenv("SELENOID_URL", "https://selenoid.autotests.cloud/wd/hub"), help="Selenoid URL")
    parser.addoption("--local", action="store_true", default=False, help="Run locally")


@pytest.fixture(scope='function')
def driver(request):
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")
    headless = request.config.getoption("--headless").lower() == "true"
    resolution = request.config.getoption("--resolution")
    base_url = request.config.getoption("--url")
    selenoid_url = request.config.getoption("--selenoid_url")
    local = request.config.getoption("--local")

    options = ChromeOptions()

    options.set_capability("browserName", browser_name)
    options.set_capability("browserVersion", browser_version)
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True
    })

    if headless:
        options.add_argument("--headless=new")

    options.add_argument(f"--window-size={resolution}")

    if local:
        driver_instance = webdriver.Chrome(options=options)
    else:
        user = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")

        if user and password:
            command_executor = f"https://{user}:{password}@{selenoid_url}"
        else:
            command_executor = selenoid_url

        driver_instance = webdriver.Remote(
            command_executor=command_executor,
            options=options
        )

    driver_instance.get(base_url)

    yield driver_instance

    try:
        attach.add_screenshot(driver_instance)
        attach.add_page_source(driver_instance)
        attach.add_console_logs(driver_instance)
        attach.add_video(driver_instance)
    except:
        pass

    try:
        driver_instance.quit()
    except:
        pass