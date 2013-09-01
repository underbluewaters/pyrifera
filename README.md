pyrifera
========

Data visualization app for the National Park Service Kelp Forest Monitoring program

Developer Installation Notes
============================

Dependencies
------------

Before embarking on installing marinemap and pyrifera you'll need the following installed on your system

  * The GIT version control system (try [Github.app](http://mac.github.com/) for OS X or [Git for Windows](http://windows.github.com/))
  * Python 2.7+ (but not 3.0). Included in OS X, [requires installation](http://www.python.org/download/) on Windows
  * [PIP](http://www.pip-installer.org/en/latest/installing.html)
  * PostGIS 2.0 (install [Postgres.app](http://postgresapp.com/) on OS X or follow the GeoDjango Postgres and PostGIS [installation instructions for Windows](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#postgresql)

Cloning the repo
----------------

```
git clone git@github.com:underbluewaters/pyrifera.git
cd pyrifera/pyrifera
pip install -r requirements.txt
```

Database Setup
--------------
**Create the initial database**
```
echo "DROP DATABASE pyrifera;" | psql -h localhost
echo "CREATE DATABASE pyrifera;" | psql -h localhost
echo "create extension postgis;" | psql -h localhost pyrifera
```
**Tell pyrifera where to store media, and how to connnect to the db**
```
head -n 4 settings_local.py.template > settings_local.py
mkdir ../deployed-media
python -c 'import os; print "MEDIA_ROOT=\"" + os.path.abspath("../deployed-media") + "\""' >> settings_local.py 
echo 'MEDIA_URL = "http://localhost:8000/media/"\n' >> settings_local.py
echo 'DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "pyrifera",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}' >> settings_local.py
```

Then set `GOOGLE_ANALYTICS_KEY` to something appropriate for the domain.

**Setup the applications database schema**
```
python manage.py syncdb
```

```
python manage.py migrate
```

Final installation steps
------------------------

```
python manage.py site localhost:8000
python manage.py install_media
```
**Build the search index (drives species search) and clear out any cache**
```
python manage.py rebuild_index
```
```
python manage.py clear_cache
```

Run the application development Server
--------------------------------------
```
python manage.py runserver
```
