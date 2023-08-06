##############################################################################
#
# Copyright (c) 2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Leonardo Rochael Almeida <leonardo@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly advised to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import unittest
from cStringIO import StringIO
from doctest import OutputChecker
from doctest import REPORT_UDIFF, NORMALIZE_WHITESPACE, ELLIPSIS

from Products.LongRequestLogger.tests.common import Sleeper
import os

class SimpleOutputChecker(OutputChecker):
    # for certain inputs the doctest output checker is much more convenient
    # than manually munging assertions, but we don't want to go through all
    # the trouble of actually writing doctests.

    optionflags = REPORT_UDIFF | NORMALIZE_WHITESPACE | ELLIPSIS

    def __init__(self, want, optionflags=None):
        self.want = want
        if optionflags is not None:
            self.optionflags = optionflags

    def __call__(self, got):
        assert self.check_output(self.want, got, self.optionflags), \
          self.output_difference(self, # pretend we're a doctest.Example
                                 got, self.optionflags)

check_dump = SimpleOutputChecker('''
Thread ...: Started on ...; Running for 0.0 secs; [No request]
<BLANKLINE>
Traceback:
...
  File ".../LongRequestLogger/dumper.py", line ..., in format_thread
    traceback.print_stack(frame, file=output)
  File ".../LongRequestLogger/dumper.py", line ..., in get_top_thread_frame
    return _current_frames()[self.thread_id]
''')

check_log = SimpleOutputChecker('''
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 0.0 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/dumper.py", line ..., in __call__
    self.log.warning(self.format_thread())
  File ".../LongRequestLogger/dumper.py", line ..., in format_thread
    traceback.print_stack(frame, file=output)
  File ".../LongRequestLogger/dumper.py", line ..., in get_top_thread_frame
    return _current_frames()[self.thread_id]
''')

check_monitor_log = SimpleOutputChecker('''
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 2.0 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
''')

check_monitor_2_intervals_log = SimpleOutputChecker('''
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 2.0 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 3.0 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 4.0 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
''')

check_publishing_1_interval_log = SimpleOutputChecker('''
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 2.0 secs; request: GET http://localhost
retry count: 0
form: {}
other: {'ACTUAL_URL': 'http://localhost',
 'PARENTS': [],
 'PUBLISHED': <Products.LongRequestLogger.tests.common.App object at 0x...>,
 'RESPONSE': HTTPResponse(''),
 'SERVER_URL': 'http://localhost',
 'TraversalRequestNameStack': [],
 'URL': 'http://localhost',
 'interval': 3.5,
 'method': 'GET'}
Traceback:
...
  File ".../LongRequestLogger/patch.py", line ..., in wrapper
    result = wrapper.original(*args, **kw)
  File ".../ZPublisher/Publish.py", line ..., in publish_module_standard
    response = publish(request, module_name, after_list, debug=debug)
...
  File ".../LongRequestLogger/tests/common.py", line 52, in __call__
    Sleeper(interval).sleep()
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 3.0 secs; request: GET http://localhost
retry count: 0
form: {}
other: {'ACTUAL_URL': 'http://localhost',
 'PARENTS': [],
 'PUBLISHED': <Products.LongRequestLogger.tests.common.App object at 0x...>,
 'RESPONSE': HTTPResponse(''),
 'SERVER_URL': 'http://localhost',
 'TraversalRequestNameStack': [],
 'URL': 'http://localhost',
 'interval': 3.5,
 'method': 'GET'}
Traceback:
...
  File ".../LongRequestLogger/patch.py", line ..., in wrapper
    result = wrapper.original(*args, **kw)
  File ".../ZPublisher/Publish.py", line ..., in publish_module_standard
    response = publish(request, module_name, after_list, debug=debug)
...
  File ".../LongRequestLogger/tests/common.py", line 52, in __call__
    Sleeper(interval).sleep()
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
''')

check_request_formating = SimpleOutputChecker('''
request: GET http://localhost/foo/bar
retry count: 0
form: {}
other: {'RESPONSE': HTTPResponse(''),
 'SERVER_URL': 'http://localhost',
 'URL': 'http://localhost/foo/bar',
 'method': 'GET'}
''')

check_monitor_environment_log = SimpleOutputChecker('''
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 3.5 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
Products.LongRequestLogger.dumper WARNING
  Thread ...: Started on ...; Running for 5.5 secs; [No request]
Traceback:
...
  File ".../LongRequestLogger/tests/common.py", line 41, in sleep
    self._sleep1()
  File ".../LongRequestLogger/tests/common.py", line 44, in _sleep1
    self._sleep2()
  File ".../LongRequestLogger/tests/common.py", line 47, in _sleep2
    time.sleep(self.interval)
''')


config_env_variables = dict(
    longrequestlogger_file='null',
    longrequestlogger_timeout=None,
    longrequestlogger_interval=None,
)

