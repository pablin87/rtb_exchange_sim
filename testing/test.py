'''
Created on 07/04/2014

@author: pablin
'''
import sys
sys.path.append('../')

import unittest
from plugin import tag_parsing


class TestTagParsing(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_tag_parsing_impression(self):
        adm = "<noscript><a href='http://localhost:8080/click/rubicon/${AUCTION_ID}?'><img src='http://i.ytimg.com/vi/mmiyJIN0LbU/mqdefault.jpg'></a></noscript><img src='http://localhost:8080/impression/rubicon/${AUCTION_ID}/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'/><img src='http://wac.450f.edgecastcdn.net/80450F/comicsalliance.com/files/2011/06/foreverc.jpg'/>"
        imp_url = 'http://192.168.1.2:4545/impression/rubicon/${AUCTION_ID}/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'
        
        parsed_url = tag_parsing.get_impression_url(adm, '192.168.1.2', '4545')
        self.assertEqual(imp_url, parsed_url)
    
    def test_tag_parsing_click(self):
        adm = "<noscript><a href='http://localhost:8080/click/rubicon/${AUCTION_ID}?'><img src='http://i.ytimg.com/vi/mmiyJIN0LbU/mqdefault.jpg'></a></noscript><img src='http://localhost:8080/impression/rubicon/${AUCTION_ID}/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'/><img src='http://wac.450f.edgecastcdn.net/80450F/comicsalliance.com/files/2011/06/foreverc.jpg'/>"
        click_url = 'http://192.168.1.2:4545/click/rubicon/${AUCTION_ID}?'
        
        parsed_url = tag_parsing.get_click_url(adm, '192.168.1.2', '4545')
        self.assertEqual(click_url, parsed_url)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()