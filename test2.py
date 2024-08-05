from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Replace these with your LinkedIn username and password
USERNAME = 'yarden1606@gmail.com'
PASSWORD = 'yarden1169'

# Set up the WebDriver with a persistent profile
options = webdriver.ChromeOptions()
user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/SeleniumProfile")
options.add_argument(f"user-data-dir={user_data_dir}")

# Set a common User-Agent
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=options)

try:
    # Open LinkedIn login page
    driver.get('https://www.linkedin.com/login')
    time.sleep(3)  # Add a delay to mimic human behavior

    # Check if the username or password input field is present
    try:
        username_field = driver.find_element(By.ID, 'username')
        username_field.send_keys(USERNAME)
        time.sleep(1)  # Add a delay to mimic human behavior
    except:
         print("userName already set.")
    try:
        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(PASSWORD)
        time.sleep(1)  # Add a delay to mimic human behavior
        password_field.send_keys(Keys.RETURN)
    except:
        print("Login form not found, assuming already logged in or user data already set.")
        # Check if already logged in by looking for the 'feed' keyword in the URL
        if "feed" in driver.current_url:
            print("Already logged in!")
        else:
            print("Login failed or additional steps required.")

    # Wait for a few seconds to ensure the login process completes
    time.sleep(5)

    # Check if verification is needed and handle it
    if "checkpoint/challenge" in driver.current_url:
        print("Verification needed. Please complete the verification manually.")
        # Wait to give time to complete the verification manually if needed
        time.sleep(30)
    elif "feed" in driver.current_url:
        print("Login successful!")
        # Keep the browser open
        input("Press Enter to close the browser...")
    else:
        print("Login failed.")

finally:
    # Close the browser
    driver.quit()
