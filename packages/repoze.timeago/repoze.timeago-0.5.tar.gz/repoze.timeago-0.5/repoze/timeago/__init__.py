##############################################################################
#
# Copyright (c) 2010 Agendaless Consulting and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################
from datetime import datetime

_NOW = datetime.utcnow

_SECONDS_PER_MINUTE = 60
_SECONDS_PER_HOUR = 60 * _SECONDS_PER_MINUTE

def _elapsed(delta):
    """ delta -> days, hours, minutes, seconds
    """
    seconds = delta.seconds
    days = delta.days

    hours, seconds = divmod(seconds, _SECONDS_PER_HOUR)
    minutes, seconds = divmod(seconds, _SECONDS_PER_MINUTE)

    if seconds >= 30:
        minutes += 1
        seconds = 0

    if minutes >= 60:
        hours += 1
        minutes = 0

    if minutes >= 30 and hours:
        hours += 1
        minutes = 0

    if hours >= 24:
        days += 1
        hours = 0

    if hours >= 12 and days:
        days += 1
        hours = 0

    if days:
        return days, 0, 0, 0

    if hours:
        return 0, hours, 0, 0

    if minutes:
        return 0, 0, minutes, 0

    return 0, 0, 0, seconds


def get_elapsed(timestamp):
    if timestamp is None:
        return 'an unknown time ago'
    delta = _NOW() - timestamp
    days, hours, minutes, seconds = _elapsed(delta)
    if days > 1:
        return '%d days ago' % days
    elif days:
        return '1 day ago'
    elif hours > 1:
        return '%d hours ago' % hours
    elif hours:
        return '1 hour ago'
    elif minutes > 1:
        return '%d minutes ago' % minutes
    elif minutes:
        return '1 minute ago'
    return 'seconds ago'
