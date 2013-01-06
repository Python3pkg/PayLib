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


from paylib.paypal import core

class GetBalance( core.Request ):
    """Obtain the available balance for a PayPal account."""

    def __init__( self ):
        self._nvp_response = None
        self._nvp_request = dict()
        self._nvp_request['METHOD'] = 'GetBalance'


    def set_all_currencies( self, all_currencies=False):
        self._nvp_request['RETURNALLCURRENCIES'] = '1' if all_currencies else '0'


    def get_nvp_request( self ):
        return copy.deepcopy(self._nvp_request)


    def set_nvp_response( self, nvp_response ):
        if not isinstance( nvp_response, dict ):
            raise ValueError( 'nvp_response must be a <dict>.' )
        self._nvp_response = copy.deepcopy( nvp_response )


    def get_nvp_response( self ):
        return copy.deepcopy( self._nvp_response )


    def __del__( self ):
        if self._nvp_response:
            del (self._nvp_response)

        if self._nvp_request:
            del ( self._nvp_request )
