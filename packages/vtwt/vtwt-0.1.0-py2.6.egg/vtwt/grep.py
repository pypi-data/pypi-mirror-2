import os, re, sys, time

from twisted.application.internet import TimerService
from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from twisted.web import error as weberr, http
from zope.interface import implements

from jersey import log
from vtwt import cli


class GrepOptions(cli.Options):

    optFlags = [
            ["ignore-case", "i", "Ignore case"],
            ["count", "c", "Count the number of matches.  Implies 'quiet'."],
            #["exclude-retweets", "p", "Print the.  Implies 'quiet'."],
            ["long", "l", "Print messages in long format"],
            ["percentage", "p", "Print the.  Implies 'quiet'."],
            ["quiet", "q", "Be quiet.  Don't print results."],
        ]

    synopsis = "[options] regex [user]"

    def parseArgs(self, regex, grepee=None):
        try:
            self["regex"] = re.compile(regex)
        except re.error, e:
            raise cli.UsageError(str(e))
        self["grepee"] = grepee


    @property
    def grepee(self):
        return self["grepee"] or self.parent["user"]


    @property
    def summaryFormat(self):
        fmt = ""
        if self["count"]:
            fmt += "{count}"
            if self["percentage"]:
                fmt += "\t{total}"
        if self["percentage"]:
            if fmt:
                fmt += "\t"
            fmt += "{percentage:.2%}"
        return fmt



class Grepper(cli.Command):

    _count = str(200)
    sleepTime = 2

    @inlineCallbacks
    def execute(self):
        try:
            log.trace("Executing Grepper on {0.config.grepee}.".format(self))
            printMatches = not (self.config["count"] or
                    self.config["percentage"] or
                    self.config["quiet"])

            page = 1
            maxId = None
            messages = None
            messageCount = matchCount = 0
            while page == 1 or messages:
                try:
                    messages = yield self._getMessages(page, maxId)

                except weberr.Error, we:
                    if int(we.status) == http.BAD_GATEWAY:
                        print >>sys.stderr, self.failWhale(we)
                        d = Deferred()
                        reactor.callLater(self.sleepTime, d.callback, True)
                        yield d
                    else:
                        raise

                else:
                    for msg in messages:
                        messageCount += 1
                        log.trace("Message {0}".format(messageCount))
                        maxId = long(msg.id) - 1 
                        if self._grepMessage(msg):
                            matchCount += 1
                            log.trace("Match {0}".format(matchCount))
                            if printMatches:
                                self.printMessage(msg)
                    page += 1

            if self.config["percentage"] or self.config["count"]:
                self._printSummary(matchCount, messageCount)

            self.exitValue = 0 if matchCount > 0 else 1
        
        except Exception, e:
            print >>sys.stderr, self.failWhale(e)
            self.exitValue = os.EX_SOFTWARE

        returnValue(self.exitValue)


    @inlineCallbacks
    def _getMessages(self, page=1, maxId=None):
        params = dict(count=self._count)  #, page=str(page))
        log.debug("Page: {0}".format(page))

        if maxId:
            params["max_id"] = str(maxId)
            log.debug("Max ID: " + params["max_id"])

        msgs = yield self.vtwt.getTimeline(self.config.grepee, params)
        log.debug("Returned: " + str(len(msgs)))

        msgs.reverse()
        returnValue(msgs)


    def _grepMessage(self, msg):
        log.trace(self.formatMsgSimple(msg))
        return self.config["regex"].search(msg.text, self._grepFlags)

    @property
    def _grepFlags(self):
        flags = 0
        if self.config["ignore-case"]:
            flags |= re.IGNORECASE
        return flags


    def printMessage(self, msg, screenNameWidth=None):
        if self.config["long"]:
            text = self.formatMsgLong(msg, screenNameWidth)
        else:
            text = self.formatMsgSimple(msg, screenNameWidth)
        self._print(text)
        return msg


    def _printSummary(self, matchCount, totalCount):
        self._print(self.config.summaryFormat.format(
            count=matchCount, total=totalCount,
            percentage=float(matchCount) / totalCount))



class GrepLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Grep tweets"
    name = "grep"
    shortcut = "g"
    options = GrepOptions
    command = Grepper


loader = GrepLoader()

