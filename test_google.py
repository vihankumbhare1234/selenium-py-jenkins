import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_google_title(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title

def test_search_python(driver):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python programming")
    search_box.send_keys(Keys.RETURN)

    # Wait until the title contains "Python"
    WebDriverWait(driver, 10).until(EC.title_contains("Python"))
    assert "Python" in driver.title

def test_search_selenium(driver):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium WebDriver")
    search_box.send_keys(Keys.RETURN)

    # Wait until the title contains "Selenium"
    WebDriverWait(driver, 10).until(EC.title_contains("Selenium"))
    assert "Selenium" in driver.title