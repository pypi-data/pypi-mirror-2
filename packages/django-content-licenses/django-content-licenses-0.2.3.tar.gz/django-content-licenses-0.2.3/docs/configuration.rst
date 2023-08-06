
=============
Configuration
=============

This section contains information about how to configure your Django projects
to use *django-content-licenses* and also contains a quick reference of the available
*settings* that can be used in order to customize the functionality of this
application.


Configuring your project
========================

In the Django project's ``settings`` module, add ``content_licenses`` to the
``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'content_licenses',
    )


Synchronize the project database
================================

Finally, synchronize the project's database using the following command::

    python manage.py syncdb


Load initial data
=================

Although optional, several commonly used licenses can be loaded by running the
following::

    python manage.py loaddata content_licenses

The ``fixtures/content_licenses.json`` data has been exported using the
following command::
    
    python manage.py dumpdata --indent=4 content_licenses.License > content_licenses.json

