# Copyright 2016-2018 Intel Corporation
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

import logging

import os
import sys
import subprocess

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

from sawtooth_ipfw.processor.ipfw_payload import IpfwPayload
from sawtooth_ipfw.processor.ipfw_state import Ipfw
from sawtooth_ipfw.processor.ipfw_state import IpfwState
from sawtooth_ipfw.addressing.ipfw_addressing import addresser


LOGGER = logging.getLogger(__name__)


class IpfwTransactionHandler(TransactionHandler):

    @property
    def family_name(self):
        return 'ipfw'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [addresser.IPFW_NAMESPACE]

    def apply(self, transaction, context):

        header = transaction.header
        signer = header.signer_public_key

        ipfw_payload = IpfwPayload.from_bytes(transaction.payload)

        ipfw_state = IpfwState(context)

        if ipfw_payload.user_action == 'delete':
            ipfw = ipfw_state.get_ipfw(ipfw_payload.num)

            if ipfw is None:
                raise InvalidTransaction(
                    'Invalid action: ipfw rule does not exist')

            ipfw_state.delete_ipfw(ipfw_payload.num)
            _display("Deleted ipfw rule.".format(signer[:6]))
            _display(
                _ipfw_data_to_str(
                    ipfw.action,
                    ipfw.rule,
                    ipfw_payload.num))

#            cmd = "ipfw show | grep " + ipfw_payload.num + " | awk '{print $1}'"
#            cmd_out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#            output = cmd_out.communicate()[0]
#            output = output.decode("utf-8")
#            output = output.rstrip('\n')
#            if output == ipfw_payload.num:

#                cmd = 'ipfw ' + 'delete' + ' ' + ipfw_payload.num
#                command = cmd.split()
#                try:
#                    res = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
#                except subprocess.CalledProcessError as e:
#                    if e.output:
#                        print("Oops... " + e.output)
##                       sys.exit(e.returncode)
#                    else:
#                        _display("Error deleting ipfw rule".format(signer[:6]))

        elif ipfw_payload.user_action == 'add':

            if ipfw_state.get_ipfw(ipfw_payload.num) is not None:
                raise InvalidTransaction(
                    'Invalid action: ipfw already exists: {}'.format(
                        ipfw_payload.num))

            ipfw = Ipfw(num=ipfw_payload.num,
                        action=ipfw_payload.action,
                        rule=ipfw_payload.rule,
                        user_action=ipfw_payload.user_action)

            ipfw_state.set_ipfw(ipfw_payload.num, ipfw)
            _display("Added ipfw rule.".format(signer[:6]))
            _display(
                _ipfw_data_to_str(
                    ipfw.action,
                    ipfw.rule,
                    ipfw_payload.num))


#            cmd = "ipfw show | grep " + ipfw_payload.num + " | awk '{print $1}'"
#            cmd_out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
#            output = cmd_out.communicate()[0]
#            output = output.decode("utf-8")
#            output = output.rstrip('\n')
#            if output != ipfw_payload.num:

#                cmd = 'ipfw ' + 'add' + ' ' + ipfw_payload.num + ' ' + ipfw_payload.action + ' ' + ipfw_payload.rule
#                command = cmd.split()
#                try:
#                    res = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
#                except subprocess.CalledProcessError as e:
#                    if e.output:
#                        print("Oops... " + e.output)
##                       sys.exit(e.returncode)
#                    else:
#                        _display("Error adding ipfw rule".format(signer[:6]))

        else:
            raise InvalidTransaction('Unhandled action: {}'.format(
                ipfw_payload.action))


def _ipfw_data_to_str(action, ipfw_rule, num):
    out = ""
    out += "ipfw rule number: {}\n".format(num)
    out += "Action: {}\n".format(action)
    out += "Rule: {}\n".format(ipfw_rule)
    return out


def _display(msg):
    n = msg.count("\n")

    if n > 0:
        msg = msg.split("\n")
        length = max(len(line) for line in msg)
    else:
        length = len(msg)
        msg = [msg]

    # pylint: disable=logging-not-lazy
    LOGGER.debug("+" + (length + 2) * "-" + "+")
    for line in msg:
        LOGGER.debug("+ " + line.center(length) + " +")
    LOGGER.debug("+" + (length + 2) * "-" + "+")
