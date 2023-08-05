============================
 Frequently Asked Questions
============================

.. contents::
    :local:

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

Celery does not depend on Django anymore. To use Celery with Django you have
to use the `django-celery`_ package.

.. _`django-celery`: http://pypi.python.org/pypi/django-celery

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

**Answer:** There might be syntax errors preventing the tasks module being imported.

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


Results
=======

How do I get the result of a task if I have the ID that points there?
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

Why is RabbitMQ crashing?
-------------------------

RabbitMQ will crash if it runs out of memory. This will be fixed in a
future release of RabbitMQ. please refer to the RabbitMQ FAQ:
http://www.rabbitmq.com/faq.html#node-runs-out-of-memory

Some common Celery misconfigurations can crash RabbitMQ:

* Events.

Running ``celeryd`` with the ``-E``/``--events`` option will send messages
for events happening inside of the worker. If these event messages
are not consumed, you will eventually run out of memory.

Events should only be enabled if you have an active monitor consuming them.

* AMQP backend results.

When running with the AMQP result backend, every task result will be sent
as a message. If you don't collect these results, they will build up and
RabbitMQ will eventually run out of memory.

If you don't use the results for a task, make sure you set the
``ignore_result`` option:

.. code-block python

    @task(ignore_result=True)
    def mytask():
        ...

    class MyTask(Task):
        ignore_result = True

Results can also be disabled globally using the ``CELERY_IGNORE_RESULT``
setting.

Can I use celery with ActiveMQ/STOMP?
-------------------------------------

**Answer**: Yes, but this is somewhat experimental for now.
It is working ok in a test configuration, but it has not
been tested in production. If you have any problems
using STOMP with celery, please report an issue here::

    http://github.com/ask/celery/issues/

The STOMP carrot backend requires the `stompy`_ library::

    $ pip install stompy
    $ cd python-stomp
    $ sudo python setup.py install
    $ cd ..

.. _`stompy`: http://pypi.python.org/pypi/stompy

In this example we will use a queue called ``celery`` which we created in
the ActiveMQ web admin interface.

**Note**: When using ActiveMQ the queue name needs to have ``"/queue/"``
prepended to it. i.e. the queue ``celery`` becomes ``/queue/celery``.

Since STOMP doesn't have exchanges and the routing capabilities of AMQP,
you need to set ``exchange`` name to the same as the queue name. This is
a minor inconvenience since carrot needs to maintain the same interface
for both AMQP and STOMP.

Use the following settings in your ``celeryconfig.py``/django ``settings.py``:

.. code-block:: python

    # Use the stomp carrot backend.
    CARROT_BACKEND = "stomp"

    # STOMP hostname and port settings.
    BROKER_HOST = "localhost"
    BROKER_PORT = 61613

    # The queue name to use (the exchange *must* be set to the
    # same as the queue name when using STOMP)
    CELERY_DEFAULT_QUEUE = "/queue/celery"
    CELERY_DEFAULT_EXCHANGE = "/queue/celery" 

    CELERY_QUEUES = {
        "/queue/celery": {"exchange": "/queue/celery"}
    }

What features are not supported when using ghettoq/STOMP?
---------------------------------------------------------

This is a (possible incomplete) list of features not available when
using the STOMP backend:

    * routing keys

    * exchange types (direct, topic, headers, etc)

    * immediate

    * mandatory

Tasks
=====

How can I reuse the same connection when applying tasks?
--------------------------------------------------------

**Answer**: See :doc:`userguide/executing`.

Can I execute a task by name?
-----------------------------

**Answer**: Yes. Use :func:`celery.execute.send_task`.
You can also execute a task by name from any language
that has an AMQP client.

    >>> from celery.execute import send_task
    >>> send_task("tasks.add", args=[2, 2], kwargs={})
    <AsyncResult: 373550e8-b9a0-4666-bc61-ace01fa4f91d>


How can I get the task id of the current task?
----------------------------------------------

**Answer**: Celery does set some default keyword arguments if the task
accepts them (you can accept them by either using ``**kwargs``, or list them
specifically)::

    @task
    def mytask(task_id=None):
        cache.set(task_id, "Running")

The default keyword arguments are documented here:
http://celeryq.org/docs/userguide/tasks.html#default-keyword-arguments

Can I specify a custom task_id?
-------------------------------

**Answer**: Yes. Use the ``task_id`` argument to
:meth:`~celery.execute.apply_async`::

    >>> task.apply_async(args, kwargs, task_id="...")

Can I use natural task ids?
---------------------------

**Answer**: Yes, but make sure it is unique, as the behavior
for two tasks existing with the same id is undefined.

The world will probably not explode, but at the worst
they can overwrite each others results.

How can I run a task once another task has finished?
----------------------------------------------------

**Answer**: You can safely launch a task inside a task.
Also, a common pattern is to use callback tasks:

