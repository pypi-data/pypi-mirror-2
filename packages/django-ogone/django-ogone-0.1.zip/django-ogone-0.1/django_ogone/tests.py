import unittest
import doctest

from django_ogone import security, Ogone

from django_ogone.alternative_signing import create_hash

class OgoneTestCase(unittest.TestCase):
    def setUp(self):
        class Settings(object):
            SHA_PRE_SECRET = 'test1234'
            SHA_POST_SECRET = 'test12345'
            HASH_METHOD = 'sha512'
            PRODUCTION = False
            PSPID = 'mycutePS'

        self.settings = Settings()

        self.ogone = Ogone

    def testValidHash(self):
        params = {u'ORDERID': u'13', u'STATUS': u'9', u'CARDNO': u'XXXXXXXXXXXX1111', u'VC': u'NO', u'PAYID': u'8285812', u'CN': u'Kaast Achternaam', u'NCERROR': u'0', u'IP': u'82.139.114.10', u'IPCTY': u'NL', u'CURRENCY': u'EUR', u'CCCTY': u'US', u'AAVCHECK': u'NO', u'BRAND': u'VISA', u'ACCEPTANCE': u'test123', u'ECI': u'7', u'TRXDATE': u'09/24/10', u'AMOUNT': u'6794.81', u'CVCCHECK': u'NO', u'ED': u'0111', u'PM': u'CreditCard'}
        params['SHASIGN'] = create_hash(params, self.settings.SHA_POST_SECRET)

        o = self.ogone(params, settings=self.settings)
        self.assert_(o.is_valid())

    def testInvalidHash(self):
        params = {u'ORDERID': u'12', u'STATUS': u'9', u'CARDNO': u'XXXXXXXXXXXX1111', u'VC': u'NO', u'PAYID': u'8285812', u'CN': u'Kaast Achternaam', u'NCERROR': u'0', u'IP': u'82.139.114.10', u'IPCTY': u'NL', u'CURRENCY': u'EUR', u'CCCTY': u'US', u'AAVCHECK': u'NO', u'BRAND': u'VISA', u'ACCEPTANCE': u'test123', u'ECI': u'7', u'TRXDATE': u'09/24/10', u'AMOUNT': u'6794.81', u'CVCCHECK': u'NO', u'ED': u'0111', u'PM': u'CreditCard'}
        params['SHASIGN'] = create_hash(params, self.settings.SHA_POST_SECRET)

        params['ORDERID'] = '23'

        o = self.ogone(params, settings=self.settings)
        self.assertFalse(o.is_valid())

    def testParseParams(self):
        params = {u'ORDERID': u'13', u'STATUS': u'9', u'CARDNO': u'XXXXXXXXXXXX1111', u'VC': u'NO', u'PAYID': u'8285812', u'CN': u'Kaast Achternaam', u'NCERROR': u'0', u'IP': u'82.139.114.10', u'IPCTY': u'NL', u'CURRENCY': u'EUR', u'CCCTY': u'US', u'AAVCHECK': u'NO', u'BRAND': u'VISA', u'ACCEPTANCE': u'test123', u'ECI': u'7', u'TRXDATE': u'09/24/10', u'AMOUNT': u'6794.81', u'CVCCHECK': u'NO', u'ED': u'0111', u'PM': u'CreditCard'}

        params['SHASIGN'] = create_hash(params, self.settings.SHA_POST_SECRET)
        o = self.ogone(params, settings=self.settings)
        o.parse_params()

        self.assertEqual(o.get_order_id(), 13)
        self.assertEqual(o.get_status(), 9)
        self.assertEqual(o.get_status_description(), 'Payment requested')

    def testForm(self):
        data = {'orderID': 14, 'ownerstate': u'', 'cn': u'Kaast Achternaam', 'language': 'en_US', 'ownertown': u'Klaas', 'ownercty': u'NL', 'exceptionurl': u'http://127.0.0.1:8000/shop/checkout/ogone/failure/', 'ownerzip': u'Postcode', 'catalogurl': u'http://127.0.0.1:8000/shop/category/', 'currency': u'EUR', 'amount': u'579', 'declineurl': u'http://127.0.0.1:8000/shop/checkout/ogone/failure/', 'homeurl': u'http://127.0.0.1:8000/shop/', 'cancelurl': u'http://127.0.0.1:8000/shop/checkout/ogone/failure/', 'accepturl': u'http://127.0.0.1:8000/shop/checkout/ogone/success/', 'owneraddress': u'Straat', 'com': u'Order #14: Kaast Achternaam', 'email': u'mathijs@mathijsfietst.nl'}
        data['PSPID'] = self.settings.PSPID
        shasign = create_hash(data, self.settings.SHA_PRE_SECRET)
        form = self.ogone.get_form(data, settings=self.settings)

        self.assertEqual(form['SHASign'].field.initial, shasign)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(security))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(OgoneTestCase))
    return suite
