"""

onlinepayment package - see README.txt for usage docs

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
from base     import OnlinePayment, register_service, SERVICES

# try loading supported services - need at least one to be functional
try:
    from authnet import AuthNetConnection
    register_service('authnet', AuthNetConnection)
except ImportError:
    pass

try:
    from paypal import PayPalConnection
    register_service('paypal', PayPalConnection)
except ImportError:
    pass

if len(SERVICES) == 0:
    raise Exception("No payment processing modules found.  You must install payflowpro and/or zc.authorizedotnet.  See http://python-onlinepayment.googlecode.com/svn/trunk/README.txt for details.")

