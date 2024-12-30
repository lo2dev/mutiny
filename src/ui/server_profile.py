# server_profile.py
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
import re as regex

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/lo2dev/Mutiny/ui/server-profile.ui')
class ServerProfile(Adw.Dialog):
    __gtype_name__ = 'ServerProfile'

    server_avatar = Gtk.Template.Child()
    server_name = Gtk.Template.Child()
    server_owner = Gtk.Template.Child()
    server_description = Gtk.Template.Child()

    official_indicator = Gtk.Template.Child()
    verified_indicator = Gtk.Template.Child()
    nsfw_indicator = Gtk.Template.Child()

    tags_box = Gtk.Template.Child()

    def __init__(self, server_data, **kwargs):
        super().__init__(**kwargs)

        self.server_avatar.props.text = server_data['name']
        self.server_name.props.label = server_data['name']
        self.server_owner.props.label = f"by {server_data['owner']}"


        # TODO: make this work
        if 'description' in server_data:
            pattern = regex.compile(r'#\w+')
            pattern2 = regex.compile(r'\n#\w+.+', regex.MULTILINE)

            tags = pattern.findall(server_data['description'])
            new_description = pattern2.sub("", server_data['description'])

            if not tags == []:
                self.tags_box.props.visible = True
                for tag in tags:
                    tag_label = Gtk.Label(label=f"{tag.strip().lower()}")
                    tag_label.add_css_class("tag")
                    self.tags_box.append(tag_label)

            self.server_description.props.label = new_description.strip()

        if 'flags' in server_data:
            match server_data['flags']:
                case 0:
                    self.verified_indicator.props.visible = True
                case 1:
                    self.official_indicator.props.visible = True
                case _:
                 pass

        if 'nsfw' in server_data:
            self.nsfw_indicator.props.visible = True

