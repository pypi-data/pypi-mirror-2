from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist

from celery import states
from celery.events.snapshot import Polaroid
from celery.utils import maybe_iso8601

from djcelery.models import WorkerState, TaskState

SUCCESS_STATES = frozenset([states.SUCCESS])
KEEP_FROM_RECEIVED = ("name", "args", "kwargs",
                      "retries", "eta", "expires")


class Camera(Polaroid):
    WorkerState = WorkerState
    TaskState = TaskState

    expire_states = {SUCCESS_STATES: timedelta(days=1),
                     states.EXCEPTION_STATES: timedelta(days=3),
                     states.UNREADY_STATES: timedelta(days=5)}

    def __init__(self, *args, **kwargs):
        super(Camera, self).__init__(*args, **kwargs)
        self.prev_count = 0

    def get_heartbeat(self, worker):
        try:
            heartbeat = worker.heartbeats[-1]
        except IndexError:
            return
        return datetime.fromtimestamp(heartbeat)

    def handle_worker(self, (hostname, worker)):
        return self.WorkerState.objects.update_or_create(
                    hostname=hostname,
                    defaults={"last_heartbeat":
                        self.get_heartbeat(worker)})

    def handle_task(self, (uuid, task), worker=None):
        if task.worker.hostname:
            worker = self.handle_worker((task.worker.hostname, task.worker))
        return self.update_task(task.state, task_id=uuid,
                defaults={"name": task.name,
                          "args": task.args,
                          "kwargs": task.kwargs,
                          "eta": maybe_iso8601(task.eta),
                          "expires": maybe_iso8601(task.expires),
                          "state": task.state,
                          "tstamp": datetime.fromtimestamp(task.timestamp),
                          "result": task.result or task.exception,
                          "traceback": task.traceback,
                          "runtime": task.runtime,
                          "worker": worker})

    def update_task(self, state, **kwargs):
        objects = self.TaskState.objects
        defaults = kwargs.pop("defaults", None) or {}
        try:
            obj = objects.get(**kwargs)
        except ObjectDoesNotExist:
            if not defaults.get("name"):
                return
            return objects.create(**dict(kwargs, **defaults))
        else:
            if state != "RECEIVED":
                defaults = dict((k, v)
                            for k, v in defaults.items()
                                if k not in KEEP_FROM_RECEIVED)

        for k, v in defaults.items():
            setattr(obj, k, v)
        obj.save()

        return obj

    def on_shutter(self, state):
        event_count = state.event_count
        if event_count != self.prev_count:
            map(self.handle_worker, state.workers.items())
            map(self.handle_task, state.tasks.items())
        self.prev_count = event_count

    def on_cleanup(self):
        dirty = sum(self.TaskState.objects.expire_by_states(states, expires)
                        for states, expires in self.expire_states.items())
        if dirty:
            self.debug("Cleanup: Marked %s objects as dirty." % (dirty, ))
            self.TaskState.objects.purge()
            self.debug("Cleanup: %s objects purged." % (dirty, ))
            return dirty
        return 0
