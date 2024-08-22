# Personal-assistant-for-finding-a-job

## Overview

PayChatm is a Python-based project designed to automate the process of job applications and manage job-related data. The system leverages Selenium for LinkedIn automation, MongoDB for database management, and OpenAI for analyzing job descriptions. The project is tailored for users seeking to streamline the job application process, including submitting resumes, tracking applications, and analyzing success rates.

## Features

- **LinkedIn Automation**: Automatically login, search for jobs, and apply to positions on LinkedIn.
- **Resume Management**: Compare success rates between different versions of your resume.
- **Email Response Tracking**: Check for and process new email responses from potential employers.
- **Database Management**: Store and manage job application data using MongoDB.
- **Data Analysis**: Generate reports on application success rates based on various factors (e.g., resume version, application method).
- **Excel Export**: Export job application data to Excel for further analysis.

## Project Structure

- **LinkedInManager.py**: Handles LinkedIn job search and application automation.
- **DBManager.py**: Manages job application data using MongoDB.
- **EmailManager.py**: Connects to your email to track responses from employers.
- **ExcelManager.py**: Provides functionality to export job data to Excel and perform basic analysis.
- **main.py**: The main script that integrates all components and provides a command-line interface for the user.

## Setup

### Prerequisites

- Python 3.x
- MongoDB
- ChromeDriver (for Selenium)
- Gmail account with IMAP enabled (for email tracking)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/PayChatm.git
   cd PayChatm
