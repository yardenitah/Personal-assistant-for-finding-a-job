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
