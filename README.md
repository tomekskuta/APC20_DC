# APC20 Device Control
Remote script for Akai APC20 controller with added few features:
- Device Control on `USER3` sliders bank
- Tap tempo
- Reverted functionality of track selection buttons

## How it works
![Akai APC20](./APC20.jpeg)

All numbered buttons works only if `SHIFT` is pressed:
- `1` - Tap tempo
- `2` - Toggle between Device view selector and Clip view selector
- `3` - Show/hide detail view
- `4` - On/off selected device
- `5` - Lock/unlock selected device to control
- `6` - Switch to previous device on chain
- `7` - Switch to next device on chain

On image I also marked button for `USER3` bank which you can activate with pressed `SHIFT` as well. Then sliders are are controlling selected device.

#### `Navigation/Track selection` buttons
It's unexpected thing but when I added device control feature functionality of these buttons reversed. Now if you push some of these buttons corresponding track will be selected. `PLAY`, `STOP`, `REC`, `MIDI OVERDUB`, navigation and `NOTE MODE` works if `SHIFT` is pressed.
Navigation buttons switch between tracks and scenes banks instead of single tracks and scenes (works like zooming session overview). It's something I don't know how to fix yet.
In general I like this reverse feature so I decided to leave it as it is now and for me it works even better.

## How to use it
TBC

## Limitations
I use original APC20 remote script from Ableton Live 10 which is written in Python2 so it probably **works only with AL10 and lower**. Remote scripts for AL11 are written with Python3.

Additional features buttons are highlighted initially. They turn off after pressing `SHIFT` button once and then are working normally.

### TODO
- Add switching between device banks
- Fix navigation buttons to switch between single track/scene instead of whole banks
- Fix initially highlight of new features buttons