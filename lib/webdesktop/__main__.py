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
webdesktop executable entrypoint.
"""

from logging import getLogger


log = getLogger(__name__)


def main(argv=None):
    """
    Main function.

    :param list argv: List of string arguments to parse.

    :return: Exit code.
    :rtype: int
    """
    from .args import parse_args
    args = parse_args(argv=argv)

    # Check dependencies
    try:
        from .webdesktop import WebDesktop

    except ImportError as e:
        if e.name == 'gi':
            log.exception(
                'gi package is missing. '
                'Install package "python3-gi" or equivalent.'
            )
            return 1
        raise e

    except ValueError as e:
        message = e.args[0]

        if 'version' in message:
            log.exception(
                '{}. Check your dependencies.'.format(message)
            )
            return 1

        if 'WebKit2' in message:
            log.exception(
                'WebKit2 namespace is missing. '
                'Install package "gir1.2-webkit2-4.0" or equivalent.'
            )
            return 1
        raise e

    # Try to set process title
    try:
        from setproctitle import setproctitle
        setproctitle('{}@{}'.format(args.name, args.uri))
    except ImportError:
        log.warning(
            'setproctitle package is missing.'
            'Unable to set the process title to "{}". ',
            args.name
        )

    web = WebDesktop(args.uri, name=args.name, menu=args.menu, jail=args.jail)
    return web.start()


__all__ = [
    'main',
]