.. code-block:: python

    @task()
    def add(x, y, callback=None):
        result = x + y
        if callback:
            subtask(callback).delay(result)
        return result


    @task(ignore_result=True)
    def log_result(result, **kwargs):
        logger = log_result.get_logger(**kwargs)
        logger.info("log_result got: %s" % (result, ))

Invocation::

    >>> add.delay(2, 2, callback=log_result.subtask())

See :doc:`userguide/tasksets` for more information.

Can I cancel the execution of a task?
-------------------------------------
**Answer**: Yes. Use ``result.revoke``::

    >>> result = add.apply_async(args=[2, 2], countdown=120)
    >>> result.revoke()

or if you only have the task id::

    >>> from celery.task.control import revoke
    >>> revoke(task_id)

Why aren't my remote control commands received by all workers?
--------------------------------------------------------------

**Answer**: To receive broadcast remote control commands, every ``celeryd``
uses its hostname to create a unique queue name to listen to,
so if you have more than one worker with the same hostname, the
control commands will be recieved in round-robin between them.

To work around this you can explicitly set the hostname for every worker
using the ``--hostname`` argument to ``celeryd``::

    $ celeryd --hostname=$(hostname).1
    $ celeryd --hostname=$(hostname).2

etc, etc.

Can I send some tasks to only some servers?
--------------------------------------------

**Answer:** Yes. You can route tasks to an arbitrary server using AMQP,
and a worker can bind to as many queues as it wants.

See :doc:`userguide/routing` for more information.

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

Should I use retry or acks_late?
--------------------------------

**Answer**: Depends. It's not necessarily one or the other, you may want
to use both.

``Task.retry`` is used to retry tasks, notably for expected errors that
is catchable with the ``try:`` block. The AMQP transaction is not used
for these errors: **if the task raises an exception it is still acked!**.

The ``acks_late`` setting would be used when you need the task to be
executed again if the worker (for some reason) crashes mid-execution.
It's important to note that the worker is not known to crash, and if
it does it is usually an unrecoverable error that requires human
intervention (bug in the worker, or task code).

In an ideal world you could safely retry any task that has failed, but
this is rarely the case. Imagine the following task:

.. code-block:: python

    @task()
    def process_upload(filename, tmpfile):
        # Increment a file count stored in a database
        increment_file_counter()
        add_file_metadata_to_db(filename, tmpfile)
        copy_file_to_destination(filename, tmpfile)

If this crashed in the middle of copying the file to its destination
the world would contain incomplete state. This is not a critical
scenario of course, but you can probably imagine something far more
sinister. So for ease of programming we have less reliability;
It's a good default, users who require it and know what they
are doing can still enable acks_late (and in the future hopefully
use manual acknowledgement)

In addition ``Task.retry`` has features not available in AMQP
transactions: delay between retries, max retries, etc.

So use retry for Python errors, and if your task is reentrant
combine that with ``acks_late`` if that level of reliability
is required.


Can I schedule tasks to execute at a specific time?
---------------------------------------------------

.. module:: celery.task.base

**Answer**: Yes. You can use the ``eta`` argument of :meth:`Task.apply_async`.

Or to schedule a periodic task at a specific time, use the
:class:`celery.task.schedules.crontab` schedule behavior:


.. code-block:: python

    from celery.task.schedules import crontab
    from celery.decorators import periodic_task

    @periodic_task(run_every=crontab(hours=7, minute=30, day_of_week="mon"))
    def every_monday_morning():
        print("This is run every monday morning at 7:30")

How do I shut down ``celeryd`` safely?
--------------------------------------

**Answer**: Use the ``TERM`` signal, and celery will finish all currently
executing jobs and shut down as soon as possible. No tasks should be lost.

You should never stop ``celeryd`` with the ``KILL`` signal (``-9``),
unless you've tried ``TERM`` a few times and waited a few minutes to let it
get a chance to shut down. As if you do tasks may be terminated mid-execution,
and they will not be re-run unless you have the ``acks_late`` option set.
(``Task.acks_late`` / ``CELERY_ACKS_LATE``).

How do I run celeryd in the background on [platform]?
-----------------------------------------------------
**Answer**: Please see :doc:`cookbook/daemonizing`.

Windows
=======

celeryd keeps spawning processes at startup
-------------------------------------------

**Answer**: This is a known issue on Windows.
You have to start celeryd with the command::

    $ python -m celeryd.bin.celeryd

Any additional arguments can be appended to this command.

See http://bit.ly/bo9RSw

The ``-B`` / ``--beat`` option to celeryd doesn't work?
----------------------------------------------------------------
**Answer**: That's right. Run ``celerybeat`` and ``celeryd`` as separate
services instead.

``django-celery`` can’t find settings?
--------------------------------------

**Answer**: You need to specify the ``--settings`` argument to ``manage.py``::

    $ python manage.py celeryd start --settings=settings

See http://bit.ly/bo9RSw
