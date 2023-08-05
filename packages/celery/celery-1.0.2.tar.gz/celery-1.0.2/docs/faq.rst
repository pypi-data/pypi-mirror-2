============================
 Frequently Asked Questions
============================

General
=======

What kinds of things should I use celery for?
---------------------------------------------

**Answer:** `Queue everything and delight everyone`_ is a good article
describing why you would use a queue in a web context.

.. _`Queue everything and delight everyone`:
    http://decafbad.com/blog/2008/07/04/queue-everything-and-delight-everyone

These are some common use cases:

* Running something in the background. For example, to finish the web request
  as soon as possible, then update the users page incrementally.
  This gives the user the impression of good performane and "snappiness", even
  though the real work might actually take some time.

* Running something after the web request has finished.

* Making sure something is done, by executing it asynchronously and using
  retries.

* Scheduling periodic work.

And to some degree:

* Distributed computing.

* Parallel execution.


Misconceptions
==============

Is celery dependent on pickle?
------------------------------

**Answer:** No.

Celery can support any serialization scheme and has support for JSON/YAML and
Pickle by default. You can even send one task using pickle, and another one
with JSON seamlessly, this is because every task is associated with a
content-type. The default serialization scheme is pickle because it's the most
used, and it has support for sending complex objects as task arguments.

You can set a global default serializer, the default serializer for a
particular Task, or even what serializer to use when sending a single task
instance.

Is celery for Django only?
--------------------------

**Answer:** No.

You can use all of the features without using Django.


Why is Django a dependency?
---------------------------

Celery uses the Django ORM for database access when using the database result
backend, the Django cache framework when using the cache result backend, and the Django signal
dispatch mechanisms for signaling.

This doesn't mean you need to have a Django project to use celery, it
just means that sometimes we use internal Django components.

The long term plan is to replace these with other solutions, (e.g. `SQLAlchemy`_ as the ORM,
and `louie`_, for signaling). The celery distribution will be split into two:

    * celery

        The core. Using SQLAlchemy for the database backend.

    * django-celery

        Celery integration for Django, using the Django ORM for the database
        backend.

We're currently seeking people with `SQLAlchemy`_ experience, so please
contact the project if you want this done sooner.

The reason for the split is for purity only. It shouldn't affect you much as a
user, so please don't worry about the Django dependency, just have a good time
using celery.

.. _`SQLAlchemy`: http://www.sqlalchemy.org/
.. _`louie`: http://pypi.python.org/pypi/Louie/


Do I have to use AMQP/RabbitMQ?
-------------------------------

**Answer**: No.

You can also use Redis or an SQL database, see `Using other
queues`_.

.. _`Using other queues`:
    http://ask.github.com/celery/tutorials/otherqueues.html

Redis or a database won't perform as well as
an AMQP broker. If you have strict reliability requirements you are
encouraged to use RabbitMQ or another AMQP broker. Redis/database also use
polling, so they are likely to consume more resources. However, if you for
some reason are not able to use AMQP, feel free to use these alternatives.
They will probably work fine for most use cases, and note that the above
points are not specific to celery; If using Redis/database as a queue worked
fine for you before, it probably will now. You can always upgrade later
if you need to.

Is celery multi-lingual?
------------------------

**Answer:** Yes.

celeryd is an implementation of celery in python. If the language has an AMQP
client, there shouldn't be much work to create a worker in your language.
A celery worker is just a program connecting to the broker to consume
messages. There's no other communication involved.

Also, there's another way to be language indepedent, and that is to use REST
tasks, instead of your tasks being functions, they're URLs. With this
information you can even create simple web servers that enable preloading of
code. See: `User Guide: Remote Tasks`_.

.. _`User Guide: Remote Tasks`:
    http://ask.github.com/celery/userguide/remote-tasks.html


Troubleshooting
===============

MySQL is throwing deadlock errors, what can I do?
-------------------------------------------------

**Answer:** MySQL has default isolation level set to ``REPEATABLE-READ``,
if you don't really need that, set it to ``READ-COMMITTED``.
You can do that by adding the following to your ``my.cnf``::

    [mysqld]
    transaction-isolation = READ-COMMITTED

