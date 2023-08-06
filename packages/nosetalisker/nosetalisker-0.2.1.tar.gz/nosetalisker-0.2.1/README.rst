Nose Talisker
==================

A nose plugin that outputs one cProfile stat dump to a file, for each test.

Install
-------------

    pip install nose-talisker

Format of the file name is::

    module-name.class-name.test-name.elapsed-milli-seconds.timestamp.prof

For example::

    zamboni.apps.files.tests.test_views.TestFileViewer.test_view_access_reviewed.001448ms.2011-06-09T01:50:34.323206.prof
    zamboni.apps.files.tests.test_views.TestFileViewer.test_view_access_reviewed.001577ms.2011-06-09T01:56:51.694283.prof


Options
--------------

- prof_path: the destination directory to write to. If not given a temporary
  one will be created for you. If you provide a directory, it must exist.

Usage
--------------------

    nosetests --with-talisker --prof-path=/tmp/output

This module is designed to be used by talisker to consume and view the profile
results. The format is deliberately based upon the runprofileserver from the
command extensions module, with the same option naming.

License: BSD
Author: Andy McKay, andym@mozilla.com
