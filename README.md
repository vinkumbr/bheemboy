bheemboy
========

bheemboy is a webapp for organizing course registrations at academic institutions.

Dependencies
------------

- Python 2.7
- django 1.9

How to deploy
-------------

- Obtain a stable release of bheemboy.
- We recommend [PostgreSQL](http://www.postgresql.org/) database for production use.
Install it, create a database and a user, and grant all permissions for the DB to the created user.
- Edit `<proj_root>/bheemboy/bheemboy/settings.py` and give a value to `SECRET_KEY`, add auth details to `DATABASES`, and set `DEBUG` to False.
- In `<proj_root>/bheemboy`, run `python manage.py migrate`.
- Test if the app is working by running `python manage.py runserver` and going to [localhost:8000/sudo](http://localhost:8000/sudo).
- Set-up a production-grade webserver such as `gunicorn` to run on start-up and configure a reverse proxy like `nginx` to proxy requests to it.
- Set-up the system to server static files at `/static/*` from `<proj_root>/bheemboy/coursereg/static/*`.

Notes for devs
--------------

- To test drive this app, run `python manage.py runserver` and goto
[localhost:8000/sudo](http://localhost:8000/sudo).
- The email address of the super-user in the SQLite database shipped with this
repo is `admin@ece.iisc.ernet.in` and the password is `test12345`.
- Using the admin login we could add users and courses and modify existing user's passwords.
- Currently the a simple student page has been setup through which we could register to courses and track their approval process.
- To tryout an individual st login, first log in as admin, create a new student or modify an existing student's password. Log out and go to [localhost:8000/] and re-log in with student ID.