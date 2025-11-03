# Test Case T015 – Purchase a Gift Certificate (F15)
# Author: Shinje Kim

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"
GIFT_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/voucher"

TEST_EMAIL = "test_t011@gmail.com"     # Replace with your test account
TEST_PASSWORD = "test_t011@gmail.com"  # Replace with your test password


# Wait until an element is visible
def wait_visible(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


# Perform login using valid credentials
def login(driver):
    driver.get(LOGIN_URL)
    wait_visible(driver, By.ID, "input-email").send_keys(TEST_EMAIL)
    driver.find_element(By.ID, "input-password").send_keys(TEST_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Address Book")))
    print("[PASS] Logged in successfully")


# Main test case: Purchase a Gift Certificate
@pytest.mark.selenium
def test_T015_purchase_gift_certificate(driver):
    print("\n=== Test Case T015: Purchase a Gift Certificate ===")

    # Step 0: Login first
    login(driver)

    # Step 1: Navigate to Gift Certificate page
    driver.get(GIFT_URL)
    wait_visible(driver, By.ID, "input-to-name")
    print("[PASS] Gift Certificate form is visible")

    # Step 2: Click Continue with all fields empty → expect validation warnings
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()
    WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger")))
    print("[PASS] Validation banner displayed for empty submission")

    # Step 3: Fill in valid data
    driver.find_element(By.ID, "input-to-name").send_keys("Alice Wu")
    driver.find_element(By.ID, "input-to-email").send_keys("alice@example.com")

    from_name = driver.find_element(By.ID, "input-from-name")
    from_email = driver.find_element(By.ID, "input-from-email")

    # Only fill “From” fields if not pre-filled after login
    if from_name.get_attribute("value").strip() == "":
        from_name.send_keys("Leah Kim")
    if from_email.get_attribute("value").strip() == "":
        from_email.send_keys("shinje.kim@student.uts.edu.au")

    # Select Theme, enter Amount, and agree to terms
    driver.find_element(By.CSS_SELECTOR, "input[name='voucher_theme_id'][value='7']").click()  # Birthday
    amt = driver.find_element(By.ID, "input-amount")
    amt.clear()
    amt.send_keys("50")
    driver.find_element(By.NAME, "agree").click()

    # Step 4: Submit form and verify success page
    driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']").click()
    success = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(.,'Thank you for purchasing a gift certificate')]")
        )
    )
    assert "Thank you for purchasing a gift certificate" in success.text
    print("[PASS] Success message displayed on confirmation page")

    print("=== Test Case T015: PASSED ===\n")

