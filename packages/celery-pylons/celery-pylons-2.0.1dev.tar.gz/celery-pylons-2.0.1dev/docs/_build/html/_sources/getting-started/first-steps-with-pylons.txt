.. _first-steps-ref:

===============================
First steps with celery-pylons 
===============================

Configuring your Pylons project to use Celery
=============================================

Installing celery-pylons is dead simple. Follow the two steps below to get Celery integrated with Pylons.

There are a few simple steps to integrate Celery into your Pylons
project.

	1. Install celery-pylons (*see* :ref:`installation`)
	
	2. Add the following [#c]_ to your ``development.ini`` file in the section ``[app:main]`` [#a]_::

	    broker.host = localhost
	    broker.port = 5672
	    broker.user = [user] [password]
    	    broker.password = [password]
    	    broker.vhost = [vhost]
    	    celery.result.backend = amqp
    	    celery.result.dburi = amqp://
    	    celery.imports = [list of classes: app.tasks.module]

	3. That's it! Give it a try [#b]_::
	    
	    $ paster celeryd development.ini

**Please Note:**

.. [#a] Application label may vary depending on Pylons setup. 

.. [#c] Working on the assumption you've set up ``user``, ``vhost``, etc using ``rabbitmqctl``

.. [#b] Depending on your Pylons setup, you may need to append
   ``#_your_app_name_`` to the ``development.ini`` paster config file
   argument::

   $ paster celeryd development.ini#foo


Running the celery worker server
================================

Assuming you've got your virtualenv activated::

    $ paster celeryd -B

However, in production you'll probably want to run the work in the
background as a daemon. You'll need to rely on the tools provided by
your platform. See the celery docs `Running Celery as a Daemon`_.

.. _`Running Celery as a Daemon`: http://celeryq.org/docs/cookbook/daemonizing.html

For a complete listing of the command line optinos available, use the help command::

    $ paster help

Defining and executing tasks
============================

**Please note:** All the tasks have to be stored in a real module, they can't
be defined in the python shell or ipython/bpython. This is because the celery
worker server needs access to the task function to be able to run it.

Put tasks in the ``tasks`` module of your Pylons application. The
worker server will **not** automatically load your tasks. They must be
listed in your ``development.ini`` file.

see `Configuring your Pylons project to use Celery`_ for more information.

.. _where-to-go:

Where to go from here
=====================

To learn more you should read the `Celery User Guide`_, and the `Celery Documentation`_.

.. _Celery User Guide: http://celeryproject.org/docs/userguide/
.. _Celery Documentation: http://celeryproject.org/docs/

Want to learn more about RabbitMQ? Check out their `getting started`_ page for a plethora of information.

.. _getting started: http://www.rabbitmq.com/how.html

Or, take a look at RabbitMQ's `configuration`_ page for more details on RabbitMQ configuration

.. _configuration: http://www.rabbitmq.com/man/rabbitmqctl.1.man.html/
