What is django-boomarker
========================

Django bookmarker is application which provides template tag which
displays the buttons for submitting current page to social bookmarks
services.

Repository URL: http://bitbucket.org/lorien/django-bookmarker


Installation
============

You have three ways:
 * easy_install django-bookmarker
 * pip install -e hg+http://bitbucket.org/lorien/django-bookmarker
 * download package and run python setup.py install


Integrating into django project
===============================
 * Put "bookmarker" into settings.INSTALLED_APPS


Example of usage in template
============================

    {% load bookmarker_tags %}
    <div class="social-bookmarks">
    {% bookmark_links obj.url obj.title %}
    </div>


Settings
========

BOOKMARKER_DESCRIPTIONS
--------------------------

Django-bookmarker contains a number of descriptions of popular services like
delicious, google bookmarks. You can look the format of descriptions in the
settings.py file inside package directory. If you want to display custom
bookmark links then define BOOKMARKER_DESCRIPTIONS variable into your
project settings file. This variable should have the same format as 
DESCRIPTIONS variable into package settings.py file.

BOOKMARKER_SERVICES
-------------------

This variable controls which services should ``bookmark_links`` tag display.
