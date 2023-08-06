.. index::
   single: environment variables
   single: settings
   single: reload
   single: debug_authorization
   single: reload_resources
   single: debug_notfound
   single: debug_all
   single: reload_all
   single: debug settings
   single: reload settings
   single: default_locale_name
   single: environment variables
   single: ini file settings
   single: PasteDeploy settings
  
.. _environment_chapter:

Environment Variables and ``.ini`` File Settings
================================================

:mod:`pyramid` behavior can be configured through a combination of
operating system environment variables and ``.ini`` configuration file
application section settings.  The meaning of the environment
variables and the configuration file settings overlap.

.. note:: Where a configuration file setting exists with the same
          meaning as an environment variable, and both are present at
          application startup time, the environment variable setting
          takes precedence.

The term "configuration file setting name" refers to a key in the
``.ini`` configuration for your application.  The configuration file
setting names documented in this chapter are reserved for
:mod:`pyramid` use.  You should not use them to indicate
application-specific configuration settings.

Reloading Templates
-------------------

When this value is true, reload templates without a restart.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_RELOAD_TEMPLATES``        |  ``reload_templates``       |
|                                 |                             |
|                                 |                             |
|                                 |                             |
+---------------------------------+-----------------------------+

Reloading Resources
-------------------

Don't cache any resource file data when this value is true.  See
also :ref:`overriding_resources_section`.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_RELOAD_RESOURCES``        |  ``reload_resources``       |
|                                 |                             |
|                                 |                             |
|                                 |                             |
+---------------------------------+-----------------------------+

Debugging Authorization
-----------------------

Print view authorization failure and success information to stderr
when this value is true.  See also :ref:`debug_authorization_section`.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_DEBUG_AUTHORIZATION``     |  ``debug_authorization``    |
|                                 |                             |
|                                 |                             |
|                                 |                             | 
+---------------------------------+-----------------------------+

Debugging Not Found Errors
--------------------------

Print view-related ``NotFound`` debug messages to stderr
when this value is true.  See also :ref:`debug_notfound_section`.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_DEBUG_NOTFOUND``          |  ``debug_notfound``         |
|                                 |                             |
|                                 |                             |
|                                 |                             |
+---------------------------------+-----------------------------+

Debugging All
-------------

Turns on all ``debug*`` settings.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_DEBUG_ALL``               |  ``debug_all``              |
|                                 |                             |
|                                 |                             |
|                                 |                             |
+---------------------------------+-----------------------------+

Reloading All
-------------

Turns on all ``reload*`` settings.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_RELOAD_ALL``              |  ``reload_all``             |
|                                 |                             |
|                                 |                             |
|                                 |                             |
+---------------------------------+-----------------------------+

.. _default_locale_name_setting:

Default Locale Name
--------------------

The value supplied here is used as the default locale name when a
:term:`locale negotiator` is not registered.  See also
:ref:`localization_deployment_settings`.

+---------------------------------+-----------------------------+
| Environment Variable Name       | Config File Setting Name    |
+=================================+=============================+
| ``BFG_DEFAULT_LOCALE_NAME``     |  ``default_locale_name``    |
|                                 |                             |
|                                 |                             |
|                                 |                             |
+---------------------------------+-----------------------------+

.. _mako_template_renderer_settings:

Mako Template Render Settings
-----------------------------

Mako derives additional settings to configure its template renderer that
should be set when using it. Many of these settings are optional and only need
to be set if they should be different from the default. The Mako Template
Renderer uses a subclass of Mako's `template lookup
<http://www.makotemplates.org/docs/usage.html#usage_lookup>`_ and accepts
several arguments to configure it.

Mako Directories
++++++++++++++++

The value(s) supplied here are passed in as the template directories. They
should be in :term:`resource specification` format, for example:
``my.package:templates``.

+-----------------------------+
| Config File Setting Name    |
+=============================+
|  ``mako.directories``       |
|                             |
|                             |
|                             |
+-----------------------------+

Mako Module Directory
+++++++++++++++++++++

