# system_message.py
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

from gi.repository import Gtk

@Gtk.Template(resource_path='/io/github/lo2dev/Mutiny/ui/chat/system-message.ui')
class SystemMessage(Gtk.Box):
    __gtype_name__ = 'SystemMessage'

    icon = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        match data['system']['type']:
            case 'user_added':
                self.content.props.label = f"{data['system']['id']} was added by {data['system']['by']}"
                self.icon.props.icon_name = "plus-symbolic"
                self.icon.props.css_classes = ["success"]
            case 'user_remove':
                self.content.props.label = f"{data['system']['id']} was removed by {data['system']['by']}"
                self.icon.props.icon_name = "minus-symbolic"
                self.icon.props.css_classes = ["error"]
            case 'user_joined':
                self.content.props.label = f"{data['system']['id']} joined"
                self.icon.props.icon_name = "arrow-turn-down-right-symbolic"
                self.icon.props.css_classes = ["success"]
            case 'user_left':
                self.content.props.label = f"{data['system']['id']} left"
                self.icon.props.icon_name = "arrow-pointing-away-from-line-left-symbolic"
                self.icon.props.css_classes = ["warning"]
            case 'user_banned':
                self.content.props.label = f"{data['system']['id']} was banned"
                self.icon.props.icon_name = "skull-symbolic"
                self.icon.props.css_classes = ["error"]
            case 'message_pinned':
                self.content.props.label = f"{data['system']['by']} pinned {data['system']['id']}"
                self.icon.props.icon_name = "pin-symbolic"
            case _:
                self.content.props.label = data['system']['content']

