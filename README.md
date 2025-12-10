# Django Task Manager API

## Setup

1. Clone the repository:
git clone <repo-url>
cd taskmanager

cpp
Copy code

2. Create virtual environment:
python -m venv venv

Windows
venv\Scripts\activate

Linux/Mac
source venv/bin/activate

markdown
Copy code

3. Install requirements:
pip install -r requirements.txt

markdown
Copy code

4. Run migrations:
python manage.py makemigrations
python manage.py migrate

pgsql
Copy code

5. Create superuser (optional for Admin):
python manage.py createsuperuser

markdown
Copy code

6. Start server:
python manage.py runserver

yaml
Copy code

---

## Authentication

### Register
`POST /api/auth/register/`
```json
{
  "username": "pooja",
  "email": "pooja@gmail.com",
  "password": "123456"
}
Login
POST /api/auth/login/

json
Copy code
{
  "username": "pooja",
  "password": "123456"
}
Response:

json
Copy code
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
Refresh Token
POST /api/auth/refresh/

json
Copy code
{
  "refresh": "<refresh_token>"
}
