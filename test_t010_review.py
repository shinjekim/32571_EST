# Test Case T010 – Write a Product Review (F10)
# Author: Shinje Kim

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PRODUCT_URL = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=30"

#Fill in the review form with the provided name, text, and rating
def write_review(driver, name, text, rating):
    driver.find_element(By.CSS_SELECTOR, "#form-review input[name='name']").clear()
    driver.find_element(By.CSS_SELECTOR, "#form-review input[name='name']").send_keys(name)
    driver.find_element(By.CSS_SELECTOR, "#form-review textarea[name='text']").clear()
    driver.find_element(By.CSS_SELECTOR, "#form-review textarea[name='text']").send_keys(text)
    if rating:
        star = driver.find_element(By.CSS_SELECTOR, f"#form-review input[name='rating'][value='{rating}']")
        driver.execute_script("arguments[0].click();", star)

#Click the Submit button on the review form
def submit_review(driver):
    submit_btn = driver.find_element(By.ID, "button-review")
    driver.execute_script("arguments[0].click();", submit_btn)

@pytest.mark.selenium
def test_T010_write_product_review(driver):
    print("\n=== Test Case T010: Write a Product Review ===")

    driver.get(PRODUCT_URL)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "form-review")))
    print("[PASS] Review form is visible on the product page")

    # Step 1: Name validation
    write_review(driver, name="", text="This is a test review with enough length.", rating=4)
    submit_review(driver)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(.,'Review Name must be between 3 and 25 characters')]"))
    )
    print("[PASS] Name validation warning displayed")

    # Step 2: Review text length validation
    write_review(driver, name="Leah Kim", text="too short", rating=4)
    submit_review(driver)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(.,'Review Text must be between 25 and 1000 characters')]"))
    )
    print("[PASS] Review text length validation displayed")

    # Step 3: Rating required validation
    driver.execute_script("""
      document.querySelectorAll("#form-review input[name='rating']").forEach(r => r.checked = false);
    """)

    write_review(
        driver,
        name="Leah Kim",
        text="This camera has decent build and image quality for the price.",
        rating=None  # 의도적으로 미선택
    )

    submit_review(driver)

    banner = WebDriverWait(driver, 8).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class,'alert') and contains(@class,'alert-danger')][contains(normalize-space(.),'Please select a review rating')]"
        ))
    )
    assert "Please select a review rating" in banner.text
    print("[PASS] Rating required warning displayed")

    # Step 4: Valid review submission
    write_review(driver, name="Leah Kim", text="Good product and smooth delivery. Satisfied overall.", rating=4)
    submit_review(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(.,'Thank you for your review')]"))
    )
    print("[PASS] Review submitted successfully (pending moderation)")

    # Step 5: Verify review not visible immediately
    time.sleep(2)
    reviews = driver.find_elements(By.CSS_SELECTOR, ".review-list .review")
    assert len(reviews) == 0, "Review should not appear instantly (requires approval)"
    print("[PASS] Review not instantly visible (moderation required)")

    print("=== Test Case T010: PASSED ===\n")
