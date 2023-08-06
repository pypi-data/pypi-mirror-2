Django Stackato Extensions
==========================

*Experimental package*

Extra commands for improved Django support in ActiveState Stackato. For the
moment, this just includes a ``createsuperuser2`` command that accepts password
from the command-line, so ``stackato run`` can be used non-interactively to set
the admin password.

Getting Started
---------------

Add ``django-stackato`` to your ``requirements.txt`` and then add ``django_stackato`` to INSTALLED_APPS of settings.py. Then run::

    python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
    python manage.py changepassword2 admin secret123



