# window.py
#
# Copyright 2024 Lo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi, json
gi.require_version('Soup', '3.0')
gi.require_version('Json', '1.0')

from gi.repository import Adw, Gtk, Soup, Json, GLib, Gio
from .websocket import ClientWebsocket
from .chat_service_api import ChatServiceApi
from .session import MutinySession
from .chat_message import ChatMessage
from .server_profile import ServerProfile

@Gtk.Template(resource_path='/io/github/lo2dev/Mutiny/window.ui')
class MutinyWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MutinyWindow'

    token_dialog = Gtk.Template.Child()
    token_entry = Gtk.Template.Child()
    servers_list = Gtk.Template.Child()
    channels_list = Gtk.Template.Child()
    server_sidebar = Gtk.Template.Child()
    chat_messages_list = Gtk.Template.Child()
    chat_view_title = Gtk.Template.Child()
    typing_indicator = Gtk.Template.Child()
    message_bar = Gtk.Template.Child()
    send_message_button = Gtk.Template.Child()

    soup_session = None
    websocket_client = None
    chat_service_api = None
    session = None
    ready_cache: dict = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.token_dialog.present(self)

        self.servers_list.connect("row_selected", self.server_row_selected)

        self.message_bar.connect("activate", self.send_chat_message)

        self.create_action("open-server-profile", self.open_server_profile)



    def open_server_profile(self, _x, _y):
        current_server = None
        server_owner = None

        for server in self.ready_cache['servers']:
            if server['_id'] == self.session.current_server:
                current_server = server

        for user in self.ready_cache['users']:
            if user['_id'] == current_server['owner']:
                server_owner = user['username']


        server_profile = ServerProfile(
            server_owner or current_server['owner'],
            current_server['name'],
            current_server['description'] if 'description' in current_server else " "
        )
        server_profile.present(self)


    @Gtk.Template.Callback()
    def send_chat_message(self, _) -> None:
        message_content = self.message_bar.props.text
        json_message = json.dumps({
            "content" : f"{message_content}"
        })

        json_message = json_message.encode()
        json_message_bytes = GLib.Bytes.new_take(json_message)
        self.chat_service_api.request("POST", f"/channels/{self.session.current_channel}/messages", None, json_message_bytes)
        self.message_bar.props.text = ""


    def server_row_selected(self, _self, row):
        self.server_sidebar.props.title = row.props.title


    @Gtk.Template.Callback()
    def token_submitted(self, _) -> None:
        self.token_dialog.close()
        self.session = MutinySession(
            "ws.revolt.chat",
            "api.revolt.chat",
            self.token_entry.props.text
        )

        self.websocket_client = ClientWebsocket(self.session)
        self.websocket_client.connect("on_websocket_message", self.process_ws_message)

        self.chat_service_api = ChatServiceApi(self.session)


    def process_ws_message(self, _, ws_message) -> None:
        ws_message_dict = json.loads(ws_message)


        if ws_message_dict['type'] == "Ready":
            # print(json.dumps(ws_message_dict['servers'], indent=4))
            self.ready_cache = ws_message_dict

            for server in ws_message_dict['servers']:
                server_item = Adw.ActionRow(title=server['name'], activatable=True)
                server_item.connect("activated", self.change_server, server, ws_message_dict['channels'])

                self.servers_list.append(server_item)
        elif ws_message_dict['type'] == "ChannelStartTyping" and self.session.current_channel == ws_message_dict['id']:
            self.typing_indicator.props.label = "Broski typing in chat"
            self.typing_indicator.props.visible = True
        elif ws_message_dict['type'] == "ChannelStopTyping":
            self.typing_indicator.props.visible = False
        elif ws_message_dict['type'] == "Message" and self.session.current_channel == ws_message_dict['channel']:
            chat_message = ChatMessage(ws_message_dict)
            self.chat_messages_list.append(chat_message)


    def change_server(self, _self, server, ready_channels):
        self.channels_list.remove_all()
        self.session.current_server = server['_id']

        for channel in ready_channels:
            if channel['server'] == server['_id']:
                channel_item = Adw.ActionRow(title=channel['name'], activatable=True)
                channel_item.connect("activated", self.on_channel_changed, channel)
                self.channels_list.append(channel_item)


    def on_channel_changed(self, _, channel):
        self.typing_indicator.props.visible = False
        self.chat_view_title.props.title = channel['name']
        if 'description' in channel:
            self.chat_view_title.props.subtitle = channel['description']
        self.session.current_channel = channel['_id']
        self.chat_service_api.request("GET", f"/channels/{channel['_id']}/messages", self.on_request_channel_messages)


    def on_request_channel_messages(self, messages_dict):
        self.chat_messages_list.remove_all()
        # print(json.dumps(messages_dict, indent=2))

        # last_message_user = None
        for message in messages_dict:
            # WIP Cascading
            # chat_message = None
            # if last_message_user == message['author'] and not 'replies' in message:
            #     chat_message = ChatMessage(message, cascade=True)
            # else:
            #     chat_message = ChatMessage(message)

            chat_message = ChatMessage(message)
            self.chat_messages_list.prepend(chat_message)
            # last_message_user = message['author']


    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"win.{name}", shortcuts)



