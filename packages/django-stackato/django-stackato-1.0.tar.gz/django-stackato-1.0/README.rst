Django Stackato Extensions
==========================

*Experimental package*

Extra commands for improved Django support in `ActiveState Stackato
<http://www.activestate.com/cloud>`_. For the moment, this just
includes a ``changepassword2`` command, an alternate implementation of
Django's `changepassword
<https://code.djangoproject.com/browser/django/trunk/django/contrib/auth/management/commands/changepassword.py>`_,
that accepts password from the command-line, so ``stackato run`` can
be used non-interactively to set the admin password.

Getting Started
---------------

* Add ``django-stackato`` to your ``requirements.txt``
* Add ``django_stackato`` to INSTALLED_APPS of settings.py. 
* Run management commands::

    python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
    python manage.py changepassword2 admin secret123



