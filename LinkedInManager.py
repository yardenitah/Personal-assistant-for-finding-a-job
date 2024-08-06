# /Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/LinkedInManager.py
import openai
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
from PyPDF2 import PdfReader


class LinkedInManager:
    def __init__(self, username, password, openai_api_key):
        self.username = username
        self.password = password
        self.openai_api_key = openai_api_key
        self.driver = None
        self.isLogin = False
        openai.api_key = self.openai_api_key

    def login(self):
        options = webdriver.ChromeOptions()
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/SeleniumProfile")
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)

        try:
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(3)

            try:
                print(self.username)
                username_field = self.driver.find_element(By.ID, 'username')
                username_field.send_keys(self.username)
                time.sleep(1)
            except:
                print("Username already set.")
            try:
                print(self.password)
                password_field = self.driver.find_element(By.ID, 'password')
                password_field.send_keys(self.password)
                time.sleep(1)
                password_field.send_keys(Keys.RETURN)
            except:
                print("Login form not found, assuming already logged in or user data already set.")
                if "feed" in self.driver.current_url:
                    print("Already logged in!")
                    self.isLogin = True
                    return
                else:
                    print("Login failed or additional steps required.")

            time.sleep(5)

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

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def ensures_acceleration_to_the_position(self, jobDescription, jobTitle):
        if "intern" in jobTitle.lower() or "student" in jobTitle.lower():
            return True
        if "senior" in jobTitle.lower() or (not self.__check_experience(jobDescription, 2)):
            return False

        # What other tests can I do?

    def __check_experience(self, jobDescription, max_experience):
        # Check for experience requirement in the description
        lines = jobDescription.split('.')
        for line in lines:
            if 'experience' in line.lower():
                words = line.split()
                for word in words:
                    if word.isdigit():
                        if int(word) > max_experience:
                            return False
        return True

    def search_jobs(self, job_title, resume_path, user_description):
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

            self.__jobs_published_last_24_hours()

            job_listings = self.driver.find_elements(By.CSS_SELECTOR, 'li.jobs-search-results__list-item')
            cv_text = self.extract_text_from_pdf(resume_path)

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
                    title = title_element.text.strip()

                    job_description_element = self.driver.find_element(By.CSS_SELECTOR,
                                                                       'div.jobs-box__html-content.jobs-description-content__text')
                    job_description = job_description_element.text.strip()

                    if (self.ensures_acceleration_to_the_position(job_description, title)):
                        print(f"{title}: this job good for you\n")
                    else:
                        print(f"{title}: this job not good for you\n")

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(3)

                    print(f"Company Name: {company_name}\nJob Title: {title}\nJob Description:  {job_description}\n")

                except Exception as e:
                    print(f"An error occurred while processing a job listing: {e}")
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            print(f"An error occurred while searching for jobs: {e}")

    def __jobs_published_last_24_hours(self):
        try:
            # Wait for the "Date posted" filter button to be clickable and then click it
            date_posted_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'searchFilter_timePostedRange'))
            )
            date_posted_button.click()
            time.sleep(2)

            # Wait for the "Past 24 hours" option to be clickable and then click it
            select_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Past 24 hours"]/ancestor::label'))
            )
            select_button.click()
            time.sleep(1)

            # Wait for the "Show results" button to be clickable and then click it
            show_results_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '//button[contains(@aria-label, "Apply current filter to show") and contains(@class, "artdeco-button--primary")]/span[text()[contains(.,"Show")]]'))
            )
            show_results_button.click()

        except Exception as e:
            print(f"An error occurred while applying the filter: {e}")

    def logout(self):
        if not self.isLogin:
            print("Not logged in. No need to log out.")
            return
        try:
            self.driver.get('https://www.linkedin.com/m/logout/')
            time.sleep(3)

            self.driver.quit()
            self.isLogin = False
            print("Logged out successfully.")
        except Exception as e:
            print(f"An error occurred during logout: {e}")
