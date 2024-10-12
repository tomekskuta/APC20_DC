# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC20/BackgroundComponent.py
# Compiled at: 2024-08-27 23:56:43
# Size of source mod 2**32: 595 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.BackgroundComponent import BackgroundComponent as BackgroundComponentBase
from _Framework.Util import nop

class BackgroundComponent(BackgroundComponentBase):

    def _clear_control(self, name, control):
        if control:
            control.add_value_listener(nop)
        elif name in self._control_map:
            self._control_map[name].remove_value_listener(nop)
        super(BackgroundComponent, self)._clear_control(name, control)
