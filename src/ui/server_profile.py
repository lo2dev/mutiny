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

from gi.repository import Adw, Gtk

@Gtk.Template(resource_path='/io/github/lo2dev/Mutiny/ui/server-profile.ui')
class ServerProfile(Adw.Dialog):
    __gtype_name__ = 'ServerProfile'

    server_avatar = Gtk.Template.Child()
    server_name = Gtk.Template.Child()
    server_owner = Gtk.Template.Child()
    server_description = Gtk.Template.Child()

    def __init__(self, server_owner, server_name, server_description, **kwargs):
        super().__init__(**kwargs)

        self.server_avatar.props.text = server_name
        self.server_name.props.label = server_name
        self.server_owner.props.label = f"by {server_owner}"
        self.server_description.props.label = server_description

