pyrifera
========

Data visualization app for the National Park Service Kelp Forest Monitoring program

Developer Installation Notes
============================

Cloning the repo
----------------

You'll need git installed, then run the following from the command line in a directory
where you would like pyrifera to be installed.

```
git clone git@github.com:underbluewaters/pyrifera.git
cd pyrifera/pyrifera
pip install -r requirements.txt
```

```
echo "DROP DATABASE pyrifera;" | psql -h localhost
echo "CREATE DATABASE pyrifera;" | psql -h localhost
echo "create extension postgis;" | psql -h localhost pyrifera
head -n 3 settings_local.py.template > settings_local.py
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


```
python manage.py syncdb
```

```
python manage.py migrate
python manage.py site localhost:8000
python manage.py install_media
python manage.py rebuild_index
python manage.py clear_cache
```

```
python manage.py runserver
```
