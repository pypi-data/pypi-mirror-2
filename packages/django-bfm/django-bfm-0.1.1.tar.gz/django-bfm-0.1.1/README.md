Django Basic File Manager
=========================

Simple Django File Manager

Features
--------

* Multifile Uploads ([Screenshot](https://github.com/simukis/django-bfm/raw/master/screenshots/Open%20Files.png))
* Live Upload Status report ([Screenshot](https://github.com/simukis/django-bfm/raw/master/screenshots/Upload2.gif), [Screenshot](https://github.com/simukis/django-bfm/raw/master/screenshots/Upload.gif))
* File listing and deleting ([Screenshot](https://github.com/simukis/django-bfm/raw/master/screenshots/Basic%20File%20Manager%20-%20Browse.png))
* No external dependencies, lightweight
* Looks like django admin (extends admin template)


Requirements
------------

django_bfm extensively uses HTML5 techniques, so modern browser is required, see Tested Browsers section.

Tested only with Django 1.3, may work with Django 1.2 or even 1.1.

Usage/Install
-------------

* `easy_install django_bfm` or `pip install django_bfm` or download package, extract it, and copy django_bfm into your project directory
* Add `'django_bfm',` to `INSTALLED_APPS` in settings.py.
* Add `url(r'^files/', include('django_bfm.urls')),` to `urlpatterns` in urls.py
* Access file manager at /files/browse/

Settings
--------

Variables in settings.py, that influence way, how BFM works.

* `BFM_MEDIA_DIRECTORY`(if not set `MEDIA_ROOT` is used) - absolute path to place, where uploaded files are.
* `BFM_FILES_IN_PAGE`(default - `20`) - integer. Tells BFM, how much files to show in one page.

Things to note
--------------

* You must be logged as staff user to use file manager
* It's very young project

Tested Browsers
-------------------------------

* Chromium 15
* Midori 0.4.0
* Chrome 13
* Firefox 6
