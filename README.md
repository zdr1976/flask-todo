# ToDo App

This simple `Flask` To-Do application demonstrate how easy it is to prototype
web application in `Python`.

## Python Virtual Environment

To-Do application use packages and modules that don’t come as part of the
standard library. This means it may not be possible for one `Python`
installation to meet the requirements of every application. 

The solution for this problem is to create a [virtual environment](https://docs.python.org/3/glossary.html#term-virtual-environment),
a self-contained directory tree that contains a Python installation for a
particular version of Python, plus a number of additional packages.

You need to create this virtual environment under project directory you just
cloned!

```bash
$ git clone https://github.com/zdr1976/flask-todo.git
$ cd flask-todo
$ python3.7 -m venv venv
```

This will create the **venv** directory if it doesn’t exist, and also create
directories inside it containing a copy of the `Python` interpreter, the standard
library, and various supporting files.

Once you’ve created a virtual environment, you may activate it.
```bash
$ source venv/bin/activate
or
$ . venv/bin/activate
```

You should deactivate virtual environment with:
```bash
(venv) $ deactivate
```

### Managing Packages With Pip
Before you can run this application locally you need to install couple of
packages the portal is depending on. You can install those packages using a
program called *pip* *pip3*.
```bash
(venv) $ pip install flask flask-wtf flask-sqlalchemy flask-migrate
```

or you can use `requirements.txt` file:
```bash
(venv) $ pip install -r requirements.txt
```

## Flask Migrate or Howto manage Database
`Flask-Migrate` is an extension that handles `SQLAlchemy` database migrations
for `Flask` applications using `Alembic`.

You can create migration repository with the following command:
```bash
(venv) $ FLASK_APP=todo.py flask db init
```

This will add a **migrations** folder to our application. The contents of this
folder need to be added to version control.

You can then generate an initial migration:
```bash
(venv) $ FLASK_APP=todo.py flask db migrate
```

The migration script needs to be reviewed and edited, as Alembic currently
does not detect every change you make to your models. In particular, Alembic is
currently unable to detect table name changes, column name changes, or
anonymously named constraints.

Then you can apply the migration to the database:
```bash
(venv) $ FLASK_APP=todo.py flask db upgrade
```

Then each time the database models change repeat the migrate and upgrade commands.

## Run it
To star this `Flask` To-Do application run.
```bash
(venv) $ python todo.py
```

