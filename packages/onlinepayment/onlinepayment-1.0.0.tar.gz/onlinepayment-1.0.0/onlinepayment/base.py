"""

onlinepayment base classes - see README.txt for usage docs

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
import logging
from warnings    import warn
from exceptions  import new_processor_exception_class as _e, \
                        ServiceNotAvailable, ProcessorException, \
                        InvalidTransactionField
from types       import ClassType
from collections import namedtuple

SERVICES = {}
def register_service(key, service_cls):
    SERVICES[key] = service_cls

def OnlinePayment (service, **kwargs):
    """ dispatch to the requested service """
    if (service in SERVICES):
        return SERVICES[service](**kwargs)
    else:
        raise ServiceNotAvailble

class OnlinePaymentResult():

    def __init__(self, code, success, orig, message='', trans_id=None):
        self.code = code
        self.message = message
        self.success = success
        self.orig = orig
        self.trans_id = trans_id

class OnlinePaymentRecurringResult(OnlinePaymentResult):

    def __init__(self, recurring_id, profile=None, payments=[], **kwargs):
        OnlinePaymentResult.__init__(self, **kwargs)
        self.recurring_id = recurring_id
        self.payments     = payments
        self.profile      = profile

OnlinePaymentRecurringPayment = \
        namedtuple('OnlinePaymentRecurringPayment',
                   'trans_id amount trans_timestamp success original')

OnlinePaymentRecurringProfile = \
        namedtuple('OnlinePaymentRecurringProfile',
                   'recurring_id payperiod status start next amount total failed_payments orig')

class OnlinePaymentBase (object):
    # enumerate exceptions
    ProcessorException    = ProcessorException

    TransactionDeclined   = _e("The transaction was declined.")
    AuthError             = _e("An internal error occurred.")
    CardNumberInvalid     = _e("The credit card number you entered is invalid.")
    CardExpirationInvalid = _e("The credit card expiration date you entered is invalid.")
    CardExpired           = _e("The credit card you entered is expired.")
    DuplicateTransaction  = _e("A duplicate transaction was detected.")
    InvalidCardType       = _e("The payment processor does not support the type of credit card you entered.")
    TryAgainLater         = _e("Please try again later.")
    AmountInvalid         = _e("The amount you entered is invalid.")
    AVSFailure            = _e("The address you entered does not match the billing address on your account.")
    FraudCheckFailed      = _e("The transaction was declined due to a fraud check.")
    CCVInvalid            = _e("The credit card verification code you entered is invalid.")
    AmountTooHigh         = _e("The amount you entered is too high.")
    AcceptedForReview     = _e("The transaction has been held for review - it may still be processed later.")
    RecurringOrderDoesNotExist = _e("The recurring order does not exist or is not active.")

    # field names for parameter validation
    TRANSACTION_FIELDS = (
        'address',
        'amount',
        'card_code',
        'card_num',
        'city',
        'company',
        'country',
        'description',
        'email',
        'exp_date',
        'extra',
        'first_name',
        'invoice_num',
        'last_name',
        'phone',
        'ship_to_address',
        'ship_to_company',
        'ship_to_country',
        'ship_to_city',
        'ship_to_first_name',
        'ship_to_last_name',
        'ship_to_state',
        'ship_to_zip',
        'state',
        'tax',
        'trans_id',
        'zip',
        'recurring_start',
        'recurring_total_occurrences',
        'recurring_period',
        'recurring_interval_length', # auth.net only, no known equivalent
        'recurring_id',
        )

    def __init__(self, auth=None, extra=None, test_mode=True, debug=False):
        self.test_mode = test_mode
        self.auth = auth
        self.extra = extra
        self.debug = debug

        self.log = logging.getLogger('onlinepayment')
        self.log.setLevel(logging.DEBUG if self.debug else logging.WARNING)

        self.validate_auth(self.auth)

    def authorize(self, **kwargs):
        raise Exception("Please implement authorize() in %s" 
                        % self.__class__.__name__)

    def capture(self, **kwargs):
        raise Exception("Please implement capture() in %s" 
                        % self.__class__.__name__)

    def sale(self, **kwargs):
        raise Exception("Please implement sale() in %s" 
                        % self.__class__.__name__)

    def credit(self, **kwargs):
        raise Exception("Please implement credit() in %s" 
                        % self.__class__.__name__)

    def void(self, **kwargs):
        raise Exception("Please implement void() in %s" 
                        % self.__class__.__name__)

    def recurring_order_create(self, **kwargs):
        raise Exception("Please implement recurring_order_create in %s"
                        % self.__class__.__name__)

    def recurring_order_update(self, **kwargs):
        raise Exception("Please implement recurring_order_update in %s"
                        % self.__class__.__name__)

    def recurring_order_cancel(self, **kwargs):
        raise Exception("Please implement recurring_order_cancel in %s"
                        % self.__class__.__name__)

    @classmethod
    def _explode_map (cls, codes):
        """ explode_map is a utility method for sub-classes, takes a
        map with codes and treats the tuples as inclusive ranges.  For
        example:

           OnlinePaymentBase._explode_map({1: 'foo', (3, 5): 'bar'})

        Returns:

           {1: 'foo', 3: 'bar', 4: 'bar', 5: 'bar'}
        """    
        result = {}
        from types import TupleType
        for code, exception in codes.items():
            if isinstance(code, TupleType):
                for x in range(*code):
                    result[x] = exception
            else:
                result[code] = exception
        return result

    def _handle_errors(self,result):
        """ recognize errors by codes and produce exceptions """
        if result.code in self.CODE_MAP:
            raise self.CODE_MAP[result.code](result)

        # if we get this far and it's not a success then throw a
        # generic processor exception
        if not result.success:
            raise self.ProcessorException(result)

    def _process_params(self,params):
        """ validates params, applies FIELD_MAP to get
        processor-specific names and adds in extra fields, both object
        and method specified.

        A parameter extra_field_map can be used to extend FIELD_MAP
        for a single call. extra_field_map takes precedence over
        FIELD_MAP."""
        result = {}
        extra_field_map = params.pop('extra_field_map',{})

        for param,value in params.items():
            # check that it's a recoginzed value
            if not param in self.TRANSACTION_FIELDS:
                raise InvalidTransactionField(
                    "Unrecognized parameter '%s'." % param)

            # apply extra_field_map
            if param in extra_field_map:
                result[extra_field_map[param]] = value
            # apply FIELD_MAP
            elif param in self.FIELD_MAP:
                result[self.FIELD_MAP[param]] = value
            else:
                result[param] = value

        # mix in extra values
        if self.extra:
            result.update(self.extra)
        if 'extra' in result:
            result.update(result.pop('extra'))

        return result
