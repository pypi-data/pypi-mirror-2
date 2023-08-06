==================================
 An Introduction to celery-pylons 
==================================

:Version: 2.0.1
:Celery Version: 2.0.1
:Web: http://celeryproject.org/
:Download: http://pypi.python.org/pypi/celery-pylons/
:Source: http://bitbucket.org/ianschenck/celery-pylons/
:Keywords: celery, pylons, task queue, job queue, asynchronous, rabbitmq, amqp, python, queue, distributed

celery-pylons provides Celery integration for pylons. The following
introduction will point to various resources and documentation to help
get you set up and running.

For more information please read the celery `documentation`_ for more information.

.. _documentation: :http://celeryproject.org/ 

Using celery-pylons
===================

Make sure to check out :ref:`first-steps-ref`

Everything works the same as described in the `Celery User Manual`_,
except you need to invoke the programs though ``paster``:

.. _Celery User Manual: http://ask.github.com/celery/userguide/index.html

=====================================  =====================================
**Program**                            **Replace with**
=====================================  =====================================
``celeryd``                            ``paster celeryd development.ini[#app_label]``
``celerybeat``                         ``paster celerybeat development.ini[#app_label]``
``camqadm``                            ``paster camqadm development.ini[#app_label]``
``celeryev``                           ``paster celeryev development.ini[#app_label]``
=====================================  =====================================

**NB:** Application label may need to be specified depending on Pylons configuration.

Documentation
=============

The `Celery User Manual`_ contains user guides, tutorials and an API
reference to celery. 

.. _Celery User Manual: http://ask.github.com/celery/userguide/index.html

.. _installation:

Installation
============

You can install ``celery-pylons`` either via the Python Package Index (PyPI)
or from source.

Downloading and installing via the Python Package Index (PyPI)
--------------------------------------------------------------

To install using ``pip``::
  
   $ pip install celery-pylons

To install using ``easy_install``::

   $ easy_install celery-pylons

Downloading and installing from source
--------------------------------------

Download the latest version of ``celery-pylons`` from
http://pypi.python.org/pypi/celery-pylons/

You can install it by issuing the following commands::
    
    $ tar xzvf celery-pylons-0.0.0.tar.gz
    $ cd celery-pylons
    $ python setup.py develop

For more information about setup.py targets, see the `distutils`_ documentation.

.. _distutils: http://foo.com

Make sure to check out :ref:`first-steps-ref` for configuration help.

Getting help
============

Mailing List
------------

For discussions about the usage, development, and future of celery,
please join the `celery-users`_ mailing list.

.. _`celery-users`: http://groups.google.com/group/celery-users/

IRC
---

Come chat with us on IRC. The `#celery`_ channel is located at the `Freenode`_
network.

.. _`#celery`: irc://irc.freenode.net/celery
.. _`Freenode`: http://freenode.net

Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them
to our issue tracker at http://bitbucket.org/ianschenck/celery-pylons/issues

Wiki
====

The ``Celery`` `wiki`_

.. _wiki: http:://wiki.github.com/ask/celery

Contributing
============

Development of ``celery-pylons`` happens (for the moment) at bitbucket:

http://bitbucket.org/ianschenck/celery-pylons

We highly encourage you to participate in the development of
``celery-pylons``. If you don't like bitbucket, you're welcome to send
regular patches.

License
=======

This software is licensed under the ``New BSD License``. See the
``LICENSE`` file in root of the distribution for the full license
text.
