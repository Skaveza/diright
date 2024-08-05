# Diright: Healthcare Diagnostic Website
Diright is a healthcare diagnostic website designed to help doctors diagnose patient symptoms efficiently. This application assists doctors with accurate diagnostic results through an intuitive user interface and advanced backend functionality.

# Key Features
User-Friendly UI/UX: Designed for easy navigation and usability.
Symptom Submission: Allows doctors to submit symptoms via a simple interface.
Accurate Diagnosis: Provides diagnostic results based on symptoms.

# Technology Stack and Tools
# Front End Development
HTML: Structure of web pages.
CSS: Styling and layout.
JavaScript: Interactivity and dynamic content.
# Back End Development
Flask: Web framework for Python.
Python: Programming language for backend logic.
Machine Learning: Utilized for diagnostic algorithms.
Code Editor: Visual Studio Code used for development.
Database
MySQL: Relational database management system for storing data.
Authentication
Flask Login: Used for user authentication.
Version Control and Management
GitHub: Platform for version control and collaborative development.
Deployment
Render: Platform used for deploying the application.

# Steps for Deployment
1. Clone the Repository
First, clone the repository to your local machine:
git clone https://github.com/Skaveza/diright.git:
cd diright

2. Create and Activate a Virtual Environment:
python -m venv venv
source venv/bin/activate

3. Install Dependencies
Install the necessary dependencies from the requirements.txt file:
pip install -r requirements.txt

4. Configure Environment Variables
Set up the environment variables needed for the application.
e.g:
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=mysql://username:password@localhost/dbname

5. Set Up the Database
Ensure you have MySQL installed and running. Create a new database for the project:
CREATE DATABASE diright;
Update your .env file with the correct database URL.

6. Initialize the Database
Run the following commands to set up the database schema:
flask db init
flask db migrate
flask db upgrade

7. Run the Application Locally
Start the Flask development server:
flask run or python main.py

8. Deploying to Render
Create a New Web Service:

Go to the Render dashboard and click on "New" and then "Web Service".
Connect Your Repository:

Select the repository you want to deploy from the list of connected repositories.
Configure the Deployment:

Environment: Select Python 3.
Build Command: pip install -r requirements.txt
Start Command: flask run
Environment Variables: Add the necessary environment variables (as configured in the .env file).
Deploy:

Click on "Create Web Service". Render will start the deployment process.

9. Post-Deployment
After deploying, ensure that:

The website is accessible via the URL provided by Render.
All functionalities are working as expected.
Monitor logs and performance metrics via the Render dashboard.

10. Troubleshooting
If you encounter issues during deployment, consider the following steps:

Check Logs: Render provides logs to help diagnose issues.
Review Configuration: Ensure all environment variables and settings are correctly configured.
Consult Documentation: Refer to the official Render documentation for specific troubleshooting steps.
Seek Help: Reach out to the Render community or support channels for assistance.
