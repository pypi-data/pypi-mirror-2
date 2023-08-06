Changelog
=========

v1.0.0-alpha (XXXX-XX-XX)
-------------------------

.. note:: ``django-staticfiles`` is a backport of the staticfiles app in
   Django contrib. If you're upgrading from ``django-staticfiles`` < ``1.0``,
   you'll need to make a few changes. See changes below.

* Renamed ``StaticFileStorage`` to ``StaticFilesStorage``.

* Application files should now live in a ``static`` directory in each app
  (previous versions of ``django-staticfiles`` used the name ``media``,
  which was slightly confusing).

* The management commands ``build_static`` and ``resolve_static`` are now
  called ``collectstatic`` and ``findstatic``.

* The settings ``STATICFILES_PREPEND_LABEL_APPS`` and
  ``STATICFILES_MEDIA_DIRNAMES`` were removed.

* The setting ``STATICFILES_RESOLVERS`` was removed, and replaced by the new
  ``STATICFILES_FINDERS`` setting.

* The default for ``STATICFILES_STORAGE`` was renamed from
  ``staticfiles.storage.StaticFileStorage`` to
  ``staticfiles.storage.StaticFilesStorage``

* If using ``runserver`` for local development (and the setting
  ``DEBUG`` setting is ``True``), you no longer need to add
  anything to your URLconf for serving static files in development.



v0.3.3 (2010-12-23)
-------------------

.. note:: With the adoption of django-staticfiles in Django >=1.3.X as a
   contrib app, the django-staticfiles 0.3.X series will be the last series
   to support Django 1.2.X and lower. Any new features will occur in
   later releases and target Django >=1.3.X.

* Fixed an issue that could prevent the ``build_static`` management command
  to fail if the destination storage doesn't implement the ``listdir``
  method.

* Fixed an issue that caused non-local storage backends to fail saving
  the files when running ``build_static``.

v0.3.2 (2010-08-27)
-------------------

* Minor cosmetic changes

* Moved repository back to Github: http://github.com/jezdez/django-staticfiles

v0.3.1 (2010-08-21)
-------------------

* Added Sphinx config files and split up README.
  
  Documetation now available under
  `django-staticfiles.readthedocs.org <http://django-staticfiles.readthedocs.org/>`_

v0.3.0 (2010-08-18)
-------------------

* Added resolver API which abstract the way staticfiles finds files.

* Added staticfiles.urls.staticfiles_urlpatterns to avoid the catch-all
  URLpattern which can make top-level urls.py slightly more confusing.
  From Brian Rosner.

* Minor documentation changes

* Updated testrunner to work with Django 1.1.X and 1.2.X.

* Removed custom code to load storage backend.

v0.2.0 (2009-11-25)
-------------------

* Renamed build_media and resolve_media management commands to build_static
  and resolve_media to avoid confusions between Django's use of the term
  "media" (for uploads) and "static" files.

* Rework most of the internal logic, abstracting the core functionality away
  from the management commands.

* Use file system storage backend by default, ability to override it with
  custom storage backend

* Removed --interactive option to streamline static file resolving.

* Added extensive tests

* Uses standard logging

v0.1.2 (2009-09-02)
-------------------

* Fixed a typo in settings.py

* Fixed a conflict in build_media (now build_static) between handling
  non-namespaced app media and other files with the same relative path.

v0.1.1 (2009-09-02)
-------------------

* Added README with a bit of documentation :)

v0.1.0 (2009-09-02)
-------------------

* Initial checkin from Pinax' source.

* Will create the STATIC_ROOT directory if not existent.
