import logging

# Plugin imports
from plugin.rubicon_plugin import RubiconPlugin
from plugin.datacratic_plugin import DatacraticPlugin
from plugin.openrtb_plugin import OpenRTBPlugin

# Max connections for bid requests allowed for the process
MAX_CONNS = 1
# Amount of connections for event notification allowed for the process
MAX_EVENT_CONNS = 1

# Endpoint list containing tuples for the DSPs (endpoint, expected_qps) where :
#  - endpoint should be a string 'host:port'
#  - expected_qps is the amount of qps expected for the endpoint
ENDPOINT_LIST = [
    ('localhost:12341', 20),
]

# Event endpoint :
# - endpoint should be a string 'host:port'
EVENT_ENDPOINT = 'localhost:12340'

# Balance time out indicating the period in seconds 
# to balance connections
BALANCE_TO = 3

# Check connections time out indicating the period in
# seconds to verify if a connection attempt was successfull
CHECK_CONNS_TO = 1

# Check pending wins and try to send them
CHECK_PENDING_TO = 1

# Timeout in seconds to periodically invoke the plugin.do method
# set to None if it does not need to be invoked
PLUGIN_DO_TO = 10

# Report wps statistics
REPORT_WINS = False

# Keep alive time out for the event conns in seconds, if no
# keep alive need to be sent set it to None 
EVENT_CONN_KEEP_ALIVE_TO = None

# Keep alive request
KEEP_ALIVE_HTTP_REQUEST = \
    'GET / HTTP/1.1\r\n' \
    'Keep-Alive: timeout=%d, max=5000\r\n' \
    'Connection: Keep-Alive\r\n' 

# Log level should be one of :
# - logging.DEBUG
# - logging.INFO
# - logging.WARNING
# - logging.ERROR
LOG_LEVEL = logging.INFO

# Parameter plugin
#PARAMETER_PLUGIN = RubiconPlugin
PARAMETER_PLUGIN = OpenRTBPlugin

# Configuration map that will be passed in the initialize 
import mopub_config 
PLUGIN_CONFIG = mopub_config.conf

# RTB request template filename
TEMPLATE_FILENAME = 'templates/request.template'