For more information about InnoDBs transaction model see `MySQL - The InnoDB
Transaction Model and Locking`_ in the MySQL user manual.

(Thanks to Honza Kral and Anton Tsigularov for this solution)

.. _`MySQL - The InnoDB Transaction Model and Locking`: http://dev.mysql.com/doc/refman/5.1/en/innodb-transaction-model.html

celeryd is not doing anything, just hanging
--------------------------------------------

**Answer:** See `MySQL is throwing deadlock errors, what can I do?`_.
            or `Why is Task.delay/apply\* just hanging?`.

Why is Task.delay/apply\*/celeryd just hanging?
-----------------------------------------------

**Answer:** There is a bug in some AMQP clients that will make it hang if
it's not able to authenticate the current user, the password doesn't match or
the user does not have access to the virtual host specified. Be sure to check
your broker logs (for RabbitMQ that is ``/var/log/rabbitmq/rabbit.log`` on
most systems), it usually contains a message describing the reason.

Why won't celeryd run on FreeBSD?
---------------------------------

**Answer:** multiprocessing.Pool requires a working POSIX semaphore
implementation which isn't enabled in FreeBSD by default. You have to enable
POSIX semaphores in the kernel and manually recompile multiprocessing.

Luckily, Viktor Petersson has written a tutorial to get you started with
Celery on FreeBSD here:
http://www.playingwithwire.com/2009/10/how-to-get-celeryd-to-work-on-freebsd/

I'm having ``IntegrityError: Duplicate Key`` errors. Why?
---------------------------------------------------------

**Answer:** See `MySQL is throwing deadlock errors, what can I do?`_.
Thanks to howsthedotcom.

Why aren't my tasks processed?
------------------------------

**Answer:** With RabbitMQ you can see how many consumers are currently
receiving tasks by running the following command::

    $ rabbitmqctl list_queues -p <myvhost> name messages consumers
    Listing queues ...
    celery     2891    2

This shows that there's 2891 messages waiting to be processed in the task
queue, and there are two consumers processing them.

One reason that the queue is never emptied could be that you have a stale
celery process taking the messages hostage. This could happen if celeryd
wasn't properly shut down.

When a message is recieved by a worker the broker waits for it to be
acknowledged before marking the message as processed. The broker will not
re-send that message to another consumer until the consumer is shut down
properly.

If you hit this problem you have to kill all workers manually and restart
them::

    ps auxww | grep celeryd | awk '{print $2}' | xargs kill

You might have to wait a while until all workers have finished the work they're
doing. If it's still hanging after a long time you can kill them by force
with::

    ps auxww | grep celeryd | awk '{print $2}' | xargs kill -9

Why won't my Task run?
----------------------

**Answer:** Did you register the task in the applications ``tasks.py`` module?
(or in some other module Django loads by default, like ``models.py``?).
Also there might be syntax errors preventing the tasks module being imported.

You can find out if celery is able to run the task by executing the
task manually:

    >>> from myapp.tasks import MyPeriodicTask
    >>> MyPeriodicTask.delay()

Watch celeryds logfile to see if it's able to find the task, or if some
other error is happening.

Why won't my Periodic Task run?
-------------------------------

**Answer:** See `Why won't my Task run?`_.

How do I discard all waiting tasks?
------------------------------------

**Answer:** Use ``celery.task.discard_all()``, like this:

    >>> from celery.task import discard_all
    >>> discard_all()
    1753

The number ``1753`` is the number of messages deleted.

You can also start celeryd with the ``--discard`` argument which will
accomplish the same thing.

I've discarded messages, but there are still messages left in the queue?
------------------------------------------------------------------------

**Answer:** Tasks are acknowledged (removed from the queue) as soon
as they are actually executed. After the worker has received a task, it will
take some time until it is actually executed, especially if there are a lot
of tasks already waiting for execution. Messages that are not acknowledged are
hold on to by the worker until it closes the connection to the broker (AMQP
server). When that connection is closed (e.g because the worker was stopped)
the tasks will be re-sent by the broker to the next available worker (or the
same worker when it has been restarted), so to properly purge the queue of
waiting tasks you have to stop all the workers, and then discard the tasks
using ``discard_all``.