The value supplied here tells Mako where to store compiled Mako templates. If
omitted, compiled templates will be stored in memory. This value should be an
absolute path, for example: ``%(here)s/data/templates`` would use a directory
called ``data/templates`` in the same parent directory as the INI file.

+-----------------------------+
| Config File Setting Name    |
+=============================+
|  ``mako.module_directory``  |
|                             |
|                             |
|                             |
+-----------------------------+

Mako Input Encoding
+++++++++++++++++++

The encoding that Mako templates are assumed to have. By default this is set
to ``utf-8``. If you wish to use a different template encoding, this value
should be changed accordingly.

+-----------------------------+
| Config File Setting Name    |
+=============================+
|  ``mako.input_encoding``    |
|                             |
|                             |
|                             |
+-----------------------------+

Examples
--------

Let's presume your configuration file is named ``MyProject.ini``, and
there is a section representing your application named ``[app:main]``
within the file that represents your :mod:`pyramid` application.
The configuration file settings documented in the above "Config File
Setting Name" column would go in the ``[app:main]`` section.  Here's
an example of such a section:

.. code-block:: ini

  [app:main]
  use = egg:MyProject#app
  reload_templates = true
  debug_authorization = true

You can also use environment variables to accomplish the same purpose
for settings documented as such.  For example, you might start your
:mod:`pyramid` application using the following command line:

.. code-block:: python

  $ BFG_DEBUG_AUTHORIZATION=1 BFG_RELOAD_TEMPLATES=1 bin/paster serve \
         MyProject.ini

If you started your application this way, your :mod:`pyramid`
application would behave in the same manner as if you had placed the
respective settings in the ``[app:main]`` section of your
application's ``.ini`` file.

If you want to turn all ``debug`` settings (every setting that starts
with ``debug_``). on in one fell swoop, you can use
``BFG_DEBUG_ALL=1`` as an environment variable setting or you may use
``debug_all=true`` in the config file.  Note that this does not affect
settings that do not start with ``debug_*`` such as
``reload_templates``.

If you want to turn all ``reload`` settings (every setting that starts
with ``reload_``). on in one fell swoop, you can use
``BFG_RELOAD_ALL=1`` as an environment variable setting or you may use
``reload_all=true`` in the config file.  Note that this does not
affect settings that do not start with ``reload_*`` such as
``debug_notfound``.

.. index:: 
   single: reload_templates
   single: reload_resources

Understanding the Distinction Between ``reload_templates`` and ``reload_resources``
-----------------------------------------------------------------------------------

The difference between ``reload_resources`` and ``reload_templates``
is a bit subtle.  Templates are themselves also treated by
:mod:`pyramid` as :term:`pkg_resources` resource files (along with
static files and other resources), so the distinction can be
confusing.  It's helpful to read :ref:`overriding_resources_section`
for some context about resources in general.

When ``reload_templates`` is true, :mod:`pyramid` takes advantage
of the underlying templating systems' ability to check for file
modifications to an individual template file.  When
``reload_templates`` is true but ``reload_resources`` is *not* true,
the template filename returned by pkg_resources is cached by
:mod:`pyramid` on the first request.  Subsequent requests for the
same template file will return a cached template filename.  The
underlying templating system checks for modifications to this
particular file for every request.  Setting ``reload_templates`` to
``True`` doesn't affect performance dramatically (although it should
still not be used in production because it has some effect).

However, when ``reload_resources`` is true, :mod:`pyramid` will not
cache the template filename, meaning you can see the effect of
changing the content of an overridden resource directory for templates
without restarting the server after every change.  Subsequent requests
for the same template file may return different filenames based on the
current state of overridden resource directories. Setting
``reload_resources`` to ``True`` affects performance *dramatically*,
slowing things down by an order of magnitude for each template
rendering.  However, it's convenient to enable when moving files
around in overridden resource directories. ``reload_resources`` makes
the system *very slow* when templates are in use.  Never set
``reload_resources`` to ``True`` on a production system.

