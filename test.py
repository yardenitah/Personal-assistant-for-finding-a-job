from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# connect to database
client = MongoClient(os.getenv("DB_URI"))

# Connect to the database and collection
db = client["JobsDB"]
collection = db["MyJobs"]

# Example: Insert a document
job_entry = {
    "company_name": "Example Corp33",
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
# Use DB