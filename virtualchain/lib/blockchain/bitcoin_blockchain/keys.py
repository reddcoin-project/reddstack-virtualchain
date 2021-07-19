#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Virtualchain
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org
    
    This file is part of Virtualchain
    
    Virtualchain is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Virtualchain is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Virtualchain.  If not, see <http://www.gnu.org/licenses/>.
"""

import pyreddcoin
import os

# depending on whether or not we're talking to 
# -testnet/-regtest or mainnet, determine which private
# and public key classes to use.

if os.environ.get("BLOCKSTACK_TESTNET", None) == "1":

    version_byte = 111

    # using testnet keys
    ReddcoinPrivateKey = pyreddcoin.ReddcoinTestnetPrivateKey
    ReddcoinPublicKey = pyreddcoin.ReddcoinTestnetPublicKey

    def hex_hash160_to_address( hexhash, version_byte=111 ):
        return pyreddcoin.hex_hash160_to_address( hexhash, version_byte=version_byte )

    def script_hex_to_address( script_hex, version_byte=111 ):
        return pyreddcoin.script_hex_to_address( script_hex, version_byte=version_byte )

    def get_private_key_obj(private_key):
        if isinstance(private_key, ReddcoinPrivateKey):
            return private_key
        else:
            return ReddcoinPrivateKey(private_key)

    def analyze_private_key(private_key, blockchain_client):
        private_key_obj = get_private_key_obj(private_key)
        # determine the address associated with the supplied private key
        from_address = private_key_obj.public_key().address() 
        # get the unspent outputs corresponding to the given address
        inputs = pyreddcoin.get_unspents(from_address, blockchain_client)
        # return the inputs
        return private_key_obj, from_address, inputs

else:

    version_byte = 61

    # using mainnet keys
    ReddcoinPrivateKey = pyreddcoin.BitcoinPrivateKey
    ReddcoinPublicKey = pyreddcoin.BitcoinPublicKey
    
    hex_hash160_to_address = pyreddcoin.hex_hash160_to_address
    script_hex_to_address = pyreddcoin.script_hex_to_address

    analyze_private_key = pyreddcoin.analyze_private_key

