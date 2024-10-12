# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC20/SliderModesComponent.py
# Compiled at: 2024-08-27 23:56:43
# Size of source mod 2**32: 2700 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from _Framework.ButtonElement import ButtonElement as ButtonElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent as ModeSelectorComponent

class SliderModesComponent(ModeSelectorComponent):

    def __init__(self, mixer, sliders, device, *a, **k):
        (super(SliderModesComponent, self).__init__)(*a, **k)
        self._mixer = mixer
        self._sliders = sliders
        self._device = device
        self._mode_index = 0

    def disconnect(self):
        super(SliderModesComponent, self).disconnect()
        self._mixer = None
        self._sliders = None
        self._device = None

    def set_mode_buttons(self, buttons):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)

        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)

        self.update()

    def number_of_modes(self):
        return 8

    def update(self):
        super(SliderModesComponent, self).update()
        if self.is_enabled():
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                else:
                    self._modes_buttons[index].turn_off()

            self._device.set_parameter_controls(None)

            for index in range(len(self._sliders)):
                strip = self._mixer.channel_strip(index)
                slider = self._sliders[index]
                slider.use_default_message()
                if self._mode_index == 7:
                    slider.set_identifier(16 + index)
                else:
                    slider.set_identifier(slider.message_identifier() - self._mode_index)
                strip.set_volume_control(None)
                strip.set_pan_control(None)
                strip.set_send_controls((None, None, None))
                slider.release_parameter()
                if self._mode_index == 0:
                    strip.set_volume_control(slider)
                if self._mode_index == 1:
                    strip.set_pan_control(slider)
                if self._mode_index >= 2 and self._mode_index < 5:
                    send_controls = [
                     None, None, None]
                    send_controls[self._mode_index - 2] = slider
                    strip.set_send_controls(tuple(send_controls))

            if self._mode_index == 7:
                self._device.set_parameter_controls(self._sliders)
