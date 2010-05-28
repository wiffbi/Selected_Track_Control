# this file stores some constants regarding MIDI-handling, etc.
# for settings which MIDI-notes trigger what functionality see settings.py

STATUS_MASK = 0xF0
CHAN_MASK =  0x0F

CC_STATUS =  0xb0
NOTEON_STATUS = 0x90
NOTEOFF_STATUS = 0x80

STATUS_ON =  0x7f
STATUS_OFF = 0x00
STATUS_OFF2 = 0x40