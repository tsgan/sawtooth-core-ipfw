# Copyright 2018 Intel Corporation
#
# Modifications copyright (C) 2018 Ganbold Tsagaankhuu <ganbold@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import hashlib

from sawtooth_sdk.processor.exceptions import InternalError


IPFW_NAMESPACE = hashlib.sha512('ipfw'.encode("utf-8")).hexdigest()[0:6]


def _make_ipfw_address(num):
    return IPFW_NAMESPACE + \
        hashlib.sha512(num.encode('utf-8')).hexdigest()[:64]


class Ipfw(object):
    def __init__(self, num, action, rule, user_action):
        self.num = num
        self.action = action
        self.rule = rule
        self.user_action = user_action


class IpfwState(object):

    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.

        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context
        self._address_cache = {}

    def delete_ipfw(self, ipfw_num):
        """Delete the Ipfw rule ipfw_num from state.

        Args:
            ipfw_num (str): The rule number.

        Raises:
            KeyError: The Ipfw with ipfw_num does not exist.
        """

        ipfws = self._load_ipfws(ipfw_num=ipfw_num)

        del ipfws[ipfw_num]
        if ipfws:
            self._store_ipfw(ipfw_num, ipfws=ipfws)
        else:
            self._delete_ipfw(ipfw_num)

    def set_ipfw(self, ipfw_num, ipfw):
        """Store the ipfw in the validator state.

        Args:
            ipfw_num (str): The rule number.
            ipfw (Ipfw): The information specifying the current ipfw.
        """

        ipfws = self._load_ipfws(ipfw_num=ipfw_num)

        ipfws[ipfw_num] = ipfw

        self._store_ipfw(ipfw_num, ipfws=ipfws)

    def get_ipfw(self, ipfw_num):
        """Get the ipfw associated with ipfw_num.

        Args:
            ipfw_num (str): The rule number.

        Returns:
            (Ipfw): All the information specifying a ipfw.
        """

        return self._load_ipfws(ipfw_num=ipfw_num).get(ipfw_num)

    def _store_ipfw(self, ipfw_num, ipfws):
        address = _make_ipfw_address(ipfw_num)

        state_data = self._serialize(ipfws)

        self._address_cache[address] = state_data

        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    def _delete_ipfw(self, ipfw_num):
        address = _make_ipfw_address(ipfw_num)

        self._context.delete_state(
            [address],
            timeout=self.TIMEOUT)

        self._address_cache[address] = None

    def _load_ipfws(self, ipfw_num):
        address = _make_ipfw_address(ipfw_num)

        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_ipfws = self._address_cache[address]
                ipfws = self._deserialize(serialized_ipfws)
            else:
                ipfws = {}
        else:
            state_entries = self._context.get_state(
                [address],
                timeout=self.TIMEOUT)
            if state_entries:

                self._address_cache[address] = state_entries[0].data

                ipfws = self._deserialize(data=state_entries[0].data)

            else:
                self._address_cache[address] = None
                ipfws = {}

        return ipfws

    def _deserialize(self, data):
        """Take bytes stored in state and deserialize them into Python
        Ipfw objects.

        Args:
            data (bytes): The UTF-8 encoded string stored in state.

        Returns:
            (dict): ipfw rule number (str) keys, Ipfw values.
        """

        ipfws = {}
        try:
            for ipfw in data.decode().split("|"):
                num, action, rule, user_action = ipfw.split(",")

                ipfws[num] = Ipfw(num, action, rule, user_action)
        except ValueError:
            raise InternalError("Failed to deserialize ipfw data")

        return ipfws

    def _serialize(self, ipfws):
        """Takes a dict of ipfw objects and serializes them into bytes.

        Args:
            ipfws (dict): ipfw rule number (str) keys, Ipfw values.

        Returns:
            (bytes): The UTF-8 encoded string stored in state.
        """

        ipfw_strs = []
        for num, g in ipfws.items():
            ipfw_str = ",".join(
                [num, g.action, g.rule, g.user_action])
            ipfw_strs.append(ipfw_str)

        return "|".join(sorted(ipfw_strs)).encode()
