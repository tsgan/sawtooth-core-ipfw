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

from __future__ import print_function

import argparse
import getpass
import logging
import os
import traceback
import sys
import pkg_resources

from colorlog import ColoredFormatter

from sawtooth_ipfw.ipfw_client import IpfwClient
from sawtooth_ipfw.ipfw_exceptions import IpfwException


DISTRIBUTION_NAME = 'sawtooth-ipfw'


DEFAULT_URL = 'http://127.0.0.1:8008'


def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)

    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)

    return clog


def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))


def add_create_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'add',
        help='Creates a new ipfw rule',
        description='Sends a transaction to start an ipfw rule with the '
        'identifier <num>. This transaction will fail if the specified '
        'rule already exists.',
        parents=[parent_parser])

    parser.add_argument(
        'num',
        type=str,
        help='rule number for the new ipfw rule')

    parser.add_argument(
        'action',
        type=str,
        help='action for the new rule (allow, accept, pass, permit, deny, drop)')

    parser.add_argument(
        'rule',
        type=str,
        help='new rule body (all from any to any, etc.)')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--disable-client-validation',
        action='store_true',
        default=False,
        help='disable client validation')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for rule to commit')


def add_list_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'list',
        help='Displays information for all ipfw rules',
        description='Displays information for all ipfw rules.',
        parents=[parent_parser])

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
        'is using Basic Auth')


def add_show_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        'show',
        help='Displays information about an ipfw rule',
        description='Displays the ipfw rule <num>',
        parents=[parent_parser])

    parser.add_argument(
        'num',
        type=str,
        help='identifier for the rule')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
        'is using Basic Auth')


def add_delete_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('delete', parents=[parent_parser])

    parser.add_argument(
        'num',
        type=str,
        help='number of the rule to be deleted')

    parser.add_argument(
        '--url',
        type=str,
        help='specify URL of REST API')

    parser.add_argument(
        '--username',
        type=str,
        help="identify name of user's private key file")

    parser.add_argument(
        '--key-dir',
        type=str,
        help="identify directory of user's private key file")

    parser.add_argument(
        '--auth-user',
        type=str,
        help='specify username for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--auth-password',
        type=str,
        help='specify password for authentication if REST API '
        'is using Basic Auth')

    parser.add_argument(
        '--wait',
        nargs='?',
        const=sys.maxsize,
        type=int,
        help='set time, in seconds, to wait for delete transaction to commit')


def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output')

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='display version information')

    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands by sending Ipfw transactions.',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_create_parser(subparsers, parent_parser)
    add_list_parser(subparsers, parent_parser)
    add_show_parser(subparsers, parent_parser)
    add_delete_parser(subparsers, parent_parser)

    return parser


def do_list(args):
    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)

    client = IpfwClient(base_url=url, keyfile=None)

    rule_list = [
        rule.split(';')
        for rules in client.list(auth_user=auth_user,
                                 auth_password=auth_password)
        for rule in rules.decode().split('|')
    ]

    if rule_list is not None:
        rule_list.sort()
        fmt = "%-8s %-8.8s %s"
        print(fmt % ('RULE NO', 'ACTION', 'RULE'))
        for rule_data in rule_list:

            num, action, rule, user_action = rule_data

            print(fmt % (num, action, rule))
    else:
        raise IpfwException("Could not retrieve rule listing.")


def do_show(args):
    num = args.num

    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)

    client = IpfwClient(base_url=url, keyfile=None)

    data = client.show(num, auth_user=auth_user, auth_password=auth_password)

    if data is not None:

        action_str, ipfw_rule = {
            num: (action, rule)
            for num, action, rule, user_action in [
                ipfw.split(';')
                for ipfw in data.decode().split('|')
            ]
        }[num]

        print("Rule Mumber : {}".format(num))
        print("Action      : {}".format(action_str))
        print("Rule body   : {}".format(ipfw_rule))
        print("")

    else:
        raise IpfwException("Rule not found: {}".format(num))


def do_create(args):
    num = args.num
    action = args.action
    rule = args.rule

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)
    print("auth user: {}".format(auth_user))

    client = IpfwClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.create(
            num, action, rule, wait=args.wait,
            auth_user=auth_user,
            auth_password=auth_password)
    else:
        response = client.create(
            num, action, rule, auth_user=auth_user,
            auth_password=auth_password)

    print("Response: {}".format(response))


def do_delete(args):
    num = args.num

    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)

    client = IpfwClient(base_url=url, keyfile=keyfile)

    if args.wait and args.wait > 0:
        response = client.delete(
            num, wait=args.wait,
            auth_user=auth_user,
            auth_password=auth_password)
    else:
        response = client.delete(
            num, auth_user=auth_user,
            auth_password=auth_password)

    print("Response: {}".format(response))


def _get_url(args):
    return DEFAULT_URL if args.url is None else args.url


def _get_keyfile(args):
    username = getpass.getuser() if args.username is None else args.username
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, username)


def _get_auth_info(args):
    auth_user = args.auth_user
    auth_password = args.auth_password
    if auth_user is not None and auth_password is None:
        auth_password = getpass.getpass(prompt="Auth Password: ")

    return auth_user, auth_password


def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)

    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose

    setup_loggers(verbose_level=verbose_level)

    if args.command == 'add':
        do_create(args)
    elif args.command == 'list':
        do_list(args)
    elif args.command == 'show':
        do_show(args)
    elif args.command == 'delete':
        do_delete(args)
    else:
        raise IpfwException("invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except IpfwException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
