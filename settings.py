from MIDI import * # import MIDI status codes

""" settings which MIDI-notes and CCs trigger which functionality """


# debug_mode: whether the log-function should output to logfile
debug_mode = False

"""
	<setting>: Note (<MIDI note#> [, <MIDI channel>])
	<setting>: CC (<MIDI CC#> [, <mapping mode> [, <MIDI channel>]])
	
	if <mapping mode> is ommitted, it is assumed MIDI.RELATIVE_TWO_COMPLIMENT (see MIDI.py for other modes)
	if <MIDI channel> is ommitted, it is assumed MIDI.DEFAULT_CHANNEL (see MIDI.py)
	
"""

# these values are only used if you map tempo-control to an absolute controller
tempo_min = 60
tempo_max = 187

volume_default = 0.55 # this value is -12db (trial-and-error to set as there is no mapping function available)

scrub_increment = 4 # scrubs by ticks

auto_select_playing_clip = False

auto_arm = False # default behaviour for auto-arming a track on selection, either False or True
has_midi_loopback = False # auto-arm on selection (including when selecting via mouse) usually only works with the STC.app on Mac, which provides MIDI-loopback-functionality. If you set has_midi_loopback = False then auto-arm on selection works even without STC.app, but only if you use STC-MIDI Remote Script and MIDI to select a track (so if you select a track via mouse, it then will not be automatically armed)

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
	
	"select_playing_clip": Note(50), # highlights clipslot with currently playing clip 
	"toggle_auto_select_playing_clip": Note(51),
	
	#"toggle_mute_selected_clip": Note(50), # does not do anything
	
	
	# global controls
	"tempo": (CC(86), CC(20, ABSOLUTE)),
	"tap_tempo": Note(86), # attention: Live 8 only!
	"tempo_increase": Note(87),
	"tempo_decrease": Note(85),
	
	"play_stop": Note(20),
	"play_pause": Note(21),
	"play_selection": Note(24),
	
	# global arrangement scrubbing
	"scrub_by": CC(90),
	"scrub_forward": Note(90),
	"scrub_rewind": Note(89),
	
	"undo": Note(80),
	"redo": Note(81),
	
	
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