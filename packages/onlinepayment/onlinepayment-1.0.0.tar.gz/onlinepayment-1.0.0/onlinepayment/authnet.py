"""

onlinepayment authorize.net connection class

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
from base import (OnlinePaymentBase, OnlinePaymentResult, 
                  OnlinePaymentRecurringResult)
from exceptions import InvalidAuthException
from zc.authorizedotnet.processing import CcProcessor
# http://bitbucket.org/adroll/authorize/
from authorize import arb

TEST_SERVER='test.authorize.net'
LIVE_SERVER='secure.authorize.net'


class AuthNetConnection (OnlinePaymentBase):
    # map codes to exceptions - tuples denote ranges
    CODE_MAP = OnlinePaymentBase._explode_map({
        2          : OnlinePaymentBase.TransactionDeclined,
        3          : OnlinePaymentBase.TransactionDeclined,
        4          : OnlinePaymentBase.TransactionDeclined,
        5          : OnlinePaymentBase.AmountInvalid,
        6          : OnlinePaymentBase.CardNumberInvalid,
        7          : OnlinePaymentBase.CardExpirationInvalid,
        8          : OnlinePaymentBase.CardExpired,
        11         : OnlinePaymentBase.DuplicateTransaction,
        13         : OnlinePaymentBase.AuthError,
        17         : OnlinePaymentBase.InvalidCardType,
        (19, 23)   : OnlinePaymentBase.TryAgainLater,
        (25, 26)   : OnlinePaymentBase.TryAgainLater,
        27         : OnlinePaymentBase.AVSFailure,
        28         : OnlinePaymentBase.InvalidCardType,
        37         : OnlinePaymentBase.CardNumberInvalid,
        41         : OnlinePaymentBase.FraudCheckFailed,
        (44, 45)   : OnlinePaymentBase.CCVInvalid,
        49         : OnlinePaymentBase.AmountTooHigh,
        (57, 63)   : OnlinePaymentBase.TryAgainLater,
        65         : OnlinePaymentBase.TransactionDeclined,
        78         : OnlinePaymentBase.CCVInvalid,
        251        : OnlinePaymentBase.FraudCheckFailed,
        (252, 253) : OnlinePaymentBase.AcceptedForReview,
        315        : OnlinePaymentBase.CardNumberInvalid,
        316        : OnlinePaymentBase.CardExpirationInvalid,
        317        : OnlinePaymentBase.CardExpired,
        318        : OnlinePaymentBase.DuplicateTransaction,
        'E00012'   : OnlinePaymentBase.DuplicateTransaction,
        'E00035'   : OnlinePaymentBase.RecurringOrderDoesNotExist,
    })

    # field map is empty for auth.net - API was based on auth.net so
    # all the names are the same
    FIELD_MAP = {
        'recurring_id'          : 'subscription_id',
        'recurring_start'             : 'start_date',
        'recurring_total_occurrences' : 'total_occurrences',
        'recurring_period'            : 'interval_unit',
        'recurring_interval_length'   : 'interval_length',
    }

    def __init__(self, **kwargs):
        super(AuthNetConnection, self).__init__(**kwargs)

        server = TEST_SERVER if self.test_mode else LIVE_SERVER
        self.cc = CcProcessor(server = server,
                              login  = self.auth['login'],
                              key    = self.auth['key'])

        self.arb = arb.Api(is_test = self.test_mode,
                           login   = u"%s" % self.auth['login'],
                           key     = u"%s" % self.auth['key'])

    def validate_auth(self, auth):
        if not "login" in auth:
            raise InvalidAuthException("Missing required 'login' parameter.")
        if not "key" in auth:
            raise InvalidAuthException("Missing required 'key' parameter.")

    def authorize(self, **kwargs):
        # check and process params
        kwargs = self._process_params(kwargs)

        # from warnings import warn
        # warn(self.cc.connection.formatRequest(kwargs))

        auth_result = self.cc.authorize(**kwargs)
        result = self._munge_result(auth_result)

        self._handle_errors(result)

        return result

    def capture(self, **kwargs):
        # check and process params
        kwargs = self._process_params(kwargs)

        cap_result = self.cc.captureAuthorized(**kwargs)
        result = self._munge_result(cap_result)

        self._handle_errors(result)

        return result

    def sale(self, **kwargs):
        # do this in two steps since zc.authdotnet doesn't have
        # AUTH_CAPTURE support yet - probably worth patching to fix
        result = self.authorize(**kwargs)
        self.capture(trans_id=result.orig.trans_id)

        return result

    def credit(self, **kwargs):
        # check and process params
        kwargs = self._process_params(kwargs)

        credit_result = self.cc.credit(**kwargs)
        result = self._munge_result(credit_result)

        self._handle_errors(result)

        return result

    def void(self, **kwargs):
        # check and process params
        kwargs = self._process_params(kwargs)

        void_result = self.cc.void(**kwargs)
        result = self._munge_result(void_result)

        self._handle_errors(result)

        return result

    def recurring_order_create(self, **kwargs):

        if ('recurring_total_occurrences' in kwargs and (
            kwargs['recurring_total_occurrences'] == 0 or 
            kwargs['recurring_total_occurrences'] == '0')):

            kwargs['recurring_total_occurrences'] = '9999'
                # authorize.net's "infinity"

        if 'recurring_interval_length' not in kwargs:
            kwargs['recurring_interval_length'] = 1

        return self._recurring_call(self.arb.create_subscription, **kwargs)

    def recurring_order_update(self, **kwargs):
        return self._recurring_call(self.arb.update_subscription, **kwargs)

    def recurring_order_cancel(self, **kwargs):
        return self._recurring_call(self.arb.cancel_subscription, **kwargs)

    def recurring_order_payments(self, **kwargs):
        raise Exception('Authorize.NET does not support querying a '
                        'recurring order for payment history. You '
                        'should complain to them too.')


    def _recurring_call(self, call, **kwargs):

        kwargs = self._convert_to_unicode(kwargs)
        kwargs['extra_field_map'] = {
            'exp_date'  : 'expiration_date',
            'card_num'  : 'card_number',
            'first_name': 'bill_first_name',
            'last_name' : 'bill_last_name',
            'company'   : 'bill_company',
            'address'   : 'bill_address',
            'city'      : 'bill_city',
            'state'     : 'bill_state',
            'zip'       : 'bill_zip',
            'country'   : 'bill_country',
        }

        kwargs = self._process_params(kwargs)

        if (self.debug):
            self.log.debug("Recurring Calling: %s" % repr(kwargs))

        result = call(**kwargs)
        result = self._recurring_munge_result(result)

        self._handle_errors(result)

        return result

    def _convert_to_unicode(self,params):
        result = {}
        for param,value in params.items():
            result[param] = u"%s" % value
        return result

    def _recurring_munge_result(self, orig):
        if (self.debug):
            self.log.debug("Recurring Result: %s" % repr(orig))

        result = {}

        response = orig['messages']

        # authorize has the worst XML parser *ever*
        result['code']      = u'%s' % response['message']['code']['text_']
        result['message']   = u'%s' % response['message']['text']['text_']
        result['orig']      = orig

        result_code = u'%s' % response['result_code']['text_']
        result['success']   = True if result_code == u'Ok' else False

        if 'subscription_id' in orig:
            result['recurring_id'] = orig['subscription_id']['text_']
        else:
            result['recurring_id'] = None

        result['trans_id'] = None

        if (self.debug):
            self.log.debug("Recurring Munged: %s" % repr(result))

        return OnlinePaymentRecurringResult(**result)

    def _munge_result(self,orig):
        if (self.debug):
            self.log.debug("Result: %s" % repr(orig.__dict__))

        result = {}

        result['code']     = int(orig.response_reason_code)
        result['message']  = orig.response_reason
        result['success']  = True if result['code'] == 1 else False
        result['trans_id'] = orig.trans_id
        result['orig']     = orig

        return OnlinePaymentResult(**result)
