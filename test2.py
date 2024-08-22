from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the credentials and URL from the environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_url = os.getenv("MONGO_CLUSTER_URL")
dbname = os.getenv("MONGO_DBNAME")

# Create the MongoDB connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/{dbname}"

# Connect to the MongoDB cluster
client = MongoClient(connection_string)

# Connect to the database and collection
db = client[dbname]
collection = db["MyJobs"]

# Example: Insert a document
job_entry = {
    "company_name": "Example Corp",
    "job_title": "Software Engineer",
    "job_link": "https://example.com/job/123",
    "date_sent": "2024-08-10",
    "cv_version": "A",
    "submission_method": "website",
    "answer": "waiting",
    "answer_date": None
}

collection.insert_one(job_entry)
print("Job entry inserted successfully.")


# def __connectToHR(self):
#     try:
#         # Wait for the HR profile link/button to be clickable and click it
#         getProfile_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH,
#                  "//div[contains(@class,'hirer-card__hirer-information')]//strong[contains(text(), '')]")
#             )
#         )
#         getProfile_button.click()
#
#         # Switch to the new window/tab that opens for the HR profile
#         self.driver.switch_to.window(self.driver.window_handles[-1])
#         time.sleep(2)
#
#         connect_button = WebDriverWait(self.driver, 10).until(  # Wait for the "Send" button to be present
#             EC.presence_of_element_located(
#                 (By.XPATH, "//div[@class='pvs-profile-actions__action']//button[contains(., 'Connect')]")
#             )
#         )
#         connect_button.click()  # Click the "Send" button
#
#         time.sleep(2)
#         try:
#             send_without_note_button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable(
#                     (By.XPATH,
#                      "//button[@aria-label='Send without a note' and contains(@class, 'artdeco-button--primary')]")
#                 )
#             )
#             send_without_note_button.click()
#         except Exception as e:
#             print("No needed send_without_note_button")
#         # After clicking the "Connect" button, close the current window/tab
#         self.driver.close()
#         self.driver.switch_to.window(self.driver.window_handles[0])
#         return True
#
#     except Exception as e:
#         print(f"An error occurred while trying to connect to HR: {str(e)}")
#         # If an error occurs, ensure you're back on the main job listing page
#         if len(self.driver.window_handles) > 1:
#             self.driver.close()
#             self.driver.switch_to.window(self.driver.window_handles[0])
#             time.sleep(2)
#             return False

#
# def login(self):
#     options = webdriver.ChromeOptions()
#     # user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome/SeleniumProfile")
#     # options.add_argument(f"user-data-dir={user_data_dir}")
#     # options.add_argument(
#     #     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
#     options.add_argument(
#         "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     )
#     self.driver = webdriver.Chrome(options=options)
#
#     try:
#         self.driver.get('https://www.linkedin.com/login')
#         time.sleep(3)
#
#         try:
#             print(self.username)
#             username_field = self.driver.find_element(By.ID, 'username')
#             username_field.send_keys(self.username)
#             time.sleep(1)
#         except:
#             print("Username already set.")
#         try:
#             print(self.password)
#             password_field = self.driver.find_element(By.ID, 'password')
#             password_field.send_keys(self.password)
#             time.sleep(1)
#             password_field.send_keys(Keys.RETURN)
#         except:
#             print("Login form not found, assuming already logged in or user data already set.")
#             if "feed" in self.driver.current_url:
#                 print("Already logged in!")
#                 self.isLogin = True
#                 return
#             else:
#                 print("Login failed or additional steps required.")
#
#         time.sleep(5)
#
#         if "checkpoint/challenge" in self.driver.current_url:
#             print("Verification needed. Please complete the verification manually.")
#             time.sleep(30)
#         elif "feed" in self.driver.current_url:
#             self.isLogin = True
#             print("Login successful!")
#         else:
#             print("Login failed.")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")


