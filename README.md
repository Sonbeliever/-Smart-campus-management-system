Smart Campus Management System

This project runs well on PythonAnywhere for testing because it keeps SQLite data
and uploaded files on persistent storage.

**PythonAnywhere Setup**

1. Create a Python 3.13 web app on PythonAnywhere using a manual Flask setup.
2. Open a Bash console and clone this repo into your home directory.
3. Create a virtualenv and install dependencies:
   `python3.13 -m venv ~/.virtualenvs/smart-campus`
   `source ~/.virtualenvs/smart-campus/bin/activate`
   `pip install -r ~/KASU-QR_ATTENDANCE\ -SYSTEM-UPGRADE/requirements.txt`
4. In the Web tab, set the virtualenv to:
   `~/.virtualenvs/smart-campus`
5. Edit the PythonAnywhere WSGI file and replace its contents with:
   `import sys`
   `path = '/home/YOUR_USERNAME/KASU-QR_ATTENDANCE -SYSTEM-UPGRADE'`
   `if path not in sys.path: sys.path.insert(0, path)`
   `from pythonanywhere_wsgi import application`
6. Reload the web app.

**Persistent Data**

- The PythonAnywhere entrypoint in `pythonanywhere_wsgi.py` stores the database in:
  `~/.smart-campus-data/attendance.db`
- Uploaded profile photos, QR codes, and receipts are stored in:
  `~/.smart-campus-data/media/`
- This keeps your test data and images across reloads and deploys.

**Default Login**

- Username: `superadmin`
- Password: `admin123`
