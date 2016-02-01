"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
from time import time, strftime, gmtime
from mbed_host_tests import BaseHostTest

class RTCTest(BaseHostTest):
    PATTERN_RTC_VALUE = "\[(\d+)\] \[(\d+-\d+-\d+ \d+:\d+:\d+ [AaPpMm]{2})\]"
    re_detect_rtc_value = re.compile(PATTERN_RTC_VALUE)

    timestamp = None
    result = None
    rtc_reads = []

    def _callback_timestamp(self, key, value, timestamp):
        self.timestamp = int(value)

    def _callback_rtc(self, key, value, timestamp):
        self.rtc_reads.append((key, value, timestamp))

    def _callback_exit(self, key, value, timestamp):
        self.notify_complete()

    def setup(self):
        self.register_callback('timestamp', self._callback_timestamp)
        self.register_callback('rtc', self._callback_rtc)
        self.register_callback('exit', self._callback_exit)

    def test(self):
        def check_strftimes_format(t):
            m = self.re_detect_rtc_value.search(t)
            if m and len(m.groups()):
                sec, time_str = int(m.groups()[0]), m.groups()[1]
                correct_time_str = strftime("%Y-%m-%d %H:%M:%S %p", gmtime(float(sec)))
                return time_str == correct_time_str
            return False

        ts = [t for _, t, _ in self.rtc_reads]
        self.result = all(filter(check_strftimes_format, ts))
        return self.result
