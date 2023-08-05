=======================
 Internals: The worker
=======================

**NOTE** This describes the internals of the development version, not the
current release.

The worker consists of 4 main components: the broker listener, the scheduler,
the mediator and the task pool. All these components runs in parallel working
with two data structures: the ready queue and the ETA schedule.

.. image:: http://cloud.github.com/downloads/ask/celery/Celery1.0-inside-worker.jpg

Data structures
===============

ready_queue
-----------

The ready queue is either an instance of :class:`Queue.Queue`, or
`celery.buckets.TaskBucket`. The latter if rate limiting is enabled.

eta_schedule
------------

The ETA schedule is a heap queue sorted by time.


Components
==========


CarrotListener
--------------

Receives messages from the broker using ``carrot``.

When a message is received it's converted into a
:class:`celery.worker.job.TaskWrapper` object.

Tasks with an ETA are entered into the ``eta_schedule``, messages that can
be immediately processed are moved directly to the ``ready_queue``.

ScheduleController
------------------

The schedule controller is running the ``eta_schedule``.
If the scheduled tasks eta has passed it is moved to the ``ready_queue``,
otherwise the thread sleeps until the eta is met (remember that the schedule
is sorted by time).

Mediator
--------
The mediator simply moves tasks in the ``ready_queue`` over to the
task pool for execution using
:meth:`celery.worker.job.TaskWrapper.execute_using_pool`.

TaskPool
--------

This is a slightly modified :class:`multiprocessing.Pool`.
It mostly works the same way, except it makes sure all of the workers
are running at all times. If a worker is missing, it replaces
it with a new one.
