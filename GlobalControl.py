#import Live

from consts import *
import settings
#from Logging import log

class GlobalControl:
	__module__ = __name__
	__doc__ = "Global parameters of SelectedTrackControl"

	def __init__(self, c_instance, selected_track_controller):
		self.c_instance = c_instance
		self.song = c_instance.song()
		
		self.midi_callbacks = {
			NOTEON_STATUS: (
				(settings.NOTE_TOGGLE_OVERDUB, self.toggle_overdub),
				(settings.NOTE_DISABLE_OVERDUB, self.disable_overdub),
				
				(settings.NOTE_TOGGLE_RECORD, self.toggle_record),

				(settings.NOTE_PUNCH_IN, self.toggle_punchin),
				(settings.NOTE_PUNCH_OUT, self.toggle_punchout),

				(settings.NOTE_METRONOME, self.toggle_metronome),
				(settings.NOTE_LOOP, self.toggle_loop)
			),
			CC_STATUS: (
				(settings.CC_LOOP_MOVE, self.move_loop_by),
				(settings.CC_LOOP_LB_MOVE, self.move_loop_left_bracket_by),
				(settings.CC_LOOP_RB_MOVE, self.move_loop_right_bracket_by),
				(settings.CC_INCREASE_TEMPO, self.increase_tempo_by)
			)
		}
		
		# register callbacks on selected_track_controller
		for status, callbacks in self.midi_callbacks.items():
			for (key, callback) in callbacks:
				selected_track_controller.register_midi_callback(status, key, callback)
	
	def disconnect(self):
		pass
	
	
	
	
	def toggle_overdub(self, velocity):
		self.song.overdub = not self.song.overdub
	
	def disable_overdub(self, velocity):
		self.song.overdub = 0
	
	
	def toggle_record(self, velocity):
		self.song.record_mode = not self.song.record_mode
	def toggle_punchin(self, velocity):
		self.song.punch_in = not self.song.punch_in
	def toggle_punchout(self, velocity):
		self.song.punch_out = not self.song.punch_out
		
	def toggle_metronome(self, velocity):
		self.song.metronome = not self.song.metronome
	
	def toggle_loop(self, velocity):
		self.song.loop = not self.song.loop
		
	def move_loop_by(self, d_value):
		self.song.loop_start = self.song.loop_start + d_value
	def move_loop_left_bracket_by(self, d_value):
		self.move_loop_by(d_value)
		self.move_loop_right_bracket_by(-d_value)
	def move_loop_right_bracket_by(self, d_value):
		self.song.loop_length = self.song.loop_length + d_value
	
	
	def increase_tempo_by(self, d_value):
		self.song.tempo = self.song.tempo + d_value
	
	