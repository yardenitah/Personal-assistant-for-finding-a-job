from DBManager import DBManager  

manager = DBManager()  

name = "Nir Shemer"

# jobList = manager.get_job_links_by_hr_name(name)
# if jobList:
#     for index, job in enumerate(jobList):
#         print(f"{index + 1}) {job}\n")
# else:
#     print(f"No jobs found for {name}.")

# if manager.does_hr_have_job(name, "Mal-Tech secure your assets", "systems engineer"):
#     print("exist")
# else:
#     print("not exist")
    
# jobs = manager.get_jobs_by_company_name("Mal-Tech secure your assets")
# for index, job in enumerate(jobs):
#     print(f"\n{index + 1}) {job}\n")

manager.export_hr_submitted_jobs_to_excel()
