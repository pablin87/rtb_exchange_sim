'''
Created on 24/06/2014

@author: pablin
'''
import logging
from parameter_plugin import ParameterPlugin
from string import Template
from adx.generator import RandomBidGeneratorWrapper
from adx.generator import realtime_bidding_pb2 as adxproto
import urlparse
import random

class AdxException(Exception): pass

class AdxPlugin(ParameterPlugin):
    '''
    Plugin for Adx. It generates bid request according to the adx specification.
    It uses the a modify version of the generator.py file from the official adx
     requester.
    '''

    def __init__(self):
        pass
    
    def initialize(self, adserver, config):
        
        self.adserver = adserver
        self.http_resource = config['http_resource']
        
        self.generator = RandomBidGeneratorWrapper()
        
        # Templates for notification endpoint
        self.use_heh_endpoint = config['use_heh_endpoint']
        if self.use_heh_endpoint :
            self.tmpl_imp_notif_file = config['heh_endpt_imp_tmpl']
            self.tmpl_click_notif_file = config['heh_endpt_click_tmpl']
        else :
            self.tmpl_imp_notif_file = config['adserver_endpt_imp_tmpl']
            self.tmpl_click_notif_file = config['adserver_endpt_click_tmpl']
        
        # Create the templates for the notifications
        self.tmpl_imp_notif = Template(self.tmpl_imp_notif_file)
        self.tmpl_click_notif = Template(self.tmpl_click_notif_file)

    def get_request(self):
        # We need to return a request line, a map of headers and a body
        
        # Create the request line
        req_line = 'POST /%s HTTP/1.1' % self.http_resource
        
        # Set the headers
        headers = {}
        headers['Host'] = 'localhost'
        headers['Connection'] = 'keep-alive'
        headers['Content-Type'] = 'application/octet-stream'
        
        # Generate payload...
        br = self.generator.GenerateBidRequest()
        payload = br.SerializeToString()
        
        # Set the header size
        headers['Content-Length'] = len(payload)
        
        return (req_line, headers, payload)

    def get_bid_price(self, br):
        if len(br.ad) == 0:
            raise AdxException("no br.ad")
        if not br.ad[0].HasField("html_snippet"):
            raise AdxException("no html_snippet")
        if len(br.ad[0].adslot) == 0:
            raise AdxException("no adslot")
        if not br.ad[0].adslot[0].HasField('max_cpm_micros'):
            raise AdxException("no max_cpm_miocros")
        return br.ad[0].adslot[0].max_cpm_micros

    def get_auction_id(self, br):
        pass

    def receive_response(self, status_code, headers, body):
        # If it is not a bid, do nothing
        if status_code == 204 :
            return (False, '', {}, '')
        
        # Extract data from bid response
        bid_resp = adxproto.BidResponse.ParseFromString(body)
        if len(bid_resp.ad) == 0:
            logging.debug("No add received")
            return (False, '', {}, '')
        
        logging.debug("Response received")
        try :
            bid_price = self.get_bid_price(bid_resp)
            auction_id = self.get_auction_id(bid_resp)
            spot_id = 1

            # With that data, create the notification...
            notif_render = { 'AUCTION_PRICE' : bid_price,
                            'AUCTION_ID' : auction_id,
                            'AUCTION_IMP_ID' : spot_id }

            # Win notification...
            url = self.tmpl_imp_notif.substitute(notif_render)
            self.__send_impression_notification(url)
        
            # Click notification... 
            click_url = self.tmpl_click_notif.substitute(notif_render)
            self.__send_click_notification(click_url)
            
        except :
            logging.exception("Could not get bid response")

        return (False, '', {}, '')
        
        
    def get_auction_price(self, json_response):
        if self.use_heh_endpoint:
            return json_response['seatbid'][0]['bid'][0]['price']
        else :
            # The value must be in Micro USD per one impression and it came in
            # CPM USD. That is the way the generic adserver expects it.
            price = float(json_response['seatbid'][0]['bid'][0]['price'])
            price = price * 1000000 # now micro USD CPM
            price = int(price / 1000) # CPM(1000 impressions) to 1 impression
            return str(price)

    def __send_click_notification(self, url):
        
        # Only generate clicks for the 2% of the cases
        if random.random() < 0.98:
            return
        
        parsed_url = urlparse(url)
        req_line = 'GET %s?%s HTTP/1.1' % (parsed_url.path,
                                           parsed_url.query)
        headers = {}
        headers['Host'] = 'localhost'
        heads = self.__headers_to_str(headers)
        buf = '%s\r\n%s\r\n' % (req_line, heads)
        
        # send the impression event in 0.1 secs
        logging.debug("Sending click notification :")
        logging.debug(buf)
        self.adserver.send_event(buf, 0.1)
        
    def __send_impression_notification(self, url):
        parsed_url = urlparse(url)
        req_line = 'GET %s?%s HTTP/1.1' % (parsed_url.path,
                                           parsed_url.query)
        headers = {}
        headers['Host'] = 'localhost'
        heads = self.__headers_to_str(headers)
        buf = '%s\r\n%s\r\n' % (req_line, heads)
        
        # send the impression event in 0.1 secs
        logging.debug("Sending impression notification :")
        logging.debug(buf)
        self.adserver.send_event(buf, 0.1)
        
    def __headers_to_str(self, headers):
        heads = ''
        for k,v in headers.iteritems():
            heads += '%s: %s\r\n' % (k, v)
        return heads

    def receive_win_response(self, status_code, headers, body):
        logging.debug('received_win_response')

    def do(self, watcher, revents):
        logging.debug('doing...')