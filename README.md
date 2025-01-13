# ECommerce-Skylander

A fully functional e-commerce website using the Django framework, integrating features such as user authentication
(login/logout), product browsing, cart management, and order placement. Designed a responsive and user-friendly interface,
implemented secure role-based access control, and optimized database handling with Django’s ORM for efficient performance

. Follow the steps below to set up and run the project locally.

---

## Prerequisites

Before getting started, ensure you have the following installed on your machine:

- Python 3.10 or later
- pip (Python package installer)
- Django (will be installed via requirements)

---

## Setup Instructions

1. **Clone the repository**  
   Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   
2. **Install Dependency**
   ```bash
   pip install -r requirements.txt

4. **Create a Superuser**
   ```bash
   python manage.py createsuperuser

5. **Make migrations**
   ```bash
   python manage.py makemigrations

7. **Apply Migrations to Database**
   ```bash
   python manage.py migrate


9. **Run the serve**
   ```bash
   python manage.py runserver
   

  The application will be available at http://127.0.0.1:8000/ by default.
