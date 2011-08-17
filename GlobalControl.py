import MIDI
import settings
from Logging import log

from Control import Control

class GlobalControl(Control):
#	__module__ = __name__
	__doc__ = "Global parameters of SelectedTrackControl"

	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		# steps, when ABSOLUTE mode for tempo CC is used
		self.tempo_step = (settings.tempo_max - settings.tempo_min)/127.0
		
	
	def get_midi_bindings(self):
		return (
			("overdub", self.toggle_overdub),
			("disable_overdub", self.disable_overdub),
			("record", self.toggle_record),
			
			("punch_in", self.toggle_punchin),
			("punch_out", self.toggle_punchout),
			
			("metronome", self.toggle_metronome),
			("loop", self.toggle_loop),
			
			
			("loop_move", self.move_loop_by),
			("loop_lb_move", self.move_loop_left_bracket_by),
			("loop_rb_move", self.move_loop_right_bracket_by),
			("tempo", self.set_tempo),
			("tempo_increase", lambda value, mode, status : self.set_tempo(1, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			("tempo_decrease", lambda value, mode, status : self.set_tempo(-1, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			("tap_tempo", self.tap_tempo),
			
			("play_stop", self.play_stop),
			("play_pause", self.play_pause),
			("play_selection", self.play_selection),
			
			("scrub_by", self.scrub_by),
			("scrub_forward", lambda value, mode, status : self.scrub_by(settings.scrub_increment, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			("scrub_rewind", lambda value, mode, status : self.scrub_by(128-settings.scrub_increment, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			
			("undo", self.undo),
			("redo", self.redo),
		)
	
	def scrub_by(self, value, mode, status):
		d_value = MIDI.relative_to_signed_int[mode](value)
		self.song.scrub_by(d_value)

	
	def play_stop(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.start_playing()
	
	def play_pause(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.continue_playing()
	
	def play_selection(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.play_selection()
	
	def undo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.undo()
	
	def redo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.redo()
	
	
	
	
	def toggle_overdub(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.overdub = not self.song.overdub
	
	def disable_overdub(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.overdub = 0
	
	
	def toggle_record(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.record_mode = not self.song.record_mode
	def toggle_punchin(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.punch_in = not self.song.punch_in
	def toggle_punchout(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.punch_out = not self.song.punch_out
		
	def toggle_metronome(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.metronome = not self.song.metronome
	
	def toggle_loop(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.loop = not self.song.loop
		
	def move_loop_by(self, value, mode, status):
		self.song.loop_start = self.song.loop_start + value
		
	def move_loop_left_bracket_by(self, value, mode, status):
		d_value = MIDI.relative_to_signed_int[mode](value)
		self.move_loop_by(d_value)
		self.move_loop_right_bracket_by(-d_value)
	
	def move_loop_right_bracket_by(self, value, mode, status):
		self.song.loop_length = self.song.loop_length + value
	
	def set_tempo(self, value, mode, status):
		if mode == MIDI.ABSOLUTE:
			self.song.tempo = settings.tempo_min + value*self.tempo_step
		else:
			d_value = MIDI.relative_to_signed_int[mode](value)
			self.song.tempo = self.song.tempo + d_value
	
	def tap_tempo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		if self.song.tap_tempo:
			self.song.tap_tempo()