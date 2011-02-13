from MIDI import *
import settings
#from Logging import log

class Control:
	__module__ = __name__
	__doc__ = "Super-class for Controls"

	def __init__(self, c_instance, selected_track_controller):
		self.c_instance = c_instance
		self.song = c_instance.song()
		self.selected_track_controller = selected_track_controller
		self.midi_callbacks = (,)
	
	def register_midi_callbacks():
		mapping = settings.midi_mapping
		for callback_items in self.midi_callbacks.items():
			# based on mapping mode, register callback with correct calculation
			key = callback_items[0]
			
			# key not in available mapping, then do not register it
			if not key in mapping or not mapping[key]:
				continue
			
			cur_mapping = mapping[key]
			
			# always make sure cur_mapping is a tuple
			if isinstance(cur_mapping, MIDI.MIDICommand):
				cur_mapping = (cur_mapping,)
			
			for m in cur_mapping:
				self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
				
	
	def disconnect(self):
		pass
	