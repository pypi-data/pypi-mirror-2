from twisted.trial import unittest
from txtwitterstream import client

import mock

try:
    import simplejson as json
except ImportError:
    try:
        import json as json
    except ImportError:
        raise RuntimeError("A JSON parser is required, e.g., simplejson at "
                           "http://pypi.python.org/pypi/simplejson/")

class ClientTest(unittest.TestCase):
    TEST_TWEET_JSON = r'{"coordinates":{"coordinates":[106.917746,-6.224203],"type":"Point"},"text":"Ketikannya ga usah lebay gitu dong -,- RT @dyonunyulz: muallleessssssss RT @devcharolline: Liat iklan dong! RT @dyonunyulz: apa sih ?","created_at":"Thu Mar 11 18:05:12 +0000 2010","geo":{"coordinates":[-6.224203,106.917746],"type":"Point"},"truncated":false,"contributors":null,"in_reply_to_screen_name":null,"favorited":false,"source":"<a href=\"http://ubertwitter.com\" rel=\"nofollow\">UberTwitter</a>","place":null,"in_reply_to_status_id":null,"user":{"verified":false,"created_at":"Sun Dec 27 15:44:36 +0000 2009","followers_count":278,"friends_count":503,"lang":"en","profile_background_color":"d281e6","location":"\u00dcT: -6.224203,106.917746","following":null,"notifications":null,"favourites_count":14,"description":"You can call me names devi :)","profile_text_color":"619143","time_zone":"Jakarta","statuses_count":3375,"profile_link_color":"1e5a70","url":"http://www.facebook.com/?sk=messages&ref=mb#!/charoline.sihombing?ref=profile","profile_image_url":"http://a1.twimg.com/profile_images/731346838/n1451341439_8331_normal.jpg","profile_background_image_url":"http://a3.twimg.com/profile_background_images/78992707/n1451341439_8331.jpg","protected":false,"contributors_enabled":false,"geo_enabled":true,"profile_sidebar_fill_color":"213b1b","screen_name":"devcharolline","name":"deeeeeviii","profile_background_tile":true,"id":99729433,"utc_offset":25200,"profile_sidebar_border_color":"4b63a6"},"id":10333118429,"in_reply_to_user_id":null}'
    TEST_TWEET = json.loads(TEST_TWEET_JSON)
    
    def test_protocol(self):
        consumer = mock.Mock()
        p = client.TwitterStreamProtocol(consumer)
        
        p.lineReceived(ClientTest.TEST_TWEET_JSON)
        
        self.assertEqual(1, consumer.tweetReceived.call_count)
        consumer.tweetReceived.assert_called_with(ClientTest.TEST_TWEET)