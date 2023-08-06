#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 by Łukasz Langa
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""A drop-in substitute for the default ``django.core.cache`` object. This
implementation is using a modified mint cache approach based on
http://www.djangosnippets.org/snippets/793/.

This implementation does not support specifying fallback values for the
``get()`` function since it would not be possible to otherwise reliably
communicate that the value is *stale* and has
to be updated.

Configured by three values in ``settings.py``:

* ``CACHE_DEFAULT_TIMEOUT`` - how long a set value should be considered valid
  (in seconds). After this period the value is considered *stale*, a single
  request starts to update it, and subsequent requests get the old value until
  the value gets updated. **Default**: 300 seconds.

* ``CACHE_FILELOCK_PATH`` - path to a non-existant file which will work as an
  interprocess lock to make cache access atomic. **Default**:
  ``/tmp/langacore_django_cache.lock``

* ``CACHE_MINT_DELAY`` - an upper bound on how long a value should take to be
  generated (in seconds). This value is used for *stale* keys and is the real
  time after which the key is completely removed from the cache. **Default**:
  30 seconds.
"""

# More info in the documentation at 
# http://packages.python.org/lck.django/

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
from threading import RLock

from django.core.cache import cache
from django.conf import settings

from lck.concurrency import synchronized

CACHE_MINT_DELAY = getattr(settings, 'CACHE_MINT_DELAY', 30)
CACHE_DEFAULT_TIMEOUT = getattr(settings, 'CACHE_DEFAULT_TIMEOUT', 300)
CACHE_FILELOCK_PATH = getattr(settings, 'CACHE_FILELOCK_PATH',
    '/tmp/langacore_django_cache.lock')


@synchronized(path=CACHE_FILELOCK_PATH)
def get(key):
    """Get a value from the cache.

    :param key: the key for which to return the value
    """

    packed_val = cache.get(key)
    if packed_val is None:
        return None
    val, refresh_time, is_stale = packed_val
    if (time.time() > refresh_time) and not is_stale:
        # Store the stale value while the cache revalidates for another
        # CACHE_MINT_DELAY seconds.
        set(key, val, timeout=CACHE_MINT_DELAY, _is_stale=True)
        return None
    return val


@synchronized(path=CACHE_FILELOCK_PATH)
def set(key, val, timeout=CACHE_DEFAULT_TIMEOUT, _is_stale=False):
    """Set a value in the cache.

    :param key: the key under which to set the value

    :param val: the value to set

    :param timeout: how long should this value be valid, by default
                    CACHE_DEFAULT_TIMEOUT

    :param _is_stale: boolean, used internally to set a stale value in the
                      cache back-end. Don't use on your own.
    """
    refresh_time = timeout + time.time()
    # if not stale, add the mint delay to the actual refresh so we can have
    # the value stored a bit longer in the backend than it would be otherwise
    real_refresh = timeout if _is_stale else timeout + CACHE_MINT_DELAY
    packed_val = (val, refresh_time, _is_stale)
    return cache.set(key, packed_val, real_refresh)


@synchronized(path=CACHE_FILELOCK_PATH)
def delete(key):
    """Removes a value from the cache.

    :param key: the key to delete from the cache
    """

    return cache.delete(key)
