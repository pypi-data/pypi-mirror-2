import socket
import unittest2 as unittest

from celery.task.builtins import PingTask
from celery.utils import gen_unique_id
from celery.worker import control
from celery.worker.revoke import revoked
from celery.registry import tasks

hostname = socket.gethostname()


class TestControlPanel(unittest.TestCase):

    def setUp(self):
        self.panel = self.create_panel(listener=object())

    def create_panel(self, **kwargs):
        return control.ControlDispatch(hostname=hostname, **kwargs)

    def test_shutdown(self):
        self.assertRaises(SystemExit, self.panel.execute, "shutdown")

    def test_dump_tasks(self):
        self.panel.execute("dump_tasks")

    def test_rate_limit(self):

        class Listener(object):

            class ReadyQueue(object):
                fresh = False

                def refresh(self):
                    self.fresh = True

            def __init__(self):
                self.ready_queue = self.ReadyQueue()

        listener = Listener()
        panel = self.create_panel(listener=listener)

        task = tasks[PingTask.name]
        old_rate_limit = task.rate_limit
        try:
            panel.execute("rate_limit", kwargs=dict(task_name=task.name,
                                                    rate_limit="100/m"))
            self.assertEqual(task.rate_limit, "100/m")
            self.assertTrue(listener.ready_queue.fresh)
            listener.ready_queue.fresh = False
            panel.execute("rate_limit", kwargs=dict(task_name=task.name,
                                                    rate_limit=0))
            self.assertEqual(task.rate_limit, 0)
            self.assertTrue(listener.ready_queue.fresh)
        finally:
            task.rate_limit = old_rate_limit

    def test_rate_limit_nonexistant_task(self):
        self.panel.execute("rate_limit", kwargs={
                                "task_name": "xxxx.does.not.exist",
                                "rate_limit": "1000/s"})

    def test_unexposed_command(self):
        self.panel.execute("foo", kwargs={})

    def test_revoke(self):
        uuid = gen_unique_id()
        m = {"command": "revoke",
             "destination": hostname,
             "task_id": uuid}
        self.panel.dispatch_from_message(m)
        self.assertIn(uuid, revoked)

        m = {"command": "revoke",
             "destination": "does.not.exist",
             "task_id": uuid + "xxx"}
        self.panel.dispatch_from_message(m)
        self.assertNotIn(uuid + "xxx", revoked)
