from MIDI import * # import MIDI status codes

""" settings which MIDI-notes and CCs trigger which functionality """


# debug_mode: whether the log-function should output to logfile
debug_mode = False

"""
	"<setting>": Note (<MIDI note#> [, <MIDI channel>])
	"<setting>": CC (<MIDI CC#> [, <mapping mode> [, <MIDI channel>]])
	
	if <mapping mode> is ommitted, it is assumed MIDI.RELATIVE_TWO_COMPLIMENT
		other modes are: ABSOLUTE, RELATIVE_BINARY_OFFSET, RELATIVE_SIGNED_BIT, RELATIVE_SIGNED_BIT2 
		see the documentation of your device which type MIDI CC it sends
	
	if <MIDI channel> is ommitted, it is assumed MIDI.DEFAULT_CHANNEL
		the DEFAULT_CHANNEL channel is set to 0 (ie. channel 1 if you count from 1-16)
		MIDI channels are zero-indexed, ie. you count from 0 to 15
		you can change DEFAULT_CHANNEL in MIDI.py
	
	
	
	
	Some examples for setting up your own mappings:
	
	
	- Mapping "arm" to Note #64 on MIDI channel 4 (if you count channels 1-16):
		
		"arm": Note(64, 3),
	
	
	- Mapping "pan" to an encoder with CC #23 on MIDI channel 8 (if you count channels 1-16):
	  Note: encoders usually send RELATIVE values - in this example in RELATIVE_TWO_COMPLIMENT format

		"pan": CC(23, RELATIVE_TWO_COMPLIMENT, 7),
	
	
	- Mapping "volume" to a fader with CC #7 on MIDI channel 2 (if you count channels 1-16):
	  Note: faders usually send ABSOLUTE values

		"arm": CC(7, ABSOLUTE, 1),
	
	
	- Mapping sends
	  Sends are mapped the same way as other controls, only that you can provide multiple CC()-defintions
	  in a so called "tuple" (that is basically a list). The first CC maps to "Send 1", the second CC 
	  to "Send 2", etc.
	  
	  A tuple is defined like so:
	  
	  (<element>, <element>, <element>)
	  
	  A basic example, mapping knobs with CC #12-19 on MIDI channel 16 (if you count channels 1-16):
	  Note: knobs usually send ABSOLUTE values
	  
		"sends": (
			CC(12, ABSOLUTE, 15),
			CC(13, ABSOLUTE, 15),
			CC(14, ABSOLUTE, 15),
			CC(15, ABSOLUTE, 15),
			CC(16, ABSOLUTE, 15),
			CC(17, ABSOLUTE, 15),
			CC(18, ABSOLUTE, 15),
			CC(19, ABSOLUTE, 15),
		),
	
	
	
	
	
	
	- ADVANCED FEATURE: binding multiple MIDI messages to the same control
	  
	  This is mainly useful to support multiple MIDI bindings in STC by default.
	  Note that e.g. volume is mapped by default to MIDI CC #22 as RELATIVE_TWO_COMPLIMENT and at the 
	  same time to MIDI CC #7 as ABSOLUTE.
	  See documentation here: http://stc.wiffbi.com/midi-implementation-chart/
	  
	  Binding multiple MIDI messages to one control is done by using a tuple of CC/Note-commands. 
	  It is actually the same as defining controls for sends. Looking at the default defintion
	  for "volume"
	
		"volume": (CC(22), CC(7, ABSOLUTE)),
	
	  and adding some white-space/newlines
	
		"volume": (
			CC(22),
			CC(7, ABSOLUTE)
		),
	  
	  reveals, that is looks similar to the definition of sends described earlier.
	  
	  BONUS: even a single send-control can be mapped to multiple MIDI-commands. As sends are defined as 
	  a tuple of CC-commands, we can instead of a single CC-command use a tuple of CC-commands. This 
	  results in a tuple of tuples of CC-commands.
	  
	  The default definition of sends are such a construct:
	
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
	  
	  "Send 1" is mapped to CC #24 in RELATIVE_TWO_COMPLIMENT on the DEFAULT_CHANNEL as well as to 
	           CC #12 in ABSOLUTE on the DEFAULT_CHANNEL
	  "Send 2" is mapped to CC #25 in RELATIVE_TWO_COMPLIMENT on the DEFAULT_CHANNEL as well as to 
	           CC #14 in ABSOLUTE on the DEFAULT_CHANNEL
	  ...
"""

# these values are only used if you map tempo-control to an absolute controller
tempo_min = 60
tempo_max = 187

volume_default = 0.55 # this value is -12db (trial-and-error to set as there is no mapping function available)

scrub_increment = 4 # scrubs by ticks

auto_select_playing_clip = False

# this feature is currently only planned
#reset_device_bank = False # Reset device-bank to 0 when selecting another device

auto_arm = False # default behaviour for auto-arming a track on selection, either False or True
has_midi_loopback = False # auto-arm on selection (including when selecting via mouse) usually only works with the STC.app on Mac, which provides MIDI-loopback-functionality. If you use STC.app, set has_midi_loopback = True, else set has_midi_loopback = False. If set to False, auto-arm on selection works even without STC.app, but only if you use STC-MIDI Remote Script and MIDI to select a track (so if you select a track via mouse, it will not be automatically armed)

# either dict or False
device_bestof = False
#device_bestof = {
#	"Impulse": (4,3,2,1,8,7,6,5),
#	"Looper": (2,1,0),
#}

