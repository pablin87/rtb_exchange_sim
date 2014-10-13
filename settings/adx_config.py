
conf = {
        
        # Definde what resource of the exchange connector endpoint is hitted
        # in order to place a bid request. 
        'http_resource' : 'adx',

        # Keys for price encryption in string hex
        'encryption_key' : "02EEa83c6c1211e10b9f88966ceec34908eb946f7ed6e441af42b3c0f3218140",
        'integrity_key' : "bfFFec55c30130c1d8cd1862ed2a4cd2c76ac33bc0c4ce8a3d3bbd3ad5687792",
        'initialization_vector' : "4a3a6f470001e2407b8c4a605b9200f2",

        # BE CAREFUL when using this parameter set to true. When it is set to
        # true, the requester will ignore the event template parameters below
        # and the EVENT_ENDPOINT from the general settings.
        # It will use directly the impression url that came in the html_snipet 
        # from the adx bid response. 
        'use_html_snippet' : False,

        # Define the url where the notifications of impressions and clicks will
        # be send. By this, the adm field is not have in count. The ip and
        # port set it here are replaced by global parameters of the endpoint 
        # settings. 
        'adserver_endpt_imp_tmpl' : "http://localhost:8080/events?ev=imp&aid=${AUCTION_ID}&apr=${AUCTION_PRICE}&sptid=${AUCTION_IMP_ID}",
        'adserver_endpt_click_tmpl' : "http://localhost:8080/events?ev=cli&aid=${AUCTION_ID}&sptid=${AUCTION_IMP_ID}",
        
        # If set to true, instead of using the 'adserver_endpt_imp_tmpl' and 
        # 'adserver_endpt_click_tmpl', it will use the following heh templates
        # in order to hit heh instead of the ad server connector directly.
        'use_heh_endpoint' : True, 
        'heh_endpt_imp_tmpl' : "http://localhost:8080/impression/adx/${AUCTION_ID}/${AUCTION_PRICE}?impid=${AUCTION_IMP_ID}",
        'heh_endpt_click_tmpl' : "http://localhost:8080/click/adx/${AUCTION_ID}?impid=${AUCTION_IMP_ID}"
        
        }
