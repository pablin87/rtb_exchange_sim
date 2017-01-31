from openrtb_plugin import OpenRTBPlugin
from xml.etree import ElementTree 
import logging
import tag_parsing as tgp

class SmaatoPlugin(OpenRTBPlugin):
    '''
        Change the way we extract the impression and click beacon from the 
        bid response, as smaato uses a private xml scheme for ad tags.
    '''
    
    def initialize(self, adserver, config):
        super(SmaatoPlugin, self).initialize(adserver, config)
        self.def_headers['x-openrtb-version'] = '2.0'

    def extract_adm_impression_beacons(self, adm):
        if tgp.is_vast(adm):
            return tgp.extract_imp_beacons_from_adm(adm)
        else :
            return self._extract_adm_impressions(adm)
    
    def _extract_adm_impressions(self, adm):
        bcns = []
        try :
            root = ElementTree.fromstring(adm)
            for bcn in root.find('imageAd').find("beacons"):
                bcns.append(bcn.text)
        except :
            logging.exception("While parsing beacons from xml : %s", adm)
        return bcns
    
    def extract_adm_click_beacons(self, adm):
        if tgp.is_vast(adm):
            return tgp.extract_click_beacons_from_adm(adm)
        else :
            return self._extract_adm_click(adm)        
    
    def _extract_adm_click(self, adm):
        return self.__extract_url_from_node(adm, 'clickUrl')
    
    def get_auction_price(self, json_response):
        # Smaato follows OpernRTB which sends price in USD CPM. And the price is sent in USD CPM.
        return json_response['seatbid'][0]['bid'][0]['price']

    def extract_image_url(self, adm):
        return self.__extract_url_from_node(adm, 'imgUrl')

    def __extract_url_from_node(self, adm, node_name):
        root = ElementTree.fromstring(adm)
        url = []
        try:
            url.append(root.find('imageAd').find(node_name).text)
        except :
            logging.exception("While parsing %s beacon from xml : %s", 
                              node_name, adm)
        return url
