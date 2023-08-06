========================
Running The Test Project
========================

#. Make sure you have Django 1.2 or greater and oauth2 at 1.5.163 or greater installed
#. Change directory to la_facebook/test_project
#. python manage.py syncdb
#. python manage.py runserver localhost:8000
#. Open a browser and point to that URL
#. Manually do the tests via your browser

Logging
-------

By default the project will print debug level logging info both to stdout and 
to a log file located at /tmp/la_facebook.log.

Test Coverage
-------------

The test project supports coverage via django-coverage. To enable it you will need on your python path::

    coverage==3.4
    django-coverage==1.1.1

To run coverage at the command-line::

    python manage.py test_coverage la_facebook