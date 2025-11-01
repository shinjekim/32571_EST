# Test Case T011 – Add Address in Address Book (F11)
# Author: Shinje Kim

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/login"
ADDRESS_ADD_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=account/address/add"

TEST_EMAIL = "test_t011@gmail.com"    # Replace with your test account
TEST_PASSWORD = "test_t011@gmail.com" # Replace with your test password

#Wait until an element becomes visible
def wait_visible(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

#Perform login using provided credentials
def login(driver):
    driver.get(LOGIN_URL)

    # Enter email and password
    wait_visible(driver, By.ID, "input-email").send_keys(TEST_EMAIL)
    driver.find_element(By.ID, "input-password").send_keys(TEST_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()

    # Verify successful login by checking for the 'Address Book' link
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Address Book"))
    )
    print("[PASS] Logged in successfully")


#Test Case 11: Add Address in Address Book (F11)
#Test Scenario: Verify that a user can add a new address successfully
@pytest.mark.selenium
def test_T011_add_address(driver):
    print("\n=== Test Case T011: Add Address in Address Book ===")

    # Step 0: Login
    login(driver)

    # Step 1: Navigate to the Add Address page and verify the form is visible
    driver.get(ADDRESS_ADD_URL)
    wait_visible(driver, By.NAME, "firstname")
    print("[PASS] Address form is visible")

    # Step 2: Leave all required fields empty and click Continue
    continue_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Continue']")
    driver.execute_script("arguments[0].click();", continue_btn)

    # Check that validation warnings are displayed
    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".text-danger"))
    )
    print("[PASS] Validation warnings displayed for empty required fields")

    # Step 3: Enter valid data and submit the form
    driver.find_element(By.NAME, "firstname").clear()
    driver.find_element(By.NAME, "firstname").send_keys("Leah")
    driver.find_element(By.NAME, "lastname").clear()
    driver.find_element(By.NAME, "lastname").send_keys("Kim")
    driver.find_element(By.NAME, "address_1").clear()
    driver.find_element(By.NAME, "address_1").send_keys("31 Blenheim St")
    driver.find_element(By.NAME, "city").clear()
    driver.find_element(By.NAME, "city").send_keys("Sydney")
    driver.find_element(By.NAME, "postcode").clear()
    driver.find_element(By.NAME, "postcode").send_keys("2031")

    # Select Country and Region/State
    country_select = Select(driver.find_element(By.NAME, "country_id"))

    # Wait until 'Australia' option is enabled
    WebDriverWait(driver, 10).until(
        lambda d: any(
            opt.text.strip() == "Australia" and opt.is_enabled()
            for opt in d.find_elements(By.CSS_SELECTOR, 'select[name="country_id"] option')
        )
    )
    country_select.select_by_visible_text("Australia")

    # Wait until zone list contains 'New South Wales'
    WebDriverWait(driver, 10).until(
        lambda d: any(
            "New South Wales" in opt.text
            for opt in d.find_elements(By.CSS_SELECTOR, 'select[name="zone_id"] option')
        )
    )

    region_select = Select(driver.find_element(By.NAME, "zone_id"))
    region_select.select_by_visible_text("New South Wales")

    # Re-locate the Continue button AFTER the DOM changes and wait until it's clickable
    continue_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Continue']"))
    )

    # (Optional) bring into view to avoid intercepted click
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", continue_btn)

    # Use JS click on the freshly re-located element
    driver.execute_script("arguments[0].click();", continue_btn)

    # Step 4: Verify that a success message appears
    success = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    print(f"[PASS] Success message shown: {success.text.strip()}")

    # Step 5: Confirm that the new address appears with Edit/Delete options
    edits = driver.find_elements(By.LINK_TEXT, "Edit")
    deletes = driver.find_elements(By.LINK_TEXT, "Delete")
    assert len(edits) > 0 and len(deletes) > 0, "Address entry not listed with Edit/Delete options"
    print("[PASS] New address listed with Edit/Delete options")

    # Step 6: Verify that the Edit form retains saved data

    # 6.1 Ensure we're on the Address Book list page (after successful add)
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/address")

    # 6.2 Click Edit for the last address entry (newly added one is typically last)
    last_edit = WebDriverWait(driver, 10).until(
       EC.presence_of_all_elements_located((By.LINK_TEXT, "Edit"))
    )[-1]
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", last_edit)
    driver.execute_script("arguments[0].click();", last_edit)

    # 6.3 Assert the form is pre-filled with what we saved
    fname_val = wait_visible(driver, By.NAME, "firstname").get_attribute("value")
    lname_val = driver.find_element(By.NAME, "lastname").get_attribute("value")
    addr1_val = driver.find_element(By.NAME, "address_1").get_attribute("value")
    city_val  = driver.find_element(By.NAME, "city").get_attribute("value")
    post_val  = driver.find_element(By.NAME, "postcode").get_attribute("value")

    assert fname_val == "Leah",   f"Expected firstname 'Leah', got '{fname_val}'"
    assert lname_val == "Kim",    f"Expected lastname 'Kim', got '{lname_val}'"
    assert addr1_val == "31 Blenheim St", f"Expected address_1, got '{addr1_val}'"
    assert city_val  == "Sydney", f"Expected city 'Sydney', got '{city_val}'"
    assert post_val  == "2031",   f"Expected postcode '2031', got '{post_val}'"

    print("[PASS] Edit form shows previously saved details")

    print("=== Test Case T011: PASSED ===\n")
