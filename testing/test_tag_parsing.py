'''
Created on 07/04/2014

@author: pablin
'''
import sys
import os
from plugin.tag_parsing import extract_click_beacons_from_adm
sys.path.append('../')

import unittest
from plugin import tag_parsing
import json

class TestTagParsing(unittest.TestCase):


    def setUp(self):
        self.examples_path = os.path.dirname(os.path.abspath(__file__))

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

    def test_tag_parsing_click_url_source(self):
        adm = "<noscript><a href='http://localhost:8080/click/rubicon/${AUCTION_ID}?'><img src='http://i.ytimg.com/vi/mmiyJIN0LbU/mqdefault.jpg'></a></noscript><img src='http://localhost:8080/impression/rubicon/${AUCTION_ID}/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'/><img src='http://wac.450f.edgecastcdn.net/80450F/comicsalliance.com/files/2011/06/foreverc.jpg'/>"
        click_source = '/click/rubicon/${AUCTION_ID}?'
        
        parsed_source = tag_parsing.get_click_url_source(adm)
        self.assertEqual(click_source, parsed_source)
    
    def test_tag_parsing_impression_url_source(self):
        adm = "<noscript><a href='http://localhost:8080/click/rubicon/${AUCTION_ID}?'><img src='http://i.ytimg.com/vi/mmiyJIN0LbU/mqdefault.jpg'></a></noscript><img src='http://localhost:8080/impression/rubicon/${AUCTION_ID}/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'/><img src='http://wac.450f.edgecastcdn.net/80450F/comicsalliance.com/files/2011/06/foreverc.jpg'/>"
        imp_source = '/impression/rubicon/${AUCTION_ID}/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'
        
        parsed_source = tag_parsing.get_impression_url_source(adm)
        self.assertEqual(imp_source, parsed_source)
        
    def test_extract_imp_beacon(self):
        adm = r'''<a href='http://54.84.51.121:12340/click/mopub/${AUCTION_ID}?impid=${AUCTION_IMP_ID}&crid=131&redir=http%3A%2F%2Ftogetherillinois.com%2F&cid=2067&platform_id=%{bidrequest.device.os#urlencode}&postal_code=%{bidrequest.location.postalCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&metro_code=%{bidrequest.device.geo.metro}'><img src='http://d1brdofu76fhhj.cloudfront.net/5_cad2f457763e3618d119298d16dffcf4_BywkAxe2jZ.jpg'></a><img src='http://54.84.51.121:12340/impression/mopub/${AUCTION_ID}/${AUCTION_PRICE}?impid=${AUCTION_IMP_ID}&crid=131&fid=2067&cid=2067&site_domain=%{bidrequest.site.domain}&app_name=%{bidrequest.app.name#urlencode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier#urlencode}&metro_code=%{bidrequest.device.geo.metro}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&device_id=%{bidrequest.device.dpidsha1}&platform_id=%{bidrequest.device.os#urlencode}'/>'''
        exp = r'''http://54.84.51.121:12340/impression/mopub/${AUCTION_ID}/${AUCTION_PRICE}?impid=${AUCTION_IMP_ID}&crid=131&fid=2067&cid=2067&site_domain=%{bidrequest.site.domain}&app_name=%{bidrequest.app.name#urlencode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier#urlencode}&metro_code=%{bidrequest.device.geo.metro}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&device_id=%{bidrequest.device.dpidsha1}&platform_id=%{bidrequest.device.os#urlencode}'''
        imp = tag_parsing.extract_imp_beacons_from_adm(adm)
        self.assertEquals(imp, [exp])

    def test_extrac_click_beacon(self):
        adm = r'''<a href='http://54.84.51.121:12340/click/mopub/${AUCTION_ID}?impid=${AUCTION_IMP_ID}&crid=131&redir=http%3A%2F%2Ftogetherillinois.com%2F&cid=2067&platform_id=%{bidrequest.device.os#urlencode}&postal_code=%{bidrequest.location.postalCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&metro_code=%{bidrequest.device.geo.metro}'><img src='http://d1brdofu76fhhj.cloudfront.net/5_cad2f457763e3618d119298d16dffcf4_BywkAxe2jZ.jpg'></a><img src='http://54.84.51.121:12340/impression/mopub/${AUCTION_ID}/${AUCTION_PRICE}?impid=${AUCTION_IMP_ID}&crid=131&fid=2067&cid=2067&site_domain=%{bidrequest.site.domain}&app_name=%{bidrequest.app.name#urlencode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier#urlencode}&metro_code=%{bidrequest.device.geo.metro}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&device_id=%{bidrequest.device.dpidsha1}&platform_id=%{bidrequest.device.os#urlencode}'/>'''
        exp = r'''http://54.84.51.121:12340/click/mopub/${AUCTION_ID}?impid=${AUCTION_IMP_ID}&crid=131&redir=http%3A%2F%2Ftogetherillinois.com%2F&cid=2067&platform_id=%{bidrequest.device.os#urlencode}&postal_code=%{bidrequest.location.postalCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&metro_code=%{bidrequest.device.geo.metro}'''
        click = tag_parsing.extract_click_beacons_from_adm(adm)
        self.assertEquals(click, [exp])

    def test_tag_parsing_extract_auction_id(self):
        html_tag = "<noscript><a href='http://localhost:8080/click/adx/0123456789abcdef?'><img src='http://i.ytimg.com/vi/mmiyJIN0LbU/mqdefault.jpg'></a></noscript><img src='http://localhost:8080/impression/adx/0123456789abcdef/${AUCTION_PRICE}?crid=315&fid=266&cid=81&platform_id=%{bidrequest.device.os}&region_code=%{bidrequest.location.regionCode}&postal_code=%{bidrequest.location.postalCode}&country_code=%{bidrequest.location.countryCode}&site_id=%{bidrequest.site.id}&app_id=%{bidrequest.app.id}&carrier_id=%{bidrequest.device.carrier}&device_id=%{bidrequest.device.dpidsha1}'/><img src='http://wac.450f.edgecastcdn.net/80450F/comicsalliance.com/files/2011/06/foreverc.jpg'/>"
        auction_id = '0123456789abcdef' 
        
        parsed_auction_id = tag_parsing.extract_auction_id(html_tag)
        self.assertEqual(auction_id, parsed_auction_id)

    def load_native_examples(self):
        native_resp1 = os.path.join(self.examples_path,'native_resp_app_wall.json')
        native_resp2 = os.path.join(self.examples_path,'native_resp_chat_list.json')
        native_resp3 = os.path.join(self.examples_path,'native_resp_content_stream_video.json')
        native_resp4 = os.path.join(self.examples_path,'native_resp_google_text_ad.json')
        self.native1 = self.file_to_str(native_resp1)
        self.native2 = self.file_to_str(native_resp2)
        self.native3 = self.file_to_str(native_resp3)
        self.native4 = self.file_to_str(native_resp4)

    def file_to_str(self, filename):
        with open(filename) as f:
            return ''.join(f.readlines())

    def test_is_native(self):
        self.load_native_examples()
        
        self.assertTrue(tag_parsing.is_native(self.native1))
        self.assertTrue(tag_parsing.is_native(self.native2))
        self.assertTrue(tag_parsing.is_native(self.native3))
        self.assertTrue(tag_parsing.is_native(self.native4))

    def test_extract_imp_beacons_from_native(self):
        self.load_native_examples()
        
        exp = set(['http: //imp.com/b', 'http: //imp.com/a'])
        js = json.loads(self.native1)
        self.assertEquals(
            set(tag_parsing.extract_imp_beacons_from_native(js)), 
            exp)

        exp = set(['http: //a.com/a', 'http: //b.com/b'])
        js = json.loads(self.native2)
        self.assertEquals(
            set(tag_parsing.extract_imp_beacons_from_native(js)), 
            exp)
        
        exp = set([])
        js = json.loads(self.native3)
        self.assertEquals(
            set(tag_parsing.extract_imp_beacons_from_native(js)), 
            exp)

        exp = set([])
        js = json.loads(self.native4)
        self.assertEquals(
            set(tag_parsing.extract_imp_beacons_from_native(js)), 
            exp)


    def test_extract_click_beacons_from_native(self):
        self.load_native_examples()
        
        exp = set(['http: //click.com/b', 'http: //click.com/a'])
        js = json.loads(self.native1)
        self.assertEquals(
            set(tag_parsing.extract_click_beacons_from_native(js)), 
            exp)
        
        exp = set(['http: //a.com/a', 'http: //b.com/b'])
        js = json.loads(self.native2)
        self.assertEquals(
            set(tag_parsing.extract_click_beacons_from_native(js)), 
            exp)

        exp = set(['http: //click.com/b', 'http: //click.com/a',
                   'http: //asset.b.com/b', 'http: //asset.a.com/a'])
        js = json.loads(self.native3)
        self.assertEquals(
            set(tag_parsing.extract_click_beacons_from_native(js)), 
            exp)

        exp = set(['http: //click.com/b', 'http: //click.com/a',
                   'http: //data3.a.com/a', 'http: //title.a.com/a',
                   'http: //title.b.com/b'])
        js = json.loads(self.native4)
        self.assertEquals(
            set(tag_parsing.extract_click_beacons_from_native(js)), 
            exp)
        
    def test_extract_imp_vast_beacons(self):
        vast_file = os.path.join(self.examples_path,'vast_example.xml')
        adm_vast_str = self.file_to_str(vast_file)
        
        bcns = tag_parsing.extract_imp_beacons_from_adm(adm_vast_str)
        
        exp = set([
            "http://creatives.example.com/videoAds/imp_1",
            "http://creatives.example.com/videoAds/imp_2",
            "http://dev.motrixi.com:12340/smaato_nurl/video/impression/3152/${AUCTION_PRICE}",
            "http://creatives.example.com/videoAds/track_1",
            "http://creatives.example.com/videoAds/track_2",
            "http://10.0.2.11:12340/impression/smaato/${AUCTION_ID}/${AUCTION_PRICE}?impid=${AUCTION_IMP_ID}&mtx=6170705f69643d736d6161746f2d31303031303030266170705f6e616d653d46616365626f6f6b2532304576656e74266361703d3026636172726965725f69643d3331302d303034266361743d4941423134266369643d3331353226636f6e6e5f747970653d3026636f756e7472795f636f64653d55534126637269643d33353136266372745f683d30266372745f773d30266465766963655f69643d30316630386664653732663966393661613338313632383961363233626538643166336536346338266465766963655f69645f6d64353d266465766963655f69703d34362e3231312e3132392e323031266465766963655f747970653d31266669643d333135322667656f5f6c61743d2667656f5f6c6f6e673d266d6574726f5f636f64653d26706c6174666f726d5f69643d694f5326706f7374616c5f636f64653d26726567696f6e5f636f64653d26736974655f646f6d61696e3d26736974655f69643d267569643d&other=",
             ])

        self.assertEquals(exp, set(bcns))
        
    def test_extract_click_vast_beacons(self):
        vast_file = os.path.join(self.examples_path,'vast_example.xml')
        adm_vast_str = self.file_to_str(vast_file)
        
        bcns = tag_parsing.extract_click_beacons_from_adm(adm_vast_str)
        exp = set([
            "http://creatives.example.com/videoAds/click_tracking1",
            "http://creatives.example.com/videoAds/click_tracking2",
            "http://10.0.2.11:12340/click/smaato/${AUCTION_ID}?impid=${AUCTION_IMP_ID}&mtx=6170705f69643d736d6161746f2d3130303130303026636475726c3d6874747025334125324625324631302e302e322e353125324664617461253246763125324631343530332532466d747831343530333134353033253346646970253344253236647069642533442532366170705f6964253344253236736974655f696425334425323665696425334425323661756374696f6e5f696425334425323663726964253344253236666964253344253236636f6e6e5f74797065253344253236636f6f6b6965253344253236706c6174666f726d2533442532366465766963655f74797065253344253236706f7374616c5f636f64652533442532366d6574726f5f636f6465253344253236726571756573745f69642533442532367261775f696661253344266369643d3331353226636c69636b6572733d3126636f6e6e5f747970653d3026637269643d33353136266372745f683d30266372745f773d30266465766963655f747970653d312667656f5f6c61743d2667656f5f6c6f6e673d266d6574726f5f636f64653d26706c6174666f726d5f69643d694f5326706f7374616c5f636f64653d267261775f6966613d46353835423145462d443534332d344639432d413339462d41323034424439433145333326736974655f69643d&other=",
            ])
        self.assertEquals(exp, set(bcns))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()