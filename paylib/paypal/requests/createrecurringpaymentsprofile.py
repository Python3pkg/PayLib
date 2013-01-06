# Copyright (C) 2012 Client Side Web <rutherford@clientsideweb.net>
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

class CreateRecurringPaymentsProfile(core.Request):
    """Creates a recurring payments profile (subscription)."""
    
    def __init__(self, token, payment, details):
        
        if (token is None) or (len(token) != 20):
            raise ValueError( 'Invalid token argument' )        
        if not isinstance(details, fields.ScheduleDetails):
            raise ValueError( 'Details must be an instance of class <ScheduleDetails>')
        
        self._nvp_response = None
        self._nvp_request = dict()
        self._nvp_request['METHOD'] = 'CreateRecurringPaymentsProfile'
        self._nvp_request['TOKEN'] = token
        
        nvp = copy.deepcopy( payment.get_nvp_request() )
        self._nvp_request.update( nvp )
        
        nvp = copy.deepcopy( details.get_nvp_request() )
        self._nvp_request.update( nvp )
        
    
    def set_recurring_payments_profile_details(self, details):
        if not isinstance(details, fields.RecurringPaymentsProfileDetails):
            raise ValueError('Details must be an instance of class <RecurringPaymentsProfileDetails>')
        nvp = copy.deepcopy( details.get_nvp_request() )
        self._nvp_request.update( nvp )
    
    def set_billing_period_details(self, details):
        if not isinstance(details, fields.BillingPeriodDetails):
            raise ValueError('Details must be an instance of class <BillingPeriodDetails>')
        nvp = copy.deepcopy( details.get_nvp_request() )
        self._nvp_request.update( nvp )
        
    def set_activation_details(self, details):
        if not isinstance(details, fields.ActivationDetails):
            raise ValueError('Details must be an instance of class <ActivationDetails>')
        nvp = copy.deepcopy( details.get_nvp_request() )
        self._nvp_request.update( nvp )
    
    def set_ship_to_address(self, address):
        if not isinstance(address, fields.ShipToAddress):
            raise ValueError('Address must be an instance of class <ShipToAddress>')
        nvp = copy.deepcopy( address.get_nvp_request() )
        self._nvp_request.update( nvp )
    
    def set_payer_information(self, payer):
        if not isinstance(payer, fields.PayerInformation):
            raise ValueError('Payer must be an instance of class <PayerInformation>')
        nvp = copy.deepcopy( payer.get_nvp_request() )
        self._nvp_request.update( nvp )
    
    def set_payer_name(self, name):
        if not isinstance(name, fields.PayerName):
            raise ValueError('Name must be an instance of class <PayerName>')
        nvp = copy.deepcopy( name.get_nvp_request() )
        self._nvp_request.update( nvp )
    
    def get_nvp_request( self ):
        return copy.deepcopy( self._nvp_request )
    
    def set_nvp_response( self, nvp_response ):
        if not isinstance( nvp_response, dict ):
            raise ValueError( 'nvp_response must be a <dict>.' )
        self._nvp_response = copy.deepcopy( nvp_response )
    
    def get_nvp_response( self ):
        return copy.deepcopy( self._nvp_response )
