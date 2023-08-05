onlinepayment - a generic Python API for making online payments
===============================================================

This module provides an API wrapper around a variety of payment
providers.  Using this module you can write code that will work the
same regardless of the payment provider in use.

Examples::

   from onlinepayment import OnlinePayment
   
   # connect to authorize.net, setup auth with login and key
   auth= { 'login': 'YOUR LOGIN HERE',
           'key':   'YOUR KEY HERE' }
  
   op = OnlinePayment('authnet', test_mode=True, auth=auth)
   
   # or for paypal, setup auth with user, pass, vendor and product:
   auth= { 'username': 'YOUR USERNAME HERE',
           'password': 'YOUR PASSWORD HERE',
           'vendor':   'YOUR VENDOR HERE',
           'product':  'YOUR PRODUCT HERE' } 
   
   # connect to PayPal
   op = OnlinePayment('paypal', test_mode=True, auth=auth)
   
   # charge a card
   try:
       result = op.sale(first_name = 'Joe',
                        last_name  = 'Example',
                        address    = '100 Example Ln.',
                        city       = 'Exampleville',
                        state      = 'NY',
                        zip        = '10001',
                        amount     = '2.00',
                        card_num   = '4007000000027',
                        exp_date   = '0530',
                        card_code  = '1234')
   
   except conn.TransactionDeclined:
      # do something when the transaction fails
   
   except conn.CardExpired:
      # tell the user their card is expired
   
   except conn.ProcessorException:
      # handle all other possible processor-generated exceptions generically
   
   # examine result, the values returned here are processor-specific
   success  = result.success
   code     = result.code
   message  = result.message
   trans_id = result.trans_id
   
   # you can get the raw data returned by the underlying processor too
   orig = result.orig

Installation
============

Before you can use this module you must install one or more payment
processors.  To install the PayPal payflowpro package::

  # easy_install pytz
  # easy_install python-payflowpro

To install the zc.authorizedotnet package and the authorize package
(for recurring support)::

  # easy_install zc.authorizedotnet
  # easy_install authorize

If you want authorize.net support you'll need to install a patched
version of zc.ssl.  Hopefully someday this will be released by the
Zope devs, but so far I haven't heard anything back.  Download the
zc.ssl source package from here::

  # http://pypi.python.org/pypi/zc.ssl/
  # tar zxvf zc.ssl-1.1.tar.gz
  # cd zc.ssl-1.1

Now download and apply my zc-ssl-timeout.patch::

  # wget http://python-onlinepayment.googlecode.com/svn/trunk/zc-ssl-timeout.patch
  # patch -p1 < /zc-ssl-timeout.patch

And install the patched module::

  # python setup.py install

(You may also need to edit setup.py and remove the
'ssl-for-setuptools' dependecy.  I did, although it may be a quirk of
my Python install rather than a general problem.)

Once you have a payment processor you can install this module:

  # easy_install onlinepayment

Connection Parameters
=====================

When creating a new connection the following named parameters are available::

  auth - required parameter containing connection-specific login info.

  debug - causes the connection classes to emit debugging info via
          logging calls.

  test_mode - sets the connection to test-mode.  The actual meaning is
              processor-specific but in all cases it should mean that
              no charges will actually happen.

Transaction Methods
===================

The following methods are available to initiate transactions:

sale([params]) 
--------------

Process a charge on a card immediately.

authorize([params])
-------------------

Requests authorization for a charge but does not process
it.  The result object will contain the trans_id needed to complete
the charge with capture.

capture(trans_id=XXXX, [params])
--------------------------------

Processes a previously authorized transaction.

void(trans_id=XXXX, [params])
-----------------------------

Voids a previous transaction.  In most cases this must be a recent
transaction which has not yet actually resulted in funds transfered.

credit(trans_id=XXXX, amount=XXXX, [params])
--------------------------------------------

Credits a previously charged amount of money back to the payer.

subscription_create(period=XXX, length=XXX, start=XXX, [params])
----------------------------------------------------------------

Creates a subscription that will charge the provided card on an ongoing basis.


subscription_update(subscription_id=XXX, [params])
---------------------------------------------------

Updates the settings for an existing subscription.

subscription_cancel(subscription_id=XXX)
-----------------------------------------

Cancels a subscription.

Transaction Parameters
======================

All transaction methods accept the same parameters, although not all
parameters may be applicable to every transaction type.  The actual
rules vary according to the processor, unfortunately.  The list of
parameters accepted is::

        address
        amount
        card_code
        card_num
        city
        company
        country
        description
        email
        exp_date
        extra
        first_name
        invoice_num
        last_name
        phone
        ship_to_address
        ship_to_company
        ship_to_country
        ship_to_city
        ship_to_first_name
        ship_to_last_name
        ship_to_state
        ship_to_zip
        state
        tax
        trans_id
        zip

