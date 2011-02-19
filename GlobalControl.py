import MIDI
import settings
#from Logging import log

from Control import Control

class GlobalControl(Control):
#	__module__ = __name__
	__doc__ = "Global parameters of SelectedTrackControl"

	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		# each callback is (mapping, callback)
		# mappings are taken from settings.midi_mapping
		m = settings.midi_mapping
		self.midi_callbacks = (
			(m["overdub"], self.toggle_overdub),
			(m["disable_overdub"], self.disable_overdub),
			(m["record"], self.toggle_record),
			
			(m["punch_in"], self.toggle_punchin),
			(m["punch_out"], self.toggle_punchout),
			
			(m["metronome"], self.toggle_metronome),
			(m["loop"], self.toggle_loop),
			
			
			(m["loop_move"], self.move_loop_by),
			(m["loop_lb_move"], self.move_loop_left_bracket_by),
			(m["loop_rb_move"], self.move_loop_right_bracket_by),
			(m["tempo"], self.set_tempo),
			(m["tap_tempo"], self.tap_tempo),
			
			(m["play_stop"], self.play_stop),
			(m["play_pause"], self.play_pause),
			(m["play_selection"], self.play_selection),
			
			(m["undo"], self.undo),
			(m["redo"], self.redo),
		)
		
		# steps, when ABSOLUTE mode for tempo CC is used
		self.tempo_step = (settings.tempo_max - settings.tempo_min)/127.0
		
		# register midi_callbacks via parent
		self.register_midi_callbacks()
	
	
	
	def play_stop(self, value, mode):
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.start_playing()
	
	def play_pause(self, value, mode):
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.continue_playing()
	
	def play_selection(self, value, mode):
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.play_selection()
	
	def undo(self, value, mode):
		self.song.undo()
	
	def redo(self, value, mode):
		self.song.redo()
	
	
	
	
	def toggle_overdub(self, value, mode):
		self.song.overdub = not self.song.overdub
	
	def disable_overdub(self, value, mode):
		self.song.overdub = 0
	
	
	def toggle_record(self, value, mode):
		self.song.record_mode = not self.song.record_mode
	def toggle_punchin(self, value, mode):
		self.song.punch_in = not self.song.punch_in
	def toggle_punchout(self, value, mode):
		self.song.punch_out = not self.song.punch_out
		
	def toggle_metronome(self, value, mode):
		self.song.metronome = not self.song.metronome
	
	def toggle_loop(self, value, mode):
		self.song.loop = not self.song.loop
		
	def move_loop_by(self, value, mode):
		self.song.loop_start = self.song.loop_start + value
		
	def move_loop_left_bracket_by(self, value, mode):
		d_value = MIDI.relative_to_signed_int[mode](value)
		self.move_loop_by(d_value)
		self.move_loop_right_bracket_by(-d_value)
	
	def move_loop_right_bracket_by(self, value, mode):
		self.song.loop_length = self.song.loop_length + value
	
	def set_tempo(self, value, mode):
		if mode == MIDI.ABSOLUTE:
			self.song.tempo = settings.tempo_min + value*self.tempo_step
		else:
			self.song.tempo = self.song.tempo + value
	
	def tap_tempo(self, value, mode):
		if self.song.tap_tempo:
			self.song.tap_tempo()