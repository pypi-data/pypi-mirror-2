========
Commands
========

Distutils2 provides a set of commands that are not present in distutils itself.
You might recognize some of them from other projects, like Distribute or
Setuptools.

``test`` - Build package and run a unittest suite
=================================================

When doing test-driven development, or running automated builds that need
testing before they are deployed for downloading or use, it's often useful
to be able to run a project's unit tests without actually deploying the project
anywhere.  The ``test`` command runs
project's unit tests without actually deploying it, by temporarily putting the
project's source on ``sys.path``, after first running ``build_ext -i``
to ensure that any C extensions are built.

You can use this command in one of two ways: either by specifying a
unittest-compatible test suite for your project (or any callable that returns
it) or by passing a test runner function that will run your tests and display
results in the console. Both options: ``suite`` and ``runner`` accept dotted
names that will be resolved into actual objects.

If none of these options are specified, distutils2 will try to perform test
discovery using either unittest2 (if installed) or unittest (if running on
recent Python version).

``--suite=NAME, -s NAME``
    Specify the test suite (or module, class, or method) to be run
    (for example ``my_package.tests.all_tests``).  The default for this option can be
    set by in your ``setup.cfg`` file.

.. code-block:: ini

    [test]
        suite = my_package.tests.all_tests

``--runner=NAME, -r NAME``
    Specify the test runner to be called.


``upload`` - Upload source and/or binary distributions to PyPI
==============================================================

The Python Package Index (PyPI) not only stores the package info, but also  the
package data if the author of the package wishes to. The distutils command
:command:`upload` pushes the distribution files to PyPI.

The command is invoked immediately after building one or more distribution
files.  For example, the command ::

    python setup.py sdist bdist_wininst upload

will cause the source distribution and the Windows installer to be uploaded to
PyPI.  Note that these will be uploaded even if they are built using an earlier
invocation of :file:`setup.py`, but that only distributions named on the command
line for the invocation including the :command:`upload` command are uploaded.

The :command:`upload` command uses the username, password, and repository URL
from the :file:`$HOME/.pypirc` file . If a :command:`register` command was
previously called in the same command, and if the password was entered in the
prompt, :command:`upload` will reuse the entered password. This is useful if
you do not want to store a clear text password in the :file:`$HOME/.pypirc`
file.

The ``upload`` command has a few options worth noting:

``--sign, -s``
    Sign each uploaded file using GPG (GNU Privacy Guard).  The ``gpg`` program
    must be available for execution on the system ``PATH``.

``--identity=NAME, -i NAME``
    Specify the identity or key name for GPG to use when signing.  The value of
    this option will be passed through the ``--local-user`` option of the
    ``gpg`` program.

``--show-response``
    Display the full response text from server; this is useful for debugging
    PyPI problems.

``--repository=URL, -r URL``
    The URL of the repository to upload to.  Defaults to
    http://pypi.python.org/pypi (i.e., the main PyPI installation).


``upload_docs`` - Upload package documentation to PyPI
======================================================

PyPI now supports uploading project documentation to the dedicated URL
http://packages.python.org/<project>/.

The ``upload_docs`` command will create the necessary zip file out of a
documentation directory and will post to the repository.

Note that to upload the documentation of a project, the corresponding version
must already be registered with PyPI, using the distutils ``register``
command -- just like the ``upload`` command.

Assuming there is an ``Example`` project with documentation in the
subdirectory ``docs``, for example::

  Example/
  |-- example.py
  |-- setup.cfg
  |-- setup.py
  |-- docs
  |   |-- build
  |   |   `-- html
  |   |   |   |-- index.html
  |   |   |   `-- tips_tricks.html
  |   |-- conf.py
  |   |-- index.txt
  |   `-- tips_tricks.txt

You can simply pass the documentation directory path to the ``upload_docs``
command::

    python setup.py upload_docs --upload-dir=docs/build/html

As with any other command, you can define useful
defaults in the ``setup.cfg`` of your Python project, for example:

.. code-block:: ini

    [upload_docs]
    upload-dir = docs/build/html

The ``upload_docs`` command has the following options:

``--upload-dir``
    The directory to be uploaded to the repository. The default value is
    ``docs`` in project root.

``--show-response``
    Display the full response text from server; this is useful for debugging
    PyPI problems.

``--repository=URL, -r URL``
    The URL of the repository to upload to.  Defaults to
    http://pypi.python.org/pypi (i.e., the main PyPI installation).


