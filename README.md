
```markdown
# Leave Management System

A Django-based Leave Management System to handle leave requests and approvals with role-based access.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration with role-based access.
- Leave request submission by employees.
- Leave approval by managers.
- View leave requests by HR and managers.
- JWT authentication for secure API access.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Leave-Management-API.git
   cd Leave-Management-API
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment**

   On Windows:
   ```bash
   .\env\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source env/bin/activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`.

## Setup

## Running the Application

1. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

2. **Access the Application**

   Open your browser and navigate to `http://127.0.0.1:8000/`.

## API Endpoints

- **User Registration**

  - **POST** `/register/`
  - Request Body: `{ "first_name": "John", "last_name": "Doe", "username": "johndoe", "email": "john@example.com", "password": "yourpassword", "role": "EMPLOYEE" }`
  
- **Submit Leave Request**

  - **POST** `/leave_request/`
  - Request Body: `{ "AssignedManager": 1, "reason": "Sick leave" }`

- **List Managers**

  - **GET** `/managers_list/`

- **View Leaves for HR**

  - **GET** `/hr_view_leaves/`

- **View Leaves for Managers**

  - **GET** `/manager_view_leaves/`

- **Approve Leave**

  - **PATCH** `/manager_approve_leave/<id>/`
  - Request Body: `{}`

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


For further documentation and API details, refer to the Django REST framework [documentation](https://www.django-rest-framework.org/).

Feel free to modify it based on any additional features or specifics of your project!