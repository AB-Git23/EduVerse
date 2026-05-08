# EduVerse

EduVerse is a scalable online learning platform built with Django and Django REST Framework.  
The platform provides course management, enrollments, instructor verification, reviews, payments, and analytics through a RESTful API architecture.

---

## Features

- JWT Authentication System
- Instructor Verification Workflow
- Course Management
- Lesson Management
- Student Enrollments
- Reviews & Ratings
- Payment Integration
- Analytics System
- RESTful API Architecture
- Swagger API Documentation

---

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### Authentication
- JWT Authentication
- Djoser

### Database
- SQLite (development)
- MySQL (planned migration)

### Documentation
- drf-spectacular
- Swagger UI

---

## Project Structure

```bash
academy/
analytics/
courses/
enrollments/
frontend/
lessons/
payments/
reviews/
users/
```

---

## API Features

- Authentication APIs
- Course APIs
- Enrollment APIs
- Review APIs
- Instructor APIs
- Lesson APIs
- Payment APIs

---

## Installation

```bash
git clone https://github.com/AB-Git23/eduverse-platform.git
cd eduverse-platform
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start development server:

```bash
python manage.py runserver
```

---

## Future Improvements

- Docker support
- CI/CD pipeline
- PostgreSQL support
- Real-time notifications
- Production deployment
- Advanced analytics dashboard

---

## Author

Abdul Basit

GitHub: https://github.com/AB-Git23
