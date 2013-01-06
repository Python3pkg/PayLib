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

from paylib.paypal import core

class GetExpressCheckoutDetails( core.Request ):
    """Obtain information about an Express Checkout transaction."""
    
    def __init__( self, token ):
        
        if (token is None) or (len(token) != 20):
            raise ValueError( 'Invalid token argument' )
        
        self._nvp_response = None
        self._nvp_request = dict()
        self._nvp_request['METHOD'] = 'GetExpressCheckoutDetails'
        self._nvp_request['TOKEN'] = token
        
    
    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)
    
    def set_nvp_response( self, nvp_response ):
        if not isinstance( nvp_response, dict ):
            raise ValueError( 'nvp_response must be a <dict>.' )
        self._nvp_response = copy.deepcopy( nvp_response )
    
    def get_nvp_response( self ):
        return copy.deepcopy( self._nvp_response )
