**Author:** Shinje Kim
**Subject:** 32571 Enterprise Software Testing
**Institution:** University of Technology Sydney (UTS)

**32571 Enterprise Software Testing – Assessment Task 3**

This repository contains automated Selenium test scripts developed for the [LambdaTest E-Commerce Playground](https://ecommerce-playground.lambdatest.io/) as part of the University of Technology Sydney (UTS) subject **32571 Enterprise Software Testing**.

---

## 🧪 How to Run the Tests

### Requirements
- **Python** 3.9 or later  
- **Google Chrome** (latest version)  
- **Selenium** automatically manages the correct ChromeDriver version  

---

### 1. Clone this repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
````

---

### 2. Install dependencies

```bash
pip install selenium pytest
```

---

### 3. Run all test cases

```bash
pytest -s
```

> The `-s` flag displays console log outputs (e.g., `[PASS]` messages).

---

### 4. Run a specific test file

```bash
pytest -s test_t014_address.py
```

---

### (Optional) Run in headless mode

If Chrome cannot open a browser window, enable headless mode in `conftest.py` by adding:

```python
options.add_argument("--headless")
```

---

### ✅ Example Output

```
=== Test Case T014: Add Address in Address Book ===
[PASS] Logged in successfully
[PASS] Address form is visible
[PASS] Validation warnings displayed for empty required fields
[PASS] Success message shown: Your address has been successfully added.
[PASS] New address listed with Edit/Delete options
[PASS] Edit form shows previously saved details
=== Test Case T014: PASSED ===
```

---
