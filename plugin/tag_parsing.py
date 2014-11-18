import re
from BeautifulSoup import BeautifulSoup

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
    '''
    Try to get the impression and click beacon from a adm openRTB field.
    The click beacon is extracted from an anchor (<a>) tag from the 
    '''
    b = BeautifulSoup(adm)
    imgtags = [ i for i in b if i.name == 'img']
    return imgtags[0]['src']

def extract_click_beacons_from_adm(adm):
    b = BeautifulSoup(adm)
    atag = b.find('a', attrs={'href':True})
    return atag['href']

