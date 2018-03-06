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

import re
import logging
import base64

from sawtooth_cli.rest_client import RestClient
from sawtooth_sdk.protobuf.transaction_receipt_pb2 import StateChangeList

from sawtooth_ipfw.addressing.ipfw_addressing.addresser import IPFW_NAMESPACE as NAMESPACE


NS_REGEX = re.compile('^{}'.format(NAMESPACE))
LOGGER = logging.getLogger(__name__)


def get_events_handler(ipfw_rule):
    """Returns a events handler with a reference to a specific ipfw_rule object.
    The handler takes a list of events and updates the ipfw_rule appropriately.
    """
    return lambda events: _handle_events(ipfw_rule, events)


def _handle_events(ipfw_rule, events):
    block_num, block_id = _parse_new_block(events)

    changes = _parse_state_changes(events)
    _apply_state_changes(ipfw_rule, changes, block_num, block_id)

#    _insert_new_block(ipfw_rule, block_num, block_id)


def _parse_new_block(events):
    try:
        block_attr = next(e.attributes for e in events
                          if e.event_type == 'sawtooth/block-commit')
    except StopIteration:
        return None, None

    block_num = int(next(a.value for a in block_attr if a.key == 'block_num'))
    block_id = next(a.value for a in block_attr if a.key == 'block_id')
    LOGGER.debug('Handling deltas for block: %s', block_id)
    return block_num, block_id


def _parse_state_changes(events):
    try:
        change_data = next(e.data for e in events
                           if e.event_type == 'sawtooth/state-delta')
    except StopIteration:
        return []

    state_change_list = StateChangeList()
    state_change_list.ParseFromString(change_data)
    return [c for c in state_change_list.state_changes
            if NS_REGEX.match(c.address)]


def _apply_state_changes(ipfw_rule, changes, block_num, block_id):
    for change in changes:
        if change.type == 1:	# SET case
            val = change.value
            num, action, rule, user_action = val.decode().split(";")
            LOGGER.debug("Adding ipfw rule: %s", num)
            LOGGER.debug("ipfw rule: %s, %s, %s, %s", num, action, rule, user_action)
            ipfw_rule.add(num, action, rule)
        elif change.type == 2:	# DELETE case
            # Get ipfw rule number from payload
            rest_client = RestClient()
            output = rest_client.get_block(block_id)
            output = output['batches']
            output = output[0]['transactions']
            output = output[0]['payload']
            LOGGER.debug("Payload: %s", base64.b64decode(output).decode())
            num, action, rule, user_action = base64.b64decode(output).decode().split(";")
            LOGGER.debug("Deleting ipfw rule: %s", num)
            ipfw_rule.delete(num)


#def _insert_new_block(ipfw_rule, block_num, block_id):
#    new_block = {'block_num': block_num, 'block_id': block_id}
#    block_results = ipfw_rule.insert('blocks', new_block)
#    if block_results['inserted'] == 0:
#        LOGGER.warning('Failed to insert block #%s: %s', block_num, block_id)
