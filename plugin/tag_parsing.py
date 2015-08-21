import re
from BeautifulSoup import BeautifulSoup
from string import Template
import json

# We do this to support ':' inside a macro
class MacroTemplate(Template):
    idpattern = r'[a-z][_a-z0-9]*(:[a-z][_a-z0-9]*)*'

CLICK_REGEX = re.compile('(.*[\'\"])(?P<http>http://).*(?P<url>/click/.*\?.*)([\'\"].*)')
IMP_REGEX = re.compile('(.*[\'\"])(?P<http>http://).*(?P<url>/impression/.*\?.*)([\'\"].*)')

def get_impression_url(adm, ip, port):
    # Given an adm with a tag for an impression url, replace the ip:port part
    # with the given ones. 
    links_list = adm.split('<')
    imp_link_line = [ line for line in links_list if 'impression' in line][0] 
    ip_port = r'\g<http>%s:%s\g<url>' % (ip, str(port))
    return IMP_REGEX.sub(ip_port, imp_link_line)


def get_click_url(adm, ip, port):
    # Given an adm with a tag for a click url, replace the ip:port part
    # with the given ones. 
    links_list = adm.split('<')
    click_link_line = [ line for line in links_list if 'click' in line][0] 
    ip_port = r'\g<http>%s:%s\g<url>' % (ip, str(port))
    return CLICK_REGEX.sub(ip_port, click_link_line)


def get_click_url_source(adm):
    # Given an adm field, extract the source part of the url (aka: without the
    # 'http://ip:port' part ) for the click
    links_list = adm.split('<')
    click_link_line = [ line for line in links_list if 'click' in line][0]
    return CLICK_REGEX.sub('\g<url>', click_link_line)


def get_impression_url_source(adm):
    # Given an adm field, extract the source part of the url (aka: without the
    # 'http://ip:port' part ) for the impression
    links_list = adm.split('<')
    imp_link_line = [ line for line in links_list if 'impression' in line][0]
    return IMP_REGEX.sub('\g<url>', imp_link_line)

def extract_auction_id(html_tag):
    # The impression url from the adm or html tag looks like this:
    # http://localhost:8080/impression/adx/${AUCTION_ID}/${AUCTION_PRICE}?(...)
    # So get the impression url and from it get the auction id.
    # This function should be used when the auction_id is replaced by ourself 
    # and not by the exchange with the macro replacement. So, for Adx.
    imp_url = get_impression_url_source(html_tag)
    return imp_url.split('/')[3]

def extract_imp_beacons_from_adm(adm):
    if is_native(adm):
        jsnative = json.loads(adm)
        return extract_imp_beacons_from_native(jsnative)
    else:
        return extract_imp_beacons_from_html(adm)

def extract_click_beacons_from_adm(adm):
    if is_native(adm):
        jsnative = json.loads(adm)
        return extract_click_beacons_from_native(jsnative)
    else:
        return extract_click_beacons_from_html(adm)

def extract_imp_beacons_from_html(adm):
    '''
    Try to get the impression from a html adm openRTB field. The impression 
    beacon is extracted from the img tag from the src field. 
    '''
    b = BeautifulSoup(adm)
    imgtags = [ i for i in b if i.name == 'img']
    return [ imgtags[0]['src'] ]

def extract_click_beacons_from_html(adm):
    '''
    Try to get the click track url from a html adm openRTB field. The click 
    beacon is extracted from an anchor (<a>) tag from the href field.
    '''
    b = BeautifulSoup(adm)
    atag = b.find('a', attrs={'href':True})
    return [ atag['href'] ]

def extract_imp_beacons_from_native(native_resp):
    '''
    Extract impression beacons from a native response json.
    Beacons are extracted from native->imptrackers.
    '''
    
    bcns = []
    if 'imptrackers' in native_resp['native']:
        bcns.extend(native_resp['native']['imptrackers'])
    return bcns

def extract_click_beacons_from_native(native_resp):
    '''
    Extract click beacons from a native response json. Beacons are extracted 
    from native->link->clicktrackers (parent link object) and from the 
    clicktrackers of the links objects in the assets.
    '''
    bcns = []
    if 'clicktrackers' in native_resp['native']['link']:
        bcns.extend(native_resp['native']['link']['clicktrackers'])
        
    for asset in native_resp['native']['assets']:
        if 'link' in asset:
            if 'clicktrackers' in asset['link']:
                bcns.extend(asset['link']['clicktrackers'])
                
    return bcns

def is_native(adm):
    '''
    Indicates if the given adm field from an OpenRTB response corresponds
    to a native ad or not.
    '''
    try:
        native = json.loads(adm)
        return native.has_key('native')
    except :
        return False
