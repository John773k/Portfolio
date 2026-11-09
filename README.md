# Palipe John Paul — Developer Portfolio

A responsive creative-developer portfolio powered by Flask, SQLite, HTML, CSS and JavaScript. Includes a protected admin dashboard to manage projects and review contact messages.

## Features
- Responsive single-page portfolio with animated hero, theme toggle and mobile navigation
- Projects loaded dynamically from SQLite
- Contact form that stores messages in the database
- Admin dashboard to create, edit and delete projects, upload project images, and manage messages
- Password hashing support through environment variables

## Run locally

### 1. Install Python
Use Python 3.10 or newer.

### 2. Create and activate a virtual environment
Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the application
```bash
python app.py
```
Open http://127.0.0.1:5000

## Admin dashboard
Open http://127.0.0.1:5000/admin/login

Development default:
- Username: `admin`
- Password: `ChangeMe123!`

**Change these before deployment.** For a safer setup, set environment variables:
- `SECRET_KEY`: long random secret
- `ADMIN_USERNAME`: admin username
- `ADMIN_PASSWORD_HASH`: Werkzeug password hash

Generate a password hash:
```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-strong-password'))"
```
Then set the printed value as `ADMIN_PASSWORD_HASH`.

Windows PowerShell example:
```powershell
$env:SECRET_KEY="replace-with-a-long-random-secret"
$env:ADMIN_USERNAME="your-admin-name"
$env:ADMIN_PASSWORD_HASH="paste-generated-hash"
python app.py
```

macOS/Linux:
```bash
export SECRET_KEY="replace-with-a-long-random-secret"
export ADMIN_USERNAME="your-admin-name"
export ADMIN_PASSWORD_HASH="paste-generated-hash"
python app.py
```

## Customize
- Edit your intro, about text, skills and social links in `templates/index.html`.
- Add projects through the admin dashboard.
- Add your resume at `static/files/resume.pdf` and update the Resume link in `index.html`.
- Replace the placeholder social URLs with your real profiles.
- Optional profile image: add `profile.jpg` to `static/images/` and update the hero image in `index.html`.

## Important before going live
- Set a strong `SECRET_KEY` and admin password hash.
- Run behind a production WSGI server (for example Gunicorn) with debug mode off.
- Use HTTPS and configure your hosting platform's environment variables.
- Add CSRF protection and rate limiting before exposing the contact/admin forms to the public internet.
- Back up `instance/portfolio.db` and uploaded images.
