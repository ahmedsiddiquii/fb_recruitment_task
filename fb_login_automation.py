import json
import time
import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Constants
PROXY_RESET_URL = "https://api.ltesocks.io/v2/port/reset/395bc511ccd51db8de4b778aa5c011560f8abd6a75e48e33a80ce4911f039576"
FACEBOOK_LOGIN_URL = "https://www.facebook.com/login"


def reset_proxy_ip():
    """Reset the proxy IP using the provided URL."""
    try:
        response = requests.get(PROXY_RESET_URL)
        print(response.status_code)
        if response.status_code == 202:
            print("Proxy IP reset successfully.")
        else:
            print("Failed to reset proxy IP.")
    except Exception as e:
        print(f"Error resetting proxy: {e}")


def get_browser_with_proxy():
    """Sets up Selenium browser with the SOCKS5 proxy."""
    chrome_options = Options()

    # Add proxy settings to Chrome options
    options = {
        'proxy': {
            'http': 'socks5://wlseo:QweasdzxC123!@ap1.socks.expert:44681',
            'https': 'socks5://wlseo:QweasdzxC123!@ap1.socks.expert:44681',
            'no_proxy': 'localhost,ENDPOINT'
        }
    }

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              seleniumwire_options=options)
    return driver


def login_facebook(driver, login_data):
    """Logs into Facebook with the provided credentials."""
    try:
        driver.get(FACEBOOK_LOGIN_URL)
        time.sleep(2)

        cookie = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Allow all cookies")][@tabindex=0]'))
        )
        cookie.click()

        # Input login credentials
        driver.find_element(By.ID, "email").send_keys(login_data["login"])
        driver.find_element(By.ID, "pass").send_keys(login_data["password"])
        driver.find_element(By.NAME, "login").click()

        time.sleep(5)  # Give time for login process

        # Check for login success by finding a known element (e.g., user's profile element)
        try:
            whats_on_your_mind = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), \"What's on your mind\")]"))
            )
            print(f"Login successful for {login_data['login']}")

            # Extract cookies
            cookies = driver.get_cookies()
            return True, cookies

        except NoSuchElementException:
            print(f"Login failed for {login_data['login']}")
            return False, None

    except TimeoutException:
        print(f"Timeout occurred during login attempt for {login_data['login']}")
        return False, None


def save_results(results):
    """Saves the login results to successful_logins.json."""
    with open('successful_logins.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)
    print("Results saved to successful_logins.json.")


def main():
    # Load login data from JSON
    with open('accounts.json', 'r') as infile:
        accounts = json.load(infile)

    results = []

    # Iterate through accounts
    for account in accounts:
        # Reset the proxy IP before every attempt
        reset_proxy_ip()

        # Start browser with proxy
        driver = get_browser_with_proxy()

        # Try to login
        success, cookies = login_facebook(driver, account)

        if success:
            # Append success result
            account_result = {
                "login": account["login"],
                "password": account["password"],
                "cookies": cookies
            }
        else:
            # Append failure result
            account_result = {
                "login": account["login"],
                "password": account["password"],
                "status": "WRONG ACCOUNT"
            }

        results.append(account_result)

        # Close the browser and wait before the next attempt
        driver.quit()
        time.sleep(3)

    # Save the final results
    save_results(results)


if __name__ == '__main__':
    main()
