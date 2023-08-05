"""

Tests for the onlinepayment module.  You must edit the code below to
add a test account for the supported payment modules.  I get them from
my Django setup, but most likely that won't work for you.

Copyright (c) 2009, We Also Walk Dogs
All rights reserved.

Onlinepayment is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

try:
    import settings

    AUTHDOTNET_AUTH = dict(login = settings.DEFAULT_AUTH_NET_LOGIN,
                           key   = settings.DEFAULT_AUTH_NET_KEY)

    PAYPAL_AUTH = dict(partner   = settings.DEFAULT_PAYPAL_PARTNER,
                       vendor    = settings.DEFAULT_PAYPAL_USERNAME,
                       username  = settings.DEFAULT_PAYPAL_VENDOR,
                       password  = settings.DEFAULT_PAYPAL_PASSWORD)

except:
    raise Exception("Please edit tests.py and setup a test acct and password for authorize.net")

# support both loading from my project, where onlinepayment is an
# integrated component, and from the root for most users
try:
    from core.onlinepayment import OnlinePayment, AuthNetConnection
except ImportError as e:
    try:
        from onlinepayment import OnlinePayment, AuthNetConnection
    except:
        raise e

import unittest
import datetime
import time
import random

from warnings import warn
import re

DEBUG=True

class OnlinePaymentPayPalTest(unittest.TestCase):
    def setUp(self):
        self.conn = self._standard_connection()

    def _standard_connection(self, **kwargs):
        args = dict(auth=PAYPAL_AUTH,
                    debug=DEBUG)
        args.update(kwargs)
        return OnlinePayment('paypal', **args)

    def test_sale(self):
        result = self.conn.sale(amount='15.00',
                                card_num='5555555555554444',
                                exp_date='1212',
                                address="123 Test Ln.",
                                zip="10562")

        self.assertEqual(result.success, True)

    def test_bad_auth(self):
        conn = self._standard_connection(auth = \
           {'partner'  : PAYPAL_AUTH['partner'],
            'vendor'   : PAYPAL_AUTH['vendor'],
            'username' : 'foo',
            'password' : 'foo'
           })
        try:
            conn.sale(amount='2.00',
                      card_num='4007000000026',
                      exp_date='0528')
        except conn.AuthError:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_declined(self):
        try:
            self.conn.sale(amount='2012',
                           card_num='4111111111111111',
                           exp_date='0527')
        except self.conn.TransactionDeclined:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_invalid_card(self):
        try:
            self.conn.sale(amount='2012',
                           card_num='0000000000000000',
                           exp_date='0530')
        except self.conn.CardNumberInvalid:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_bad_exp(self):
        try:
            self.conn.sale(amount='2.00',
                           card_num='4007000000027',
                           exp_date='aabb')
        except self.conn.CardExpirationInvalid:
            pass
        else:
            self.fail("Expected exception not caught!")

    # note that paypal doesn't have a separate exception for this
    def test_expired(self):
        try:
            self.conn.sale(amount='2.00',
                           card_num='4007000000027',
                           exp_date='0101')
        except self.conn.CardExpirationInvalid:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_authorize(self):
        result = self.conn.authorize(amount='2.00',
                                     card_num='4111111111111111',
                                     exp_date='0530')

        self.assertEquals(result.success, True)

    def test_capture(self):
        result = self.conn.authorize(amount='2.00',
                                     card_num='4111111111111111',
                                     exp_date='0530')
        self.assertEquals(result.success, True)

        result2 = self.conn.capture(trans_id=result.trans_id)
        self.assertEquals(result2.success, True)

    def test_void(self):
        result = self.conn.sale(amount='2.00',
                                card_num='4111111111111111',
                                exp_date='0530')
        self.assertEqual(result.success, True)
        void_result = self.conn.void(trans_id=result.trans_id)
        self.assertEqual(void_result.success, True)

    def test_credit(self):
        result = self.conn.sale(amount='2.00',
                                card_num='4111111111111111',
                                exp_date='0530')
        self.assertEqual(result.success, True)
        void_result = self.conn.credit(trans_id=result.trans_id)
        self.assertEqual(void_result.success, True)

    def test_all_params(self):
        result = self.conn.sale(
            address            = 'address',
            amount             = '2.00',
            card_code          = '1234',
            card_num           = '4111111111111111',
            city               = 'city',
            company            = 'company',
            country            = 'country',
            description        = 'description',
            email              = 'email@example.com',
            exp_date           = '0530',
            first_name         = 'first_name',
            invoice_num        = 'invoice_num',
            last_name          = 'last_name',
            phone              = 'phone',
            ship_to_address    = 'ship_to_address',

            # paypal has no equivalent field, oddly
            # ship_to_company  = 'ship_to_company', 

            ship_to_country    = 'ship_to_country',
            ship_to_city       = 'ship_to_city',
            ship_to_first_name = 'ship_to_first_name',
            ship_to_last_name  = 'ship_to_last_name',
            ship_to_state      = 'ship_to_state',
            ship_to_zip        = '10001',
            state              = 'state',
            tax                = '1.00',
            zip                = '10001')
        self.assertEqual(result.success, True)

    def test_recurring_order(self):

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        result = self.conn.recurring_order_create(
            address            = 'address number',
            amount             = '2.00',
            card_code          = '1234',
            card_num           = '4111111111111111',
            city               = 'city',
            state              = 'state',
            zip                = '10002',
            country            = 'country',
            description        = 'description',
            email              = 'email@example.com',
            exp_date           = '0530',
            first_name         = 'first_name',
            last_name          = 'last_name',

            # recurring fields
            recurring_start       = u'%s' % tomorrow,
            recurring_period      = 'months',
            recurring_total_occurrences = 0,

        )
        self.assertEqual(result.success, True)
        recurring_id = result.recurring_id

        result = self.conn.recurring_order_update(
            recurring_id = recurring_id,
            address = 'my new address'
        )
        self.assertEqual(result.success, True)

        self.conn.recurring_order_cancel(
           recurring_id = recurring_id
        )
        self.assertEqual(result.success, True)



class OnlinePaymentAuthNetTest(unittest.TestCase):

    def setUp(self):
        self.conn = self._standard_connection()

    def _standard_connection(self, **kwargs):
        # note duplicate_window is ignored, as far as I can tell
        args = dict(auth=AUTHDOTNET_AUTH,
                    debug=DEBUG,
                    extra={'duplicate_window':-1})
        args.update(kwargs)
        return OnlinePayment('authnet', **args)

    def test_connect(self):
        self.assert_(isinstance(self.conn, AuthNetConnection))

        result = self.conn.authorize(amount='2.01',
                                     invoice_num=self._get_invoice_num(),
                                     card_num=self._get_card(),
                                     exp_date='0530')

        self.assertEquals(result.success, True)

    def test_sale(self):
        result = self.conn.sale(amount='2.02',
                                card_num=self._get_card(),
                                invoice_num=self._get_invoice_num(),
                                exp_date='0630')
        self.assertEqual(result.success, True)

    def test_extra(self):
        try:
            result = self.conn.sale(amount='2.03',
                                    card_num=self._get_card(),
                                    invoice_num=self._get_invoice_num(),
                                    exp_date='0730')
            self.assertEqual(result.success, True)
        except self.conn.DuplicateTransaction as e:
            warn("%r" % e.result.orig)

    def test_credit(self):
        result = self.conn.sale(amount='2.04',
                                card_num=self._get_card(),
                                invoice_num=self._get_invoice_num(),
                                exp_date='0820')

        self.assertEqual(result.success, True)

        # it would be nice to test a successful credit, but apparently
        # that's not possible - all test credits fail because there's
        # no settlement in test-land.
        try:
            credit_result = self.conn.credit(trans_id=result.trans_id,
                                             amount='2.05',
                                             card_num=self._get_card(),
                                             invoice_num=self._get_invoice_num(),
                                             exp_date='0930')
        except self.conn.ProcessorException as e:
            self.assertEqual(e.code, 54)
        else:
            self.fail("Didn't get exception as expected!")

    def test_void(self):
        card = self._get_card()
        result = self.conn.sale(amount='2.06',
                                card_num=card,
                                invoice_num=self._get_invoice_num(),
                                exp_date='1030')
        self.assertEqual(result.success, True)
        void_result = self.conn.void(trans_id=result.trans_id,
                                     amount='2.06',
                                     card_num=card,
                                     invoice_num=self._get_invoice_num(),
                                     exp_date='1130')
        self.assertEqual(void_result.success, True)

    def test_bad_auth(self):
        conn = self._standard_connection(auth={'login': 'foo', 'key': 'bar'})
        try:
            conn.sale(amount='2.07',
                      card_num='4007000000026',
                      exp_date='1230')
        except conn.AuthError:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_bad_cc(self):
        try:
            self.conn.sale(amount='2.08',
                           card_num='4007000000026',
                           exp_date='1229')
        except self.conn.CardNumberInvalid:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_bad_exp(self):
        try:
            self.conn.sale(amount='2.09',
                           card_num='4007000000027',
                           exp_date='aabb')
        except self.conn.CardExpirationInvalid:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_expired(self):
        try:
            self.conn.sale(amount='2.10',
                           card_num='4007000000027',
                           exp_date='0101')
        except self.conn.CardExpired:
            pass
        else:
            self.fail("Expected exception not caught!")

    def test_bad_amount(self):
        try:
            self.conn.sale(amount='foooo',
                           card_num='4007000000027',
                           exp_date='0215')
        except self.conn.AmountInvalid:
            pass
        except self.conn.ProcessorException as e:
            print "Auth.net is still returning the wrong error for bad amounts!"
        else:
            self.fail("Expected exception not caught!")

    def test_amount_too_high(self):
        try:
            self.conn.sale(amount='9999999.00',
                           card_num='4007000000027',
                           exp_date='0315')
        except self.conn.AmountTooHigh:
            pass
        else:
            self.fail("Expected exception not caught!")

    # this test isn't as good as the others - it doesn't prove that
    # the mapping of code to exception makes sense.  But it is the
    # only way to test codes that don't have another way to stimulate,
    # like AVS failures and "come back later" error codes.
    def test_all_codes(self):
        for code, exception in self.conn.CODE_MAP.items():
            # The ARB codes are non-numeric and don't work here
            if not isinstance(code,int):
                continue 
            try:
                # special auth.net test card that generates
                # amount-driven errors
                self.conn.sale(amount='%d.00' % code,
                               card_num='4222222222222',
                               exp_date='0415')
            except exception:
                pass
            except self.conn.ProcessorException as e:
                self.fail("Caught wrong exception for %d" % code)
            else:
                self.fail("Failed to generate exception for %d" % code)

    # try a test that sets (almost) all valid params
    def test_all_params(self):
        result = self.conn.sale(
            address            = 'address',
            amount             = '2.12',
            card_code          = '1234',
            card_num           = self._get_card(),
            city               = 'city',
            company            = 'company',
            country            = 'country',
            description        = 'description',
            email              = 'email@example.com',
            exp_date           = '0515',
            first_name         = 'first_name',
            invoice_num        = self._get_invoice_num(),
            last_name          = 'last_name',
            phone              = 'phone',
            ship_to_address    = 'ship_to_address',
            ship_to_company    = 'ship_to_company',
            ship_to_country    = 'ship_to_country',
            ship_to_city       = 'ship_to_city',
            ship_to_first_name = 'ship_to_first_name',
            ship_to_last_name  = 'ship_to_last_name',
            ship_to_state      = 'ship_to_state',
            ship_to_zip        = '10001',
            state              = 'state',
            tax                = '1.00',
            zip                = '10001'
            )
        self.assertEqual(result.success, True)

    def test_recurring_order(self):

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        recurring_id = None

        try:
            result = self.conn.recurring_order_create(
                address            = 'address',
                amount             = '2.00',
                card_code          = '1234',
                card_num           = self._get_card(),
                city               = 'city',
                state              = 'state',
                zip                = '10001',
                country            = 'country',
                description        = 'description',
                email              = 'email@example.com',
                exp_date           = '0529',
                first_name         = 'first_name',
                last_name          = 'last_name',

                # recurring fields
                recurring_start        = u'%s' % tomorrow,
                recurring_period       = 'months',
                recurring_total_occurrences  = 0,
            )
            self.assertEqual(result.success, True)
            recurring_id = result.recurring_id
        except self.conn.ProcessorException, e:
            if hasattr(e, 'code') and e.code == 'E00012':
                (recurring_id,) = \
                    re.findall(r'a duplicate of Subscription (\d+)', e.msg)
            else:
                raise e

        self.assertNotEqual(recurring_id, None)

        result = self.conn.recurring_order_update(
            recurring_id = recurring_id,
            address = '%i Millisecond Blvd' % (time.mktime(time.gmtime()),),
        )
        self.assertEqual(result.success, True)

        self.conn.recurring_order_cancel(
           recurring_id = recurring_id
        )
        self.assertEqual(result.success, True)

    # auth.net's duplicate detection has gone from crazy to totally
    # busted - the only way I've found to avoid it is by switching
    # card numbers.  Differing amounts, names, cust_ids don't help and
    # duplicate_window is being ignored.
    TEST_CARDS = ['5555555555554444',
                  '5105105105105100',
                  '4111111111111111',
                  '4012888888881881',
                  # '4222222222222',
                  '378282246310005',
                  '371449635398431',
                  '378734493671000',
                  '6011111111111117',
                  '6011000990139424']
    NEXT_CARD = 0

    LAST_INVOICE_NUM = random.randint(0,1000000000)

    def _get_card(self):
        card = self.TEST_CARDS[self.NEXT_CARD]
        self.NEXT_CARD = (self.NEXT_CARD + 1) % len(self.TEST_CARDS)
        return card

    def _get_invoice_num(self):
        self.LAST_INVOICE_NUM += 1
        return self.LAST_INVOICE_NUM

if __name__ == "__main__":
    unittest.main(argv=['', '-v'])
