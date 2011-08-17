import Live

import MIDI
import settings
import math
from Logging import log

from Control import Control

import ParamSetter



class DeviceControl(Control):
#	__module__ = __name__
	__doc__ = "Device control section of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		self._device = None
		self._locked_to_device = False
		
		self.bank = 0
		if "device_params" in settings.midi_mapping:
			self.params_per_bank = len(settings.midi_mapping["device_params"])
		else:
			self.params_per_bank = 8
		self.max_banks = int(math.ceil(128.0/self.params_per_bank))
		
		#if "reset_device_bank" in settings:
		#	TODO: add listener to tracks if selected device has changed
		
		if settings.auto_select_device:
			self.song.view.add_selected_track_listener(self.auto_select_device)
		
		if settings.device_bestof:
			# we have best-of parameters for devices => use these parameters first, then the rest
			for device_name, indizes in settings.device_bestof.items():
				new_indizes = [0,] + list(indizes)
				i = 0
				while i < 128:
					if i not in indizes:
						new_indizes.append(i)
					i = i + 1
				settings.device_bestof[device_name] = new_indizes
		
		
		if "device_params" in settings.midi_mapping:
			for i in range(len(settings.midi_mapping["device_params"])):
				# begin with parameter 1, as 0 is device-on/off
				self.setup_device_param_set(i+1, settings.midi_mapping["device_params"][i])
		
		if "reset_device_params" in settings.midi_mapping:
			for i in range(len(settings.midi_mapping["reset_device_params"])):
				# begin with parameter 1, as 0 is device-on/off
				self.setup_device_param_reset(i+1, settings.midi_mapping["reset_device_params"][i])
	
	
	def get_midi_bindings(self):
		return (
			("scroll_devices", self.scroll_devices),
			("prev_device", self.prev_device),
			("next_device", self.next_device),
			
			("device_on_off", self.device_on_off),
			("select_device_bank", self.select_device_bank),
			("prev_device_bank", self.prev_device_bank),
			("next_device_bank", self.next_device_bank),
			("reset_device_bank", lambda value, mode, status: self.select_device_bank(0, MIDI.ABSOLUTE, MIDI.CC_STATUS)),
			
			
			("select_instrument", self.select_instrument),
		)
	
	
	
	
	def auto_select_device(self):
		select_device = None
		index = -1
		# loop through devices
		for device in self.song.view.selected_track.devices:
			i = 1
			for name in settings.auto_select_device:
				if device.name == name:
					if i < index or index == -1:
						index = i
						select_device = device
						if index == 0:
							break
				elif not index == -1 and i > index:
					break
					
				i = i+1
			
			if index == 0:
				break
		if select_device:
			#log("select %s" % select_device.name)
			self.song.view.select_device(device)
		
	
	
	def set_device(self, device):
		self._device = device
		#log("Device '%s' has the following Parameters:" % device.name)
		#for i in range(len(device.parameters)):
		#	log("%s - %s (%s; %s - %s : %s)" % (i, device.parameters[i].name, device.parameters[i].value, device.parameters[i].min, device.parameters[i].max, device.parameters[i].is_quantized))
	
	def set_lock_to_device(self, lock, device):
		assert isinstance(lock, type(False))
		assert (lock is not self._locked_to_device)
		if lock:
			self.set_device(device)
		else:
			assert (device == self._device)
		
		self._locked_to_device = lock
	
	
	def setup_device_param_set(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode, status : self.set_device_param(i, value, mode, status)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
	
	
	def set_device_param(self, i, value, mode, status):
		track = self.song.view.selected_track
		if self._device:
			device = self._device
		else:
			device = track.view.selected_device
		if not device:
			return
		
		# if param index == 0 => device on/off => do not apply banking!
		if i > 0:
			i = i + self.params_per_bank*self.bank
			# if there are best-of settings for the selected device
			# then apply the index-translation
			if settings.device_bestof and device.name in settings.device_bestof:
				i = settings.device_bestof[device.name][i]
		
		param = device.parameters[i]
		if not param:
			return
		
		# get ParamSetter for selected device and set value
		ParamSetter.get(device)(self.song, device, param, value, mode, status)
	
	
	
	
	
	
	
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
	
	
	def device_on_off(self, value, mode, status):
		# if e.g. a pad sends CC, then ignore the off-value (same behaviour as Note-On/Note-Off)
		if status == MIDI.CC and not value:
			return
		# force toggle behaviour by status == MIDI.NOTEON_STATUS
		# this breaks controlling on/off with a knob!
		self.set_device_param(0, value, mode, MIDI.NOTEON_STATUS)
	
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
	
	def get_device_relative_recursive(self, selected_device, delta):
		container = selected_device.canonical_parent # either track or chain
		len_devices = len(container.devices)
		index = self.get_device_index(selected_device, container.devices) + delta
		
		if not type(container) == type(Live.Track.Track):
			# as we are not inside a Track, we must be inside a Rack
			if index < 0:
				# if first device is selected and we move left, try to move up a device_container and select the containing device
				return self.get_device_relative_recursive(container.canonical_parent, index+1)
			elif index >= len_devices:
				# if last device is selected and we move right, try to move up a device_container and select next device
				#return self.get_device_relative_recursive(container.canonical_parent, index-len_devices+1)
				# if last device is selected and we move right, try to move up a device_container and select the containing device
				return self.get_device_relative_recursive(container.canonical_parent, index-len_devices)
		
		# we cannot move further out => stay inside the index-boundary of available devices
		index = max(0, min(len_devices-1, index))
		
		return container.devices[index]
	
	
	
	def scroll_devices(self, value, mode, status):
		if mode == MIDI.ABSOLUTE:
			#container = self.song.view.selected_track
			container = self.song.view.selected_track.view.selected_device.canonical_parent
			len_devices = len(container.devices)
			device = container.devices[len_devices*value/128]
		else:
			# relative navigation
			device = self.get_device_relative_recursive(self.song.view.selected_track.view.selected_device, value)
		
		self.song.view.select_device(device)
	
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
	