from openrtb_plugin import OpenRTBPlugin

class SharethroughPlugin(OpenRTBPlugin):
    
    def initialize(self, adserver, config):
        super(SharethroughPlugin, self).initialize(adserver, config)
        
        # Native is supported since openrtb 2.3
        self.def_headers['x-openrtb-version'] = '2.3'
