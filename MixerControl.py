import MIDI
import settings
#from Logging import log
from Live import MixerDevice

from Control import Control

class MixerControl(Control):
#	__module__ = __name__
	__doc__ = "Mixer parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		
		# arming on track-selection does not work from within the callback
		# see SessionControl for at least auto-arm when using STC to select track
		if settings.auto_arm:
			self.song.view.add_selected_track_listener(self.on_track_selected)
		
		
		# use helper-functions to set up callback via lambda-functions
		# a closure inside the lambda-functions is needed, so i is always the current i
		
		#if "reset_sends" in settings.midi_mapping:
		#	for i in range(len(settings.midi_mapping["reset_sends"])):
		#		self.setup_send_reset(i, settings.midi_mapping["reset_sends"][i])
		
		if "sends" in settings.midi_mapping:
			for i in range(len(settings.midi_mapping["sends"])):
				self.setup_send_set(i, settings.midi_mapping["sends"][i])
		
	
	def disconnect(self):
		pass
	
	
	def get_midi_bindings(self):
		return (
			("arm", self.toggle_arm),
			("arm_exclusive", self.toggle_arm_exclusive),
			("arm_kill", self.arm_kill),
			
			("toggle_auto_arm", self.toggle_auto_arm),
			
			("solo", self.toggle_solo),
			("solo_exclusive", self.toggle_solo_exclusive),
			("solo_kill", self.solo_kill),
			("mute", self.toggle_mute),
			("mute_exclusive", self.toggle_mute_exclusive),
			("mute_kill", self.mute_kill),
			("mute_flip", self.mute_flip),
			("reset_pan", self.reset_pan),
			("reset_volume", self.reset_volume),
			("switch_monitoring", self.switch_monitoring),
			
			("input_rotate", self.input_rotate),
			("input_sub_rotate", self.input_sub_rotate),
			("input_none", self.input_none),
			
			("output_rotate", self.output_rotate),
			("output_sub_rotate", self.output_sub_rotate),
			("output_none", self.output_none),
			
			("assign_crossfade", self.assign_crossfade),
			("toggle_crossfade_a", lambda value, mode, status: self.toggle_crossfade(MixerDevice.MixerDevice.crossfade_assignments.A)),
			("toggle_crossfade_b", lambda value, mode, status: self.toggle_crossfade(MixerDevice.MixerDevice.crossfade_assignments.B)),
			("assign_crossfade_none", lambda value, mode, status: self.toggle_crossfade(MixerDevice.MixerDevice.crossfade_assignments.NONE)),
			
			("crossfader", self.set_crossfader),
			("cue_volume", self.set_cue_volume),
			("master_volume", self.set_master_volume),
			
			("volume", self.set_volume),
			("pan", self.set_pan)
		)
	
	
	
	def setup_send_reset(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode, status : self.reset_send(i)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
		
	def setup_send_set(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode, status : self.set_send(i, value, mode, status)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
		
	
	
	
	
	
	
	
	
	
	def get_tracks(self):
		# this does not work in Live 9 as tracks are now of an object of type "Vector"
		# manually join the tracks and return_tracks into one list
		#return self.song.tracks + self.song.return_tracks
		tracks = [track for track in self.song.tracks]
		for track in self.song.return_tracks:
			tracks.append(track)
		return tracks
	
	
	# arming a track inside this callback does not work :(
	def on_track_selected(self):
		if settings.auto_arm:
			# send MIDI through loopback for auto-arm
			mapping = settings.midi_mapping["arm"]
			if not isinstance(mapping, MIDI.MIDICommand):
				mapping = mapping[0]
			
			midi_bytes = (mapping.status, mapping.channel, 1)
			self.c_instance.send_midi(midi_bytes)
			
			# the following does not work :(, therefore this MIDI loopback
			#track = self.song.view.selected_track
			#if track.can_be_armed:
			#	track.arm = True
			#for t in self.song.tracks:
			#	if not t == track and t.can_be_armed:
			#		t.arm = False
	
	
	def toggle_auto_arm(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		settings.auto_arm = not settings.auto_arm
		
		track = self.song.view.selected_track
		if track.can_be_armed:
			track.arm = settings.auto_arm
		
		if settings.auto_arm:
			self.song.view.add_selected_track_listener(self.on_track_selected)
			
			for t in self.song.tracks:
				if not t == track and t.can_be_armed:
					t.arm = False
		else:
			self.song.view.remove_selected_track_listener(self.on_track_selected)
	
	
	def toggle_arm_track(self, track, exclusive):
		if track.can_be_armed:
			track.arm = not track.arm
		if exclusive: # arm exclusive
			for t in self.song.tracks:
				if not t == track and t.can_be_armed:
					t.arm = False
	def toggle_arm(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		# toggle exclusive depending on settings
		self.toggle_arm_track(self.song.view.selected_track, self.song.exclusive_arm)
	def toggle_arm_exclusive(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		# toggle exclusive depending on settings
		self.toggle_arm_track(self.song.view.selected_track, (not self.song.exclusive_arm))
	
	def arm_kill(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		for t in self.song.tracks:
			if t.can_be_armed:
				t.arm = False
	
	
	def toggle_solo_track(self, track, exclusive):
		track.solo = not track.solo
		if exclusive: # solo exclusive
			for t in self.get_tracks():
				if not t == track:
					t.solo = False
	def toggle_solo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		# toggle exclusive depending on settings
		self.toggle_solo_track(self.song.view.selected_track, self.song.exclusive_solo)
	def toggle_solo_exclusive(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		# toggle exclusive depending on settings
		self.toggle_solo_track(self.song.view.selected_track, (not self.song.exclusive_solo))
	
	def solo_kill(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		for t in self.get_tracks():
			t.solo = False
	
	
	def toggle_mute_track(self, track, exclusive):
		track.mute = not track.mute
		if exclusive: # mute exclusive
			for t in self.get_tracks():
				if not t == track:
					t.mute = False
	def toggle_mute(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.toggle_mute_track(self.song.view.selected_track, False)
	def toggle_mute_exclusive(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.toggle_mute_track(self.song.view.selected_track, True)
		
	def mute_kill(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		for t in self.get_tracks():
			t.mute = False
	
	def mute_flip(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		for t in self.song.tracks:
			t.mute = not t.mute
	
	
	
	def set_volume(self, value, mode, status):
		self._set_volume(self.song.view.selected_track.mixer_device.volume, value, mode)
#		param = self.song.view.selected_track.mixer_device.volume
#		if mode == MIDI.ABSOLUTE:
#			param.value = value/127.0
#		else:
#			param.value = max(0.0, min(1.0, param.value + (value/200.0)))

	# _set_volume can be used to either set volume-parameter of mixer or cue_volume of master track's mixer
	def _set_volume(self, param, value, mode):
		if mode == MIDI.ABSOLUTE:
			param.value = value/127.0
		else:
			param.value = max(0.0, min(1.0, param.value + (value/200.0)))
	
	def reset_volume(self, value, mode, status):
		self.song.view.selected_track.mixer_device.volume.value = settings.volume_default
	
	
	def set_pan(self, value, mode, status):
		param = self.song.view.selected_track.mixer_device.panning
		if mode == MIDI.ABSOLUTE:
			param.value = (value-64)/64.0
			
		else:
			param.value = max(-1.0, min(1.0, param.value + (value/100.0)))
	
	def reset_pan(self, value, mode, status):
		self.song.view.selected_track.mixer_device.panning.value = 0.0
	
	
	def set_send(self, i, value, mode, status):
		param = self.song.view.selected_track.mixer_device.sends[i]
		if param:
			if mode == MIDI.ABSOLUTE:
				param.value = value/127.0
			else:
				param.value = max(0.0, min(1.0, param.value + (value/100.0)))
	
	def reset_send(self, i):
		param = self.song.view.selected_track.mixer_device.sends[i]
		if param:
			param.value = 0.0
	
	
	def switch_monitoring(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		track = self.song.view.selected_track
		if (hasattr(track, "current_monitoring_state")):
			track.current_monitoring_state = (track.current_monitoring_state + 1) % len(track.monitoring_states.values)
	
	
	
	
	
	def get_routing_index(self, value, mode, status, current_routing, routings):
		routings_len = len(routings)
		if status == MIDI.CC_STATUS and mode == MIDI.ABSOLUTE:
			return min(value/(127/routings_len), routings_len)
		else:
			# tuple does not have index-function *urgh*
			i = 0
			for routing in routings:
				if routing == current_routing:
					break
				i = i+1
			if mode == MIDI.ABSOLUTE:
				i = i+1
			else:
				i = i+value
			
			i = i % routings_len
		return i
		
	def input_rotate(self, value, mode, status):
		track = self.song.view.selected_track
		track.current_input_routing = track.input_routings[self.get_routing_index(value, mode, status, track.current_input_routing, track.input_routings)]
	
	def input_sub_rotate(self, value, mode, status):
		track = self.song.view.selected_track
		track.current_input_sub_routing = track.input_sub_routings[self.get_routing_index(value, mode, status, track.current_input_sub_routing, track.input_sub_routings)]
	
	def input_none(self, value, mode, status):
		track = self.song.view.selected_track
		track.current_input_routing = track.input_routings[-1]
	
	def output_rotate(self, value, mode, status):
		track = self.song.view.selected_track
		track.current_output_routing = track.output_routings[self.get_routing_index(value, mode, status, track.current_output_routing, track.output_routings)]

	def output_sub_rotate(self, value, mode, status):
		track = self.song.view.selected_track
		track.current_output_sub_routing = track.output_sub_routings[self.get_routing_index(value, mode, status, track.current_output_sub_routing, track.output_sub_routings)]

	def output_none(self, value, mode, status):
		track = self.song.view.selected_track
		track.current_output_routing = track.output_routings[-1]
	
	
	
	def set_master_volume(self, value, mode, status):
		self._set_volume(self.song.master_track.mixer_device.volume, value, mode)

	def set_cue_volume(self, value, mode, status):
		self._set_volume(self.song.master_track.mixer_device.cue_volume, value, mode)
	
	def set_crossfader(self, value, mode, status):
		param = self.song.master_track.mixer_device.crossfader
		if mode == MIDI.ABSOLUTE:
			param.value = (value/127.0)*2.0 - 1.0
		else:
			param.value = max(-1.0, min(1.0, param.value + (value/100.0)))
	
	
	def toggle_crossfade(self, crossfade_assign):
		track = self.song.view.selected_track
		if not track == self.song.master_track:
			if track.mixer_device.crossfade_assign == crossfade_assign:
				track.mixer_device.crossfade_assign = MixerDevice.MixerDevice.crossfade_assignments.NONE
			else:
				track.mixer_device.crossfade_assign = crossfade_assign
	
	
	def assign_crossfade(self, value, mode, status):
		# ignore CC toggles (like on LPD8)
		if status == MIDI.CC_STATUS and not value:
			return
		
		track = self.song.view.selected_track
		if track == self.song.master_track:
			return
		
		assignments = MixerDevice.MixerDevice.crossfade_assignments
		mixer = track.mixer_device
		
		if status == MIDI.NOTEON_STATUS or (not mode == MIDI.ABSOLUTE and value > 0):
			if mixer.crossfade_assign == assignments.NONE:
				mixer.crossfade_assign = assignments.A
			elif mixer.crossfade_assign == assignments.A:
				mixer.crossfade_assign = assignments.B
			else:
				mixer.crossfade_assign = assignments.NONE
		elif status == MIDI.CC_STATUS:
			if mode == MIDI.ABSOLUTE:
				if value < 64:
					mixer.crossfade_assign = assignments.A
				elif value > 64:
					mixer.crossfade_assign = assignments.B
				else:
					mixer.crossfade_assign = assignments.NONE
			else:
				# relative values < 0
				if mixer.crossfade_assign == assignments.B:
					mixer.crossfade_assign = assignments.A
				elif mixer.crossfade_assign == assignments.NONE:
					mixer.crossfade_assign = assignments.B
				else:
					mixer.crossfade_assign = assignments.NONE
	
	
