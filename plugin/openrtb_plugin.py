from parameter_plugin import ParameterPlugin
import random
import json
import logging
from urlparse import urlparse
from tag_parsing import extract_click_beacons_from_adm
from tag_parsing import extract_imp_beacons_from_adm
from tag_parsing import MacroTemplate


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
                tmpl = MacroTemplate(''.join(f.readlines()))
                self.request_body_templates.append(tmpl)
        
        # Templates for notification endpoint
        self.use_heh_endpoint = config['use_heh_endpoint']
        if self.use_heh_endpoint :
            self.tmpl_imp_notif_file = config['heh_endpt_imp_tmpl']
            self.tmpl_click_notif_file = config['heh_endpt_click_tmpl']
        else :
            self.tmpl_imp_notif_file = config['adserver_endpt_imp_tmpl']
            self.tmpl_click_notif_file = config['adserver_endpt_click_tmpl']
        
        # Create the templates for the notifications
        self.tmpl_imp_notif = MacroTemplate(self.tmpl_imp_notif_file)
        self.tmpl_click_notif = MacroTemplate(self.tmpl_click_notif_file)
        
        # Check if we are going to use the adm field directly
        self.use_adm = config['use_adm']
        
        self.def_headers = {}
        self.def_headers['Host'] = 'localhost'
        self.def_headers['Connection'] = 'keep-alive'
        self.def_headers['Content-Type'] = 'application/json'
        self.def_headers['x-openrtb-version'] = '2.1'

    def get_request(self):
        # We need to return a request line, a map of headers and a body
        
        # Create the request line
        req_line = 'POST /%s HTTP/1.1' % self.http_resource
        
        # Set the headers
        headers = self.def_headers.copy()
        
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
        adm = self.get_adm(js)
        
        # With that data, create the notification...
        notif_data = { 'AUCTION_PRICE' : price,
                       'AUCTION_PRICE:BF' : price, # for bluefish encryption
                       'AUCTION_ID' : auction_id,
                       'AUCTION_IMP_ID' : spot_id,
                       'exchange' : self.exchange,
                       'adm' : adm }
        
        self.do_beaconning(notif_data)
                
        return (False, '', {}, '')
    
    def do_beaconning(self, br_data):
        if self.use_adm :
            imp_beacons = self.extract_adm_impression_beacons(br_data['adm'])
            imp_beacons = [ MacroTemplate(bcn) for bcn in imp_beacons ]
            click_beacons = self.extract_adm_click_beacons(br_data['adm'])
            click_beacons = [ MacroTemplate(bcn) for bcn in click_beacons ]
        else :
            imp_beacons = [ self.tmpl_imp_notif ]
            click_beacons = [ self.tmpl_click_notif ]
        
        # Render and call the win notifications...
        for imp_bcn in imp_beacons:
            url = imp_bcn.substitute(br_data)
            self.__send_impression_notification(url)
        
        # Render and call the click notifications... 
        for click_bcn in click_beacons:
            click_url = click_bcn.substitute(br_data)
            self.__send_click_notification(click_url)
    
    def extract_adm_impression_beacons(self, adm):
        '''
        Return a list of url beacons to be called to generate impressions.
        The urls may have macros that need to be replaced
        '''
        bcns = [ extract_imp_beacons_from_adm(adm) ]
        return bcns
    
    def extract_adm_click_beacons(self, adm):
        '''
        Return a list of url beacons to be called to generate clicks.
        The urls may have macros that need to be replaced
        '''
        bcns = [ extract_click_beacons_from_adm(adm) ]
        return bcns
    
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

    def get_auction_id(self, json_response):
        return json_response['id']

    def get_auction_impression_id(self, json_response):
        return json_response['seatbid'][0]['bid'][0]['impid']
    
    def get_adm(self, json_response):
        return json_response['seatbid'][0]['bid'][0]['adm']

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

