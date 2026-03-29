import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils import attach


def pytest_addoption(parser):
    parser.addoption("--url", default="https://demoqa.com/automation-practice-form", help="Адрес тестируемого сайта")
    parser.addoption("--selenoid_url", default="https://selenoid.autotests.cloud/wd/hub", help="Адрес Selenoid")
    parser.addoption("--browser", default="chrome", choices=("chrome", "firefox", "edge", "opera", "safari"), help="Браузер")
    parser.addoption("--browser_version", default="128.0", help="Версия браузера")
    parser.addoption("--headless", action="store_true", default=False, help="Headless режим")
    parser.addoption("--resolution", default="1920x1080", help="Разрешение экрана")
    parser.addoption("--environment", default="", choices=("", "stage", "prod", "dev", "local"), help="Окружение")
    parser.addoption("--local", action="store_true", default=False, help="Запускать локально")


@pytest.fixture(scope='session', autouse=True)
def load_env(request):
    env = request.config.getoption("--environment")
    env_file = f"{env}.env" if env else ".env"
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file, override=True)


@pytest.fixture(scope='function')
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope='function')
def selenoid_url(request):
    return request.config.getoption("--selenoid_url")


@pytest.fixture(scope='function')
def setup_browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='function')
def browser_version(request):
    return request.config.getoption("--browser_version")


@pytest.fixture(scope='function')
def driver(request, base_url, selenoid_url, setup_browser, browser_version):
    browser = setup_browser
    version = browser_version
    headless = request.config.getoption("--headless")
    resolution = request.config.getoption("--resolution")
    local = request.config.getoption("--local")

    options = ChromeOptions()

    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={resolution}")

    if local:
        driver_instance = webdriver.Chrome(options=options)
    else:
        login = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")

        selenoid_capabilities = {
            "browserName": browser,
            "browserVersion": version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)

        if login and password:
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(selenoid_url)
            command_executor = urlunparse((
                parsed.scheme,
                f"{login}:{password}@{parsed.netloc}",
                parsed.path, parsed.params, parsed.query, parsed.fragment
            ))
        else:
            command_executor = selenoid_url

        driver_instance = webdriver.Remote(command_executor=command_executor, options=options)

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