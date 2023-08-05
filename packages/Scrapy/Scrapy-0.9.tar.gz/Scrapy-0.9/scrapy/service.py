import sys, os

from twisted.python import log
from twisted.internet import reactor, defer, protocol, error
from twisted.application.service import Service

from scrapy.utils.py26 import cpu_count
from scrapy.conf import settings


class ScrapyService(Service):

    def startService(self):
        reactor.callWhenRunning(self.spawn_processes)

    def spawn_processes(self):
        for settings_module, count in settings['PROJECTS'].items():
            for i in range(count or cpu_count()):
                self.spawn_process(settings_module, i)

    def spawn_process(self, settings_module, position):
        args = [sys.executable, '-m', 'scrapy.cmdline', 'start']
        env = os.environ.copy()
        botname = self.get_bot_name(settings_module)
        logfile = self.get_log_file(settings_module, position)
        env['SCRAPY_SETTINGS_MODULE'] = settings_module
        env['SCRAPY_LOG_FILE'] = logfile
        pp = ScrapyProcessProtocol(botname, settings_module, logfile)
        pp.deferred.addCallback(lambda _: reactor.callLater(5, \
            self.spawn_process, settings_module, position))
        reactor.spawnProcess(pp, sys.executable, args=args, env=env)

    def get_log_file(self, settings_module, position):
        botname = self.get_bot_name(settings_module)
        basename = "%s-%s" % (botname, position) if position else botname
        return os.path.join(settings['LOG_DIR'], "%s.log" % basename)

    def get_bot_name(self, settings_module):
        mod = __import__(settings_module, {}, {}, [''], -1)
        return mod.BOT_NAME

class ScrapyProcessProtocol(protocol.ProcessProtocol):

    TAIL_LINES = 100

    def __init__(self, botname, settings_module, logfile):
        self.botname = botname
        self.settings_module = settings_module
        self.logfile = logfile
        self.pid = None
        self.deferred = defer.Deferred()
        self.outdata = ''
        self.errdata = ''

    def outReceived(self, data):
        self.outdata = self._tail(self.outdata + data)

    def errReceived(self, data):
        self.errdata = self._tail(self.errdata + data)

    def connectionMade(self):
        self.pid = self.transport.pid
        log.msg("Crawler %r started: pid=%r settings=%r log=%r" % \
            (self.botname, self.pid, self.settings_module, self.logfile))

    def processEnded(self, status):
        if isinstance(status.value, error.ProcessDone):
            msg = "Crawler %r finished: pid=%r settings=%r log=%r" % \
                (self.botname, self.pid, self.settings_module, self.logfile)
        else:
            msg = "Crawler %r died: exitstatus=%r pid=%r settings=%r log=%r" % \
                (self.botname, status.value.exitCode, self.pid, self.settings_module, \
                self.logfile)
        self._log_ended(msg)
        self.deferred.callback(self)

    def _log_ended(self, msg):
        tolog = [msg]
        if self.outdata:
            tolog += [">>> stdout (last %d lines) <<<" % self.TAIL_LINES]
            tolog += [self.outdata]
        if self.errdata:
            tolog += [">>> stderr (last %d lines) <<<" % self.TAIL_LINES]
            tolog += [self.errdata]
        log.msg(os.linesep.join(tolog))

    def _tail(self, data, lines=TAIL_LINES):
        return os.linesep.join(data.split(os.linesep)[-lines:])
