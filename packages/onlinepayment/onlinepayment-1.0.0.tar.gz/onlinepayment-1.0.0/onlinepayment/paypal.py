"""

onlinepayment payflowpro connection class - see README.txt for usage
docs

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
from payflowpro.classes import (CreditCard, Amount, Profile, 
                                Address, Tracking, Response,
                                CustomerInfo, ShippingAddress,
                                PurchaseInfo, ProfileResponse,
                                RecurringPayments)
from payflowpro.client import (PayflowProClient, find_classes_in_list,
                               find_class_in_list)

import logging
import re
import pytz

from datetime   import datetime
from base       import (OnlinePaymentBase, OnlinePaymentResult, 
                        OnlinePaymentRecurringResult, 
                        OnlinePaymentRecurringPayment,
                        OnlinePaymentRecurringProfile)
from exceptions import InvalidAuthException

class PayPalConnection (OnlinePaymentBase):
    # map codes to exceptions - tuples denote ranges
    CODE_MAP = OnlinePaymentBase._explode_map({
        1         : OnlinePaymentBase.AuthError,
        2         : OnlinePaymentBase.InvalidCardType,
        4         : OnlinePaymentBase.AmountInvalid,
        12        : OnlinePaymentBase.TransactionDeclined,
        23        : OnlinePaymentBase.CardNumberInvalid,
        24        : OnlinePaymentBase.CardExpirationInvalid,
        26        : OnlinePaymentBase.AuthError,
        30        : OnlinePaymentBase.DuplicateTransaction,
        33        : OnlinePaymentBase.RecurringOrderDoesNotExist,
        50        : OnlinePaymentBase.TransactionDeclined,
        51        : OnlinePaymentBase.AmountTooHigh,
        102       : OnlinePaymentBase.TryAgainLater,
        106       : OnlinePaymentBase.TryAgainLater,
        112       : OnlinePaymentBase.AVSFailure,
        114       : OnlinePaymentBase.CCVInvalid,
        (125,128) : OnlinePaymentBase.FraudCheckFailed,
    })

    TRANS_STATES = {
          1: 'error',
          6: 'settlement pending',
          7: 'settlement in progress',
          8: 'settlement completed/successfully',
          11: 'settlement failed',
          14: 'settlement incomplete',
    }

    FIELD_MAP = {
        'card_num'           : 'acct',
        'card_code'          : 'cvv2',
        'exp_date'           : 'expdate',
        'amount'             : 'amt',
        'address'            : 'street',
        'company'            : 'companyname',
        'description'        : 'comment1',
        'ship_to_address'    : 'shiptostreet',
        'ship_to_first_name' : 'shiptofirstname',
        'ship_to_last_name'  : 'shiptolastname',
        'ship_to_country'    : 'shiptocountry',
        'ship_to_city'       : 'shiptocity',
        'ship_to_state'      : 'shiptostate',
        'ship_to_zip'        : 'shiptozip',
        'first_name'         : 'firstname',
        'last_name'          : 'lastname',
        'phone'              : 'phonenum',
        'invoice_num'        : 'ponum',

        # recurring fields
        'recurring_id'    : 'profile_id',
        'recurring_start'       : 'start',
        'recurring_period'      : 'payperiod',
        'recurring_total_occurrences' : 'term',
    }

    RECURRING_FIELD_MAPPING = {
        'AMT'             : 'amount',
        'START'           : 'start',
        'NEXTPAYMENT'     : 'next',
        'AGGREGATEAMT'    : 'total',
        'NUMFAILPAYMENTS' : 'failed_payments'
    }

    PAY_PERIOD_MAPPING = {
        'months': 'MONT',
        'weeks' : 'WEEK',
    }

    REVERSE_PAY_PERIOD_MAPPING = dict(
        (v,k) for (k,v) in PAY_PERIOD_MAPPING.items())

    def __init__(self, **kwargs):
        super(PayPalConnection, self).__init__(**kwargs)

        if not self.debug:
            logging.getLogger('payflow_pro').setLevel(logging.WARNING)


        url_base = PayflowProClient.URL_BASE_TEST if self.test_mode \
                   else PayflowProClient.URL_BASE_LIVE
        self.cc = PayflowProClient(url_base=url_base, **self.auth)

    def validate_auth(self, auth):
        for key in ("partner", "vendor", "username", "password"):
            if not key in auth:
                raise InvalidAuthException("Missing required '%s' parameter."\
                                           % key)

    def authorize(self, **kwargs):
        (card, amount, extras) = self._process_params(kwargs)

        sale_result = self.cc.authorization(card, amount, extras=extras)
        result = self._munge_result(sale_result)
        
        self._handle_errors(result)

        return result

    def capture(self, **kwargs):
        trans_id = kwargs['trans_id']
        del(kwargs['trans_id'])

        # card and amount aren't really used here
        (card, amount, extras) = self._process_params(kwargs)

        sale_result = self.cc.capture(trans_id, extras=extras)
        result = self._munge_result(sale_result)
        
        self._handle_errors(result)

        return result


    def sale(self, **kwargs):
        (card, amount, extras) = self._process_params(kwargs)

        sale_result = self.cc.sale(card, amount, extras=extras)
        result = self._munge_result(sale_result)
        
        self._handle_errors(result)

        return result

    def void(self, **kwargs):
        trans_id = kwargs['trans_id']
        del(kwargs['trans_id'])

        # card and amount aren't really used here
        (card, amount, extras) = self._process_params(kwargs)

        void_result = self.cc.void(trans_id, extras=extras)
        result = self._munge_result(void_result)
        
        self._handle_errors(result)

        return result

    def credit(self, **kwargs):
        trans_id = kwargs['trans_id']
        del(kwargs['trans_id'])

        # card and amount aren't really used here
        (card, amount, extras) = self._process_params(kwargs)

        credit_result = self.cc.credit_referenced(trans_id, extras=extras)
        result = self._munge_result(credit_result)
        
        self._handle_errors(result)

        return result

    def inquiry(self, **kwargs):
        trans_id = kwargs['trans_id']
        del(kwargs['trans_id'])

        inquiry_result = self.cc.inquiry(original_pnref=trans_id)
        result = self._munge_result(inquiry_result)

        self._handle_errors(result)

        return result


    def recurring_order_create(self, **kwargs):

        (card, amount, extras) = self._process_params(kwargs)
        (profile,) = find_classes_in_list(Profile, extras)

        result = self.cc.profile_add(profile, card, amount, extras=extras)
        result = self._munge_result(result)

        self._handle_errors(result)

        logging.debug('result = %s' % (result,))

        return result

    def recurring_order_update(self, **kwargs):
        profile_id = kwargs['recurring_id']
        del(kwargs['recurring_id'])

        (card, amount, extras) = self._process_params(kwargs)

        # everything is an extra for update
        extras.append(amount)
        extras.append(card)

        result = self.cc.profile_modify(profile_id, extras=extras)
        result = self._munge_result(result)

        self._handle_errors(result)

        return result


    def recurring_order_cancel(self, **kwargs):
        profile_id = kwargs['recurring_id']
        del(kwargs['recurring_id'])

        result = self.cc.profile_cancel(profile_id)
        result = self._munge_result(result)

        self._handle_errors(result)

        return result

    def recurring_order_payments(self, **kwargs):
        profile_id = kwargs['recurring_id']
        del(kwargs['recurring_id'])

        payment_history_only = kwargs.get('payment_history_only', True)

        result = self.cc.profile_inquiry(
            profile_id, payment_history_only=payment_history_only)
        result = self._munge_result(result)

        self._handle_errors(result)

        return result

    def recurring_order_inquiry(self, **kwargs):
        return \
            self.recurring_order_payments(payment_history_only=False, **kwargs)

    # override process params to build payflow objects after mapping names
    def _process_params(self, kwargs):
        # check and process params
        kwargs = super(PayPalConnection, self)._process_params(kwargs)

        card = self._build_card(kwargs)
        amount = self._build_amount(kwargs)
        extras = self._build_extras(kwargs)

        # if there's anything left in kwargs it's not getting to
        # paypal, so log a warning.  I'm tempted to make this fatal,
        # but I imagine in many cases it's not such a big deal - just
        # a trivial extra field that would be accepted by another
        # processor that's not applicable to paypal.
        if len(kwargs):
            self.log.warning("Extra parameters found: %s" % ','.join(kwargs))

        return (card, amount, extras)

    # Code to build the objects the payflow pro lib uses, only to
    # flatten them again later.  Yeesh.
    def _build_card(self, param):
        return CreditCard(acct    = param.pop('acct', ''),
                          expdate = param.pop('expdate', ''),
                          cvv2    = param.pop('cvv2', ''))

    def _build_amount(self, param):
        return Amount(amt      = param.pop('amt', ''),
                      currency = param.pop('currency', 'USD'),
                      taxamt   = param.pop('tax',''))


    def _build_extras(self, param):
        extras = []

        extras.append(self._build_address(param))
        extras.append(self._build_tracking(param))
        extras.append(self._build_shipping_address(param))
        extras.append(self._build_cust_info(param))
        extras.append(self._build_purchase_info(param))
        extras.append(self._build_recurring_info(param))

        return extras

    def _build_recurring_info(self, param):
        
        start = '%s' % param.pop('start', '')
        if re.match(r'\d{4}-\d{2}-\d{2}', start):
            start = re.sub(r'^(\d{4})-(\d{2})-(\d{2})', r'\2\3\1', start)

        profilename = param.pop('profilename', '')
        if not profilename:
            profilename = 'Default Profile Name'

        term = param.pop('term', '0') # default to forever

        payperiod = param.pop('payperiod', 'MONT')
        if payperiod in self.PAY_PERIOD_MAPPING:
            payperiod = self.PAY_PERIOD_MAPPING[payperiod]

        # For some reason having a blank desc is an error.  And it's
        # only an error on the live server, of course.
        desc = param.pop('desc', '')
        if not len(desc):
            desc = "unused"

        return Profile(
            profilename             = profilename,
            start                   = start,
            term                    = term,
            payperiod               = payperiod,
            maxfailpayments         = param.pop('maxfailpayments', ''),
            desc                    = desc,
            optionaltrx             = param.pop('optionaltrx', ''),
            optionaltrxamt          = param.pop('optionaltrxamt', ''),
            status                  = param.pop('status', ''),
            paymentsleft            = param.pop('paymentsleft', ''),
            nextpayment             = param.pop('nextpayment', ''),
            end                     = param.pop('end', ''),
            numfailpayments         = param.pop('numfailpayments', ''),
            retrynumdays            = param.pop('retrynumdays', ''),
            aggregateamt            = param.pop('aggregateamt', ''),
            aggregateoptionalamt    = param.pop('aggregateoptionalamt', ''))

    def _build_address(self, param):
        return Address(street      = param.pop('street', ''),
                       zip         = param.pop('zip', ''),
                       city        = param.pop('city', ''),
                       state       = param.pop('state', ''),
                       country     = param.pop('country', ''),
                       companyname = param.pop('companyname', ''))

    def _build_tracking(self, param):
        return Tracking(comment1   = param.pop('comment1',''),
                        comment2   = param.pop('comment2',''),
                        verbosity  = param.pop('verbosity',''))

    def _build_shipping_address(self, param):
        return ShippingAddress(
            shiptostreet           = param.pop('shiptostreet',''),
            shiptocity             = param.pop('shiptocity',''),
            shiptofirstname        = param.pop('shiptofirstname',''),
            shiptomiddlename       = param.pop('shiptomiddlename',''),
            shiptolastname         = param.pop('shiptolastname',''),
            shiptostate            = param.pop('shiptostate',''),
            shiptocountry          = param.pop('shiptocountry',''),
            shiptozip              = param.pop('shiptozip',''))
           
    def _build_cust_info(self, param):
        return CustomerInfo(
            custcode               = param.pop('custcode',''),
            email                  = param.pop('email',''),
            firstname              = param.pop('firstname',''),
            name                   = param.pop('name',''),
            middlename             = param.pop('middlename',''),
            lastname               = param.pop('lastname',''),
            phonenum               = param.pop('phonenum',''))

    def _build_purchase_info(self, param):
        return PurchaseInfo(
            ponum                  = param.pop('ponum',''))

    def _parse_transaction_time(self, ts):
        # '24-Nov-09  04:33 AM'
        parsed  = datetime.strptime(ts, '%d-%b-%y  %I:%M %p')
        pacific = pytz.timezone('America/Los_Angeles')
        return pacific.localize(parsed).astimezone(pytz.utc)
        # return datetime(utc.year, utc.month, utc.day, utc.hour, utc.second)

    def _build_recurring_payment(self, payment):
        return OnlinePaymentRecurringPayment(
            trans_id        = payment.p_pnref,
            amount          = payment.p_amt,
            trans_timestamp = self._parse_transaction_time(payment.p_transtime),
            success         = payment.p_result == '0',
            original        = payment,
        )

    def _munge_result(self, orig):

        (response,) = find_classes_in_list([Response],orig[0])
        if (self.debug):
            self.log.debug("Result: %s" % repr(response.__dict__))

        result = {}

        result['code']     = int(response.result)
        result['message']  = response.respmsg
        result['success']  = True if result['code'] == 0 else False
        result['trans_id'] = response.pnref
        result['orig']     = response

        # recurring response of some kind
        (profile_response,) = find_classes_in_list([ProfileResponse], orig[0])
        if profile_response:
            return self._munge_recurring_result(profile_response, result, orig)

        return OnlinePaymentResult(**result)

    def _munge_recurring_result(self, profile_response, result, orig):

        result['trans_id'] = profile_response.rpref
        if hasattr(profile_response, 'profileid'):
            result['recurring_id'] = profile_response.profileid
        else:
            result['recurring_id'] = None

        # Profile, means a profile status request?
        (profile,) = find_classes_in_list([Profile], orig[0])
        if profile:
            payperiod = self.REVERSE_PAY_PERIOD_MAPPING.get(
                           profile.payperiod, profile.payperiod)
            result['profile'] = OnlinePaymentRecurringProfile(
                recurring_id  = profile_response.profileid,
                payperiod           = payperiod,
                status              = profile.status,
                start               = profile.start,
                next                = profile.nextpayment,
                amount              = '', # profile.amt does not exist, amount not included!?
                total               = profile.aggregateamt,
                failed_payments     = profile.numfailpayments,
                orig                = profile
            )

        # RecurringPayments, means we've got a payment history
        (profile_payments,) = find_classes_in_list([RecurringPayments], orig[0])
        if profile_payments:
            result['payments'] = [ self._build_recurring_payment(p) 
                                   for p in profile_payments.payments ]

        return OnlinePaymentRecurringResult(**result)
