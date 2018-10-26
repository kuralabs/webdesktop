# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 KuraLabs S.R.L
# Copyright (C) 2014 Carlos Jenkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Arguments parsing module.
"""

import logging
from argparse import ArgumentParser

from . import __version__


log = logging.getLogger(__name__)


def booleanize(value):
    """
    Convert a string to a boolean.

    :raises: ValueError if unable to convert.

    :param str value: String to convert.

    :return: True if value in lowercase match yes, true, or False if no or
     false.
    :rtype: bool
    """
    valuemap = {
        'true': True,
        'yes': True,
        'false': False,
        'no': False,
    }
    casted = valuemap.get(value.lower(), None)
    if casted is None:
        raise ValueError(str(value))
    return casted


def validate_args(args):
    """
    Validate that arguments are valid.

    :param args: An arguments namespace.
    :type args: :py:class:`argparse.Namespace`

    :return: The validated namespace.
    :rtype: :py:class:`argparse.Namespace`
    """
    try:
        from colorlog import ColoredFormatter as Formatter
        logfrmt = (
            '  {thin_white}{asctime}{reset} | '
            '{log_color}{levelname:8}{reset} | '
            '{thin_white}{processName}{reset} | '
            '{log_color}{message}{reset}'
        )
    except ImportError as e:
        from logging import Formatter
        logfrmt = (
            '  {asctime} | '
            '{levelname:8} | '
            '{processName} | '
            '{message}'
        )

    verbosity_levels = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }

    stream = logging.StreamHandler()
    stream.setFormatter(Formatter(fmt=logfrmt, style='{'))

    level = verbosity_levels.get(args.verbosity, logging.DEBUG)
    logging.basicConfig(handlers=[stream], level=level)

    log.debug('Verbosity at level {}'.format(args.verbosity))

    return args


def parse_args(argv=None):
    """
    Argument parsing routine.

    :param argv: A list of argument strings.
    :type argv: list

    :return: A parsed and verified arguments namespace.
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = ArgumentParser(
        description='WebDesktop Kiosk Browser'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Increase verbosity level',
        default=0,
        dest='verbosity',
        action='count',
    )
    parser.add_argument(
        '--version',
        action='version',
        version='{} v{}'.format(parser.description, __version__)
    )

    parser.add_argument(
        '--name',
        default='webdesktop',
        help='Name of the application',
    )
    parser.add_argument(
        '--menu',
        type=booleanize,
        default=False,
        help='Enable or disable the context menu',
    )
    parser.add_argument(
        '--jail',
        type=booleanize,
        default=True,
        help='Enable or disable the domain jail',
    )
    parser.add_argument(
        '--width',
        type=int,
        default=None,
        help='Force window width',
    )
    parser.add_argument(
        '--height',
        type=int,
        default=None,
        help='Force window height',
    )
    parser.add_argument(
        '--monitor',
        type=int,
        default=None,
        help='Show WebDesktop in monitor number',
    )

    parser.add_argument(
        'uri',
        help='URI to connect to',
    )

    args = parser.parse_args(args=argv)
    args = validate_args(args)
    return args


__all__ = [
    'parse_args',
]
