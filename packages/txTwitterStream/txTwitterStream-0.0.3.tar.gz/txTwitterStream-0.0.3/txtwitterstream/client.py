# coding: utf-8
#
# Copyright 2009 Alexandre Fiori
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import urllib

from twisted.protocols import basic
from twisted.internet import defer, reactor, protocol
from twisted.web import client
from twisted.web.http_headers import Headers

from twisted.web.client import ResponseDone
from twisted.web.http import PotentialDataLoss

import txtwitterstream
from txtwitterstream.util import StringProducer, auth_header

try:
    import simplejson as _json
except ImportError:
    try:
        import json as _json
    except ImportError:
        raise RuntimeError("A JSON parser is required, e.g., simplejson at "
                           "http://pypi.python.org/pypi/simplejson/")

class TweetReceiver(object):
    def connectionMade(self):
        pass

    def connectionFailed(self, why):
        pass

    def tweetReceived(self, tweet):
        raise NotImplementedError

    def _registerProtocol(self, protocol):
        self._streamProtocol = protocol

    def disconnect(self):
        if hasattr(self, "_streamProtocol"):
            self._streamProtocol.factory.continueTrying = 0
            self._streamProtocol.transport.loseConnection()
        else:
            raise RuntimeError("not connected")
    
    def reconnect(self):
        if hasattr(self, "_streamProtocol"):
            self._streamProtocol.transport.loseConnection()
        else:
            raise RuntimeError("not connected")

class TwitterStreamProtocol(basic.LineReceiver):
    def __init__(self, consumer):
        self.consumer = consumer

    def lineReceived(self, line):
        line = line.strip()
        if line:
            tweet = _json.loads(line)
            self.consumer.tweetReceived(tweet)
            
    def connectionLost(self, reason):
        if reason.check(ResponseDone) or reason.check(PotentialDataLoss):
            pass
        else:
            print "connection lost: %s" % reason

class HTTPReconnectingClientFactory(protocol.ReconnectingClientFactory):
    maxDelay = 120
    protocol = client.HTTP11ClientProtocol

    def __init__(self, method, path, headers, consumer, body=None):
        self.method = method
        self.path = path
        self.headers = headers
        self.consumer = consumer
        self.proto = None
        self.body = body

    def buildProtocol(self, addr):
        self.resetDelay()
        proto = self.protocol()
        proto.factory = self
        reactor.callLater(0, self.connected, proto)
        self.proto = proto
        return proto

    def force_reconnect(self):
        self.proto.transport.loseConnection()

    def connected(self, proto):
        d = proto.request(client.Request(self.method, self.path, self.headers, (self.body and StringProducer(self.body))))
        d.addCallback(self._got_headers, self.consumer)
        d.addErrback(defer.logError)
        return d

    def _got_headers(self, response, consumer):
        if response.code == 200:
            response.deliverBody(TwitterStreamProtocol(self.consumer))
            consumer.connectionMade()
        else:
            consumer.connectionFailed(Exception("Server returned: %s %s" % (response.code, response.phrase)))
            self.continueTrying = 0
            if self.proto.transport:
                self.proto.transport.loseConnection()
    
class Client(object):
    def __init__(self, username, password, host="stream.twitter.com", port=80, user_agent=("txtwitterstream/%s" % txtwitterstream.__version__)):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def stream(self, consumer, endpoint, post_body=None):
        headers = Headers()
        headers.addRawHeader("Authorization", auth_header(self.username, self.password))
        headers.addRawHeader("Host", "%s:%s" % (self.host, self.port))
        
        f = None
        if post_body:
            headers.addRawHeader("Content-Type", "application/x-www-form-urlencoded")
            f = HTTPReconnectingClientFactory("POST", endpoint, headers, consumer, post_body)
        else:
            f = HTTPReconnectingClientFactory("GET", endpoint, headers, consumer)
        reactor.connectTCP(self.host, self.port, f)

    def firehose(self, consumer):
        self.stream(consumer, "/1/statuses/firehose.json")

    def retweet(self, consumer):
        self.stream(consumer, "/1/statuses/retweet.json")

    def sample(self, consumer):
        self.stream(consumer, "/1/statuses/sample.json")

    def filter(self, consumer, count=0, delimited=0, track=[], follow=[], locations=None):
        qs = []
        if count:
            qs.append("count=%s" % urllib.quote(count))
        if delimited:
            qs.append("delimited=%d" % delimited)
        if follow:
            qs.append("follow=%s" % ",".join(follow))
        if track:
            qs.append("track=%s" % ",".join([urllib.quote(s) for s in track]))
        if locations:
            qs.append("locations=%s" % urllib.quote(locations))

        if not (track or follow or locations):
            raise RuntimeError("At least one parameter is required: track, follow or locations")
    
        self.stream(consumer, "/1/statuses/filter.json", "&".join(qs))