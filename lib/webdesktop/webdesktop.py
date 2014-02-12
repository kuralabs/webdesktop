# -*- coding:utf-8 -*-
#
# Copyright 2014 Carlos Jenkins <carlos@jenkins.co.cr>
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

from gi.repository import Gtk, WebKit2  # gir1.2-webkit2-3.0
from os.path import abspath, dirname, join

WHERE_AM_I = abspath(dirname(__file__))


class WebDesktop(object):
    """
    Simple WebDesktop class.

    Uses WebKit introspected bindings for Python:
    http://webkitgtk.org/reference/webkit2gtk/stable/
    """

    def __init__(self, uri, menu=False, jail=True):
        """
        Build GUI
        """
        # Save URI
        self.uri = uri

        # Build GUI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(join(WHERE_AM_I, 'webdesktop.ui'))

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
                print('Warning: trying to leave jail to {}'.format(uri))
                self.webview.load_uri(self.uri)
