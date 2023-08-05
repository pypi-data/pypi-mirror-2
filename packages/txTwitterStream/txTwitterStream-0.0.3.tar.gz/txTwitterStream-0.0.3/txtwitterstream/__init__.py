"""Twisted client library for the Twitter Streaming API:
http://apiwiki.twitter.com/Streaming-API-Documentation"""

__author__ = "Wade Simmons"
__version__ = "0.0.3"

from txtwitterstream.client import Client, TweetReceiver

__all__ = ["Client", "TweetReceiver"]