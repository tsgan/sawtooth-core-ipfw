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

import sys
import argparse
import logging

from sawtooth_ipfw.ledger_sync.ipfw_ledger_sync.ipfw_rule import Ipfw_Rule
from sawtooth_ipfw.ledger_sync.ipfw_ledger_sync.subscriber import Subscriber
from sawtooth_ipfw.ledger_sync.ipfw_ledger_sync.deltas.handlers import get_events_handler


LOGGER = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='Increase level of output sent to stderr')
    parser.add_argument('--validator',
                        help='The url of the validator to sync with',
                        default='tcp://localhost:4004')
    return parser.parse_args(args)


def init_logger(level):
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    if level == 1:
        logger.setLevel(logging.INFO)
    elif level > 1:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)


def main():
    try:
        opts = parse_args(sys.argv[1:])
        init_logger(opts.verbose)

        LOGGER.info('Starting Ledger Sync...')

        ipfw_rule = Ipfw_Rule()

        subscriber = Subscriber(opts.validator)
        subscriber.add_handler(get_events_handler(ipfw_rule))

        subscriber.start()

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as err:  # pylint: disable=broad-except
        LOGGER.exception(err)
        sys.exit(1)

    finally:
        try:
            subscriber.stop()
        except UnboundLocalError:
            pass

        LOGGER.info('Ledger Sync shut down successfully')
