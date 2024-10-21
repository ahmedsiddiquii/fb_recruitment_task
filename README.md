# Facebook Login Automation

This Python script automates the login process for Facebook accounts using credentials from a JSON file. It uses Selenium to interact with the Facebook login page and rotates proxies for each login attempt. The script saves successful login cookies and marks failed attempts as "WRONG ACCOUNT" in the output JSON file.

## Features
- Reads login credentials from a JSON file (`accounts.json`).
- Utilizes a SOCKS5 proxy for each login attempt.
- Resets the proxy IP before each login attempt using a provided API.
- Saves cookies for successful logins.
- Marks incorrect credentials as "WRONG ACCOUNT".
- Saves the results in `successful_logins.json`.

## Requirements
- Python 3.x
- Selenium and Selenium Wire for browser automation with proxies.
- WebDriver Manager for managing ChromeDriver.
- Requests for interacting with the proxy reset API.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. Create a virtual environment (optional but recommended):
    ```bash
   python -m venv venv
    source venv/bin/activate
3. Install the required packages:
    ```bash
   pip install -r requirements.txt
4. Run script:
    ```bash
   python fb_login_automation.py