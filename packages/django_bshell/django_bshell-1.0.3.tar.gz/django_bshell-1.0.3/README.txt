django-bshell
=============

A django app that adds a management command 'bshell', that starts a new shell, using bpython, and imports all of the project's models.

Usage:

    add 'bshell' to your settings.INSTALLED_APPS
    
    $ python manage.py bshell

You must have bpython installed to use this!