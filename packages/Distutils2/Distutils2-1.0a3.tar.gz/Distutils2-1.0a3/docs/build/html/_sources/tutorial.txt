===================
Distutils2 tutorial
===================

Welcome to the Distutils2 tutorial ! We will learn here how to use Distutils2 
to package your project.

Installing Distutils2
=====================

Quite simple, my dear reader::

    $ pip install Distutils2

Or.. grab it at PyPI and run::

    $ python setup.py install



Getting started
===============

Distutils2 works with the *setup.cfg* file. It contains all the metadata for
your project, as defined in PEP 345, but also declare what your project
contains. 

Let's say you have a project called *Keyring* containing one package called
*keyring*. You can use the *mkcfg* script to create a *setup.cfg* file that
works for you. The script will ask you a few questions::

    $ python -m distutils2.mkcfg 



