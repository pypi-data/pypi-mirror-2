.. pycdep documentation master file, created by
   sphinx-quickstart on Sun Apr 24 21:08:15 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

What is pycdep about?
=====================

For background information and ideas about pycdep read the `techno gems`_ blog.

Pycdep is an include file dependency analyzer. 
It consists of a python script that goes over the C and C++ files and
extracts dependency information from it. The dependency information
is saved as a prolog program. The prolog program can be used to perform all kinds of analyses on the dependency graph, and to convert the dependency graph (or subsets thereof) to a .dot file. It comes with a lot of predefined queries.

Examples of things for which predefined queries are available: (only your imagination and knowledge of prolog limit the possibilities for adding new ones):
 * finding which files are included by another file
 * finding which files are recursively included by another file
 * finding out via which path one file depends on another file
 * finding out which files depend on some file
 * finding out which files need to be recompiled if you touch a given file
 * finding files that are included twice or more by the same file
 * finding .cpp files that are included
 * finding circular dependencies
 * finding out which header files are transitively implied by other header files included by the same file
 * checking design constraints to ensure that certain projects do not include from other projects

There's also an experimental chat bot implementation that can answer some of your questions about the code base being examined.

The whole system is intended to be cross-platform. That means that we need to deal with filename case (in)sensitivity issues. In particular, on linux systems we want to be able to examine windows code, and vice versa (as far as possible). The usage of upper and lower case in code written for windows systems is often sloppy, whereas for code intended for to be compiled on case sensitive filesystems the difference in case could (in principle) point to a different file.

.. _techno gems: http://technogems.blogspot.com

Requirements
============

At the very least you will need to install: 

* `python 2.X`_, where X >= 6
* easy_install the following packages - it may work with lower versions than the ones indicated here, but it is only tested with those versions:

  * path.py version 2.2.2 or higher
  * mako version 0.4.1 or higher
  * oset version 0.1.1 or higher

* `swi prolog`_ 
   
.. note::
  if you are using the debian package of SWI prolog, you don't have the plunit unit test library. You can install it from source. You only need it if you want to run the unit tests contained in test.pl.

.. _python 2.X: http://www.python.org/
.. _swi prolog: http://www.swi-prolog.org/

Downloading pycdep
==================

You can visit the project page: https://sourceforge.net/projects/pycdep/

Getting started
===============

Contents:

.. toctree::
   :maxdepth: 2

   Getting Started

Indices and tables
==================

* :ref:`search`

