===============================================
 celery-pylons - Celery Integration for Django
===============================================

.. image:: http://bitbucket.org/ianschenck/celery-pylons/downloads/celery_pylons-03.png

:Version: 2.1.4
:Celery Version: 2.1.4
:Web: http://celeryproject.org
:Download: http://pypi.python.org/pypi/celery-pylons
:Contributors: Jonathan Stasiak
:Source: http://bitbucket.org/ianschenck/celery-pylons
:Keywords: celery, pylons, task queue, job queue, asynchronous, rabbitmq, amqp, python, queue, distributed

--

celery-pylons provides Celery integration for pylons.

For more information please read the celery
.. _`documentation`:http://celeryproject.org/ for more information


Using celery-pylons
===================

To enabled ``celery-pylons`` for your project you need to add ``celery-pylons``...

Everything works the same as described in the `Celery User Manual`_,
except you need to invoke the processes though ``paster``:

=====================================  =====================================
**Program**                            **Replace with**
=====================================  =====================================
``celeryd``                            ``paster celeryd``
``celerybeat``                         ``paster celerybeat``
``camqadm``                            ``paster camqadm``
``celeryev``                           ``paster celeryev``
=====================================  =====================================

Documentation
=============

The `Celery User Manual`_ contains user guides, tutorials and an API
reference. Also the `django-celery documentation`_, contains information
about the Django integration.

Installation
============


Getting help
============


Mailing list
============


Bug tracker
===========


Wiki
====


Contributing
============

License
=======

