import Live

from consts import *
import settings
#from Logging import log


from SessionControl import SessionControl
from MixerControl import MixerControl
from GlobalControl import GlobalControl

class SelectedTrackControl:
	__module__ = __name__
	__doc__ = 'MIDI Remote Script to control the selected track'
	__name__ = "SelectedTrackControl MIDI Remote Script"
	
	def __init__(self, c_instance):
		#log("SelectedTrackControl::__init__")
		self.c_instance = c_instance
		
		# mappings for registered MIDI notes/CCs
		self.midi_callbacks = {}
		
		self.components = (
			SessionControl(c_instance, self),
			MixerControl(c_instance, self),
			GlobalControl(c_instance, self),
		)
		

		
	
	def suggest_map_mode(self, cc_no):
		#log("suggest_map_mode")
		return Live.MidiMap.MapMode.relative_two_compliment
		#return Live.MidiMap.MapMode.absolute
	
	
	def disconnect(self):
		for c in self.components:
			c.disconnect()
	
	def refresh_state(self):
		#log("refresh_state")
		#for c in self.components:
		#	c.refresh_state()
		pass
	
	def update_display(self):
		#log("update_display")
		#for c in self.components:
		#	c.update_display()
		pass
	
	
	
	
	# called from Live to build the MIDI bindings
	def build_midi_map(self, midi_map_handle):
		#log("SelectedTrackControl::build_midi_map")
		script_handle = self.c_instance.handle()
		
		for note in self.midi_callbacks.get(NOTEON_STATUS,{}).keys():
			Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, settings.MIDI_CHANNEL, note)
			
		for cc in self.midi_callbacks.get(CC_STATUS,{}).keys():
			Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, settings.MIDI_CHANNEL, cc)
	
	
	
	
	# called from Live when MIDI messages are received
	def receive_midi(self, midi_bytes):
		#log("receive_midi")
		channel = (midi_bytes[0] & CHAN_MASK)
		status = (midi_bytes[0] & STATUS_MASK)
		key = midi_bytes[1]
		value = midi_bytes[2]
		
		# if CC => calculate relative_two_compliment value
		if (status == CC_STATUS and value > 64):
			value = value - 128
		
		callbacks = self.midi_callbacks.get(status,{}).get(key,[])
		for callback in callbacks:
			callback(value)


	def suggest_input_port(self):
		return str('STC Virtual IN')

	def suggest_output_port(self):
		return str('')

	def can_lock_to_devices(self):
		return False

	def can_lock_to_device(self):
		return False
	
	
	
	
	# internal method to register callbacks from different controls
	def register_midi_callback(self, status, key, callback):
		#log("register_midi_callback(%s, %s)" % (status, key))
		if status in self.midi_callbacks:
			if key in self.midi_callbacks[status]:
				self.midi_callbacks[status][key].append(callback)
			else:
				self.midi_callbacks[status][key] = [callback, ]
		else:
			self.midi_callbacks[status] = {
				key: [callback, ]
			}
	
#	# helper-functions to register callbacks / UNUSED
#	def register_midi_note(self, note, callback):
#		self.register_midi_callback(NOTEON_STATUS, note, callback)
#		
#	def register_midi_cc(self, cc, callback):
#		self.register_midi_callback(CC_STATUS, cc, callback)
#
