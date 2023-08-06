##############################################################################
#
# Copyright (c) 2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Leonardo Rochael Almeida <leonardo@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly advised to contract a Free Software
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

import os
import os.path
import traceback
import logging
from cStringIO import StringIO
from thread import get_ident
import time
from pprint import pformat

try:
    from sys import _current_frames
except ImportError:
    # Python 2.4 and older
    from threadframe import dict as _current_frames

class NullHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        # for comparison purposes below
        self.baseFilename = 'null'

    def emit(self, *args, **kw):
        pass

# we might want to change this name later to something more specific
logger_name = __name__  
log = logging.getLogger(logger_name)
log.propagate = False
handler = NullHandler()
log.addHandler(handler)

formatter = logging.Formatter("%(asctime)s - %(message)s")

DEFAULT_TIMEOUT = 2
DEFAULT_INTERVAL = 1

def do_enable():
    global handler
    # this function is not exactly thread-safe, but it shouldn't matter.
    # The worse that can happen is that a change in longrequestlogger_file
    # will stop or change the logging destination of an already running request
    logfile = os.environ.get('longrequestlogger_file')
    if logfile:
        if logfile != 'null':
            # to imitate FileHandler
            logfile = os.path.abspath(logfile)
        if handler.baseFilename != logfile:
            log.removeHandler(handler)
            handler.close()
            if logfile == 'null':
                handler = NullHandler()
            else:
                handler = logging.FileHandler(logfile)
                handler.formatter = formatter
            log.addHandler(handler)
        return log # which is also True as boolean
    return None # so that Dumpers know they are disabled

def get_configuration():
    return dict(
        timeout=float(os.environ.get('longrequestlogger_timeout', 
                                       DEFAULT_TIMEOUT)),
        interval=float(os.environ.get('longrequestlogger_interval', 
                                       DEFAULT_INTERVAL)),
    )

THREAD_FORMAT = "Thread %s: Started on %.1f; Running for %.1f secs; %s"
REQUEST_FORMAT = """
request: %(method)s %(url)s
retry count: %(retries)s
form: %(form)s
other: %(other)s
""".strip()

class Dumper(object):

    def __init__(self, thread_id=None):
        if thread_id is None:
            # assume we're being called by the thread that wants to be
            # monitored
            thread_id = get_ident()
        self.thread_id = thread_id
        self.start = time.time()
        # capture it here in case it gets disabled in the future
        self.log = do_enable()
        conf = get_configuration()
        self.timeout = conf['timeout']
        self.interval = conf['interval']

    def is_enabled(self):
        return bool(self.log)

    def format_request(self, request):
        if request is None:
            return "[No request]"
        url = request.getURL()
        if request.get('QUERY_STRING'):
            url += '?' + request['QUERY_STRING']
        retries = request.retry_count
        method = request['REQUEST_METHOD']
        form = pformat(request.form)
        other = pformat(request.other)
        return REQUEST_FORMAT % locals()

    def extract_request(self, frame):
        # We try to fetch the request from the 'call_object' function because
        # it's the one that gets called with retried requests.
        # And we import it locally to get even monkey-patched versions of the
        # function.
        from ZPublisher.Publish import call_object
        func_code = call_object.func_code #@UndefinedVariable
        while frame is not None:
            code = frame.f_code
            if (code is func_code):
                request = frame.f_locals.get('request')
                return request
            frame = frame.f_back

    def extract_request_info(self, frame):
        request = self.extract_request(frame)
        return self.format_request(request)

    def get_top_thread_frame(self):
        return _current_frames()[self.thread_id]

    def get_thread_info(self, frame):
        request_info = self.extract_request_info(frame)
        now = time.time()
        runtime = now - self.start
        info = THREAD_FORMAT % (self.thread_id,
                                self.start,
                                runtime,
                                request_info)
        return info

    def format_thread(self):
        frame = self.get_top_thread_frame()
        output = StringIO()
        thread_info = self.get_thread_info(frame)
        print >> output, thread_info
        print >> output, "Traceback:"
        traceback.print_stack(frame, file=output)
        del frame
        return output.getvalue()

    def __call__(self):
        self.log.warning(self.format_thread())
