import os, sys, traceback

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python.filepath import FilePath
from twisted.python.text import greedyWrap

from jersey import cli, log

from vtwt import util
from vtwt.svc import VtwtService

from oauth import oauth


# XXX HACK
from twisted.python import reflect
def safe_unicode(obj):
    return reflect._safeFormat(unicode, obj)
reflect.safe_str = safe_unicode


class Options(cli.Options):
    pass


class CommandBase(cli.Command):

    def __init__(self, config):
        cli.Command.__init__(self, config)


    def failWhale(self, error):
        config = self.config
        while config.parent and "COLUMNS" not in config:
            config = config.parent
        columns = config.get("COLUMNS", 80)
        return util.failWhale(error, columns)


    def formatMsgSimple(self, msg, screenNameWidth=None):
        fmt = "{msg.user.screen_name:{w}}  {text}"
        w = screenNameWidth if screenNameWidth else len(msg.user.screen_name)
        padding = " " * (w + 2)
        return self._formatMsg(msg, fmt, padding, w)


    def formatMsgLong(self, msg, screenNameWidth=None):
        fmt = "--- {msg.user.screen_name:{w}} {msg.created_at} [{msg.id}]\n" \
              "    {text}"
        w = screenNameWidth if screenNameWidth else len(msg.user.screen_name)
        padding = " " * 4
        return self._formatMsg(msg, fmt, padding, w)


    def _formatMsg(self, msg, fmt, padding, w):
        fmt = unicode(fmt)
        out = None
        while out is None:
            fmt = unicode(fmt)
            text = unicode(self._wrapText(msg, fmt, padding))
            out = fmt.format(msg=msg, text=text, w=w)
        return out


    def _wrapText(self, msg, fmt, padding):
        width = self.config.parent["COLUMNS"] - len(padding)
        lines = greedyWrap(msg.text, width)
        return ("\n"+padding).join(lines)


    def _print(self, text, stream=None):
        if stream is None:
            stream = sys.stdout
        enc = getattr(stream, "encoding", None)
        if enc:
            text.encode(enc)
        print >>stream, text



class Command(CommandBase):

    def __init__(self, config):
        CommandBase.__init__(self, config)
        self.vtwt = self._buildVtwt()

    def _buildVtwt(self):
        if "oauth-token" not in self.config.parent \
                or "oauth-token-secret" not in self.config.parent:
            raise cli.UsageError("No authentication token specified")
        oauthToken = oauth.OAuthToken(
                self.config.parent["oauth-token"],
                self.config.parent["oauth-token-secret"])
        svc = VtwtService(oauthToken)
        svc.setServiceParent(self)
        return svc



class CommandFactory(cli.CommandFactory):
    pass



class VtwtOptions(cli.PluggableOptions):

    defaultSubCommand = "watch"

    optFlags = [
            ["debug", "D", "Turn debugging messages on",]
        ]

    optParameters = [
            ["config-file", "c",
                os.path.expanduser("~/.vtwtrc"), "Vtwt config file",],
            ["oauth-token", "o", None, "OAuth access token."],
            ["oauth-token-secret", "O", None, "OAuth access token secret."],
        ]


    @property
    def commandPackage(self):
        import vtwt
        return vtwt


    def postOptions(self):
        if self["debug"]:
            self.logLevel = log.TRACE  # Allow all log messages.
        else:
            self.logLevel = log.ERROR+1  # Ignore ~all log messages.

        cf = FilePath(self["config-file"])
        if cf.exists():
            self.readConfigFile(cf)

        if self.subCommand != "oauth" and \
                not (self["oauth-token"] and self["oauth-token-secret"]):
            raise cli.UsageError(
                    "No OAuth token specified.  Run the 'oauth' subcommand.")

        self["COLUMNS"] = int(os.getenv("COLUMNS", 80))


    def readConfigFile(self, configFile):
        fileNS = dict()
        execfile(configFile.path, fileNS)
        for configKey in fileNS.iterkeys():
            k = configKey.replace("_", "-")
            if k in self and self[k] is None:
                self[k] = fileNS[configKey]



class VtwtCommander(cli.PluggableCommandRunner):

    def preApplication(self):
        # twittytwister.txml raises a weird Exception.  Suppress it.
        import logging
        logging.raiseExceptions = False



def run(args=sys.argv[:]):
    program = os.path.basename(args[0])
    args = args[1:]

    opts = VtwtOptions(program)
    try:
        opts.parseOptions()

        vtwt = VtwtCommander(program, opts)
        vtwt.run()

    except cli.UsageError, ue:
        print >>sys.stderr, str(opts)
        print >>sys.stderr, str(ue)
        raise SystemExit(os.EX_USAGE)

    else:
        raise SystemExit(vtwt.exitValue)


