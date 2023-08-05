from distutils.core import setup

setup(
    name = "django_bshell",
    version = "1.0.3",
    description = "Django management command to run bpython, and import all models",
    url = "http://bitbucket.org/schinckel/django-bshell/",
    author = "Matthew Schinckel",
    author_email = "matt@schinckel.net",
    packages = [
        'bshell', 
        'bshell.management', 
        'bshell.management.commands',
    ],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
