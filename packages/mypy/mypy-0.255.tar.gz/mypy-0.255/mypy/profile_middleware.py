#coding:utf-8

PROFILE_FUNC_LIST = []
from mypy import cookie

import hotshot, hotshot.stats
from os import getpid
from cStringIO import StringIO
import os
import re
import time
from os.path import abspath, dirname, join
from tempfile import gettempdir
tempdir = gettempdir()
PROFILE_LOG_FILENAME_PATTERN = join(tempdir, 'profile-%s.prof')
PROFILE_PICKLE_FILENAME_PATTERN = join(tempdir, 'profile-%s.pickle')
PROFILE_LIMIT = 60

class ProfileInfo:
    """
    Stage 1: profiling
    Stage 2: profile stop, waiting for check result
    """
    def __init__(self, stage, pid, profiler_id=None):
        self.stage = stage
        self.pid = pid
        self.profiler_id = profiler_id and str(profiler_id)

    def get_stats(self):
        stats = load_stats(PROFILE_LOG_FILENAME_PATTERN % self.pid)
        s1 = format_stats(stats, sort='time')
        s2 = format_stats(stats, sort='cumulative')
        return s1 + '\n'*3 + '='*80 + '\n'*3 + s2

def request_start_profile(request, profiler_id, req_count=100):
    request.start_profile = req_count
    pid = getpid()
    info = ProfileInfo(1, pid, profiler_id)
    pickle_fn = PROFILE_PICKLE_FILENAME_PATTERN % pid
    dump(info, open(pickle_fn, 'wb'))

def start_profile(filename=None):
    if filename is None:
        filename = PROFILE_LOG_FILENAME_PATTERN % getpid()
    prof = hotshot.Profile(filename)
    return prof

def on_profile_finished():
    pid = getpid()
    pickle_fn = PROFILE_PICKLE_FILENAME_PATTERN % pid
    try:
        info = load(open(pickle_fn, 'rb'))
        info.stage = 2
    except IOError:
        info = ProfileInfo(2, pid)
    dump(info, open(pickle_fn, 'wb'))

def get_profile_info(pid=None):
    pid = pid or os.getpid()
    pickle_fn = PROFILE_PICKLE_FILENAME_PATTERN % pid
    try:
        profinfo = load(open(pickle_fn, 'rb'))
        return profinfo
    except IOError:
        return None

def delete_profile_info(pid=None):
    pid = pid or os.getpid()
    try:
        os.remove(PROFILE_PICKLE_FILENAME_PATTERN % pid)
    except IOError:
        pass

def load_stats(filename=None):
    if filename is None:
        filename = PROFILE_LOG_FILENAME_PATTERN % getpid()
    stats = hotshot.stats.load(filename)
    try:
        os.remove(filename)
    except IOError:
        pass
    return stats

def format_stats(stats, strip_dirs=None, sort='time'):
    if strip_dirs:
        stats.strip_dirs()
    stats.sort_stats(sort, 'calls')
    so = StringIO()
    stats.stream = so
    stats.print_stats(PROFILE_LIMIT)
    stats.print_callers(PROFILE_LIMIT)
    r = so.getvalue()
    if not strip_dirs:
        rootdir = dirname(
            dirname(dirname(dirname(abspath(__file__))))
        ).lower()+os.sep
        r = r.replace(rootdir, "")
    return r

normalize_re = re.compile(r'\d+')
class CallLogger(object):
    """Log every call"""

    def __init__(self, obj):
        self.obj = obj
        self.log = []

    def __getattr__(self, name):
        attr = getattr(self.obj, name)
        def _(*a, **kw):
            call = format_call(name, *a, **kw)
            ncall = normalize_re.sub('-', call)
            t1 = time.time()
            r = attr(*a, **kw)
            cost = time.time() - t1
            self.log.append((call, ncall, cost))
            return r
        return _

def format_call(funcname, *a, **kw):
    arglist = []
    for v in a:
        v = repr(v)
        if len(v) > 70:
            v = v[:70]+"..."
        arglist.append(v)

    r = []
    for k, v in kw.iteritems():
        if len(v) > 70:
            v = v[:70]+"..."
        r.append((k, v))

    arglist += ["%s=%r" % (k, v) for k, v in r]
    return "%s(%s)" % (funcname, ", ".join(arglist))

def ProfileMiddleware(application):
    def _application(request):
        profile = request.query.profile
        cookie_profile = request.cookie.get("profile")
        if profile or cookie_profile:
            if profile == "0":
                cookie.delete("profile", request=request)
            else:
                if not cookie_profile:
                    cookie.set("profile", "1", request=request)
                #from zku.autumn.model import sqlstore
                prof = start_profile()
                for i in PROFILE_FUNC_LIST:
                    i.start_log()
                #sqlstore.
                #mc.start_log()
                so = []
                result = None
                try:
                    result = prof.runcall(application, request)
                    for i in PROFILE_FUNC_LIST:
                        so.append(i.get_log())
                #    so += sqlstore.get_log()
                #    so += mc.get_log()
                finally:
                    for i in PROFILE_FUNC_LIST:
                        i.stop_log()
                    #    mc.stop_log()
                    #    sqlstore.stop_log()
                    prof.close()

                if result is not None and (result.lstrip().startswith("<") or profile):
                    #disable output for json
                    stats = load_stats()

                    so.append( format_stats(stats, sort='time') )
                    so.append( format_stats(stats, sort='cumulative') )

                    from cgi import escape
                    splitor = """\n<hr style="border:0;border-bottom:1px dashed;margin:20px 0">\n"""
                    so = splitor.join(escape(i.strip()) for i in so)
                    so = """<pre style="clear:both;padding:1em;background:#ffffde;color:#033">\n%s\n</pre>"""%so
                    result = "%s %s"%(result, so)
                return result
        return application(request)
    return _application
