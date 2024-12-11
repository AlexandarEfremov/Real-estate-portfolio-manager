# Real Estate Portfolio Manager

![image](https://github.com/user-attachments/assets/c0e68119-ea38-46c6-a4c3-2bfeb529d0b1)


## Overview

Real Estate Portfolio Manager is a Django-based web application designed to help users manage their real estate investments. The platform provides tools for property management, tenant tracking, financial calculations, and more. This repository contains the source code and necessary configurations to run the application locally or on a server.

---

## Features

- **Accounts Management:** User authentication and profile management.
- **Property Management:** Add, view, and manage property details.
- **Tenant Management:** Track tenant information and rental agreements.
- **Finance Tools:** Calculate investment returns and manage financial records.
- **API Access:** Calculator API for performing various real estate-related calculations.
- **Media Handling:** Upload and manage property-related images and documents.
- **Admin Dashboard:** Includes groups "Staff" and "Admins" with specific permissions for user and property management.
- **Hybrid MVT and REST Architecture:** Combines Django's traditional Model-View-Template architecture with REST API features for flexibility and scalability.

---

## Project Structure

### Main Directory
```
real_estate_manager/
|-- manage.py             # Main entry point for Django commands
|-- media/                # Directory for user-uploaded media files
|-- real_estate_manager/  # Main application folder
|-- static/               # Static assets (CSS, JS, images, etc.)
|-- templates/            # HTML templates for the application
```

### Application Directory: `real_estate_manager`
```
real_estate_manager/
|-- __init__.py          # Marks the directory as a Python package
|-- asgi.py              # ASGI configuration for the project
|-- wsgi.py              # WSGI configuration for the project
|-- settings.py          # Main settings file for the Django project
|-- urls.py              # URL routing configuration
|-- forms.py             # Centralized form definitions
|-- tests/               # Test cases for the application
|-- accounts/            # Handles user accounts and authentication
|-- calculator_api/      # API for financial calculations
|-- finance/             # Finance-related models and logic
|-- properties/          # Property management logic
|-- tenants/             # Tenant management logic
```

---

## Getting Started

### Prerequisites
- Python 3.x
- Django 4.x (or compatible version)
- PostgreSQL (optional, can be configured with SQLite for testing)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/real-estate-portfolio-manager.git
    cd real-estate-portfolio-manager
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

6. Access the application in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Configuration

- **Database:**
  Configure the database in `settings.py` under the `DATABASES` section.

- **Static Files:**
  Collect static files using:
  ```bash
  python manage.py collectstatic
  ```

- **Environment Variables:**
  Use a `.env` file to store sensitive information like database credentials, secret keys, etc.

  **Note:** Sensitive data has been deliberately left exposed in this repository for the ease of the proctor evaluating the project. In a production environment, all sensitive data should be stored securely in an `.env` file and never exposed in the codebase.

---

## Admin Dashboard

The application includes an admin dashboard with two predefined groups:

1. **Admins:**
   - Full permissions across all modules.
   - Can add, view, edit, and delete users, properties, tenants, and financial records.

2. **Staff:**
   - Limited permissions tailored for operational needs.
   - Can view and manage properties, tenants, and limited finance records but cannot delete critical data.

These groups and their permissions are automatically configured during migrations.

---

## Hybrid MVT and REST Architecture

The application includes a Return on Investment (ROI) Calculator that demonstrates its hybrid nature. It offers both a traditional HTML form-based interface and a REST API endpoint for calculation:

- **Template-based View:** Users can calculate ROI using a form rendered in HTML and processed server-side.
- **API Endpoint:** A dedicated API endpoint accepts JSON payloads and returns ROI results, enabling integration with other systems.

This dual approach showcases the flexibility of Django, supporting both dynamic web applications and API-driven integrations.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgements

- [Django Framework](https://www.djangoproject.com/)

