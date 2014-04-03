from parameter_plugin import ParameterPlugin
from string import Template
import random
import json
import logging
from urlparse import urlparse


class OpenRTBPlugin(ParameterPlugin):
    '''
        Generic Open Rtb plugin
    '''
    def __init__(self):
        self.request_body_templates = []
        self.render_map = {}
        self.tmpl_imp_notif = ''
    
    def initialize(self, adserver, config):
        
        self.adserver = adserver
        self.http_resource = config['http_resource']
        self.exchange = config['exchange']
        
        # Map to render the bid request body templates
        self.render_map = config['render_map']
        
        # Create templates fot the bid requests...
        self.request_body_templates_files = config['req_body_templates']
        for filename in self.request_body_templates_files:
            with open(filename) as f:
                logging.info('Using file template %s' % filename)
                tmpl = Template(''.join(f.readlines()))
                self.request_body_templates.append(tmpl)
        
        # Templates for notification endpoint
        if config['use_heh_endpoint'] :
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
        headers['Content-Type'] = 'application/json'
        headers['x-openrtb-version'] = '2.1'
        
        # Render the body...
        tmpl = random.choice(self.request_body_templates)
        fun_rendered_map = { k : fun() for k, fun in self.render_map.items()}
        body = tmpl.substitute(fun_rendered_map)
        
        # Set the header size
        headers['Content-Length'] = len(body)
        
        logging.debug('Message body being sent :')
        logging.debug(body)
        return (req_line, headers, body)

    def receive_response(self, status_code, headers, body):
        # If it is not a bid, do nothing
        if status_code == 204 :
            return (False, '', {}, '')
        
        # Extract data from bid response
        js = json.loads(body)
        logging.debug("Response received :")
        logging.debug(str(js))
        price = self.get_auction_price(js)
        auction_id = self.get_auction_id(js)
        spot_id = self.get_auction_impression_id(js)
        
        # With that data, create the notification...
        notif_render = { 'AUCTION_PRICE' : price,
                         'AUCTION_ID' : auction_id,
                         'AUCTION_IMP_ID' : spot_id,
                         'exchange' : self.exchange }
        
        # Win notification...
        url = self.tmpl_imp_notif.substitute(notif_render)
        self.__send_impression_notification(url)
        
        # Click notification... 
        click_url = self.tmpl_click_notif.substitute(notif_render)
        self.__send_click_notification(click_url)
        
        return (False, '', {}, '')
        
    def get_auction_price(self, json_response):
        return json_response['seatbid'][0]['bid'][0]['price']

    def get_auction_id(self, json_response):
        return json_response['id']

    def get_auction_impression_id(self, json_response):
        return json_response['seatbid'][0]['bid'][0]['impid']

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
