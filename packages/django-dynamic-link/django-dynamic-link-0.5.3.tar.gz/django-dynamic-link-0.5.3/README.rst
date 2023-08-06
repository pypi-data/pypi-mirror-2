===========
Description
===========

Django file streaming application to provide download links without showing the real path to the served file. The links can be set to expire by date or by clicks. It is also possible to use it for counting clicks on a download link.

**License**

    New BSD license

**Notes**

    * Tested with Django 1.2 / 1.3
    * Example project is included

========
Features
========

    * Link expires by clicks (optional)
    * Link expires by time (optional)
    * Is usable for counting clicks

============
Installation
============

**Dependences**

    * This app
    * Django itself, its redirects from django.contrib and its locale middleware.

**Installation**

    *Download & installation with pip (recommended)*

        *Pip will download and install the package and take care of all the dependences.*

        * Use the stable release (recommended)

            Type in your terminal:
        
            ::

            :~$ pip install django-dynamic-link

        * Or the development version

            Than type in your terminal:

            ::

            :~$ pip install -e hg+https://bitbucket.org/catapela/django-dynamic-link/#egg=django-dynamic-link

        * With pip you can also uninstall it:

        ::

        :~$ pip uninstall django-dynamic-link

    *Manual Installation*

        * To get the package from pypi (stable) or bitbucket (dev) see here_.

.. _here: http://pypi.python.org/pypi/django-dynamic-link/#downloads

        * Download the file and unzip it.
        * Copy the folder in your project root.
        * Make shure all package dependences are fulfilled.

    *Other possibilities*

        * Open a terminal and change to the folder which contains the setup.py and then type:

        ::

        :~$ python setup.py install

**test your installation**

    Go to console and type:

    ::

    :~$ python

    ... than type:
    
    >>> import dynamicLink
    >>> dynamicLink.VERSION
    
=====
Setup
=====
    
    * Add "dynamicLink" to you installed apps in the settings file.

    * Make sure that:
        1.   'django.middleware.locale.LocaleMiddleware', is in your MIDDLEWARE_CLASSES.
        2.   Your Admin is enabled ('django.contrib.admin', is in your INSTALLED_APPS).
        3.   'django.contrib.auth.context_processors.auth', (also for admin) is in TEMPLATE_CONTEXT_PROCESSORS.
        4.   'django.core.context_processors.request', is in TEMPLATE_CONTEXT_PROCESSORS.

    * Add the following to your urls.py:
        1.   from dynamicLink import presettings
        2.   (r'^\w+/%s/' % presettings.DYNAMIC_LINK_URL_BASE_COMPONENT, include('dynamicLink.urls')),
    
    * Finally run:

    ::

    :~$ python manage.py syncdb
    :~$ python manage.py runserver

**Make it custom**

    Use the global settings.py in your projects root to overwrite the applications presettings with the following variables.

    * DYNAMIC_LINK_MEDIA
        - Default: settings.MEDIA_ROOT
        - A path to a directory. From this point you can walk down the subdirectories to choose your files to serve.
    * DYNAMIC_LINK_URL_BASE_COMPONENT
        - Default: 'serve'
        - A string that modifies your url serve path.
        - Example: www.example.com/DYNAMIC_LINK_URL_BASE_COMPONENT/link/3839hd8HKl3/example.zip.

=====
Usage
=====

Open the admin interface and go to "Dynamiclink" section. The rest should be self-explanatory.

**Hints**

    * Zero value for link age means never expires.
    * Zero value for clicks means unlimited clicks.
    * If a link never expires you can use it for click counting.
    * Trough the action menu you can serve a site with several links. 
    * The filename from the created links are only for human readability. You can delete or change these filenames in any way you want.

===============
Example project
===============

djang-dynamic-links ships with an example proect.

    1. Install the package (see install section).
    2. Run "python manage.py syncdb" and "python manage.py runserver".
    3. Open a Browser, go to: http://127.0.0.1:8000/