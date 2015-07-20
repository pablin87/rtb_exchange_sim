import unittest
from plugin.smato_plugin import SmaatoPlugin


class Test(unittest.TestCase):


    adm_example1 = '''<ad xmlns:xsi="http://www.w3.org/2001/XMLSchema-
instance" xsi:noNamespaceSchemaLocation="smaato_ad_v0.9.xsd" modelVersion="
0.9">
<imageAd>
<clickUrl>http://mysite.com/click</clickUrl>
<imgUrl>http://mysite.com/impression/myad.jpg</imgUrl>
<width>728</width>
<height>90</height>
<toolTip>This is a tooltip text</toolTip>
<additionalText>Additional text to be displayed</additionalText>
<beacons>
<beacon>http://mysite.com/beacons/mybeacon1</beacon>
<beacon>http://mysite.com/beacons/mybeacon2</beacon>
</beacons>
</imageAd>
</ad>'''

    adm_bad_example1 = '''<ad xmlns:xsi="http://www.w3.org/2001/XMLSchema-
instance" >
<imageAd>
<toolTip>This is a tooltip text</toolTip>
</imageAd>
</ad>'''


    def testExtractImpressionBeacon(self):
        adm = self.adm_example1
        smt = SmaatoPlugin()
        expected_imp = 'http://mysite.com/impression/myad.jpg'
        imp = smt.extract_adm_impression_beacon(adm)
        self.assertEquals(imp, expected_imp)
        
        bad_adm = self.adm_bad_example1
        self.assertEquals("", smt.extract_adm_impression_beacon(bad_adm))
    
    def testExtractClickBeacon(self):
        adm = self.adm_example1
        smt = SmaatoPlugin()
        expected_click = 'http://mysite.com/click'
        click = smt.extract_adm_click_beacon(adm)
        self.assertEquals(click, expected_click)
        
        bad_adm = self.adm_bad_example1
        self.assertEquals("", smt.extract_adm_click_beacon(bad_adm))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()