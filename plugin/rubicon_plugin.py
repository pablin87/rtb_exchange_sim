from openrtb_plugin import OpenRTBPlugin

class RubiconPlugin(OpenRTBPlugin):
    '''
        Only need to redefine the price encoding.
    '''

    def get_auction_price(self, json_response):
        return 'A8026991338B87A4' # for now just return fixed one
