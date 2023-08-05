from billiard.utils.functional import curry

from celery import conf
from celery.utils import get_cls_by_name

BACKEND_ALIASES = {
    "amqp": "celery.backends.amqp.AMQPBackend",
    "database": "celery.backends.database.DatabaseBackend",
    "db": "celery.backends.database.DatabaseBackend",
    "redis": "celery.backends.pyredis.RedisBackend",
    "cache": "celery.backends.cache.CacheBackend",
    "mongodb": "celery.backends.mongodb.MongoBackend",
    "tyrant": "celery.backends.tyrant.TyrantBackend",
}

_backend_cache = {}


def get_backend_cls(backend):
    """Get backend class by name/alias"""
    if backend not in _backend_cache:
        _backend_cache[backend] = get_cls_by_name(backend, BACKEND_ALIASES)
    return _backend_cache[backend]


"""
.. function:: get_default_backend_cls()

    Get the backend class specified in :setting:`CELERY_RESULT_BACKEND`.

"""
get_default_backend_cls = curry(get_backend_cls, conf.RESULT_BACKEND)


"""
.. class:: DefaultBackend

    The default backend class used for storing task results and status,
    specified in :setting:`CELERY_RESULT_BACKEND`.

"""
DefaultBackend = get_default_backend_cls()

"""
.. data:: default_backend

    An instance of :class:`DefaultBackend`.

"""
default_backend = DefaultBackend()
