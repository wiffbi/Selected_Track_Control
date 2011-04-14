import MIDI
#import inspect
import settings
#from Logging import log

class Control:
#	__module__ = __name__
	__doc__ = "Super-class for Controls"

	def __init__(self, c_instance, selected_track_controller):
		self.c_instance = c_instance
		if c_instance:
			self.song = c_instance.song()
		self.selected_track_controller = selected_track_controller
		#self.midi_callbacks = (,)
		
		
		for key, callback in self.get_midi_bindings():
			if not key in settings.midi_mapping:
				
				continue
			
			mapping = settings.midi_mapping[key]
			# always make sure mapping is a tuple
			if isinstance(mapping, MIDI.MIDICommand):
				mapping = (mapping,)
			
			for m in mapping:
				self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
				
	
	def disconnect(self):
		pass
	
	def get_midi_bindings(self):
		return set()