Windows: The ``-B`` / ``--beat`` option to celeryd doesn't work?
----------------------------------------------------------------
**Answer**: That's right. Run ``celerybeat`` and ``celeryd`` as separate
services instead.

Results
=======

How dow I get the result of a task if I have the ID that points there?
----------------------------------------------------------------------

**Answer**: Use ``Task.AsyncResult``::

    >>> result = MyTask.AsyncResult(task_id)
    >>> result.get()

This will give you a :class:`celery.result.BaseAsyncResult` instance
using the tasks current result backend.

If you need to specify a custom result backend you should use
:class:`celery.result.BaseAsyncResult` directly::

    >>> from celery.result import BaseAsyncResult
    >>> result = BaseAsyncResult(task_id, backend=...)
    >>> result.get()

Brokers
=======

Can I use celery with ActiveMQ/STOMP?
-------------------------------------

**Answer**: Yes, but this is somewhat experimental for now.
It is working ok in a test configuration, but it has not
been tested in production like RabbitMQ has. If you have any problems with
using STOMP and celery, please report the bugs to the issue tracker:

    http://github.com/ask/celery/issues/

First you have to use the ``master`` branch of ``celery``::

    $ git clone git://github.com/ask/celery.git
    $ cd celery
    $ sudo python setup.py install
    $ cd ..

Then you need to install the ``stompbackend`` branch of ``carrot``::

    $ git clone git://github.com/ask/carrot.git
    $ cd carrot
    $ git checkout stompbackend
    $ sudo python setup.py install
    $ cd ..

And my fork of ``python-stomp`` which adds non-blocking support::

    $ hg clone http://bitbucket.org/asksol/python-stomp/
    $ cd python-stomp
    $ sudo python setup.py install
    $ cd ..

In this example we will use a queue called ``celery`` which we created in
the ActiveMQ web admin interface.

**Note**: For ActiveMQ the queue name has to have ``"/queue/"`` prepended to
it. i.e. the queue ``celery`` becomes ``/queue/celery``.

Since a STOMP queue is a single named entity and it doesn't have the
routing capabilities of AMQP you need to set both the ``queue``, and
``exchange`` settings to your queue name. This is a minor inconvenience since
carrot needs to maintain the same interface for both AMQP and STOMP (obviously
the one with the most capabilities won).

Use the following specific settings in your ``settings.py``:

.. code-block:: python

    # Makes python-stomp the default backend for carrot.
    CARROT_BACKEND = "stomp"

    # STOMP hostname and port settings.
    BROKER_HOST = "localhost"
    BROKER_PORT = 61613

    # The queue name to use (both queue and exchange must be set to the
    # same queue name when using STOMP)
    CELERY_DEFAULT_QUEUE = "/queue/celery"
    CELERY_DEFAULT_EXCHANGE = "/queue/celery" 

    CELERY_QUEUES = {
        "/queue/celery": {"exchange": "/queue/celery"}
    }

Now you can go on reading the tutorial in the README, ignoring any AMQP
specific options. 

What features are not supported when using STOMP?
--------------------------------------------------

This is a (possible incomplete) list of features not available when
using the STOMP backend:

    * routing keys

    * exchange types (direct, topic, headers, etc)

    * immediate

    * mandatory

Features
========

Can I send some tasks to only some servers?
--------------------------------------------

**Answer:** Yes. You can route tasks to an arbitrary server using AMQP,
and a worker can bind to as many queues as it wants.

Say you have two servers, ``x``, and ``y`` that handles regular tasks,
and one server ``z``, that only handles feed related tasks, you can use this
configuration:

* Servers ``x`` and ``y``: settings.py:

.. code-block:: python

    CELERY_DEFAULT_QUEUE = "regular_tasks"
    CELERY_QUEUES = {
        "regular_tasks": {
            "binding_key": "task.#",
        },
    }
    CELERY_DEFAULT_EXCHANGE = "tasks"
    CELERY_DEFAULT_EXCHANGE_TYPE = "topic"
    CELERY_DEFAULT_ROUTING_KEY = "task.regular"

