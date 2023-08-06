dolmenproject provides an easy way to get started with a `Dolmen
<http://www.dolmen-project.org/>`_ web application.
It's an extension of grokproject package.

This documentation is adapted from grokproject README.txt.
And so is the most of the code :). Thanks to grokproject developers!

Simply install ``dolmenproject``::

  $ easy_install dolmenproject

If you have an old version of ``dolmenproject`` installed then you can
upgrade doing::

  $ easy_install -U dolmenproject

Afterwards you can run the ``dolmenproject`` script with the name of the
project you'd like to create as an argument::

  $ dolmenproject DruidicRitual
  ... many lines of output here

This will not only create a project area for you to work in, it will
also download and install Grok and its dependencies.

After the project area has been created successfully, you will find an empty
Python package "skeleton" in the ``src`` directory in which you can place the
code for your web application.

To start the application server, execute::

  $ cd DruidicRitual
  $ bin/paster serve parts/etc/deploy.ini

Start/stop it in daemon mode::

  $ bin/daemon start/stop

There is also an Ajax enabled debugger (point your browser to
http://localhost:8080/@@login.html when using this)::

  $ bin/paster serve parts/etc/debug.ini

To start the interactive debugger prompt::

  $ bin/interactive_debugger

To run an ad-hoc Python script against a full setup application::

  $ bin/interactive_debugger [name_of_python_script].py

Python scripts run this way, will have access to a ``root``, ``debugger``, and
an ``app`` object avaible for "interacting" with the application environment.

For those who know paster: ``grokproject`` is just a wrapper around a
paster template.  So instead of running the ``grokproject`` command,
you can also run::

  $ paster create -t dolmen DruidicRitual

All configuration files used for running Grok can be found in the
``parts/etc/`` directory of your project. These configuration files are
generated automatically from the templates in ``etc/`` on each ``buildout``
run. To modify the configuration files edit the approriate templates in
``etc/`` and rerun ``buildout`` afterwards::

  $ bin/buildout

This will rebuild the files in ``parts/etc/``.
