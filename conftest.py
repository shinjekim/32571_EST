# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def base_url():
    return "https://ecommerce-playground.lambdatest.io"