# either a list of Device-names or False
# automatically selects the device if available when switched to the track
auto_select_device = False
#auto_select_device = ["Looper", "Impulse", "Simpler"]


# clip_trigger_quantization_steps reflects the quantization setting in the transport bar. 
# 0: None 
# 1: 8 Bars 
# 2: 4 Bars 
# 3: 2 Bars 
# 4: 1 Bar 
# 5: 1/2 
# 6: 1/2T 
# 7: 1/4 
# 8: 1/4T 
# 9: 1/8 
# 10: 1/8T 
# 11: 1/16 
# 12: 1/16T 
# 13: 1/32

# define which quantization steps should be stepped through - use range(14) to step through all available
clip_trigger_quantization_steps = [0, 1, 2, 3, 4, 5, 7, 9, 11, 13]

# to use all quantization steps, remove the # at the beginning of the following line
#clip_trigger_quantization_steps = range(14)



# midi_recording_quantization_steps reflects the current selection of the Edit->Record Quantization menu. 
# 0: None 
# 1: 1/4 
# 2: 1/8 
# 3: 1/8T 
# 4: 1/8 + 1/8T 
# 5: 1/16 
# 6: 1/16T 
# 7: 1/16 + 1/16T 
# 8: 1/32

# define which quantization steps should be stepped through - use range(9) to step through all available
midi_recording_quantization_steps = [0, 1, 2, 5, 8]

# to use all quantization steps, remove the # at the beginning of the following line
#midi_recording_quantization_steps = range(9)



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
	
	"input_rotate": (Note(60), CC(60, ABSOLUTE)),
	"input_sub_rotate": (Note(61), CC(61, ABSOLUTE)),
	"input_none": Note(62),
	
	"output_rotate": (Note(63), CC(63, ABSOLUTE)),
	"output_sub_rotate": (Note(64), CC(64, ABSOLUTE)),
	"output_none": Note(65),
	
	
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
	"select_scene": CC(2, ABSOLUTE),
	"select_track": CC(8, ABSOLUTE),
	
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
	"toggle_selected_clip": Note(73),
	"play_next_clip": Note(45),
	"play_prev_clip": Note(41),
	"play_next_available_clip": Note(44),
	"play_prev_available_clip": Note(42),
	"stop_all_clips": Note(49),
	"stop_selected_track": Note(48),
	
	"select_playing_clip": Note(50), # highlights clipslot with currently playing clip 
	"toggle_auto_select_playing_clip": Note(51),
	
	#"toggle_mute_selected_clip": Note(50), # does not do anything
	
	"toggle_track_collapsed": (CC(79), Note(94)),
	
	"toggle_track_fold": CC(73),
	"assign_crossfade": CC(74, ABSOLUTE),
	"toggle_crossfade_a": Note(91),
	"toggle_crossfade_b": Note(92),
	"assign_crossfade_none": Note(93),
	"crossfader": (CC(75), CC(76, ABSOLUTE)),
	"cue_volume": (CC(77), CC(78, ABSOLUTE)),
	"master_volume": (CC(80), CC(81, ABSOLUTE)),
	
	
	# global controls
	"tempo": (CC(86), CC(20, ABSOLUTE)),
	"tap_tempo": Note(86), # attention: Live 8 only!
	"tempo_increase": Note(87),
	"tempo_decrease": Note(88),
	
	"play_stop": Note(20),
	"play_pause": Note(21),
	"play_selection": Note(24),
	"stop_playing": Note(27),
	"start_playing": Note(28),
	"continue_playing": Note(29),
	
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
	"back_to_arranger": Note(13),
	"overdub": Note(14),
	"disable_overdub": Note(15),
	"record": Note(19),
	"punch_in": Note(16),
	"punch_out": Note(17),
	
	
	
	# quantization control
	
	# steps through list of quantizations - see top for clip_trigger_quantization_steps
	"clip_trigger_quantization": (CC(49), CC(51, ABSOLUTE), Note(25)),
	
	
	 # steps through list of quantizations - see top for midi_recording_quantization_steps
	"midi_recording_quantization": (CC(50), CC(52, ABSOLUTE), Note(26)),
	
	
	
	
	# device control
	"scroll_devices": CC(32),
	"select_instrument": Note(66),
	"prev_device": Note(67),
	"next_device": Note(68),
	"prev_device_bank": Note(71),
	"next_device_bank": Note(72),
	"reset_device_bank": Note(70),
	"device_on_off": Note(69),
	"device_params": (
		(CC(33), CC(41, ABSOLUTE)),
		(CC(34), CC(42, ABSOLUTE)),
		(CC(35), CC(43, ABSOLUTE)),
		(CC(36), CC(44, ABSOLUTE)),
		(CC(37), CC(45, ABSOLUTE)),
		(CC(38), CC(46, ABSOLUTE)),
		(CC(39), CC(47, ABSOLUTE)),
		(CC(40), CC(48, ABSOLUTE)),
	),
	"reset_device_params": (
		Note(52),
		Note(53),
		Note(54),
		Note(55),
		Note(56),
		Note(57),
		Note(58),
		Note(59),
	),
	
	
	
	
	"toggle_browser": Note(74),
	"toggle_session_arranger": Note(75),
	"toggle_detail": Note(76),
	"toggle_detail_clip_device": Note(77),
	"toggle_detail_clip": Note(78),
	"toggle_detail_device": Note(79),
}