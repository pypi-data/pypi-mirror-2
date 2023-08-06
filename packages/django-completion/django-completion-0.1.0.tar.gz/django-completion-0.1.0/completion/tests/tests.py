import warnings

from django.conf import settings

from completion import constants
from completion.tests.site import *
from completion.tests.utils import *


try:
    import psycopg2
except ImportError:
    warnings.warn('Skipping postgres backend tests, psycopg2 not installed')
else:
    from completion.tests.pg_backend import *

try:
    import redis
except ImportError:
    warnings.warn('Skipping redis backend tests, redis-py not installed')
else:
    if not constants.REDIS_CONNECTION:
        warnings.warn('Skipping redis backend tests, no connection configured')
    else:
        from completion.tests.redis_backend import *

try:
    import pysolr
except ImportError:
    warnings.warn('Skipping solr backend tests, pysolr not installed')
else:
    if not constants.SOLR_CONNECTION:
        warnings.warn('Skipping solr backend tests, no connection configured')
    else:
        from completion.tests.solr_backend import *
