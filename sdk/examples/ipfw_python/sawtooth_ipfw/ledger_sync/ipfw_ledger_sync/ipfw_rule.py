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
# -----------------------------------------------------------------------------

import logging

import os
import sys
import subprocess

LOGGER = logging.getLogger(__name__)


class Ipfw_Rule(object):

    def add(self, num, action, rule):
        """Adds ipfw rule
        """

        # Check if such ipfw rule exist
        output = _get_ipfw_rule(num)
        if output != num:

            cmd = 'ipfw ' + 'add' + ' ' + num + ' ' + action + ' ' + rule
            command = cmd.split()
            try:
                res = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                if e.output:
                    print("Oops... " + e.output)
                else:
                    _display("Error adding ipfw rule".format(signer[:6]))

    def delete(self, num):
        """Delete ipfw rule
        """

        # Check if such ipfw rule exist
        output = _get_ipfw_rule(num)
        if output == num:

            cmd = 'ipfw ' + 'delete' + ' ' + num
            command = cmd.split()
            try:
                res = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                if e.output:
                    print("Oops... " + e.output)
                else:
                    _display("Error deleting ipfw rule".format(signer[:6]))


def _get_ipfw_rule(num):
    cmd = "ipfw show " + num + " | awk '{print $1}'"
    cmd_out = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = cmd_out.communicate()[0]
    output = output.decode("utf-8")
    output = output.rstrip('\n')

    return output


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

