import re

def get_impression_url(adm, ip, port):
    # Given an adm with a tag for an impression url, replace the ip:port part
    # with the given ones. 
    links_list = adm.split('<')
    imp_link_line = [ line for line in links_list if 'impression' in line][0] 
    ip_port = r'\g<http>%s:%s\g<url>' % (ip, str(port))
    return re.sub('(.*[\'\"])(?P<http>http://).*(?P<url>/impression/.*\?.*)([\'\"].*)', ip_port, imp_link_line)
    

def get_click_url(adm, ip, port):
    # Given an adm with a tag for a click url, replace the ip:port part
    # with the given ones. 
    links_list = adm.split('<')
    click_link_line = [ line for line in links_list if 'click' in line][0] 
    ip_port = r'\g<http>%s:%s\g<url>' % (ip, str(port))
    return re.sub('(.*[\'\"])(?P<http>http://).*(?P<url>/click/.*\?.*)([\'\"].*)', ip_port, click_link_line)