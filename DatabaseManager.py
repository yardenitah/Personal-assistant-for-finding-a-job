from pymongo import MongoClient
import datetime

class DatabaseManager:
    def __init__(self, db_uri="mongodb://localhost:27017/", db_name="job_search_db"):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.jobs_collection = self.db['jobs']

    def add_job(self, company_name, link, title, cv_version, hr_or_website):
        job_entry = {
            "company_name": company_name,
            "job_title": title,
            "job_link": link,
            "cv_version": cv_version,
            "submission_method": hr_or_website,
            "date_sent": datetime.datetime.today().strftime('%Y-%m-%d'),
            "answer": "waiting",
            "answer_date": None
        }
        self.jobs_collection.insert_one(job_entry)
        print("New job entry added successfully.")

    def get_avg_of_cv_versions(self):
        pipeline = [
            {"$match": {"answer": "yes"}},
            {"$group": {"_id": "$cv_version", "positive_count": {"$sum": 1}, "total_count": {"$sum": 1}}},
        ]
        results = self.jobs_collection.aggregate(pipeline)

        avg_cv_a = avg_cv_b = 0
        total_cv_a = total_cv_b = 0

        for result in results:
            if result['_id'].lower() == 'a':
                avg_cv_a = result['positive_count'] / result['total_count']
                total_cv_a = result['total_count']
            elif result['_id'].lower() == 'b':
                avg_cv_b = result['positive_count'] / result['total_count']
                total_cv_b = result['total_count']

        return avg_cv_a, avg_cv_b

    def compare_submission_methods(self):
        pipeline = [
            {"$match": {"answer": "yes"}},
            {"$group": {"_id": "$submission_method", "positive_count": {"$sum": 1}, "total_count": {"$sum": 1}}},
        ]
        results = self.jobs_collection.aggregate(pipeline)

        hr_success_rate = website_success_rate = 0

        for result in results:
            if result['_id'].lower() == 'hr':
                hr_success_rate = result['positive_count'] / result['total_count']
            elif result['_id'].lower() == 'website':
                website_success_rate = result['positive_count'] / result['total_count']

        return hr_success_rate, website_success_rate

    def analyze_preference_by_submission_method(self):
        pipeline = [
            {"$match": {"answer": "yes"}},
            {"$group": {"_id": {"submission_method": "$submission_method", "cv_version": "$cv_version"},
                        "count": {"$sum": 1}}}
        ]
        results = self.jobs_collection.aggregate(pipeline)

        preferences = {
            'HR': {'CV A': 0, 'CV B': 0},
            'Website': {'CV A': 0, 'CV B': 0}
        }

        for result in results:
            method = result['_id']['submission_method'].capitalize()
            cv_version = result['_id']['cv_version'].capitalize()
            preferences[method][f'CV {cv_version}'] += result['count']

        return preferences

    def get_company_names_by_answer(self):
        positive_companies = []
        negative_companies = []

        cursor = self.jobs_collection.find({})
        for job in cursor:
            if job['answer'].lower() == 'yes':
                positive_companies.append(job['company_name'])
            else:
                negative_companies.append(job['company_name'])

        return positive_companies, negative_companies

    def delete_jobs_before_2024(self):
        cutoff_date = datetime.datetime(2024, 1, 1)
        result = self.jobs_collection.delete_many({"date_sent": {"$lt": cutoff_date}})
        print(f"Deleted {result.deleted_count} jobs before 2024.")

    def edit_job_by_company_name(self, company_name, link=None, title=None, cv_version=None, hr_or_website=None):
        update_fields = {}
        if link:
            update_fields['job_link'] = link
        if title:
            update_fields['job_title'] = title
        if cv_version:
            update_fields['cv_version'] = cv_version
        if hr_or_website:
            update_fields['submission_method'] = hr_or_website
        if update_fields:
            result = self.jobs_collection.update_one(
                {"company_name": company_name},
                {"$set": update_fields}
            )
            if result.modified_count > 0:
                print(f"Job for company '{company_name}' updated successfully.")
            else:
                print(f"No job found for company '{company_name}' or nothing to update.")
        else:
            print("No fields provided for update.")

    def delete_jobs_by_company_name(self, company_name):
        result = self.jobs_collection.delete_many({"company_name": company_name})
        print(f"Deleted {result.deleted_count} jobs for company '{company_name}'.")