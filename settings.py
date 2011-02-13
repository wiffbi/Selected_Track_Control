from MIDI import * # import MIDI status codes

""" settings which MIDI-notes and CCs trigger which functionality """


# debug_mode: whether the log-function should output to logfile
debug_mode = False

"""
	<key>: (<MIDI note/CC number> [, <mapping mode> [, <status type> [, <MIDI channel>]]])
	
	if <mapping mode> is ommitted, <status type> is assumed NOTEON_STATUS
	if <mapping mode> is given, but <status type> is ommitted, <status type> is assumed CC_STATUS
	
	this allows for fast common configuration but also enables interesting mappings such as mapping volume absolute to a note events velocity:
	
	"volume": (
		22, # MIDI note
		ABSOLUTE, # mapping mode of value
		NOTEON_STATUS, # status type
		MIDI_CHANNEL
	)
	
	Note: if you want to use a different MIDI channel than the default one, then you have to fully qualify all parameters
	
"""

# these values are only used if you map tempo-control to an absolute controller
tempo_min = 60
tempo_max = 187


midi_mapping = {
	# track controls
	"arm": Note(0),
	"arm_exclusive": Note(3),
	"solo": Note(1),
	"sole_exclusive": Note(4),
	"mute": Note(2),
	"mute_exclusive": Note(5),
	"switch_monitoring": Note(6),
	
	
	"volume": (CC(22), CC(7, ABSOLUTE)),
	"pan": (CC(23), CC(10, ABSOLUTE)),
	
#	"volume_up": Note(7),
#	"volume_down": Note(8),
#	"pan_left": Note(9),
#	"pan_right": Note(10),
	
	"reset_volume": Note(22),
	"reset_pan": Note(23),
	
	"send_1": (CC(24), CC(12, ABSOLUTE)),
	"send_2": (CC(25), CC(13, ABSOLUTE)),
	"send_3": (CC(26), CC(14, ABSOLUTE)),
	"send_4": (CC(27), CC(15, ABSOLUTE)),
	"send_5": (CC(28), CC(16, ABSOLUTE)),
	"send_6": (CC(29), CC(17, ABSOLUTE)),
	"send_7": (CC(30), CC(18, ABSOLUTE)),
	"send_8": (CC(31), CC(19, ABSOLUTE)),
	
	"reset_send_1": Note(24),
	"reset_send_2": Note(25),
	"reset_send_3": Note(26),
	"reset_send_4": Note(27),
	"reset_send_5": Note(28),
	"reset_send_6": Note(29),
	"reset_send_7": Note(30),
	"reset_send_8": Note(31),
	
	
	# session controls
	"scroll_scene": CC(84),
	"scroll_track": CC(85),
	
	"prev_scene": Note(82),
	"next_scene": Note(83),
	"prev_track": Note(84),
	"next_track": Note(85),
	
	"play_selected_scene": Note(38),
	"play_next_scene": Note(40),
	"play_prev_scene": Note(36),
	
	"first_scene": Note(37),
	"last_scene": Note(39),
	"first_track": Note(46),
	"last_track": Note(47),
	
	"play_selected_clip": Note(43),
	"play_next_clip": Note(45),
	"play_prev_clip": Note(41),
	"play_next_available_clip": Note(44),
	"play_prev_available_clip": Note(42),
	"stop_selected_track": Note(48), # TODO
	
	
	# global controls
	"tempo": CC(86),
	"tap_tempo": Note(86), # TODO (attention: Live 8 only!)
	"tempo_increase": Note(87),
	"tempo_decrease": Note(85),
	
	
	"loop": Note(18),
	"loop_move": CC(87),
	"loop_lb_move": CC(88),
	"loop_rb_move": CC(89),
	
	"metronome": Note(12),
	"overdub": Note(14),
	"disable_overdub": Note(15),
	"record": Note(19),
	"punch_in": Note(16),
	"punch_out": Note(17)
}




## flatten mapping to common format mapping[<name>] = (<key>, <mode>, <status>, <channel>)
## and fill midi_cc_to_mode for fast lookup
#for k in mapping.keys():
#	m = mapping[k]
#	
#	channel = midi_channel
#	if type(m) == type(1) \
#		or (type(m) == type((1,2)) and len(m) == 1):
#		# just an int, so it is a MIDI note on
#		key = m
#		mode = ABSOLUTE
#		status = NOTEON_STATUS
#		
#	elif type(mapping) == type((1,2)):
#		# is one element 
#		if m[0] == type((1,2)):
#			
#		
#		key = m[0]
#		status = CC_STATUS
#		
#		if len(mapping) < 1: # a mode is supplied
#			mode = m[1]
#		if len(mapping) < 2: # a status is supplied
#			status = mapping[2]
#		if len(mapping) > 3: # a custom MIDI channel is supplied
#			channel = mapping[3]
#	else:
#		mapping[key] = None # TODO: key löschen. delete?
#	
#	mapping[key] = (key, mode, status, channel)
#


####
####
##### MIDI CCs - all in relative_two_compliment
####
####CC_SCENE_SCROLL = 84
####CC_TRACK_SCROLL = 85
####
####CC_INCREASE_TEMPO = 86
####CC_LOOP_MOVE = 87
####CC_LOOP_LB_MOVE = 88
####CC_LOOP_RB_MOVE = 89
####
####
####CC_VOLUME_BC = 7 # backwards-compatible
####CC_PAN_BC = 10 # backwards-compatible
####
####CC_VOLUME = 22
####CC_PAN = 23
####
##### CCs for sends 1-4
####CC_SENDS = [24, 25, 26, 27]
####
####
####
####
####
##### MIDI notes
####
##### track controls
####NOTE_ARM = 0
####NOTE_ARM_EXCLUSIVE = 3
####NOTE_SOLO = 1
####NOTE_SOLO_EXCLUSIVE = 4
####NOTE_MUTE = 2
####NOTE_MUTE_EXCLUSIVE = 5
####
####NOTE_SWITCH_MONITORING = 6
####
####NOTE_VOLUME_RESET = 22
####VOLUME_DEFAULT = 0.55 # this value is -12db (trial-and-error to set as there is no mapping function available)
####
####NOTE_PAN_CENTER = 23
####PAN_CENTER_VALUE = 0.0
####
####NOTE_SENDS_RESET = [24, 25, 26, 27]
####
####
####
####
####
##### Session controls
####NOTE_PLAY_SELECTED_SCENE = 38
####NOTE_PLAY_NEXT_SCENE = 40
####NOTE_PLAY_PREV_SCENE = 36
####
####NOTE_FIRST_SCENE = 37
####NOTE_LAST_SCENE = 39
####
####NOTE_FIRST_TRACK = 46
####NOTE_LAST_TRACK = 47
####NOTE_PLAY_SELECTED_CLIP = 43
####NOTE_PLAY_NEXT_CLIP = 45
####NOTE_PLAY_PREV_CLIP = 41
####NOTE_PLAY_NEXT_AVAILABLE_CLIP = 44
####NOTE_PLAY_PREV_AVAILABLE_CLIP = 42
####
####
####
##### Global controls
####NOTE_METRONOME = 12
####NOTE_TOGGLE_OVERDUB = 14
####NOTE_DISABLE_OVERDUB = 15
####
####NOTE_TOGGLE_RECORD = 19
####
####NOTE_PUNCH_IN = 16
####NOTE_PUNCH_OUT = 17
####NOTE_LOOP = 18
####
####
####
####
####