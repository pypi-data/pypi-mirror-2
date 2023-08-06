
=====
Usage
=====

This section contains information, including examples, about how to use
*django-postgresql-manager* in your existing Django projects or applications.


Running the example project
===========================
``django-postgresql-manager`` ships with an example Django project which can be
used to demonstrate the application. The example project is located in the
``contrib`` directory.

The following information also exists in the ``contrib/example-project/QUICKSTART``
file and describes the steps to run the example project. By following these
instructions you will be able to use the web-based PostgreSQL manager in a few
seconds.

The example project has the following requirements:

- Django (``pip install Django``)
- Python bindings for SQLite 3 (``pip install pysqlite``)
- Python bindings for PostgreSQL (``pip install psycopg2``)

Once these are installed in your system, create the ``administrator`` role
in your *PostgreSQL Cluster*::

    CREATE ROLE administrator WITH LOGIN CREATEDB CREATEROLE PASSWORD '1234';

Then load the example project's ``settings`` module in any text editor::

    vi settings.py

And make sure the ``postgresql_manager_conn`` database connection settings
are correct, otherwise the Django project won't be able to connect to the
PostgreSQL Cluster.

Next *synchronize* the Django project database (``test.db``)::

    python manage.py syncdb

Make sure you create a ``root`` account when prompted.

Finally run Django's internal web server::

    python manage.py runserver 127.0.0.1:8000

Use any web browser to connect to the admin interface::

    http://127.0.0.1:8000/admin/

Enjoy.
