# chat_message.py
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

import json
import re as regex
from gi.repository import Adw, Gtk, GLib
from ulid import ULID as ulid
# from .chat_service_api import ChatServiceApi

@Gtk.Template(resource_path='/io/github/lo2dev/Mutiny/ui/chat/chat-message.ui')
class ChatMessage(Gtk.Box):
    __gtype_name__ = 'ChatMessage'

    id = None
    avatar_menu = Gtk.Template.Child()
    message_avatar = Gtk.Template.Child()
    username = Gtk.Template.Child()
    content = Gtk.Template.Child()
    attachments = Gtk.Template.Child()
    replies = Gtk.Template.Child()
    is_edited = Gtk.Template.Child()
    date = Gtk.Template.Child()

    embed = Gtk.Template.Child()
    embed_title = Gtk.Template.Child()
    embed_description = Gtk.Template.Child()

    def __init__(self, message_data, cascade=False, client_user=None, **kwargs):
        super().__init__(**kwargs)

        self.id = message_data['_id']

        ulid_object = ulid.from_str(self.id)
        datetime = GLib.DateTime.new_from_unix_local(ulid_object.timestamp)
        localtime_now = GLib.DateTime.new_now_local()
        time_difference = localtime_now.difference(datetime)

        if localtime_now.format("%x") == datetime.format("%x"):
            self.date.props.label = datetime.format("%R")
        elif localtime_now.format("%y") != datetime.format("%y"):
            self.date.props.label = datetime.format("%d %b %y %R")
        # 7 Days
        elif time_difference > 604800000000:
            self.date.props.label = datetime.format("%d %b %R")
        # 1 Day
        elif time_difference > 86400000000:
            self.date.props.label = datetime.format("%a %R")

        if 'edited' in message_data:
            self.is_edited.props.visible = True
            self.is_edited.props.tooltip_text = f"Edited {message_data['edited']}"

        if cascade:
            self.avatar_menu.props.visible = False
            self.username.props.visible = False

        # 'user' is coming from the websocket message data
        if 'user' in message_data:
            self.message_avatar.props.text = message_data['user']['username']
            self.username.props.label = message_data['user']['username']
        else:
            self.message_avatar.props.text = message_data['name']
            self.username.props.label = message_data['name']

        if 'content' in message_data and not message_data['content'] == "":
            self.content.props.label = message_data['content']
            self.content.props.visible = True

            if client_user:
                mentions = regex.findall(r"<@.+>", message_data['content'])
                for mention in mentions:
                    mention = regex.sub(r"<@|>","", mention)
                    if mention == client_user['_id']:
                        self.add_css_class("pinged")

        if 'mentions' in message_data:
            for mention in message_data['mentions']:
                if mention == client_user['_id']:
                    self.add_css_class('pinged')

        if 'embeds' in message_data:
            for embed in message_data['embeds']:
                if embed['type'] == "Text":
                    self.embed.props.visible = True
                    self.embed_title.props.label = embed['title']
                    self.embed_description.props.label = embed['description']


        if 'attachments' in message_data:
            self.attachments.props.visible = True

        if 'replies' in message_data:
            self.replies.props.visible = True



