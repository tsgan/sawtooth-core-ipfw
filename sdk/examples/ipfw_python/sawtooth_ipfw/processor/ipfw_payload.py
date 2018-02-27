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

from sawtooth_sdk.processor.exceptions import InvalidTransaction


class IpfwPayload(object):

    def __init__(self, payload):
        try:
            # The payload is csv utf-8 encoded string
            num, action, rule, user_action = payload.decode().split(",")
        except ValueError:
            raise InvalidTransaction("Invalid payload serialization")

        if not num:
            raise InvalidTransaction('Rule number is required')

        if '|' in num:
            raise InvalidTransaction('Rule number cannot contain "|"')

        if not user_action:
            raise InvalidTransaction('User action is required')

        if not action and user_action == 'add':
            raise InvalidTransaction('Action is required')

        if user_action == 'add' and action not in ('allow', 'accept', 'pass', 'permit', 'deny', 'drop'):
            raise InvalidTransaction('Invalid action: {}'.format(action))

        if user_action == 'add' and not rule:
            raise InvalidTransaction('Rule is required')



        self._num = num
        self._action = action
        self._rule = rule
        self._user_action = user_action

    @staticmethod
    def from_bytes(payload):
        return IpfwPayload(payload=payload)

    @property
    def num(self):
        return self._num

    @property
    def action(self):
        return self._action

    @property
    def rule(self):
        return self._rule

    @property
    def user_action(self):
        return self._user_action
