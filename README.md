# [Demo](http://173.44.119.82:8000)

___

# Library-ETD

Fall 2018 spring 2019 Senior design Project

Electronic Thesis and Dissertation system for the MSState Library

## Requirements

- Python 3.7.2
- Pycharm

## Helpfu Links

- [Flask](http://flask.pocoo.org/) microframework
- [Jinja2](http://jinja.pocoo.org/) Templating Engine
- [Flask-User](https://flask-user.readthedocs.io/en/latest/) User system
  - [Flask-Login](https://flask-login.readthedocs.io/en/latest/) Login system
  - [Flask-Mail](https://pythonhosted.org/Flask-Mail/) Mail Extension
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) Object Relational Mapper
  - [PostgresSQL](https://www.postgresql.org/) Database engine
  - [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) Database Migration
- [Flask-WTForms](https://flask-wtf.readthedocs.io/en/stable/index.html#) Form verification
- [Flask-Assets](https://flask-assets.readthedocs.io/en/latest/) webassets integration
- [Passlib Argon2](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.argon2.html) Password Hashing algorithm
- [Flask-User Configuration settings](https://flask-user.readthedocs.io/en/latest/configuring_settings.html)
- [pycountry](https://pypi.org/project/pycountry/) Country listing
- [arrow](https://arrow.readthedocs.io/en/latest/) Time humanization
- [phonenumbers](https://pypi.org/project/phonenumbers/) Phone number formatting 

# Setup

## Developement

- Clone repo and setup in Pycharm as a flask project
- Setup postgresql database for development
- Make a copy of `/app/local_settings_example.py` and name it `local_settings.py`
  - Edit the `SQLALCHEMY_DATABASE_URI` to point to your database.
  - Input your email server settings
    - Edit the Admin email, this is used in returning email errors
- Edit the password hashing options in `settings.py`

## Deployment

### Docker

- Same as above except no Pycharm
- `DEBUG = False`
- Generate `SECRET_KEY`
- In root of repo, run: (edit the path mappings first)

```docker
#build the container
docker build -t etd:latest .

# deploy the container
docker run --name etd -d -p 8000:8000 -v /path/on/host/submissions:/data/submissions -v /path/on/host/documents:/data/documents -v /path/on/host/signatures:/data/signatures  etd:latest
```

- This will start the container on the machine on port `8000` and the data directories mapped outside the contianer

### Not Docker

Same as above, except run:

```bash
pip install -r requirements.txt
pip install gunicorn
gunicorn -b :8000 -w 4 wsgi:app
```

This will start Gunicorn with 4 workers.

This is the same thing that the Docker container does

# Notes

- `/app/__init__.py` 
  - Main application file
- `/app/main.py`
  - Main route
  - Templates `/app/templates/main`
- `/app/submissions.py`
  - Submissions Route
  - Templates `/app/templates/submissions`
- `/app/revisions.py`
  - Revisions Route
  - Templates `/app/templates/revisions`
- `/app/templates/flask_user/`
  - Flask User Templates
  - `/app/templates/flask_user/emails/`
    - Flask User email templates
- `/app/models.py`
  - Database model definitions
- `/app/schemas.py`
  - Schema definitions
- `/app/commands.py`
  - Custom Flask commands
  - `flask init_db`
    - Initializes database. WARNING: This is destructive and will destroy and existing database
- `/app/static/scss/site.scss`
  - Custom SCSS goes here
