# Copyright 2017 Intel Corporation
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
# ------------------------------------------------------------------------------

from sawtooth_processor_test.message_factory import MessageFactory


class IpfwMessageFactory:
    def __init__(self, signer=None):
        self._factory = MessageFactory(
            family_name="ipfw",
            family_version="1.0",
            namespace=MessageFactory.sha512("ipfw".encode("utf-8"))[0:6],
            signer=signer)

    def _num_to_address(self, num):
        return self._factory.namespace + \
            self._factory.sha512(num.encode())[0:64]

    def create_tp_register(self):
        return self._factory.create_tp_register()

    def create_tp_response(self, status):
        return self._factory.create_tp_response(status)

    def _create_txn(self, txn_function, num, action, rule):
        payload = ",".join([
            str(num), str(action), str(rule), "add"
        ]).encode()

        addresses = [self._num_to_address(num)]

        return txn_function(payload, addresses, addresses, [])

    def create_tp_process_request(self, action, num, rule):
        txn_function = self._factory.create_tp_process_request
        return self._create_txn(txn_function, num, action, rule)

    def create_transaction(self, num, action, rule):
        txn_function = self._factory.create_transaction
        return self._create_txn(txn_function, num, action, rule)

    def create_get_request(self, num):
        addresses = [self._num_to_address(num)]
        return self._factory.create_get_request(addresses)

    def create_get_response(
        self, num, action, rule
    ):
        address = self._num_to_address(num)

        data = None
        if action is not None:
            data = ",".join([num, action, rule, "add"]).encode()
        else:
            data = None

        return self._factory.create_get_response({address: data})

    def create_set_request(
        self, num, action, rule
    ):
        address = self._num_to_address(num)

        data = None
        if rule is not None:
            data = ",".join([num, action, rule, "add"]).encode()
        else:
            data = None

        return self._factory.create_set_request({address: data})

    def create_set_response(self, num):
        addresses = [self._num_to_address(num)]
        return self._factory.create_set_response(addresses)

    def get_public_key(self):
        return self._factory.get_public_key()
