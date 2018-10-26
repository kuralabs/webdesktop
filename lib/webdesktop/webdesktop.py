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
webdesktop main UI class.
"""

from logging import getLogger

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

# noqa for E402: module level import not at top of file
from gi.repository import Gtk, WebKit2  # noqa
from pkg_resources import resource_filename # noqa


log = getLogger(__name__)


class WebDesktop(object):
    """
    Simple WebDesktop class.

    Uses WebKit introspected bindings for Python:

        http://webkitgtk.org/reference/webkit2gtk/stable/

    :param str uri: URI to connect to.
    :param str name: Name of the application.
    :param bool menu: Enable or disable the context menu.
    :param bool jail: Enable or disable the domain jail.
    """

    def __init__(self, uri, name='webdesktop', menu=False, jail=True):
        """
        Build GUI
        """
        # Save URI
        self.uri = uri

        # Build GUI from Glade file
        ui = resource_filename(__name__, 'webdesktop.ui')
        log.debug('Found UI at {}'.format(ui))
        self.builder = Gtk.Builder.new_from_file(ui)

        # Get objects
        go = self.builder.get_object
        self.window = go('window')
        self.scrolled = go('scrolled')

        # Create WebView
        self.webview = WebKit2.WebView()
        self.webview.load_uri(uri)
        self.scrolled.add_with_viewport(self.webview)

        # Connect signals
        self.builder.connect_signals(self)
        if not menu:
            self.webview.connect('context-menu', self.context_menu_cb)
        if jail:
            self.webview.connect('load-changed', self.load_changed_cb)
        self.window.connect('delete-event', Gtk.main_quit)

        # Everything is ready
        self.window.fullscreen()
        self.window.show_all()

    def context_menu_cb(self, webview, menu, event, htr, user_data=None):
        """
        Callback to disable context menu.
        """
        return True

    def load_changed_cb(self, webview, event, user_data=None):
        """
        Callback for when the load operation in webview changes.
        """
        ev = str(event)
        uri = self.webview.get_uri()
        if 'WEBKIT_LOAD_STARTED' in ev:
            if not uri.startswith(self.uri):
                log.warning('Warning: trying to leave jail to {}'.format(uri))
                self.webview.load_uri(self.uri)

    def start(self):
        """
        Start the WebDesktop application.
        """
        value = Gtk.main()
        log.debug('Main returned value {}'.format(value))
        return value


__all__ = [
    'WebDesktop',
]
