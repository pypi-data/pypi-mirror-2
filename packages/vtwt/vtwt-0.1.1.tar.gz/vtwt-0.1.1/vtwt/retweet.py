import sys

from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class RetweetOptions(cli.Options):

    optFlags = [
            ["long", "l", "Display messages in long format."],
        ]

    def parseArgs(self, msgId):
        self["id"] = msgId


class Retweeter(cli.Command):

    @inlineCallbacks
    def execute(self):
        try:
            msg = yield self.vtwt.retweet(self.config["id"])
            self.printMessage(msg)

        except Exception, e:
            print >>sys.stderr, self.failWhale(e)
            self.exitValue = os.EX_SOFTWARE

    def printMessage(self, msg, screenNameWidth=None):
        if self.config["long"]:
            text = self.formatMsgLong(msg, screenNameWidth)
        else:
            text = self.formatMsgSimple(msg, screenNameWidth)
        self._print(text)
        return msg



class RetweetLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Retweet a message"
    name = "retweet"
    shortcut = "r"
    options = RetweetOptions
    command = Retweeter


loader = RetweetLoader()

