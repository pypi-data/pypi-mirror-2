
=============
Configuration
=============

This section contains information about how to configure your Django projects
to use *django-postgresql-manager* and also contains a quick reference of the available
*settings* that can be used in order to customize the functionality of this
application.


PostgreSQL Administrator Role
=============================
This application requires that you create a PostgreSQL (refered to as *Pg*
hereafter) role which will be used for the role and database management.

While in the Pg shell as a superuser, create the *administrator* role::

    CREATE ROLE administrator WITH LOGIN CREATEDB CREATEROLE PASSWORD '1234';


Configuring your project
========================

This section outlines the configuration options that need to be set in your
Django project's ``settings.py`` file.

Add an extra database connection, named ``postgresql_manager_conn``,
which will be used to connect to the PostgreSQL cluster using the
``administrator`` role::

    DATABASES = {
        ...
        # Database connection settings for postgresql_manager
        'postgresql_manager_conn': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'administrator',
            'PASSWORD': '1234',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {
                'autocommit': True,
            },
        },
        ...
    }

**Important Note**: It should be noted that the ``postgresql_manager_conn``
database connection is only used to perform role and database management
on the PostgreSQL Cluster. No extra databases or tables will be created.
The ``postgresql_manager`` application specific tables will be created in
the Django project's default database, which may exist in any database
backend.

In the Django project's ``settings`` module, add ``postgresql_manager`` to the
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'postgresql_manager',
    )


Reference of the application settings
=====================================

The following settings can be specified in the Django project's ``settings``
module to customize the functionality of *django-postgresql-manager*.

``PGMANAGER_FORBIDDEN_USER_NAMES``
    A list of role names that should not be used. By default, the following role
    names are forbidden: postgres, postgresql, pg, admin, administrator, root,
    sys, system.
``PGMANAGER_FORBIDDEN_DATABASE_NAMES``
    A list of database names that should not be used. By default, the following
    names are forbidden: postgres, template0, template1.


Synchronize the project database
================================

Finally, synchronize the project's database using the following command::

    python manage.py syncdb

