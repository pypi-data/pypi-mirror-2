import os, sys, time

from twisted.application.internet import TimerService
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class WatchOptions(cli.Options):

    optParameters = [
            ["limit", "L", None,
                "The maximum number of messages to be displayed at once.", int],
            ["interval", "i", None, "Time between requests", int],
        ]

    optFlags = [
            ["long", "l", "Display in messages long format."],
        ]


    def parseArgs(self, watchee="home"):
        self["watchee"] = watchee

    def postOptions(self):
        log.debug("Going to watch {0[watchee]} ")


class Watcher(cli.Command):

    def execute(self):
        log.trace("Executing watcher.")

        self._lastPrintedId = None
        self._lastError = None
        if self.config["interval"]:
            svc = TimerService(self.config["interval"], self.showTimeline)
            svc.setServiceParent(self)

            # Since this runs ~forever, just return a Deferred that doesn't call
            # back.  A swift SIGINT will kill it.
            d = Deferred()

        else:
            # Print it once and exit
            d = self.showTimeline()

        return d


    @inlineCallbacks
    def showTimeline(self):
        try:
            log.debug(("Requesting {0.config[watchee]} timeline since "
                       "{0._lastPrintedId}").format(self))
            watchee = self.config["watchee"]
            params = dict()

            if self._lastPrintedId:
                params["since_id"] = self._lastPrintedId

            messages = yield self.vtwt.getTimeline(watchee, params)

            messages = self._limitMessages(messages, self.config["limit"])
            if messages:
                self.printMessages(messages)
                self._lastPrintedId = messages[-1].id

        except Exception, e:
            if repr(self._lastError) != repr(e):
                print >>sys.stderr, self.failWhale(e)
                self._lastError = e
        else:
            self._lastError = None


    @staticmethod
    def _limitMessages(messages, limit=None):
        if limit and limit < len(messages):
            log.trace("Limiting messages: {0}".format(", ".join(
                    m.id for m in messages[:-limit])))
            del messages[:-limit]
        return messages


    def printMessages(self, messages):
        screenNameWidth = max(len(msg.user.screen_name) for msg in messages)
        for msg in messages:
            self.printMessage(msg, screenNameWidth)

        if messages and self.config["interval"] and not self.config["long"]:
            self.printTimestamp()

    def printTimestamp(self):
        self._print("# {0}".format(time.ctime()))


    def printMessage(self, msg, screenNameWidth=None):
        if self.config["long"]:
            text = self.formatMsgLong(msg, screenNameWidth)
        else:
            text = self.formatMsgSimple(msg, screenNameWidth)
        self._print(text)
        return msg


class WatchLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Watch the twitter"
    name = "watch"
    shortcut = "w"
    options = WatchOptions
    command = Watcher


loader = WatchLoader()

