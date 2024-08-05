# /Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/main.pyfrom CreateExcelFile import CreateExcelFile
from ExcelManager import ExcelManager
from LinkedInManager import LinkedInManager
import datetime


def main():
    excel_path = "/Users/yrdnqldrwn/Desktop/SOFTWARE/PayChatm/Info_aboutCVsubmitted/DATA.xlsx"
    manager = ExcelManager(excel_path)
    linkedin_username = 'yarden1606@gmail.com'
    linkedin_password = 'yarden1169'
    job_title = "software engineer intern"
    linkedin_manager = LinkedInManager(linkedin_username, linkedin_password)

    while True:
        print("1. Add new line.")
        print("2. Which version of CV is better.")
        print("3. Compare submission methods (HR vs Website).")
        print("4. Analyze preferences by submission method (HR vs Website).")
        print("5. Get company names by answer.")
        print("6. Plot CV success rates.")
        print("7. Apply for jobs in Linkedin.")
        print("8. Exit")

        choice = input("Enter your choice: ")
        print("\n")


        if choice == '1':
            company_name = input("Enter company name: ") or ""
            link = input("Enter link (Optional): ") or ""
            title = input("Enter title (optional): ") or ""
            cv_version = input("Enter CV version: ") or ""
            hr_or_website = input("Enter HR or website (optional): ") or ""
            date_sent = datetime.datetime.today().strftime('%Y-%m-%d')  # Format the date as a string
            answer = "No answer"
            answer_date = ""

            new_line = (company_name, link, title, cv_version, hr_or_website, date_sent, answer, answer_date)

            manager.add_line(new_line)
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
            print(
                f"Websites liked CV A {preferences['Website']['CV A']} times and CV B {preferences['Website']['CV B']} times.")

        elif choice == '5':
            positive_companies, negative_companies = manager.get_company_names_by_answer()
            print(f"Companies with positive answers: {positive_companies}")
            print(f"Companies with negative answers: {negative_companies}")

        elif choice == '6':
            manager.plot_success_rates()

        elif choice == '7':
            linkedin_manager.login()
            linkedin_manager.search_jobs(job_title)


        elif choice == '8':
            print("Exiting...")
            break



        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