* Server ``z``: settings.py:

.. code-block:: python

        CELERY_DEFAULT_QUEUE = "feed_tasks"
        CELERY_QUEUES = {
            "feed_tasks": {
                "binding_key": "feed.#",
            },
        }
        CELERY_DEFAULT_EXCHANGE = "tasks"
        CELERY_DEFAULT_ROUTING_KEY = "task.regular"
        CELERY_DEFAULT_EXCHANGE_TYPE = "topic"

``CELERY_QUEUES`` is a map of queue names and their exchange/type/binding_key,
if you don't set exchange or exchange type, they will be taken from the
``CELERY_DEFAULT_EXCHANGE``/``CELERY_DEFAULT_EXCHANGE_TYPE`` settings.

Now to make a Task run on the ``z`` server you need to set its
``routing_key`` attribute so it starts with the words ``"task.feed."``:

.. code-block:: python

    from feedaggregator.models import Feed
    from celery.decorators import task

    @task(routing_key="feed.importer")
    def import_feed(feed_url):
        Feed.objects.import_feed(feed_url)

or if subclassing the ``Task`` class directly:

.. code-block:: python

    class FeedImportTask(Task):
        routing_key = "feed.importer"

        def run(self, feed_url):
            Feed.objects.import_feed(feed_url)


You can also override this using the ``routing_key`` argument to
:func:`celery.task.apply_async`:

    >>> from myapp.tasks import RefreshFeedTask
    >>> RefreshFeedTask.apply_async(args=["http://cnn.com/rss"],
    ...                             routing_key="feed.importer")


 If you want, you can even have your feed processing worker handle regular
 tasks as well, maybe in times when there's a lot of work to do.
 Just add a new queue to server ``z``'s ``CELERY_QUEUES``:

 .. code-block:: python

        CELERY_QUEUES = {
            "feed_tasks": {
                "binding_key": "feed.#",
            },
            "regular_tasks": {
                "binding_key": "task.#",
            },
        }

Since the default exchange is ``tasks``, they will both use the same
exchange.

If you have another queue but on another exchange you want to add,
just specify a custom exchange and exchange type:

.. code-block:: python

    CELERY_QUEUES = {
            "feed_tasks": {
                "binding_key": "feed.#",
            },
            "regular_tasks": {
                "binding_key": "task.#",
            }
            "image_tasks": {
                "binding_key": "image.compress",
                "exchange": "mediatasks",
                "exchange_type": "direct",
            },
        }

If you're confused about these terms, you should read up on AMQP and RabbitMQ.
`Rabbits and Warrens`_ is an excellent blog post describing queues and
exchanges. There's also AMQP in 10 minutes*: `Flexible Routing Model`_,
and `Standard Exchange Types`_. For users of RabbitMQ the `RabbitMQ FAQ`_
could also be useful as a source of information.

.. _`Rabbits and Warrens`: http://blogs.digitar.com/jjww/2009/01/rabbits-and-warrens/
.. _`Flexible Routing Model`: http://bit.ly/95XFO1
.. _`Standard Exchange Types`: http://bit.ly/EEWca
.. _`RabbitMQ FAQ`: http://www.rabbitmq.com/faq.html

Can I use celery without Django?
--------------------------------

**Answer:** Yes.

Celery uses something called loaders to read/setup configuration, import
modules that register tasks and to decide what happens when a task is
executed. Currently there are two loaders, the default loader and the Django
loader. If you want to use celery without a Django project, you either have to
use the default loader, or write a loader of your own.

The rest of this answer describes how to use the default loader.

While it is possible to use Celery from outside of Django, we still need
Django itself to run, this is to use the ORM and cache-framework.
Duplicating these features would be time consuming and mostly pointless, so
while me might rewrite these in the future, this is a good solution in the
mean time.
Install Django using your favorite install tool, ``easy_install``, ``pip``, or
whatever::

    # easy_install django # as root