class TestLongRequestLogger(unittest.TestCase):

    def setUp(self):
        from Products.LongRequestLogger.patch import do_patch
        from Products.LongRequestLogger.dumper import logger_name
        from zope.testing.loggingsupport import InstalledHandler
        self.setTestEnvironment()
        do_patch()
        self.loghandler = InstalledHandler(logger_name)
        self.requests = []

    def tearDown(self):
        from Products.LongRequestLogger.patch import do_unpatch
        do_unpatch()
        self.restoreTestEnvironment()
        self.loghandler.uninstall()
        for request in self.requests:
            request.response.stdout.close()
            request.clear()

    def setTestEnvironment(self):
        self.old_env = {}
        for var, value in config_env_variables.items():
            self.old_env[var] = os.environ.pop(var, None)
            if value:
                os.environ[var] = value

    def restoreTestEnvironment(self):
        for var, value in self.old_env.items():
            os.environ.pop(var, None)
            if value is not None:
                os.environ[var] = value

    def makeRequest(self, path='/', **kw):
        # create fake request and response for convenience
        from ZPublisher.HTTPRequest import HTTPRequest
        from ZPublisher.HTTPResponse import HTTPResponse
        stdin = StringIO()
        stdout = StringIO()
        # minimal environment needed
        env = dict(SERVER_NAME='localhost',
                   SERVER_PORT='80',
                   REQUEST_METHOD='GET',
                   SCRIPT_NAME=path)
        response = HTTPResponse(stdout=stdout)
        request = HTTPRequest(stdin, env, response)
        self.requests.append(request)
        return request

    def testDumperFormat(self):
        from Products.LongRequestLogger.dumper import Dumper
        dumper = Dumper()
        check_dump(dumper.format_thread())

    def testDumperRequestExtraction(self):
        # The dumper extract requests by looking for the frame that contains
        # call_object and then looking for the 'request' variable inside it
        from ZPublisher.Publish import call_object
        from Products.LongRequestLogger.dumper import Dumper
        def callable():
            dumper = Dumper()
            return dumper.extract_request(dumper.get_top_thread_frame())

        request = self.makeRequest('/foo')
        retrieved_request = call_object(callable, (), request)
        self.assertTrue(request is retrieved_request)

    def testRequestFormating(self):
        from Products.LongRequestLogger.dumper import Dumper
        dumper = Dumper()
        request = self.makeRequest('/foo/bar')
        check_request_formating(dumper.format_request(request))

    def testDumperLog(self):
        from Products.LongRequestLogger.dumper import Dumper
        dumper = Dumper()
        # check the dumper will log what we expect when called
        dumper()
        check_log(str(self.loghandler))

    def testMonitorStopBeforeTimeout(self):
        from Products.LongRequestLogger.monitor import Monitor
        m = Monitor()
        # sleep just a little to let the other thread start
        s = Sleeper(0.01)
        s.sleep()
        self.assertTrue(m.isAlive())
        self.assertTrue(m.running)
        m.stop()
        self.assertFalse(m.running)
        self.assertFalse(m.isAlive())
        # unless this test is so slow that there were 2 seconds interval
        # between starting the monitor and stopping it, there should be no
        # logged messages
        self.assertFalse(self.loghandler.records)

    def testMonitorStopAfterTimeout(self):
        from Products.LongRequestLogger.monitor import Monitor
        m = Monitor()
        s = Sleeper(m.timeout + 0.5) 
        # sleep a little more than the timeout to be on the safe side
        s.sleep()
        m.stop()
        check_monitor_log(str(self.loghandler))

    def testMonitorStopAfterTimeoutAndTwoIntervals(self):
        from Products.LongRequestLogger.monitor import Monitor
        m = Monitor()
        s = Sleeper(m.timeout + 2 * m.interval + 0.5) 
        # sleep a little more than timeout + intervals to be on the safe
        # side
        s.sleep()
        m.stop()
        check_monitor_2_intervals_log(str(self.loghandler))

    def testMonitorConfigurationDisabled(self):
        from Products.LongRequestLogger.monitor import Monitor
        os.environ['longrequestlogger_file'] = ''
        m = Monitor()
        s = Sleeper(m.timeout + 2 * m.interval + 0.5) 
        # sleep a little more than timeout + intervals
        s.sleep()
        # the thread shouldn't run disabled
        self.assertFalse(m.isAlive())
        self.assertFalse(m.running)
        # stopping shouldn't break nonetheless
        m.stop()
        self.assertFalse(m.running)
        self.assertFalse(m.isAlive())
        # and there should be no records
        self.assertFalse(self.loghandler.records)

    def testMonitorWithEnvorinmentConfiguration(self):
        from Products.LongRequestLogger.monitor import Monitor
        os.environ['longrequestlogger_timeout'] = '3.5'
        os.environ['longrequestlogger_interval'] = '2'
        m = Monitor()
        s = Sleeper(m.timeout + m.interval + 0.5) 
        # sleep a little more than the timeout to be on the safe side
        s.sleep()
        m.stop()
        check_monitor_environment_log(str(self.loghandler))

    def testIsPatched(self):
        import ZPublisher.Publish
        import Products.LongRequestLogger
        self.assertEquals(
            ZPublisher.Publish.publish_module_standard,
            Products.LongRequestLogger.patch.wrapper
        )

    def testPublish(self):
        from ZPublisher.Publish import publish_module_standard
        # Before publishing, there should be no slow query records.
        self.assertFalse(self.loghandler.records)
        # Request taking (timeout + interval + margin) 3.5 seconds...
        request = self.makeRequest('/', interval=3.5)
        request['interval'] = 3.5
        publish_module_standard('Products.LongRequestLogger.tests.common',
                                request=request,
                                response=request.response,
                                debug=True)
        # ...should generate query log records like these
        check_publishing_1_interval_log(str(self.loghandler))

def test_suite():
    return unittest.TestSuite((
         unittest.makeSuite(TestLongRequestLogger),
    ))
