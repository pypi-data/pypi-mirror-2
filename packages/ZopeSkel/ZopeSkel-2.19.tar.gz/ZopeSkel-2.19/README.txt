.. contents :: 

Introduction
============

ZopeSkel provides a collection of project templates for Plone 
and Zope development projects.

ZopeSkel uses the `paster <http://pythonpaste.org/script/>`_ Python library
internally.

Installing ZopeSkel
===================

ZopeSkel can be installed in one of two ways: with `buildout
<http://www.buildout.org/>`_ or with `virtualenv
<http://virtualenv.openplans.org/>`_. Despite existing documentation to the
contrary, it is not recommended to install ZopeSkel in your system python.

Buildout installation 
---------------------------

Add to your ``buildout.cfg``::
        
    parts =
        ...
        zopeskel
    

    [zopeskel]
    recipe = zc.recipe.egg
    eggs = 
            ZopeSkel 
            ${instance:eggs}

After building your buildout, this will leave ``zopeskel`` and ``paster`` 
commands in the ``bin`` directory of your buildout.

Virtualenv installation
-----------------------------

First, install virtualenv into your system::

    easy_install virtualenv

Next, create a virtual environment with the new ``virtualenv`` command::

    virtualenv --no-site-packages --distribute zopeskelenv

Once virtualenv is finished, you can install zopeskel to your new virtual 
environment::

    zopeskelenv/bin/easy_install zopeskel

Once this is complete, you will be left with ``zopeskel`` and ``paster``
commands in the ``bin`` directory inside your virtualenv.


Available Templates
===================

To see details of the available templates::

    zopeskel --list
    
... or more info about how zopekskel works::

	zopeskel --help
		    
Using Templates
===============

Creating a Plone 4 buildout using virtualenv ZopeSkel installation::
    
    source zopeskelenv/bin/activate
	zopeskel plone4_buildout yourfoldername

The folder created, ``yourfoldername``, can be checked into the versioning
system of your choice.  It is now a portable, self-contained, ready-to-build 
Plone site.  You can build the system at any time using the following::

	cd yourfoldername
	python bootstrap.py 
	bin/buildout

The ``plone4_buildout`` recipe results in a self-contained version of ZopeSkel
installed via the buildout method described above. It thus provides the 
``zopeskel`` and ``paster`` commands inside its ``bin`` folder. You can use these
commands inside the buildout to create packages for your new Plone site::

    bin/zopeskel plone3_theme src/plonetheme.yourcompanyid

The command will ask a few questions such as desired package name and a
description and output a complete package you can immediately start using.
Interactive help is available by entering "?" as a response to any question.

.. note ::

    Because ZopeSkel is built on paster you can do anything we describe here
    using the ``paster`` command directly.  If you do so, you can gain access to 
    certain features of ``paster`` that have been disabled for ``zopeskel``, but
    you also will lose access to many of the nicer features of ``zopeskel``, 
    including validation and in-line help.

Local Commands
==============

In addition to project templates, the ZopeSkel system provides local commands.
Local commands are context aware commands that help you to add more
functionality to an existing ZopeSkel generated project.

.. note ::

	Local commands require using the ``paster`` command directly - the 
	``zopeskel`` command does not support them yet.

.. note ::

    Not all ZopeSkel templates provide local commands.  In general, if local
    commands are available, you will be informed of the fact as your new
    package is generated.

Using local commands to create a content type package
-----------------------------------------------------

Starting inside your Plone buildout, first create an archetypes package::

    cd src
    ../bin/zopeskel archetype mycompanyid.mycustomcontenttypes

Next, change directories into your new package and invoke ``paster`` to add a
content type::

    cd mycompanyid.mycustomcontenttypes
    ../../bin/paster
    
    Usage: ../../bin/paster COMMAND
    usage: paster [paster_options] COMMAND [command_options]
    
    ...
    
    Commands:
    ...

    ZopeSkel local commands:
	    addcontent   Adds plone content types to your project
                

As you can see from the ``paster`` command output, your new package supports a
local command called ``addcontent``. Tou can use ``addcontent`` command to add
new code to your package. As with both ``zopskel`` and ``paster``, you can use
the ``--list`` option to see what local commands are available in the context of
the package you've created.

    ../../bin/paster addcontent --list
    
    Available templates:
        atschema:      A handy AT schema builder
        browserlayer:  A Plone browserlayer
        contenttype:   A content type skeleton
        form:          A form skeleton
        formfield:     Schema field for a form
        i18nlocale:    An i18n locale directory structure
        portlet:       A Plone 3 portlet
        view:          A browser view skeleton
        zcmlmeta:      A ZCML meta directive skeleton

You can add an archetypes content type for managing lectures::

        ../../bin/paster addcontent -t contenttype LectureInfo

Then you can add schema fields to that content type::

        ../../bin/paster addcontent -t atschema

local commands can be run as many times as needed to create your package.  You 
can iteratively develop your content type, other content types, and more.

.. note ::

    When changing the your package code local commands will often change
    GenericSetup XML files (found in the in ``profiles/default`` folder of your
    package). These changes will not appear in Plone/Zope simply by restarting your
    instance. You will usually need to re-install your package in your development
    Plone site if you run any local commands in a package you've already installed.

More info

* http://collective-docs.plone.org/tutorials/paste.html

Testing
=======

Since version 1.5, ZopeSkel has tests.  It's required to run these
before you check in any changes you make. They can be run like so::

    python setup.py test

More info
=========

Issue tracker

* http://plone.org/products/zopeskel/issues

Source code

* http://svn.plone.org/svn/collective/ZopeSkel/trunk

Mailing List

* https://lists.plone.org/mailman/listinfo/zopeskel

Please contribute by submitting patches for what you consider 'best of
breed' file layouts for starting Zope projects.
