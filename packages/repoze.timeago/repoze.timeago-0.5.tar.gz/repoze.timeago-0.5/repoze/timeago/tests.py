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
import unittest

class Test_get_elapsed(unittest.TestCase):

    _old_now = None

    def tearDown(self):
        if self._old_now is not None:
            self._setNow(self._old_now)

    def _callFUT(self, timestamp):
        from repoze.timeago import get_elapsed
        return get_elapsed(timestamp)

    def _setNow(self, callable):
        import repoze.timeago
        repoze.timeago._NOW, self._old_now = callable, repoze.timeago._NOW

    def _verify(self, THEN, NOW, expected):
        self._setNow(lambda: NOW)
        result = self._callFUT(THEN)
        self.assertEqual(result, expected)

    def test_none(self):
        self.assertEqual(self._callFUT(None), 'an unknown time ago')

    def test_one_second(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 57, 33)
        NOW = datetime(2010, 7, 13, 12, 57, 34)
        self._verify(THEN, NOW, 'seconds ago')

    def test_multiple_seconds(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 57, 30)
        NOW = datetime(2010, 7, 13, 12, 57, 34)
        self._verify(THEN, NOW, 'seconds ago')

    def test_multiple_seconds_not_quite_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 57, 0)
        NOW = datetime(2010, 7, 13, 12, 57, 29)
        self._verify(THEN, NOW, 'seconds ago')

    def test_one_minute_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 57, 0)
        NOW = datetime(2010, 7, 13, 12, 57, 30)
        self._verify(THEN, NOW, '1 minute ago')

    def test_one_minute_exact(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 56, 34)
        NOW = datetime(2010, 7, 13, 12, 57, 34)
        self._verify(THEN, NOW, '1 minute ago')

    def test_one_minute_not_quite_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 56, 0)
        NOW = datetime(2010, 7, 13, 12, 57, 29)
        self._verify(THEN, NOW, '1 minute ago')

    def test_two_minutes_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 56, 0)
        NOW = datetime(2010, 7, 13, 12, 57, 30)
        self._verify(THEN, NOW, '2 minutes ago')

    def test_fifty_nine_minutes_not_quite_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 0, 0)
        NOW = datetime(2010, 7, 13, 12, 59, 29)
        self._verify(THEN, NOW, '59 minutes ago')

    def test_one_hour_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 0, 0)
        NOW = datetime(2010, 7, 13, 12, 59, 30)
        self._verify(THEN, NOW, '1 hour ago')

    def test_one_hour_exact(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 59, 33)
        NOW = datetime(2010, 7, 13, 13, 59, 33)
        self._verify(THEN, NOW, '1 hour ago')

    def test_one_hour_not_quite_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 13, 0, 0)
        NOW = datetime(2010, 7, 13, 14, 29, 29)
        self._verify(THEN, NOW, '1 hour ago')

    def test_two_hours_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 59, 33)
        NOW = datetime(2010, 7, 13, 14, 29, 33)
        self._verify(THEN, NOW, '2 hours ago')

    def test_twenty_three_hours_not_quite_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 59, 33)
        NOW = datetime(2010, 7, 14, 11, 29, 32)
        self._verify(THEN, NOW, '23 hours ago')

    def test_one_day_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 12, 0, 0)
        NOW = datetime(2010, 7, 14, 11, 30, 0)
        self._verify(THEN, NOW, '1 day ago')

    def test_one_day_exact(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 13, 59, 33)
        NOW = datetime(2010, 7, 14, 13, 59, 33)
        self._verify(THEN, NOW, '1 day ago')

    def test_one_day_not_quite_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 0, 0, 0)
        NOW = datetime(2010, 7, 14, 11, 29, 29)
        self._verify(THEN, NOW, '1 day ago')

    def test_two_days_rounded_up(self):
        from datetime import datetime
        THEN = datetime(2010, 7, 13, 10, 0, 0)
        NOW = datetime(2010, 7, 14, 22, 0, 0)
        self._verify(THEN, NOW, '2 days ago')
