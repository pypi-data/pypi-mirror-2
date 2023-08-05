"""

onlinepayment exceptions - see README.txt for usage docs

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
class ServiceNotAvailable (Exception):
    pass

class InvalidTransactionField (Exception):
    pass

class InvalidAuthException (Exception):
    pass

class ProcessorException(Exception):
    """ Generic processor exception """
    def __init__(self, result):
        self.result = result
        self.code   = result.code
        self.msg    = result.message

    def __str__(self):
        return "onlinepayment.ProcessorException(code='%s', msg='%s')" % \
               (self.code, self.msg)

    def description(self):
        """ returns a description of the error suitable for display to
        an end-user."""
        return "%s (%s)" % (self.msg, self.code)
    
def new_processor_exception_class(desc):
    """ dynamically create a sub-class of ProcessorException """
    class cls (ProcessorException):
        def description(self):
            """ returns a description of the error suitable for display to
            an end-user."""
            return desc
    return cls
