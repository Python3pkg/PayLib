# Copyright (C) 2011 Luca Sepe <luca.sepe@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import copy


from paylib.paypal import core, fields

class DoExpressCheckoutPayment( core.Request ):
    """Obtain the available balance for a PayPal account."""

    def __init__( self, payment, token, payment_action, payer_id ):
        """payment    Should be the same as for SetExpressCheckout
        token    PayPal token
        payment_action How you want to obtain payment
        payerId    Unique PayPal customer account identification 
                number as returned by GetExpressCheckoutDetails response."""

        if not isinstance(payment, fields.Payment ):
            raise ValueError( 
                'payment must be an instance of class <Payment>.' )

        if (token is None) or (len(token) != 20):
            raise ValueError( 'Invalid token argument' )

        if payment_action not in ['Sale','Authorization','Order']:
            raise ValueError( 
                'payment_action must be Sale, Authorization or Order.' )

        if (payer_id is None) or (len(payer_id) != 13):
            raise ValueError( 'Invalid payer id' )

        self._nvp_response = dict()
        self._nvp_request = dict()
        self._nvp_request['METHOD'] = 'DoExpressCheckoutPayment'
        
        nvp = copy.deepcopy( payment.get_nvp_request() )
        self._nvp_request.update( nvp )
        self._nvp_request['TOKEN'] = token
        self._nvp_request['PAYMENTACTION'] = payment_action
        self._nvp_request['PAYERID'] = payer_id


    def set_return_fmf( self, fmf ):
        """Flag to indicate whether you want the results returned 
        by Fraud Management Filters. By default this is false."""
        self._nvp_request['RETURNFMFDETAILS'] = '1' if fmf else '0'


    def set_user_selected_options( self, user_options ):
        """Sets user selected options."""
        if not isinstance(user_options, fields.UserSelectedOptions):
            raise ValueError( 
                'user_options must be an instance of class <UserSelectedOptions>.' )

        nvp = copy.deepcopy( user_options.get_nvp_request() )
        self._nvp_request.update( nvp )

        
    def set_address( self, address ):
        """Sets address fields."""
        if not isinstance(address, fields.Address):
            raise ValueError( 
                'address must be an instance of class <Address>.' )

        nvp = copy.deepcopy( address.get_nvp_request() )
        self._nvp_request.update( nvp )

    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)


    def set_nvp_response( self, nvp_response ):
        if not isinstance( nvp_response, dict ):
            raise ValueError( 'nvp_response must be a <dict>.' )
        self._nvp_response = copy.deepcopy( nvp_response )


    def get_nvp_response( self ):
        return copy.deepcopy( self._nvp_response )
