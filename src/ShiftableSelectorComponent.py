#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC20/ShiftableSelectorComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.Layer import Layer
from _APC.ControlElementUtils import make_button
from .consts import NOTE_MODE, ABLETON_MODE

class ShiftableSelectorComponent(ModeSelectorComponent):
    u""" SelectorComponent that assigns buttons to functions based on the shift button """

    def __init__(self, select_buttons, master_button, tap_tempo_button, arm_buttons, matrix, session, zooming, mixer, transport, slider_modes, mode_callback, note_matrix, background, device, detail_view_toggler, device_on_off_button, device_lock_button, device_clip_toggle_button, detail_toggle_button, detail_left_button, detail_right_button, device_bank_prev_button, device_bank_next_button, nudge_up_button, nudge_down_button, *a, **k):
        assert len(select_buttons) == 8
        assert len(arm_buttons) == 8
        super(ShiftableSelectorComponent, self).__init__(*a, **k)
        self._toggle_pressed = False
        self._note_mode_active = False
        self._invert_assignment = False
        self._select_buttons = select_buttons
        self._master_button = master_button
        self._tap_tempo_button = tap_tempo_button
        self._slider_modes = slider_modes
        self._arm_buttons = arm_buttons
        self._transport = transport
        self._session = session
        self._zooming = zooming
        self._matrix = matrix
        self._mixer = mixer
        self._mode_callback = mode_callback
        self._note_matrix = note_matrix
        self._background = background
        self._device = device
        self._detail_view_toggler = detail_view_toggler
        self._device_on_off_button = device_on_off_button
        self._device_lock_button = device_lock_button
        self._device_clip_toggle_button = device_clip_toggle_button
        self._detail_toggle_button = detail_toggle_button
        self._detail_left_button = detail_left_button
        self._detail_right_button = detail_right_button
        self._device_bank_prev_button= device_bank_prev_button
        self._device_bank_next_button = device_bank_next_button
        self._nudge_up_button = nudge_up_button
        self._nudge_down_button = nudge_down_button
        # It's silly fix but it works.
        # I create fake button with non existing in APC20 midi parameters to cheat _is_banking_enabled function from Framework.DeviceComponent
        # it makes banking enabled even if shift button is not pressed
        self._fake_button = make_button(10, 87, name=u'Fake_Button')
        self._master_button.add_value_listener(self._master_value)

    def disconnect(self):
        super(ShiftableSelectorComponent, self).disconnect()
        self._master_button.remove_value_listener(self._master_value)
        self._select_buttons = None
        self._master_button = None
        self._tap_tempo_button = None
        self._slider_modes = None
        self._arm_buttons = None
        self._transport = None
        self._session = None
        self._zooming = None
        self._matrix = None
        self._mixer = None
        self._mode_callback = None
        self._note_matrix = None
        self._background = None
        self._device = None
        self._detail_view_toggler = None
        self._device_on_off_button = None
        self._device_lock_button = None
        self._device_clip_toggle_button = None
        self._detail_toggle_button = None
        self._detail_left_button = None
        self._detail_right_button = None
        self._device_bank_prev_button= None
        self._device_bank_next_button = None
        self._nudge_up_button = None
        self._nudge_down_button = None
        
    def set_mode_toggle(self, button):
        super(ShiftableSelectorComponent, self).set_mode_toggle(button)
        self.set_mode(0)

    def invert_assignment(self):
        self._invert_assignment = True
        self._recalculate_mode()

    def number_of_modes(self):
        return 2

    def _set_session_navigation_controls(self, left, right, up, down):
        self._session.set_track_bank_buttons(right, left)
        self._session.set_scene_bank_buttons(down, up)
        self._zooming.set_nav_buttons(up, down, left, right)

    def _set_transport_controls(self, play, stop, rec, overdub, tap_tempo, nudge_up, nudge_down):
        self._transport.set_play_button(play)
        self._transport.set_stop_button(stop)
        self._transport.set_record_button(rec)
        self._transport.set_overdub_button(overdub)
        self._transport.set_tap_tempo_button(tap_tempo)
        self._transport.set_nudge_buttons(nudge_up, nudge_down)

    def _set_device_buttons(self, on_off, lock, prev_bank, next_bank):
        self._device.set_on_off_button(on_off)
        self._device.set_lock_button(lock)
        self._device.set_bank_prev_button(prev_bank)
        self._device.set_bank_next_button(next_bank)

    def _set_details_button(self, clip_toggle, detail_toggle, left_button, right_button):
        self._detail_view_toggler.set_device_clip_toggle_button(clip_toggle)
        self._detail_view_toggler.set_detail_toggle_button(detail_toggle)
        self._detail_view_toggler.device_nav_left_button.set_control_element(left_button)
        self._detail_view_toggler.device_nav_right_button.set_control_element(right_button)

    def update(self):
        super(ShiftableSelectorComponent, self).update()
        if self.is_enabled():
            if self._mode_index == 0:
                for index in range(len(self._select_buttons)):
                    strip = self._mixer.channel_strip(index)
                    strip.set_select_button(None)

                self._mixer.master_strip().set_select_button(None)
                self._set_transport_controls(self._select_buttons[0], self._select_buttons[1], self._select_buttons[2], self._select_buttons[3], self._tap_tempo_button, self._nudge_up_button, self._nudge_down_button)
                self._set_device_buttons(self._device_on_off_button, self._device_lock_button, self._device_bank_prev_button, self._device_bank_next_button)
                self._set_details_button(self._device_clip_toggle_button, self._detail_toggle_button, self._detail_left_button, self._detail_right_button)
                if not self._note_mode_active:
                    self._set_session_navigation_controls(self._select_buttons[4], self._select_buttons[5], self._select_buttons[6], self._select_buttons[7])
                self._on_note_mode_changed()
            elif self._mode_index == 1:
                self._set_transport_controls(None, None, None, None, None, None, None)
                self._set_device_buttons(None, None, None, self._fake_button)
                self._set_details_button(None, None, None, None)
                self._set_session_navigation_controls(None, None, None, None)
                for index in range(len(self._select_buttons)):
                    strip = self._mixer.channel_strip(index)
                    strip.set_select_button(self._select_buttons[index])

                self._mixer.master_strip().set_select_button(self._master_button)
            else:
                assert False
            if self._mode_index == int(self._invert_assignment):
                self._slider_modes.set_mode_buttons(None)
                for index in range(len(self._select_buttons)):
                    self._mixer.channel_strip(index).set_arm_button(self._arm_buttons[index])

            else:
                for index in range(len(self._select_buttons)):
                    self._mixer.channel_strip(index).set_arm_button(None)

                self._slider_modes.set_mode_buttons(self._arm_buttons)

    def _toggle_value(self, value):
        assert self._mode_toggle != None
        assert value in range(128)
        self._toggle_pressed = value > 0
        self._recalculate_mode()

    def _recalculate_mode(self):
        self.set_mode((int(self._toggle_pressed) + int(self._invert_assignment)) % self.number_of_modes())

    def _master_value(self, value):
        assert self._master_button != None
        assert value in range(128)
        if self.is_enabled() and self._invert_assignment == self._toggle_pressed:
            if not self._master_button.is_momentary() or value > 0:
                for button in self._select_buttons:
                    button.turn_off()

                self._matrix.reset()
                mode_byte = NOTE_MODE
                if self._note_mode_active:
                    mode_byte = ABLETON_MODE
                self._mode_callback(mode_byte)
                self._note_mode_active = not self._note_mode_active
                if self._note_mode_active:
                    for button in self._note_matrix:
                        button.clear_send_cache()

                    self._note_matrix.reset()
                self._set_transport_controls(self._select_buttons[0], self._select_buttons[1], self._select_buttons[2], self._select_buttons[3], self._tap_tempo_button, self._nudge_up_button, self._nudge_down_button)
                self._set_device_buttons(self._device_on_off_button, self._device_lock_button, self._device_bank_prev_button, self._device_bank_next_button)
                self._set_details_button(self._device_clip_toggle_button, self._detail_toggle_button, self._detail_left_button, self._detail_right_button)
                self._transport.update()
                if self._note_mode_active:
                    for button in self._note_matrix:
                        button.clear_send_cache()

                    self._note_matrix.reset()
                if self._note_mode_active:
                    self._set_session_navigation_controls(None, None, None, None, None)
                    self._background.layer = Layer(left_button=self._select_buttons[4], right_button=self._select_buttons[5], up_button=self._select_buttons[6], down_button=self._select_buttons[7])
                else:
                    self._background.layer = None
                    self._set_session_navigation_controls(self._select_buttons[4], self._select_buttons[5], self._select_buttons[6], self._select_buttons[7])
                self._zooming.set_ignore_buttons(self._note_mode_active)
                self._on_note_mode_changed()

    def _on_note_mode_changed(self):
        assert self._master_button != None
        if self.is_enabled() and self._invert_assignment == self._toggle_pressed:
            if self._note_mode_active:
                self._master_button.turn_on()
            else:
                self._master_button.turn_off()