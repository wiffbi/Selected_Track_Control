import MIDI
import settings
from Logging import log

from Control import Control

class QuantizationControl(Control):
#	__module__ = __name__
	__doc__ = "Quantization parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		self._midi_recording_quantization_labels = ["None", "1/4", "1/8", "1/8T", "1/8 + 1/8T", "1/16", "1/16T", "1/16 + 1/16T", "1/32"]
		
		for key, max_steps in (("clip_trigger_quantizations", 13), ("midi_recording_quantizations", 8)):
			if not key in settings.midi_mapping:
				continue
			mappings = settings.midi_mapping[key]
			for i in range(min(max_steps, len(mappings))):
				if mappings[i]:
					self.setup_quantizations(key[:-1], i, mappings[i])
			
	def get_midi_bindings(self):
		return (
			("clip_trigger_quantization", self.clip_trigger_quantization), # 0-13
			("midi_recording_quantization", self.midi_recording_quantization), # 0-8
		)
	
	
	
	
	def setup_quantizations(self, key, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
			
		callback = lambda value, mode, status : self.set_quantization(key, i)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
	
	
	
	def set_quantization(self, key, i):
		log("set %s to %d" % (key, i))
		self.song[key] = i
	
	def clip_trigger_quantization(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		
		self.song.clip_trigger_quantization = self._get_quantization(value, mode, status, self.song.clip_trigger_quantization, settings.clip_trigger_quantization_steps)
	
	
	def midi_recording_quantization(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		
		self.song.midi_recording_quantization = self._get_quantization(value, mode, status, self.song.midi_recording_quantization, settings.midi_recording_quantization_steps)
		
		self.show_message("MIDI recording quantization: %s" % self._midi_recording_quantization_labels[self.song.midi_recording_quantization])
		
	
	
	
	
	def _get_quantization(self, value, mode, status, current_quantization, quantizations):
		nr_of_quantizations = len(quantizations)
		
		if status == MIDI.CC_STATUS and mode == MIDI.ABSOLUTE:
			return quantizations[nr_of_quantizations*value/128]
		else:
			# note or relative CC
			if not current_quantization in quantizations:
				for quantization in quantizations:
					if quantization > current_quantization:
						current_quantization = quantization
						break
				next_index = quantizations.index(current_quantization)
			else:
				next_index = quantizations.index(current_quantization)+1
			
			
			if status == MIDI.NOTEON_STATUS:
				# go round
				next_index = next_index % nr_of_quantizations
			else:
				if value < 0:
					next_index = next_index - 2
				next_index = min(max(0, next_index), nr_of_quantizations-1)
				
			return quantizations[next_index]
	
	
	
	
	
	