# def __get_job_list(self, job_title, easyApply_filter):
#     self.driver.get('https://www.linkedin.com/jobs/')
#     try:
#         search_box = WebDriverWait(self.driver, 5).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, 'input.jobs-search-box__text-input.jobs-search-box__keyboard-text-input'))
#         )
#         search_box.send_keys(job_title)
#         time.sleep(3)
#         search_box.send_keys(Keys.RETURN)
#         time.sleep(4)
#
#         # self.__jobs_published_last_24_hours()
#         if not self.__experience_level(self.experienceLevel):
#             return
#         self.__jobs_published_last_24_hours()
#         # if (easyApply_filter and not self.easyApplyState) or (not easyApply_filter and self.easyApplyState):
#         #     self.__turns_off_and_on_easy_apply()
#
#         job_listings = self.driver.find_elements(By.CSS_SELECTOR, 'li.jobs-search-results__list-item')
#         print(f'len of job_listings: {len(job_listings)}')
#
#         return job_listings
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None


# def __connectToHR(self):
#     try:
#         profile_element = WebDriverWait(self.driver, 5).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//div[contains(@class,'hirer-card__hirer-information')]//a[contains(@href, '/in/')]")
#             )
#         )
#         hr_name = profile_element.text.strip().split('\n')[0]
#         print(f"HR Name: {hr_name}")
#         profile_link = profile_element.get_attribute('href')
#         print(f"HR Profile Link: {profile_link}")
#         self.driver.execute_script("window.open(arguments[0]);", profile_link)
#         self.driver.switch_to.window(self.driver.window_handles[2])
#         time.sleep(4)
#     except Exception as e:
#         print(f"Could not find HR element or navigate to HR profile: {str(e)}")
#         return False
#
#     try:
#         connect_button = WebDriverWait(self.driver, 5).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, f"(//button[contains(@aria-label, 'Invite {hr_name} to connect')])[2]")
#             )
#         )
#         connect_button.click()
#         time.sleep(2)
#     except Exception as e:
#         fallback_attempts = [
#             "(//button[contains(@class, 'artdeco-button--primary') and .//span[text()='Connect']])[2]",
#             f"(//button[contains(@aria-label, 'Invite {hr_name} to connect') and contains(@class, 'artdeco-button--secondary')])[1]",
#             "//div[@class='pvs-profile-actions__action']//button[span[text()='Connect']]",
#             f"(//button[@aria-label='Invite {hr_name} Shushan to connect'])[2]"
#         ]
#
#         for attempt in fallback_attempts:
#             try:
#                 connect_button = WebDriverWait(self.driver, 5).until(
#                     EC.element_to_be_clickable((By.XPATH, attempt))
#                 )
#                 connect_button.click()
#                 time.sleep(2)
#                 break
#             except Exception as fallback_error:
#                 print(f"Cannot find connect button using fallback: {str(fallback_error)}")
#         else:
#             print(f"Cannot find connect button for {hr_name} after all attempts.")
#             self.driver.close()
#             self.driver.switch_to.window(self.driver.window_handles[1])
#             time.sleep(3)
#             return False
#
#     try:
#         send_without_note_button = WebDriverWait(self.driver, 5).until(
#             EC.element_to_be_clickable(
#                 (
#                 By.XPATH, "//button[@aria-label='Send without a note' and contains(@class, 'artdeco-button--primary')]")
#             )
#         )
#         send_without_note_button.click()
#         print("Connection request sent successfully.")
#         time.sleep(3)
#     except TimeoutException:
#         print("No 'Send now' button found, possibly already connected or another issue.")
#
#     self.__sendWithoutNote()  # Ensure this method is correctly implemented and needed
#     self.driver.close()
#     self.driver.switch_to.window(self.driver.window_handles[1])
#     time.sleep(3)
#     return True


# message = (
#     f"Hi {hr_first_name},\n\n"
#     f"Hi {hr_first_name},I hope you’re doing well!\n\n"
#     f"I’m Yarden, a third-year Software Engineering student. I’m passionate about tackling challenging problems, "
#     f"algorithms, and creative thinking—exactly what excites me about the {job_title} role at {company_name}.\n\n"
#     "I’ve developed strong problem-solving skills through both my studies and mentoring leadership programs. I believe I can "
#     "bring value to your team and would love to chat about how I can contribute.\n\n"
#     "I’d be happy to send you my resume and discuss the opportunity further.\n\n"
#     "Looking forward to hearing from you!\n\n"
#     "Best, Yarden.\n\n"
#     f"Here’s the link to the job posting: {job_link}"
# )


