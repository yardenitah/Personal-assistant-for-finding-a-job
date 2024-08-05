# /Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/LinkedInManager.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import os
from ExcelManager import ExcelManager



class LinkedInManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.isLogin = False

    def login(self):
        # Set up the WebDriver with a persistent profile
        options = webdriver.ChromeOptions()
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/SeleniumProfile")
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)

        try:
            # Open LinkedIn login page
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(3)  # Add a delay to mimic human behavior

            # Check if the username or password input field is present
            try:
                print(self.username)
                username_field = self.driver.find_element(By.ID, 'username')
                username_field.send_keys(self.username)
                time.sleep(1)  # Add a delay to mimic human behavior
            except:
                print("Username already set.")
            try:
                print(self.password)
                password_field = self.driver.find_element(By.ID, 'password')
                password_field.send_keys(self.password)
                time.sleep(1)  # Add a delay to mimic human behavior
                password_field.send_keys(Keys.RETURN)
            except:
                print("Login form not found, assuming already logged in or user data already set.")
                if "feed" in self.driver.current_url:
                    print("Already logged in!")
                    self.isLogin = True
                    return
                else:
                    print("Login failed or additional steps required.")

            # Wait for a few seconds to ensure the login process completes
            time.sleep(5)

            # Check if verification is needed and handle it
            if "checkpoint/challenge" in self.driver.current_url:
                print("Verification needed. Please complete the verification manually.")
                time.sleep(30)
            elif "feed" in self.driver.current_url:
                self.isLogin = True
                print("Login successful!")
            else:
                print("Login failed.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def Compatibility_test(self, job_html, title):
        if "intern" in title.lower() or "student" in title.lower():
            return True

    def check_experience(self, description, max_experience):
        # Check for experience requirement in the description
        lines = description.split('.')
        for line in lines:
            if 'experience' in line.lower():
                words = line.split()
                for word in words:
                    if word.isdigit():
                        if int(word) <= max_experience:
                            return True
        return False

    def search_jobs(self, job_title):
        if not self.isLogin:
            print("Not logged in. Please log in first.")
            return
        self.driver.get('https://www.linkedin.com/jobs/')
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'input.jobs-search-box__text-input.jobs-search-box__keyboard-text-input'))
            )
            search_box.send_keys(job_title)
            time.sleep(3)
            search_box.send_keys(Keys.RETURN)
            time.sleep(4)

            job_listings = self.driver.find_elements(By.CSS_SELECTOR, 'li.jobs-search-results__list-item')
            for job in job_listings:
                try:
                    company_name_element = job.find_element(By.CLASS_NAME, 'job-card-container__primary-description')
                    company_name = company_name_element.text.strip()

                    job_element = job.find_element(By.CSS_SELECTOR, 'a.job-card-list__title')
                    job_link = job_element.get_attribute('href')

                    self.driver.execute_script("window.open(arguments[0]);", job_link)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(3)

                    title_element = self.driver.find_element(By.CSS_SELECTOR, 'h1.t-24.t-bold.inline')
                    title_element = title_element.text.strip()

                    job_page_source = self.driver.page_source
                    # if self.Compatibility_test(job_page_source, title_element) or check_experience()

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(3)
                    print("Company Name: " + company_name + "title: " + title_element)

                except Exception as e:
                    print(f"An error occurred while processing a job listing: {e}")
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            print(f"An error occurred while searching for jobs: {e}")

    def logout(self):
        if not self.isLogin:
            print("Not logged in. No need to log out.")
            return
        try:
            # Navigate to the LinkedIn logout page
            self.driver.get('https://www.linkedin.com/m/logout/')
            time.sleep(3)  # Add a delay to ensure the logout process completes

            # Optionally close the browser
            self.driver.quit()
            self.isLogin = False
            print("Logged out successfully.")
        except Exception as e:
            print(f"An error occurred during logout: {e}")
