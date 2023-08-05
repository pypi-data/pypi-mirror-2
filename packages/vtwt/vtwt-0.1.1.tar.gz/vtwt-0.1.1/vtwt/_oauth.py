import os, sys

from oauth import oauth

from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from twisted.python.util import untilConcludes
from twisted.web.error import Error as WebError
from zope.interface import implements

from pendrell.agent import Agent
from jersey import log
from vtwt import cli


class OAuthOptions(cli.Options):
    optParameters = [
        ["consumer-key", "c", "xkCemphqejlUZ9W11MUMsA", "OAuth Consumer Key"],
        ["consumer-secret", "C", "QsnJx6SDhH6SjWNG95jcUR3FnKyFWFoOvDcf90E",
            "OAuth Consumer Secret"],
        ]


class OAuther(cli.CommandBase):

    BASE_URL = "https://api.twitter.com"
    TOKEN_REQUEST_URL = BASE_URL + "/oauth/request_token"
    AUTHORIZATION_URL = BASE_URL + "/oauth/authorize"
    ACCESS_TOKEN_URL = BASE_URL + "/oauth/access_token"

    @inlineCallbacks
    def execute(self):
        log.debug("Doing the OAuth")
        try:
            self.agent = Agent()
            self.consumer = self.buildConsumer()
            self.sig = oauth.OAuthSignatureMethod_HMAC_SHA1()

            self.requestToken = rt = yield self.getRequestToken()
            authUrl = self.getAuthorizationURL()
            print "Get authorization PIN from {0}".format(authUrl)
            pin = self._getPin()
            self.accessToken = at = yield self.getAccessToken(pin)
            print ("oauth_token = {0.key!r}\n"
                   "oauth_token_secret = {0.secret!r}").format(at)

        except Exception, e:
            print >>sys.stderr, self.failWhale(e)
            self.exitValue = os.EX_SOFTWARE


    def buildConsumer(self):
        return oauth.OAuthConsumer(
                self.config["consumer-key"],
                self.config["consumer-secret"])


    @inlineCallbacks
    def getRequestToken(self):
        tokenReq = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                http_url=self.TOKEN_REQUEST_URL)
        tokenReq.sign_request(self.sig, self.consumer, None)
        tokenRsp = yield self._openOAuth(tokenReq)
        token = oauth.OAuthToken.from_string(tokenRsp.content)
        returnValue(token)


    def getAuthorizationURL(self):
        authReq = oauth.OAuthRequest.from_token_and_callback(
                token=self.requestToken, http_url=self.AUTHORIZATION_URL)
        authReq.sign_request(self.sig, self.consumer, self.requestToken)
        return authReq.to_url()


    @inlineCallbacks
    def getAccessToken(self, pin):
        accessReq = oauth.OAuthRequest.from_consumer_and_token(self.consumer,
                token=self.requestToken, verifier=pin,
                http_url=self.ACCESS_TOKEN_URL)
        accessReq.sign_request(self.sig, self.consumer, self.requestToken)
        accessRsp = yield self._openOAuth(accessReq)
        token = oauth.OAuthToken.from_string(accessRsp.content)
        returnValue(token)


    def _openOAuth(self, req, **kw):
        kw.setdefault("method", req.http_method)
        kw.setdefault("headers", req.to_header())
        return self.agent.open(req.http_url, **kw)


    _pinPrompt = "PIN: "

    def _getPin(self):
        try:
            untilConcludes(sys.stdout.write, self._pinPrompt)
            untilConcludes(sys.stdout.flush)
            pin = raw_input()
        except (KeyboardInterrupt, OSError):
            log.err()
            raise NoOAuthPin()
        else:
            if pin:
                pin = pin.strip()
            if not pin:
                raise NoOAuthPin()
        return pin



class NoOAuthPin(Exception):
    def __init__(self):
        Exception.__init__(self, "No OAuth PIN")


class OAuthLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Get an OAuth Access Token"
    name = "oauth"
    shortcut = "o"
    options = OAuthOptions
    command = OAuther


loader = OAuthLoader()

