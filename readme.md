Here is a concise and clear `README.md` file description based on the provided project requirements:

---

# Job Portal System

This repository contains the backend design for a **Job Portal System**. The platform includes user authentication, profile management, job listings, and administrative features tailored for job seekers, employers, and administrators.

---

## Features

### 1. **Authentication**
- **Sign Up**: Users can create an account; email verification is required.
- **Login**: Secure login to the platform.
- **Change Password**: Update account password.
- **Forgot Password**: Request a password reset via email verification.
- **Email Verification**: Links for verifying email addresses and resetting passwords are sent via email.

---

### 2. **User Profiles**
#### **Job Seeker Profile**
Fields:
- First Name, Last Name, Email, Gender, Date of Birth
- Qualification, CV Upload, Country, City
- Profile Image

Endpoints:
- Create/Update Profile: `POST /profile/job-seeker`, `PUT /profile/job-seeker`

#### **Employer Profile**
Fields:
- First Name, Last Name, Email, Gender, Date of Birth
- Company Name, Country, City, Company Size, Logo

Endpoints:
- Create/Update Profile: `POST /profile/employer`, `PUT /profile/employer`

---

### 3. **Job Listings**
#### **Guest Access**
- View 20 latest job posts with search filters and pagination: `GET /jobs`

#### **Logged-In Access**
- Additional details like salary range and apply buttons.

#### **Job Profile**
- Endpoint: `GET /jobs/<id>`
- Displays company and job details.

#### **Employer Job Management**
- Create Job Post: `POST /jobs`
- View Employer’s Jobs: `GET /jobs/my-jobs`
- Update Job Post: `PUT /jobs/<id>`
- Toggle Job Post Status: `PUT /jobs/<id>/toggle`
- View Applicants: `GET /jobs/<id>/applicants`
- Update Applicant Status: `PUT /jobs/<id>/applicants/<applicant_id>/status`

---

### 4. **Job Applications and Notifications**
#### **Job Seeker Applications**
- Apply to Job: `PUT /jobs/<id>/apply`
- View My Applications: `GET /jobs/my-applications`

#### **Notifications**
- Job Seeker Notifications: `GET /notifications`
- Employer Notifications: `GET /notifications`

---

### 6. **Guest Features**
- Homepage: Displays the latest 20 job listings with filters for city, country, job type, and company.

---


Here's the setup guide in `README.md` format:

---

# Django REST Framework Project Setup

This guide provides step-by-step instructions for setting up the Django REST Framework project with the specified libraries.

---

## Prerequisites

- Python 3.8+
- Virtual environment tool (e.g., `virtualenv`)
- Up-to-date `pip` (`python -m pip install --upgrade pip`)

---

## Step 1: Clone the Repository

Clone the project repository and navigate into the project directory:

```bash
git clone <repository_url>
cd <project_directory>
```

---

## Step 2: Create and Activate Virtual Environment

Set up a virtual environment to manage dependencies:

```bash
# Create the environment
python -m venv venv

# Activate the environment
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate
```

---

## Step 3: Install Required Libraries

Install the dependencies specified in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Step 4: Configure the Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```plaintext
DJANGO_EMAIL_HOST_PASSWORD=<your_email_host_password>
DJANGO_EMAIL_HOST_USER=<your_email_host_user>
CLOUDINARY_API=<your_cloudinary_api_key>
CLOUDINARY_SECRET=<your_cloudinary_secret>
```

> **Note:** Ensure the `.env` file is added to `.gitignore` to prevent it from being committed to version control.

---

## Step 5: Initial Project Setup

Run the following commands to configure the application:

### Apply Migrations
```bash
python manage.py migrate
```


---

## Step 6: Start the Development Server

Run the development server to start the application:

```bash
python manage.py runserver
```

Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).


## Additional Configuration

### Cloudinary Integration

Add the following to `cloudinary.py` for Cloudinary configuration:

```python
import cloudinary

cloudinary.config(
    cloud_name='<your_cloud_name>',
    api_key=os.getenv('CLOUDINARY_API'),
    api_secret=os.getenv('CLOUDINARY_SECRET')
)
```


## Libraries Used

- **`djangorestframework`**: Core REST API functionality
- **`djangorestframework-simplejwt`**: JWT-based authentication
- **`drf-yasg`**: Swagger API documentation
- **`django-filter`**: Advanced query filtering
- **`django-otp` and `pyotp`**: Two-factor authentication
- **`cloudinary`**: Media file storage
- **`python-dotenv`**: Environment variable management

paste the above libraries in the requirement.txt file.

---

This setup ensures seamless integration of all libraries and services. If you encounter any issues, feel free to create a new issue or contact the maintainer.