You need a configuration file named ``celeryconfig.py``, either in the
directory you run ``celeryd`` in, or in a Python library path where it is
able to find it. The configuration file can contain any of the settings
described in :mod:`celery.conf`. In addition; if you're using the
database backend you have to configure the database. Here is an example
configuration using the database backend with MySQL:

.. code-block:: python

    # Broker configuration
    BROKER_HOST = "localhost"
    BROKER_PORT = "5672"
    BROKER_VHOST = "celery"
    BROKER_USER = "celery"
    BROKER_PASSWORD = "celerysecret"
    CARROT_BACKEND="amqp"

    # Using the database backend.
    CELERY_RESULT_BACKEND = "database"
    DATABASE_ENGINE = "mysql" # see Django docs for a description of these.
    DATABASE_NAME = "mydb"
    DATABASE_HOST = "mydb.example.org"
    DATABASE_USER = "myuser"
    DATABASE_PASSWORD = "mysecret"

    # Number of processes that processes tasks simultaneously.
    CELERYD_CONCURRENCY = 8

    # Modules to import when celeryd starts.
    # This must import every module where you register tasks so celeryd
    # is able to find and run them.
    CELERY_IMPORTS = ("mytaskmodule1", "mytaskmodule2")
    
With this configuration file in the current directory you have to
run ``celeryinit`` to create the database tables::

    $ celeryinit

At this point you should be able to successfully run ``celeryd``::

    $ celeryd --loglevel=INFO

and send a task from a python shell (note that it must be able to import
``celeryconfig.py``):

    >>> from celery.task.builtins import PingTask
    >>> result = PingTask.apply_async()
    >>> result.get()
    'pong'

The celery test-suite is failing
--------------------------------

**Answer**: If you're running tests from your Django project, and the celery
test suite is failing in that context, then follow the steps below. If the
celery tests are failing in another context, please report an issue to our
issue tracker at GitHub:

    http://github.com/ask/celery/issues/

That Django is running tests for all applications in ``INSTALLED_APPS``
by default is a pet peeve for many. You should use a test runner that either

    1) Explicitly lists the apps you want to run tests for, or

    2) Make a test runner that skips tests for apps you don't want to run.

For example the test runner that celery is using:

    http://bit.ly/NVKep

To use this test runner, add the following to your ``settings.py``:

.. code-block:: python

    TEST_RUNNER = "celery.tests.runners.run_tests"
    TEST_APPS = (
        "app1",
        "app2",
        "app3",
        "app4",
    )

Or, if you just want to skip the celery tests:

.. code-block:: python

    INSTALLED_APPS = (.....)
    TEST_RUNNER = "celery.tests.runners.run_tests"
    TEST_APPS = filter(lambda k: k != "celery", INSTALLED_APPS)


Can I change the interval of a periodic task at runtime?
--------------------------------------------------------

**Answer**: Yes. You can override ``PeriodicTask.is_due`` or turn
``PeriodicTask.run_every`` into a property:

.. code-block:: python

    class MyPeriodic(PeriodicTask):

        def run(self):
            # ...

        @property
        def run_every(self):
            return get_interval_from_database(...)


Does celery support task priorities?
------------------------------------

**Answer**: No. In theory, yes, as AMQP supports priorities. However
RabbitMQ doesn't implement them yet.

The usual way to prioritize work in celery, is to route high priority tasks
to different servers. In the real world this may actually work better than per message
priorities. You can use this in combination with rate limiting to achieve a
highly performant system.

Can I schedule tasks to execute at a specific time?
---------------------------------------------------

.. module:: celery.task.base

**Answer**: Yes. You can use the ``eta`` argument of :meth:`Task.apply_async`.

However, you can't schedule a periodic task at a specific time yet.
The good news is, if anyone is willing
to implement it, it shouldn't be that hard. Some pointers to achieve this has
been written here: http://bit.ly/99UQNO


How do I shut down ``celeryd`` safely?
--------------------------------------

**Answer**: Use the ``TERM`` signal, and celery will finish all currently
executing jobs and shut down as soon as possible. No tasks should be lost.

You should never stop ``celeryd`` with the ``KILL`` signal (``-9``),
unless you've tried ``TERM`` a few times and waited a few minutes to let it
get a chance to shut down.
