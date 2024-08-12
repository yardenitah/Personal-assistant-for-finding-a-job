# /Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/LinkedInManager.py
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from ExcelManager import ExcelManager
from AIManager import AIManager
import time
import os
from PyPDF2 import PdfReader


class LinkedInManager:
    def __init__(self, username, password, openai_api_key, resume_A_path, resume_B_path):
        self.username = username
        self.password = password
        self.openai_api_key = openai_api_key
        self.driver = None
        self.isLogin = False
        self.ai_manager = AIManager(self.openai_api_key)
        self.easyApply = False
        self.CV = False
        self.resume_A_path = resume_A_path
        self.resume_B_path = resume_B_path
        self.excel_path = "/Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/DATA.xlsx"
        # openai.api_key = self.openai_api_key

    def login(self):
        options = webdriver.ChromeOptions()
        # user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/SeleniumProfile")
        # options.add_argument(f"user-data-dir={user_data_dir}")
        # options.add_argument(
        #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
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

    def search_jobs(self, job_title, user_description):
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
            if not self.__experience_level('entry level'):
                return

            job_listings = self.driver.find_elements(By.CSS_SELECTOR, 'li.jobs-search-results__list-item')

            resume_text = self.extract_text_from_pdf(self.resume_A_path)
            print(f'len of job_listings: {len(job_listings)}')
        except Exception as e:
            print(f"An error occurred: {e}")

        self.__search_with_hr(user_description, job_listings, resume_text)
        time.sleep(2)
        self.__search_easy_apply(job_title, user_description)

    def __search_with_hr(self, user_description, job_listings, resume_text):
        excelManager = ExcelManager(self.excel_path)
        if self.easyApply:
            self.__turns_off_and_on_easy_apply()
        try:

            job_listings = job_listings[2:]
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

                    if self.ensures_acceleration_to_the_position(job_description, title, resume_text, user_description):
                        print(f"{title}: This job is suitable for you.\n")
                        isHR, hrName = self.__send_message_to_hr(title, company_name)
                        if isHR:
                            version = 'A' if self.CV == 'A' else 'B'
                            excelManager.add_line(company_name, job_link, title, version, f"HR: {hrName}.")
                        else:
                            print(f"{title}: no hr\n")

                    else:
                        print(f"{title}: This job is not suitable for you.\n")

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

    def __search_easy_apply(self, job_title, user_description):
        excelManager = ExcelManager(self.excel_path)
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
            # self.__experience_level('entry level')
            if not self.easyApply:
                self.__turns_off_and_on_easy_apply()

            job_listings = self.driver.find_elements(By.CSS_SELECTOR, 'li.jobs-search-results__list-item')

            resume_text = self.extract_text_from_pdf(self.resume_A_path)
            print(f'len of job_listings: {len(job_listings)}')

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

                    if self.ensures_acceleration_to_the_position(job_description, title, resume_text, user_description):
                        print(f"{title}: This job is suitable for you.\n")
                        if self.__send_resume_to_hr(title, company_name):
                            pass

                        if self.__easy_apply():
                            version = 'A' if self.CV == 'A' else 'B'
                            excelManager.add_line(company_name, job_link, title, version, 'web', )
                        else:
                            print(f"{title}: This job allredy submited.\n")

                    else:
                        print(f"{title}: This job is not suitable for you.\n")

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

        finally:
            if self.easyApply:
                self.__turns_off_and_on_easy_apply()

    def __send_message_to_hr(self, job_title, company_name):
        openChat = False
        try:
            # Wait for the "Message" button to be present and clickable using XPath
            message_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Message"]]'))
            )

            # Extract the HR name
            hr_name_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'hirer-card__hirer-information')]//strong[contains(text(), '')]")
                )
            )
            hr_name = hr_name_element.text.strip()
            hr_first_name = hr_name.split()[0]

            # Click the "Message" button
            message_button.click()
            openChat = True

            # Wait for the message div to be present
            message_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.msg-form__contenteditable[contenteditable="true"]')
                )
            )
            message_div.clear()

            # Message content using f-string
            message = f"""
            Hi {hr_first_name}, I hope this message finds you well.

            My name is Yarden, and I am a third-year Software Engineering student with a strong passion for problem-solving and algorithm design.

            I am reaching out regarding the {job_title} position at {company_name}, which I recently came across and am genuinely excited about.

            I am confident that my background and skill set would be a valuable addition to the team, and I would welcome the opportunity to discuss how I can contribute to the success of {company_name}.

            Please find my resume attached for your review. I look forward to the possibility of speaking with you further about this exciting opportunity.

            Thank you for your time and consideration.

            Best regards,
            Yarden
            """

            # Send the message to the div
            message_div.send_keys(message)
            time.sleep(2)

            # Wait for the "Send" button to be present
            send_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[normalize-space()='Send']")
                )
            )

            # Click the "Send" button
            send_button.click()
            time.sleep(1)

            # Close the chat after sending the message using a more generic XPath
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//button[contains(@class, 'msg-overlay-bubble-header__control') and contains(., 'Close your conversation')]")
                )
            )
            close_button.click()
            return True, hr_name

        except Exception as e:
            print(f"HR does not exist or an error occurred: {str(e)}")
            if openChat:
                # Close the chat after sending the message
                close_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         "//button[contains(@class, 'msg-overlay-bubble-header__control') and contains(., 'Close your conversation')]")
                    )
                )
                close_button.click()

            return False

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def __connectTO(self):
        try:
            getProfile_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(@class,'hirer-card__hirer-information')]//strong[contains(text(), '')]")
                )
            )
            getProfile_button.click()
            connect_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[@class='pvs-profile-actions__action']")
                )
            )
            connect_button.click()
        except Exception as e:
            print(f"Allredy connected: {str(e)}")

    def ensures_acceleration_to_the_position(self, job_description, job_title, resume_text, user_description):
        if "intern" in job_title.lower() or "student" in job_title.lower() or "junior" in job_title.lower():
            return True

        if "senior" in job_title.lower() or (not self.__check_experience(job_description, 2)):
            return False

        # ai_result = self.ai_manager.evaluate_job_suitability(job_description, resume_text, user_description)
        # score, explanation = self.__parse_ai_result(ai_result)
        #
        # print(f"AI Suitability Score: {score}\nExplanation: {explanation}\n")
        # return score > 70
        return True

    def __parse_ai_result(self, ai_result):
        lines = ai_result.split('\n')
        score = 0
        explanation = ""
        for line in lines:
            if "Suitability score" in line:
                score = int(line.split(':')[-1].strip())
            elif "Explanation" in line:
                explanation = line.split(':')[-1].strip()
        return score, explanation

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
            time.sleep(3)

        except Exception as e:
            print(f"An error occurred while applying the filter: {e}")

    def __turns_off_and_on_easy_apply(self):
        try:
            # Try finding the element by its aria-label attribute
            easy_apply_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Easy Apply filter."]')
            easy_apply_button.click()
            time.sleep(2)
            self.easyApply = not self.easyApply

        except Exception as e:
            print(f"An error occurred while applying the filter: {e}")

    def __easy_apply(self):
        try:
            easy_apply_button = self.driver.find_element(By.XPATH,
                                                         '//div[contains(@class, "jobs-apply-button--top-card")]//button[@id="ember39"]')
            easy_apply_button.click()
            time.sleep(1)

            submit_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Submit application"]')
            submit_button.click()
            time.sleep(3)

            return True

        except Exception as e:
            print(f"An error occurred while applying the filter: {e}")
            return False

    def __selectCV_for_AB_testing(self):
        if self.CV:
            self.CV = not self.CV
            return self.resume_A_path
        self.CV = not self.CV
        return self.resume_B_path

    def __experience_level(self, level):
        try:
            # Locate the button by its ID and click it
            experience_level_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='searchFilter_experience']"))
            )
            experience_level_button.click()
            print("Clicked on 'Experience level' button")

            time.sleep(2)
            print("Clicked on 'All filters' button")

            if level.lower() == 'entry level':
                # Click on "Internship" checkbox
                internship_checkbox = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-1']/following-sibling::label"))
                )
                internship_checkbox.click()
                time.sleep(1)
                print("Selected 'Internship' filter")

                # Click on "Entry level" checkbox
                entry_level_checkbox = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-2']/following-sibling::label"))
                )
                entry_level_checkbox.click()
                time.sleep(1)
                print("Selected 'Entry level' filter")

                associate_level_checkbox = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-3']/following-sibling::label"))
                )
                associate_level_checkbox.click()
                time.sleep(1)
                print("Selected 'Entry level' filter")
            else:
                # Click on "Mid-Senior level" checkbox
                mid_senior_checkbox = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-4']/following-sibling::label"))
                )
                mid_senior_checkbox.click()
                print("Selected 'Mid-Senior level' filter")

            time.sleep(2)
            # Show results and check if the number of results is greater than zero
            show_results_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "(//button[contains(@aria-label, 'Apply current filter to show') and contains(@class, 'artdeco-button')])[2]"))
            )
            res = show_results_button.text.split()
            show_results_button.click()
            print("Clicked on 'Show results' button")
            time.sleep(3)

            if int(res[1]) > 0:
                print(f"{res[1]} jobs were found for you")
                return True

            print("no result for you experience")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

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
