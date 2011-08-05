import MIDI
import settings
import math
from Logging import log

from Control import Control

class DeviceControl(Control):
#	__module__ = __name__
	__doc__ = "Device control section of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		self.bank = 0
		self.params_per_bank = len(settings.midi_mapping["device_params"])
		self.max_banks = int(math.ceil(128.0/self.params_per_bank))
		
		#if "reset_device_bank" in settings:
		#	TODO: add listener to tracks if selected device has changed
		
		if "device_params" in settings.midi_mapping:
			for i in range(len(settings.midi_mapping["device_params"])):
				self.setup_device_param_set(i, settings.midi_mapping["device_params"][i])
		
		if "reset_device_params" in settings.midi_mapping:
			for i in range(len(settings.midi_mapping["reset_device_params"])):
				self.setup_device_param_reset(i, settings.midi_mapping["reset_device_params"][i])
	
	
	def get_midi_bindings(self):
		return (
			("scroll_devices", self.scroll_devices),
			("prev_device", self.prev_device),
			("next_device", self.next_device),
			
			
			("select_device_bank", self.select_device_bank),
			("prev_device_bank", self.prev_device_bank),
			("next_device_bank", self.next_device_bank),
			("reset_device_bank", lambda value, mode, status: self.select_device_bank(0, MIDI.ABSOLUTE, MIDI.CC_STATUS)),
			
			
			("select_instrument", self.select_instrument),
		)
	
	
	
	def setup_device_param_set(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode, status : self.set_device_param(i, value, mode, status)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
	
	
	def set_device_param(self, i, value, mode, status):
		track = self.song.view.selected_track
		device = track.view.selected_device
		if not device:
			return
		
		i = i + self.params_per_bank*self.bank
		
		param = device.parameters[i]
		if not param:
			return
		
		param_range = param.max - param.min
		#log ("%s is_quantized: %d; default_value: %s" % (param.name, param.is_quantized, param.default_value))
		if param.is_quantized:
			if mode == MIDI.ABSOLUTE:
				param.value = round(param_range*value/127.0 + param.min)
			else:
				param.value = max(param.min, min(param.max, param.value + value))
		else:
			if mode == MIDI.ABSOLUTE:
				param.value = param_range*value/127.0 + param.min
			else:
				param.value = max(param.min, min(param.max, param.value + (value/100.0)))
	
	
	
	
	
	
	
	def setup_device_param_reset(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode, status : self.reset_device_param(i, value, mode, status)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
	
	
	def reset_device_param(self, i, value, mode, status):
		track = self.song.view.selected_track
		device = track.view.selected_device
		if device:
			i = i + self.params_per_bank*self.bank
			param = device.parameters[i]
			if param:
				if param.is_quantized:
					param.value = 1
				else:
					param.value = param.default_value
	
	
	
	def select_device_bank(self, value, mode, status):
		if mode == MIDI.ABSOLUTE:
			self.bank = self.max_banks*value/128
		else:
			self.bank = max(0, min(self.max_banks-1, self.bank + value))
		
		#log("STC: Device Bank %d" % (self.bank+1))
		self.c_instance.show_message("STC: Device Bank %d" % (self.bank+1))
	
	def prev_device_bank(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.select_device_bank(-1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)

	def next_device_bank(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.select_device_bank(1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)
	
	
	
	
	
	def get_device_index(self, device, devices):
		index = 0
		for d in devices:
			if d == device:
				return index
			index = index + 1
		return -1
	
	def scroll_devices(self, value, mode, status):
		track = self.song.view.selected_track
		len_devices = len(track.devices)
		
		if mode == MIDI.ABSOLUTE:
			index = len_devices*value/128
		else:
			index = self.get_device_index(track.view.selected_device, track.devices)
			index = max(0, min(len_devices-1, index + value))
		
		self.song.view.select_device(track.devices[index])
	
	def prev_device(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.scroll_devices(-1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)
	
	def next_device(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.scroll_devices(1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)

	
	
	
	def select_instrument(self, value, mode, status):
		self.song.view.selected_track.view.select_instrument()
	