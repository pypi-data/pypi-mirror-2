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

"""A couple of useful middleware classes related to common framework
functionality (including contrib)."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime, timedelta
from operator import add
import re
from time import time

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.utils import translation


class TimingMiddleware(object):
    """Taken from https://code.djangoproject.com/wiki/PageStatsMiddleware.

    Requires ending the base template with ``<!--STATS-->``.

    in the base template. Also, this middleware should be absolutely the first
    one on the list. That way the measurements are more realistic. See:

    https://docs.djangoproject.com/en/dev/topics/http/middleware/
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        n = len(connection.queries)
        start = time()
        response = view_func(request, *view_args, **view_kwargs)
        totTime = time() - start
        queries = len(connection.queries) - n
        if queries:
            dbTime = reduce(add, [float(q['time']) for q in
                connection.queries[n:]])
        else:
            dbTime = 0.0
        pyTime = totTime - dbTime
        stats = {
            'totTime': "%.2f" % totTime,
            'pyTime': "%.2f" % pyTime,
            'dbTime': "%.2f" % dbTime,
            'queries': "%d" % queries,
        }
        if response and response.content:
            content = response.content.rstrip()
            if content.endswith(b"<!--STATS-->"):
                content = content.decode(response._charset)
                stat_fmt = "<!-- Total: {totTime}"
                if settings.DEBUG:
                    stat_fmt += (" Python: {pyTime} DB: {dbTime} Queries: "
                        "{queries}")
                stat_fmt += " -->"
                content = content[:-12] + stat_fmt.format(**stats)
                response.content = content.encode(response._charset)
        return response


class AdminForceLanguageCodeMiddleware(object):
    """Add this middleware to force the admin to always use the language
    specified in ``settings.LANGUAGE_CODE`` instead of sniffing it from
    the user agent."""

    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANG = settings.LANGUAGE_CODE
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG

class ActivityMiddleware(object):
    """Updates the `last_active` profile field for every logged in user with
    the current timestamp. It pragmatically stores a new value every 40 seconds
    (one third of the seconds specified ``CURRENTLY_ONLINE_INTERVAL`` setting).
    """

    def process_request(self, request):
        now = datetime.now()
        seconds = getattr(settings, 'CURRENTLY_ONLINE_INTERVAL', 120)
        delta = now - timedelta(seconds=seconds)
        users_online = cache.get('users_online', {})
        guests_online = cache.get('guests_online', {})
        if request.user.is_authenticated():
            users_online[request.user.id] = now
            profile = request.user.get_profile()
            last_active = profile.last_active
            if not last_active or 3 * (now - last_active).seconds > seconds:
                profile.last_active = now
                profile.save()
        else:
            guest_sid = request.COOKIES.get(settings.SESSION_COOKIE_NAME, '')
            guests_online[guest_sid] = now

        for user_id in users_online.keys():
            if users_online[user_id] < delta:
                del users_online[user_id]

        for guest_id in guests_online.keys():
            if guests_online[guest_id] < delta:
                del guests_online[guest_id]

        cache.set('users_online', users_online, 60*60*24)
        cache.set('guests_online', guests_online, 60*60*24)
