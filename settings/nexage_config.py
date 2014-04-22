from render_utils import random_id

conf = {
        
        # Name of the exchange being simulated (used to generate notifications)
        # in the correct path
        'exchange' : 'nexage',
        
        # This define the body templates that are being sent to the rtbkit
        # exchange connector endpoint (files).
        'req_body_templates' : [ 
                                'plugin/nexage/nexage_body1.tmpl', 
                                'plugin/nexage/nexage_body2.tmpl',
                                'plugin/nexage/nexage_body3.tmpl'
                                ],
        
        # This map defines a list of functions that when being called return a 
        # value to be rendered in the templates defined in the 
        # 'req_body_templates' field. For example to return a constant value 
        # 'auction_id' : lambda : 5   (will return always five)
        'render_map' : {
                        'auction_id' : random_id()
                        },
        
        # Definde what resource of the exchange connector endpoint is hitted
        # in order to place a bid request. 
        'http_resource' : 'nexage',

        # Define the url where the notifications of impressions and clicks will
        # be send. By this, the adm field is not have in count. The ip and
        # port set it here are replaced by global parameters of the endpoint 
        # settings. 
        'adserver_endpt_imp_tmpl' : "http://localhost:8080/events?ev=imp&aid=${AUCTION_ID}&apr=${AUCTION_PRICE}&sptid=${AUCTION_IMP_ID}",
        'adserver_endpt_click_tmpl' : "http://localhost:8080/events?ev=cli&aid=${AUCTION_ID}&sptid=${AUCTION_IMP_ID}",
        
        # If set to true, instead of using the 'adserver_endpt_imp_tmpl' and 
        # 'adserver_endpt_click_tmpl', it will use the following heh templates
        # in order to hit heh instead of the ad server connector directly.
        'use_heh_endpoint' : False, 
        'heh_endpt_imp_tmpl' : "http://localhost:8080/impression/${exchange}/${AUCTION_ID}/${AUCTION_PRICE}?impid=${AUCTION_IMP_ID}",
        'heh_endpt_click_tmpl' : "http://localhost:8080/click/${exchange}/${AUCTION_ID}?impid=${AUCTION_IMP_ID}"
        
        }
