# settings which MIDI-notes and CCs trigger which functionality

# DEBUG_MODE: whether the log-function should output to logfile
DEBUG_MODE = False

# global channel the MIDI signal comes through
MIDI_CHANNEL = 0



# MIDI CCs - all in relative_two_compliment

CC_SCENE_SCROLL = 84
CC_TRACK_SCROLL = 85

CC_INCREASE_TEMPO = 86
CC_LOOP_MOVE = 87
CC_LOOP_LB_MOVE = 88
CC_LOOP_RB_MOVE = 89


CC_VOLUME_BC = 7 # backwards-compatible
CC_PAN_BC = 10 # backwards-compatible

CC_VOLUME = 22
CC_PAN = 23

# CCs for sends 1-4
CC_SENDS = [24, 25, 26, 27]





# MIDI notes

# track controls
NOTE_ARM = 0
NOTE_ARM_EXCLUSIVE = 3
NOTE_SOLO = 1
NOTE_SOLO_EXCLUSIVE = 4
NOTE_MUTE = 2
NOTE_MUTE_EXCLUSIVE = 5

NOTE_SWITCH_MONITORING = 6

NOTE_VOLUME_RESET = 22
VOLUME_DEFAULT = 0.55 # this value is -12db (trial-and-error to set as there is no mapping function available)

NOTE_PAN_CENTER = 23
PAN_CENTER_VALUE = 0.0

NOTE_SENDS_RESET = [24, 25, 26, 27]





# Session controls
NOTE_PLAY_SELECTED_SCENE = 38
NOTE_PLAY_NEXT_SCENE = 40
NOTE_PLAY_PREV_SCENE = 36

NOTE_FIRST_SCENE = 37
NOTE_LAST_SCENE = 39

NOTE_FIRST_TRACK = 46
NOTE_LAST_TRACK = 47
NOTE_PLAY_SELECTED_CLIP = 43
NOTE_PLAY_NEXT_CLIP = 45
NOTE_PLAY_PREV_CLIP = 41
NOTE_PLAY_NEXT_AVAILABLE_CLIP = 44
NOTE_PLAY_PREV_AVAILABLE_CLIP = 42



# Global controls
NOTE_METRONOME = 12
NOTE_TOGGLE_OVERDUB = 14
NOTE_DISABLE_OVERDUB = 15

NOTE_TOGGLE_RECORD = 19

NOTE_PUNCH_IN = 16
NOTE_PUNCH_OUT = 17
NOTE_LOOP = 18




