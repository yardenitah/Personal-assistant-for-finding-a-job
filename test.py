from pymongo import MongoClient

# Replace the <username>, <password>, <cluster-url>, and <dbname> with your details
client = MongoClient("mongodb+srv://admin-yarden:yarden1169@cluster0.z9ikx3b.mongodb.net/JobsDB")

# Connect to the database and collection
db = client["JobsDB"]
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
# Use DB