In cases where these names do not match the names expected by the
processor a mapping is employed.  If you need to pass parameters that
have no equivalent above, you can pass them via the 'extra' parameter,
which accepts a dictionary of key-value pairs.  For example, to pass
in the special 'duplicate_window' parameter to authorize.net::

  op.sale(..., extra={'duplicate_window':0})

You can also set extra parameters when you create your OnlinePayment
object and they will be applied to all transaction methods called::

  op = OnlinePayment('authnet', auth=..., extra={'duplicate_window':0})

Results
=======

Successful transactions return an OnlinePaymentResults object.  This
object has the following attributes::

  success - true if the transaction succeeded

  code - the result code returned by the processor.

  message - the message returned by the processor.

  trans_id - the transaction ID returned by the processor (aka pnref
  for payflowpro).  This is the value you need to keep to be able to
  call capture(), void() or credit() later.

  orig - the raw data returned by the underlying connection library.
  You might need this for debugging purposes.

Unsuccessful transactions result in...

Exceptions
==========

When a transaction fails an exception will be raised.  The exception
classes are all attributes of the connection object, so you don't need
to import anything to reference them.

All exceptions raised during transaction processing are sub-classes of
ProcessorException, so if you want to just catch all possible errors
and handle them the same you can write::

  # authorize a charge
  try:
      result = op.authorize(amount='2.00',
                            cc_num='4007000000027',
                            cc_exp='0530')
  except op.ProcessorException:
      print("It didn't work and I don't care why.  Cry some more!")

The exception object contains information about why it failed, aside
from its type.  The attributes available are::

  code - the result code returned by the processor.

  msg - the message returned by the processor.

  result - the OnlinePaymentResult object which would have been
  returned if the request had succeed

You might use them to log the processor's code and message::

  # authorize a charge
  try:
      result = conn.authorize(amount='2.00',
                              cc_num='4007000000027',
                              cc_exp='0530')
  except conn.ProcessorException as e:
      log.warning("Processor returned code %d, message %s" % (e.code, e.msg))

In addition a method is available called description() which contains
something reasonable to display to an end user.  For example::

  except op.ProcessorException, e:
      print("Sorry, that didn't work.  %s" % e.description())

In the case of a CardExpired exception that would print::

  Sorry, that didn't work.  The credit card you entered is expired.

You can also catch and handle specific error conditions.  The
available classes are::

    AVSFailure           
    AcceptedForReview    
    AmountInvalid        
    AmountTooHigh        
    AuthError            
    CCVInvalid           
    CardExpirationInvalid
    CardExpired          
    CardNumberInvalid    
    DuplicateTransaction 
    FraudCheckFailed     
    InvalidCardType      
    TransactionDeclined  
    TryAgainLater        

Of course this isn't a complete list of all the errors any processor
could return.  I've taken the approach that it's most useful to
identify the errors that a user might reasonable be able to fix.  The
rest just end up as generic ProcessorException errors and you can
examine their code and message if you wish to differentiate.

Authorize.net
=============

The authorize.net connection class uses the zc.authorizedotnet
library. You can learn more about it here:

   http://pypi.python.org/pypi/zc.authorizedotnet/1.3

Since this module started with auth.net you'll find that the parameter
names are mostly the same.

This module performs the following mapping to express parameters in
Authorize.net language::

    'term'      : 'length',
    'payperiod' : 'unit',

Auth parameters should look like::

  auth= { 'login': 'YOUR LOGIN HERE',
          'key':   'YOUR KEY HERE' }

PayPal - aka PayFlowPro
=======================

The paypal connection class uses the payflowpro library.  The project is here:

   http://code.google.com/p/python-payflowpro/

This module performs the following mapping to express parameters in
payflowpro language::

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

If you need to set any parameters not in this set just use the 'extra'
parameter described above.

Note that the payflowpro API only uses trans_id for credit(), void()
and capture().  You can pass other values but they are ignored.

Auth parameter setup should look like::

  auth= { 'username': 'YOUR USERNAME HERE',
          'password': 'YOUR PASSWORD HERE',
          'vendor':   'YOUR VENDOR HERE',
          'product':  'YOUR PRODUCT HERE' } 

Credits
=======

- Sam Tregar - framework, one-time processing

- Aaron Ross - recurring billing

- We Also Walk Dogs - maintainance, bug fixes, morale boost

- Jason Kohles - created Business::OnlinePayment, the model for this module

Copyright and License
=====================

Copyright (c) 2009, 2010, We Also Walk Dogs
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
