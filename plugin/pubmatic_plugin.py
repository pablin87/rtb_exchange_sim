from openrtb_plugin import OpenRTBPlugin

class PubmaticPlugin(OpenRTBPlugin):
    '''
        Replace the AUCTION_CLICKTRACK_URL macro.
    '''

    def initialize(self, adserver, config):
        super(PubmaticPlugin, self).initialize(adserver, config)
        self.auction_clicktrack_url = config['auction_clicktrack_url']

    def get_auction_price(self, json_response):
        # Mopub sends price in USD CPM. And the price is sent in USD CPM.
        return json_response['seatbid'][0]['bid'][0]['price']

    def get_beacon_macros(self, jsbr):
        dic = super(PubmaticPlugin, self).get_beacon_macros(jsbr)
        dic['AUCTION_CLICKTRACK_URL'] = self.auction_clicktrack_url
        return dic