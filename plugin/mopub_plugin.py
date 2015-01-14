from openrtb_plugin import OpenRTBPlugin

class MopubPlugin(OpenRTBPlugin):
    '''
        Only need to make the price in CPM.
    '''

    def get_auction_price(self, json_response):
        # Mopub sends price in USD CPM. And the price is sent in USD CPM.
        return json_response['seatbid'][0]['bid'][0]['price']
