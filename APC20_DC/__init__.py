# Embedded file name: output/Live/mac_universal_64_static/Release/python-bundle/MIDI Remote Scripts/APC20/__init__.py
# Compiled at: 2024-08-27 23:56:43
# Size of source mod 2**32: 739 bytes
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.Capabilities import CONTROLLER_ID_KEY, NOTES_CC, PORTS_KEY, REMOTE, SCRIPT, controller_id, inport, outport
from .APC20 import APC20

def create_instance(c_instance):
    return APC20(c_instance)


def get_capabilities():
    return {CONTROLLER_ID_KEY: (controller_id(vendor_id=2536,
                          product_ids=[123],
                          model_name="Akai APC20")), 
     
     PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[SCRIPT, REMOTE])]}
