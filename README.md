# Helpdesk Lite 🎫

A lightweight **customer support ticket tracker** built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**. Designed as a beginner-friendly full-stack portfolio project.

## Features

- Create tickets with title, description, and priority (Low / Medium / High)
- View all tickets and filter by status
- Update status (Open / In Progress / Resolved)
- Delete tickets with confirmation
- Live dashboard counts
- Persistent SQLite storage, created automatically on first run
- Responsive, dark-themed interface
- JSON REST API with validation and basic automated tests

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, vanilla JavaScript |
| Backend | Python, Flask |
| Database | SQLite |
| API | REST-style JSON endpoints |

## Run locally

**Prerequisite:** Python 3.9+.

```bash
# 1. Clone the repository (or unzip this project)
cd helpdesk-lite

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

> Note: On some Windows machines, use `py` instead of `python`.

## API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tickets` | List tickets |
| POST | `/api/tickets` | Create ticket |
| PATCH | `/api/tickets/<id>` | Update ticket status |
| DELETE | `/api/tickets/<id>` | Delete ticket |

Create example:

```json
{"title": "Cannot log in", "description": "Password reset link expired", "priority": "High"}
```

Update example:

```json
{"status": "In Progress"}
```

## Run tests

From the project folder:

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
helpdesk-lite/
├── app.py                 # Flask app and API endpoints
├── templates/
│   └── index.html         # Dashboard markup
├── static/
│   ├── style.css          # Responsive styling
│   └── app.js             # UI + API calls
├── tests/
│   └── test_app.py        # API tests
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Upload to GitHub

1. Create a new **public** repository named `helpdesk-lite` on GitHub.
2. Extract this ZIP, open a terminal inside the `helpdesk-lite` folder.
3. Run:

```bash
git init
git add .
git commit -m "Initial commit: Helpdesk Lite ticket tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/helpdesk-lite.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Alternatively, use **Add file → Upload files** on your new GitHub repository and upload the *extracted files*, not the ZIP itself.

## Limitations / next steps

This is a **local portfolio demo**, not a production-ready multi-user helpdesk. It has no login, access controls, rate limiting, or CSRF protection. Do not deploy it publicly with real customer data without adding security controls. Suggested improvements: authentication, ticket assignment, search, pagination, PostgreSQL, SLA timers, and automated deployment.

## Resume-ready description

**Helpdesk Lite – Full-Stack Ticket Management System**  
Developed a responsive customer support ticket tracker using Python, Flask, SQLite, and JavaScript, featuring REST APIs, ticket prioritization, status management, dashboard analytics, input validation, and automated API tests.
