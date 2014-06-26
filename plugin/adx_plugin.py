'''
Created on 24/06/2014

@author: pablin
'''
import logging
from string import Template

from parameter_plugin import ParameterPlugin
import tag_parsing

from adx.generator import RandomBidGeneratorWrapper
from adx import realtime_bidding_pb2 as adxproto
from adx.encryption.adx_encryption_utils import adx_encrypt_price


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
        
        self.enc_key = config['encryption_key']
        self.int_key = config['integrity_key']
        self.iv = config['initialization_vector']
        
        self.generator = RandomBidGeneratorWrapper()
        
        self.use_html_snippet = config['use_html_snippet']
        
        if not self.use_html_snippet:
            self.init_templates(config)

    def init_templates(self, config):
        
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
        logging.debug("adx generated :")
        logging.debug(str(br))
        
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
        # For now only support html_snippet.
        return tag_parsing.extract_auction_id(br.ad[0].html_snippet)

    def receive_response(self, status_code, headers, body):
        # If it is not a bid, do nothing
        if status_code == 204 :
            return (False, '', {}, '')
        
        # Extract data from bid response
        bid_resp = adxproto.BidResponse()
        bid_resp.ParseFromString(body)
        logging.debug("adx bid response received :")
        logging.debug(str(bid_resp))
        if len(bid_resp.ad) == 0:
            logging.debug("No add received")
            return (False, '', {}, '')
        
        logging.debug("Response received")
        try :
            bid_price = self.get_bid_price(bid_resp)
            auction_id = self.get_auction_id(bid_resp)
            spot_id = 1
            
            # Encode the price...
            enc_price = adx_encrypt_price(bid_price, self.enc_key,
                                           self.int_key, self.iv)
            
            # With that data, create the notification...
            notif_render = { 'AUCTION_PRICE' : enc_price,
                            'AUCTION_ID' : auction_id,
                            'AUCTION_IMP_ID' : spot_id }
            self.do_events(notif_render, bid_resp)
            
        except :
            logging.exception("Could not get bid response")

        return (False, '', {}, '')

    def do_events(self, notif_render_map, bid_resp):
        # This function is in charge of sending impressions and clicks
        if self.use_html_snippet :
            self.do_event_from_html_snippet(bid_resp, notif_render_map)
        else :
            self.do_event_from_templates(notif_render_map)

    def do_event_from_html_snippet(self, bid_resp, notif_render_map):
        # Get the corresponding urls and set the price to the imp url

        tag = bid_resp.ad[0].html_snippet

        price = notif_render_map['AUCTION_PRICE']
        imp_url = tag_parsing.get_impression_url_source(tag)
        imp_url = self.replace_price_macro(imp_url, price)
        self.__send_impression_notification(imp_url)
        
        # now for the click url
        clicl_url = tag_parsing.get_click_url_source(tag)
        self.__send_click_notification(clicl_url)
    
    def replace_price_macro(self, imp_url, price):
        PRICE_MACRO = "%%WINNING_PRICE%%"
        return imp_url.replace(PRICE_MACRO, str(price))
    
    def do_event_from_templates(self, notif_render_map):
        # Win notification...
        url = self.tmpl_imp_notif.substitute(notif_render_map)
        self.__send_impression_notification(url)
        
        # Click notification... 
        click_url = self.tmpl_click_notif.substitute(notif_render_map)
        self.__send_click_notification(click_url)

        
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
        