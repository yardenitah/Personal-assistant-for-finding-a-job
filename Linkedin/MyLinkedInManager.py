from playwright.sync_api import sync_playwright
from ExcelManager import ExcelManager
from AIManager import AIManager
from PyPDF2 import PdfReader
import time


class LinkedInManager:
    def __init__(self, username, password, openai_api_key, resume_A_path, resume_B_path):
        self.username = username
        self.password = password
        self.openai_api_key = openai_api_key
        self.browser = None
        self.page = None
        self.isLogin = False
        self.ai_manager = AIManager(self.openai_api_key)
        self.easyApply = False
        self.CV = False
        self.resume_A_path = resume_A_path
        self.resume_B_path = resume_B_path
        self.excel_path = "/Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/DATA.xlsx"
        self.playwright = None  # Store playwright instance to close it later

    def start_playwright(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def stop_playwright(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def login(self):
        self.start_playwright()

        try:
            self.page.goto('https://www.linkedin.com/login')
            time.sleep(3)

            self.page.fill('input#username', self.username)
            self.page.fill('input#password', self.password)
            self.page.click('button[type="submit"]')

            time.sleep(5)

            if "checkpoint/challenge" in self.page.url:
                print("Verification needed. Please complete the verification manually.")
                time.sleep(30)
            elif "feed" in self.page.url:
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

    def ensures_acceleration_to_the_position(self, job_description, job_title, resume_text, user_description):
        if "intern" in job_title.lower() or "student" in job_title.lower() or "junior" in job_title.lower():
            return True

        if "senior" in job_title.lower() or (not self.__check_experience(job_description, 2)):
            return False

        return True

    def __check_experience(self, jobDescription, max_experience):
        lines = jobDescription.split('.')
        for line in lines:
            if 'experience' in line.lower():
                words = line.split()
                for word in words:
                    if word.isdigit():
                        if int(word) > max_experience:
                            return False
        return True

    def search_jobs(self, job_title, user_description):
        if not self.isLogin:
            print("Not logged in. Please log in first.")
            return

        excelManager = ExcelManager(self.excel_path)
        self.page.goto('https://www.linkedin.com/jobs/')
        try:
            self.page.fill('input.jobs-search-box__text-input', job_title)
            time.sleep(3)
            self.page.keyboard.press('Enter')
            time.sleep(4)

            self.__jobs_published_last_24_hours()
            self.__experience_level('entry level')
            self.__turns_off_and_on_easy_apply()

            job_listings = self.page.query_selector_all('li.jobs-search-results__list-item')

            resume_text = self.extract_text_from_pdf(self.resume_A_path)
            print(f'len of job_listings: {len(job_listings)}')

            for job in job_listings:
                try:
                    company_name = job.query_selector('div.job-card-container__primary-description').inner_text().strip()
                    job_link = job.query_selector('a.job-card-list__title').get_attribute('href')

                    self.page.goto(job_link)
                    time.sleep(3)

                    title = self.page.query_selector('h1.t-24.t-bold.inline').inner_text().strip()
                    job_description = self.page.query_selector(
                        'div.jobs-box__html-content.jobs-description-content__text').inner_text().strip()

                    if self.ensures_acceleration_to_the_position(job_description, title, resume_text, user_description):
                        print(f"{title}: This job is suitable for you.\n")
                        if self.__easy_apply():
                            excelManager.add_line(company_name, job_link, title, 'A', 'web')
                        else:
                            print(f"{title}: This job already submitted.\n")
                    else:
                        print(f"{title}: This job is not suitable for you.\n")

                    self.page.go_back()
                    time.sleep(3)

                except Exception as e:
                    print(f"An error occurred while processing a job listing: {e}")

        except Exception as e:
            print(f"An error occurred while searching for jobs: {e}")

    def __turns_off_and_on_easy_apply(self):
        try:
            easy_apply_button = self.page.query_selector('button[aria-label="Easy Apply filter."]')
            if easy_apply_button:
                easy_apply_button.click()
                time.sleep(1)
                self.easyApply = not self.easyApply
        except Exception as e:
            print(f"An error occurred while applying the filter: {e}")

    def __jobs_published_last_24_hours(self):
        try:
            # Open the "Date posted" filter dropdown
            self.page.click('#searchFilter_timePostedRange')
            time.sleep(2)

            # Select the "Past 24 hours" option
            self.page.click('label[for="timePostedRange-r86400"]')
            time.sleep(1)

            # Click the "Show results" button by its id
            self.page.click('#ember1775')
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred while applying the filter: {e}")

    def __experience_level(self, level):
        try:
            self.page.click('#searchFilter_experience')
            time.sleep(2)

            if level.lower() == 'entry level':
                self.page.click('//input[@id="experience-2"]/following-sibling::label')
                time.sleep(1)
                self.page.click('//input[@id="experience-1"]/following-sibling::label')
            else:
                self.page.click('//input[@id="experience-4"]/following-sibling::label')

            time.sleep(3)
            self.page.click('//button[contains(@aria-label, "Apply current filter to show") and contains(@class, "artdeco-button--primary")]')
            time.sleep(3)

        except Exception as e:
            print(f"An error occurred while applying the experience level filter: {e}")

    def __easy_apply(self):
        try:
            easy_apply_button = self.page.query_selector('div.jobs-apply-button--top-card button')
            if easy_apply_button:
                easy_apply_button.click()
                time.sleep(1)
                submit_button = self.page.query_selector('button[aria-label="Submit application"]')
                if submit_button:
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

    def logout(self):
        if not self.isLogin:
            print("Not logged in. No need to log out.")
            return
        try:
            self.page.goto('https://www.linkedin.com/m/logout/')
            time.sleep(3)
            self.stop_playwright()  # Ensure the browser and playwright are stopped
            self.isLogin = False
            print("Logged out successfully.")
        except Exception as e:
            print(f"An error occurred during logout: {e}")
