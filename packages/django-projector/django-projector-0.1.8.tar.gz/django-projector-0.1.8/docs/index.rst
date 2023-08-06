.. django-projector documentation master file, created by
   sphinx-quickstart on Thu Feb 18 23:18:28 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

============================================
Welcome to django-projector's documentation!
============================================

``django-projector`` is a project management application with task tracker and
repository backend integration. Aimed to work with Django_ 1.2 or later. We are
sick of Trac [1]_ and wanted to create simple application which can be easily
customized or plugged into existing systems.

.. image:: static/django-projector-01.png
   :width: 760px

--------
Features
--------

- Mercurial_ repository integration
- Easy repositories forking
- Granual permissions management (see :ref:`authorization`)
- Scalable architecture (AMQP) build on top of excellent celery_
- Task tracker with full history of changes
- Repository web browser
- Customizable workflow for each project
- Grouping tasks in milestones
- Roadmap
- Teams support
- Documents based on `restructuredText`_
- Email notification
- Make use of `django-richtemplates`_ so templates are ready to use
  out of the box

--------
Incoming
--------

Here are some additional points which are the target for future
release.

- Wiki per project
- Plugin system
- Code review
- Sphinx integration
- Other version control systems in backend (git_, subversion_...)
- Charts, statistics, graphs, plots, analyzies
- Functional timeline
- `django-piston`_ integration for RESTful API

.. warning::
   This application is at early-development stage but we strongly encourage
   you to give it a try if you are looking for project management toolkit
   for your Django_ based project. Still, it probably should **NOT** be used
   in production as it wasn't fully tested and may contain security issues.

-----------
Source code
-----------

Source code is along with issue tracker is available at
http://bitbucket.org/lukaszb/django-projector/.

------------
Demo project
------------

Demo project have been deployed at https://forge.django-projector.org. It is
still rather experimental.

-------
License
-------

``django-projector`` is released under MIT_ license. You should get a copy
of the license with source distribution, at the root location, within
``LICENSE`` file.

-------------
Documentation
-------------

**Installation:**

.. toctree::
   :maxdepth: 1

   installation
   configuration
   authorization

**Usage:**

.. toctree::
   :maxdepth: 1

   usage/example_project
   usage/teamwork
   usage/projects/index.rst

**Development**

.. toctree::
   :maxdepth: 1

   dev/testing

**API**

.. toctree::
   :maxdepth: 2

   api/index
 
------------
Other topics
------------

* :ref:`genindex`
* :ref:`search`

.. _celery: http://celeryproject.org/
.. _django: http://www.djangoproject.com/
.. _django-richtemplates: http://bitbucket.org/lukaszb/django-richtemplates/
.. _django-piston: http://bitbucket.org/jespern/django-piston/
.. _restructuredText: http://docutils.sourceforge.net/rst.html
.. _mercurial: http://mercurial.selenic.com/
.. _subversion: http://subversion.tigris.org/
.. _git: http://git-scm.com/
.. _trac: http://trac.edgewall.org/
.. _MIT: http://www.opensource.org/licenses/mit-license.php

.. [1] Don't get us wrong, Trac_ is great tool but we believe that
   django's pluggable applications are far easier to configure and
   deploy.

