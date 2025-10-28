# Mini Project 3

It is a Flask-based web application called TaskBoard that allows users to register, log in, and manage personal tasks.
Each user can create, categorize, and mark tasks as complete through an intuitive Bootstrap interface with modals. 
The app uses an SQLite database with three tables linked by foreign keys(`users`,`categories`,`tasks`)

---

## Installation

To install, clone the repository and install the required packages:

```bash
git clone https://github.com/<YourUsername>/MiniProject3---IlliaIvanov.git
cd MiniProject3-IlliaIvanov
pip install -r requirements.txt
```
## Usage

Before running the web app, initialize the SQLite database by executing:

```bash
python init_db.py
```
This will create the `instance/taskboard.db` database file and seed default categories such as:
* General
* Study
* Work

After initializing the database, start the Flask development server:

```
python run.py
```

then open your browser and go to:
```
http://127.0.0.1:5000
```

you can register a new user, log in, and begin creating tasks.


## Project Structure
```
MiniProject3---IlliaIvanov/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── forms.py
│   ├── models.py
│   ├── static/
│   │   └── css/
│   │       └── styles.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── categories.html
│       └── tasks.html
│
├── instance/
│   └── taskboard.db
│
├── init_db.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```
