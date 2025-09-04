import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def _timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _make_driver(browser: str):
    browser = (browser or "chrome").lower()
    if browser == "chrome":
        opts = ChromeOptions()
        # Headless for CI
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1366,768")
        return webdriver.Chrome(options=opts)  # Selenium Manager resolves driver
    elif browser == "firefox":
        opts = FirefoxOptions()
        opts.add_argument("-headless")
        return webdriver.Firefox(options=opts)  # Selenium Manager resolves driver
    else:
        raise ValueError(f"Unsupported browser: {browser}")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=os.getenv("BROWSER", "chrome"),
                     help="Browser to use: chrome or firefox")

@pytest.fixture
def browser(request):
    driver = _make_driver(request.config.getoption("--browser"))
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Take screenshot on test failure
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed and "browser" in item.fixturenames:
        driver = item.funcargs["browser"]
        _ensure_dir("reports/screenshots")
        fname = f"reports/screenshots/{item.name}_{_timestamp()}.png"
        try:
            driver.save_screenshot(fname)
        except Exception:
            pass  # don't break reporting