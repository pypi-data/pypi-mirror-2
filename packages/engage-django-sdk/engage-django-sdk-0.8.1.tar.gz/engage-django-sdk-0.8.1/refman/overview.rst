Overview
================
The overall workflow for deploying a Django application on genForma's
hosting service is:

#. Review your application to see if you need to make any adjustments. See
   :doc:`requirements` for details. You may need to include or document external
   dependencies (e.g Django apps or Python eggs). You may also have to adjust
   your Django settings slightly (e.g. to remove absolute file paths).

#. Run the prepare-dir or prepare-archive command of the SDK to validate your
   application and to create a packaged application archive suitable for
   deployment. See :doc:`deployment` for details.

#. Go to the genForma website and start the deployment of your
   application (http://beta.genforma.com/deploy/start).

#. You will receive an email when your deployment is complete. This email will
   include the URL for your application. If there is a problem in deployment,
   you will receive an email explaining the problem. If you are unsure how to
   address the problem, please contact support@genforma.com.

#. After deploying your application, you can package changes (bug
   fixes and enhancements, including schema changes) and automatically
   deploy them to your running application. See :doc:`upgrading` for details.

#. Demo instances will be destroyed after a fixed amount of time. To
   keep your instance around longer, contact sales@genforma.com. You can also
   destroy your application instance at any time from the application
   status page (http://beta.genforma.com/deploy/status).


.. _running_example:

Running Example
----------------
To illustrate how to package Django applications for deployment, we
will use a running example. All files in our example application are
placed under a common directory ``test_app_v1``. The application's
files are organized as follows::

  test_app_v1/
    requirements.txt
    test_app/
      __init__.py
      settings.py
      urls.py
    media/
      img/
        hello.jpg
      templates/
        base.html
        core/
          index.html
      app/
        __init__.py
        views.py
        migrations/
          __init__.py
          0001_initial.py
    utils/
      __init__.py
      fileutils.py
      misc.py
