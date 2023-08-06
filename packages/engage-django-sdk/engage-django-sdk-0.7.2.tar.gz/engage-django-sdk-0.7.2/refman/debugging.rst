Debugging Guide
==============

We now look at common problems that you might run into and how to debug/fix them.

Validation and Packaging Errors
------------------------------
The application packager performs a number of checks on your Django settings
file to ensure that that your application can be deployed on an arbitrary server.
For definite issues, it will report *errors* and refuse to package your application.
For potential issues, it will report *warnings* but still package the application.

Missing Applications
~~~~~~~~~~~~~~~~~~~~
If you get an error message like one of the following, the validator could not
find one of the applications listed in your ``INSTALLED_APPS`` setting:
 1. Warning: *Django Application 'foo' not found. Perhaps you wanted to include the 'django_foo' package in your requirements.txt file*
 2. Warning: *Django Application 'foo' not found within the application's directory tree. This may be OK if you have an asssociated entry in your requirements.txt file. If it is supposed to be a python package included with you application, check the value you provided for the settings module.*

The validator checks that each application listed in the ``INSTALLED_APPS``
setting will be available on the deployment server.  Apps can be provided in
one of the following ways:
 * As Python modules included under your application's root directory. The
   modules should be placed at the same level in the directory hierarchy as
   your settings file (see :ref:`file_layout` for details).
 * As packages that are included in your requirements.txt file. The validator
   keeps a mapping from popular package names to the Django app names installed
   by the package. 
 * The validator knows about apps that come with the Django distribution (e.g.
   django.contrib.*).

In the case of the first warning above,  the application 'foo' *may* correspond to
the well-known Python package 'django_foo'. If that is indeed the case, you just need
to add 'django_foo' to your requirements.txt file.

In the case of the the second warning above, no obvious candidate package could
be found corresponding to package 'foo'.  This might just be that foo is not
in the validator's database, because it is not so well known or specific to your project.
That's OK, the validator will still package your application and deploy it.

If 'foo' is a package that was included under your application root directory, then
this warning message indicates that the validator could not find your package.
This is usually because the package name you provided as the *Django settings module* is
pointing at the wrong level in the hierarchy.  As a result, the ``PYTHONPATH`` variable
is set to the wrong directory. In our example directory layout :ref:`running_example`, 
the Django settings module should be set to ``test_app.settings``. This causes
``PYTHONPATH`` to be set to the ``test_app_v1`` directory,  allowing access to
the ``app`` and ``utils`` modules. If you instead specified the Django settings module
as ``settings``, ``PYTHONPATH`` would point to ``test_app_v1/test_app``, and the
``app`` and ``utils`` modules would not be found.

Settings Import Errors
~~~~~~~~~~~~~~~~~~~
To analyze your settings file, the validator must import it. If this fails, you will
get an error message like *Error in settings import: Exc(val)*,
where *Exc* is the exception type and *val* is the exception value. 

If the exception type is ``ImportError``, then perhaps you are importing a module
that is not accessible to the validator. If the module is located under your application
root directory, then perhaps your Django settings module is not specified correctly.
See the discussion above for details.

If the module being imported corresponds to a module installed by one of the packages
in your ``requirements.txt`` file,  then try catching the import exception in your settings
file.


Deployment Errors
--------------------
If your application is packaged successfully, but it fails to install on the
deployed node, you will get an email including the specific error that
occurred. In addition, the logfiles from the install will be available through
the genForma website. The key logfiles are:
 * ``install.log`` -- this file has all the gory details about the installation
 * ``upgrade.log`` -- this is the logfile for upgrades
 * ``upgrade_subprocess.log`` -- this is a more detailed logfile for upgrades
 * ``django`` -- this directory contains the logfiles from your actual Django instance

