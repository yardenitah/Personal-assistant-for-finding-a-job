from LinkedInManager import LinkedInManager
from DBManager import DBManager  # Updated from ExcelManager to DBManager
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    manager = DBManager()  # Updated to use DBManager
    linkedin_username = os.getenv('LINKEDIN_USERNAME')
    linkedin_password = os.getenv('LINKEDIN_PASSWORD')
    openai_api_key = " "
    job_title_list = ["backend engineer", "software engineer student", "software engineer intern", "Elbit", "backend", "Java", "Python"]
    # job_title_list = ["Java", "backend engineer", "software engineer student", "software engineer intern", "Elbit", "backend", "Python"]

    resume_A_path = "/Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/CV_A.pdf"
    resume_B_path = "/Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/CV_B.pdf"
    user_description = os.getenv('USER_DESCRIPTION')
    linkedin_manager = LinkedInManager(linkedin_username, linkedin_password, openai_api_key, resume_A_path, resume_B_path)

    while True:
        print("1. Add new line.")
        print("2. Which version of CV is better.")
        print("3. Compare submission methods (HR vs Website).")
        print("4. Analyze preferences by submission method (HR vs Website).")
        print("5. Get company names by answer.")
        print("6. Plot CV success rates.")
        print("7. Apply for jobs on LinkedIn.")
        print("8. Delete jobs before 2024.")
        print("9. Edit a line by company name.")
        print("10. Delete lines by company name.")
        print("11. Export all jobs to Excel.")
        print("12. Exit")

        choice = input("Enter your choice: ")
        print("\n")

        if choice == '1':
            company_name = input("Enter company name: ") or ""
            link = input("Enter link (Optional): ") or ""
            title = input("Enter title (optional): ") or ""
            cv_version = input("Enter CV version: ") or ""
            hr_or_website = input("Enter HR or website (optional): ") or ""

            manager.add_line(company_name, link, title, cv_version, hr_or_website)
            print("New line added successfully.\n")

        elif choice == '2':
            avg_cv_a, avg_cv_b = manager.get_avg_of_cv_versions()
            print(f"Average positive response rate for CV version A: {avg_cv_a:.2f}")
            print(f"Average positive response rate for CV version B: {avg_cv_b:.2f}")

        elif choice == '3':
            hr_success_rate, website_success_rate = manager.compare_submission_methods()
            print(f"Success rate for HR submissions: {hr_success_rate:.2f}")
            print(f"Success rate for website submissions: {website_success_rate:.2f}")

        elif choice == '4':
            preferences = manager.analyze_preference_by_submission_method()
            print(f"HR liked CV A {preferences['HR']['CV A']} times and CV B {preferences['HR']['CV B']} times.")
            print(f"Websites liked CV A {preferences['Website']['CV A']} times and CV B {preferences['Website']['CV B']} times.")

        elif choice == '5':
            positive_companies, negative_companies = manager.get_company_names_by_answer()
            print(f"Companies with positive answers: {positive_companies}")
            print(f"Companies with negative answers: {negative_companies}")

        elif choice == '6':
            manager.plot_success_rates()

        elif choice == '7':
            linkedin_manager.login()
            for job_title in job_title_list:
                linkedin_manager.search_jobs(job_title, user_description)

        elif choice == '8':
            manager.delete_jobs_before_2024()

        elif choice == '9':
            company_name = input("Enter the company name to edit: ")
            link = input("Enter new link (leave blank to keep current): ") or None
            title = input("Enter new title (leave blank to keep current): ") or None
            cv_version = input("Enter new CV version (leave blank to keep current): ") or None
            hr_or_website = input("Enter new HR or website (leave blank to keep current): ") or None

            manager.edit_line_by_company_name(company_name, link, title, cv_version, hr_or_website)

        elif choice == '10':
            company_name = input("Enter the company name to delete: ")
            manager.delete_lines_by_company_name(company_name)

        elif choice == '11':
            output_file_path = input("Enter the output Excel file path (default: JobsExport.xlsx): ") or "JobsExport.xlsx"
            manager.export_jobs_to_excel(output_file_path)

        elif choice == '12':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
