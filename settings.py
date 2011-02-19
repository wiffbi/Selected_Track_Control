from MIDI import * # import MIDI status codes

""" settings which MIDI-notes and CCs trigger which functionality """


# debug_mode: whether the log-function should output to logfile
debug_mode = True

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

volume_default = 0.55 # this value is -12db (trial-and-error to set as there is no mapping function available)

auto_arm = False # default behaviour for auto-arming a track on selection, either False or True

midi_mapping = {
	# track controls
	"arm": Note(0),
	"arm_exclusive": Note(3),
	"arm_kill": Note(10),
	"solo": Note(1),
	"solo_exclusive": Note(4),
	"solo_kill": Note(7),
	"mute": Note(2),
	"mute_exclusive": Note(5),
	"mute_kill": Note(8),
	"mute_flip": Note(9),
	"switch_monitoring": Note(6),
	
	"volume": (CC(22), CC(7, ABSOLUTE)),
	"pan": (CC(23), CC(10, ABSOLUTE)),
	
	"reset_volume": Note(22),
	"reset_pan": Note(23),
	
	"sends": (
		(CC(24), CC(12, ABSOLUTE)),
		(CC(25), CC(13, ABSOLUTE)),
		(CC(26), CC(14, ABSOLUTE)),
		(CC(27), CC(15, ABSOLUTE)),
		(CC(28), CC(16, ABSOLUTE)),
		(CC(29), CC(17, ABSOLUTE)),
		(CC(30), CC(18, ABSOLUTE)),
		(CC(31), CC(19, ABSOLUTE)),
	),
	# reset_sends is deprecated
	#"reset_sends": (
	#	Note(24),
	#	Note(25),
	#	Note(26),
	#	Note(27),
	#	Note(28),
	#	Note(29),
	#	Note(30),
	#	Note(31),
	#),
	
	
	# session controls
	"scroll_scenes": (CC(84), CC(9, ABSOLUTE)),
	"scroll_tracks": (CC(85), CC(11, ABSOLUTE)),
	
	"toggle_auto_arm": Note(11),
	
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
	"stop_all_clips": Note(49),
	"stop_selected_track": Note(48),
	
	"toggle_mute_selected_clip": Note(50),
	
	
	# global controls
	"tempo": (CC(86), CC(20, ABSOLUTE)),
	"tap_tempo": Note(86), # attention: Live 8 only!
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