#import Live

from consts import *
import settings
#from Logging import log

class MixerControl:
	__module__ = __name__
	__doc__ = "Mixer parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		#log("MixerControl::__init__")
		self.c_instance = c_instance
		self.song = c_instance.song()
		
		#self.on_track_selected_callback = lambda : self.on_track_selected()
		#song.view.add_selected_track_listener(self.on_track_selected_callback)
		#self.track_selected = 0
		
		self.midi_callbacks = {
			NOTEON_STATUS: [
				(settings.NOTE_ARM, self.toggle_arm),
				(settings.NOTE_ARM_EXCLUSIVE, self.toggle_arm_exclusive),
				(settings.NOTE_SOLO, self.toggle_solo),
				(settings.NOTE_SOLO_EXCLUSIVE, self.toggle_solo_exclusive),
				(settings.NOTE_MUTE, self.toggle_mute),
				(settings.NOTE_MUTE_EXCLUSIVE, self.toggle_mute_exclusive),
				(settings.NOTE_PAN_CENTER, self.reset_pan),
				(settings.NOTE_VOLUME_RESET, self.reset_volume),
				(settings.NOTE_SWITCH_MONITORING, self.switch_monitoring),
				#(settings.NOTE_SENDS_RESET[0], self.reset_send_1),
				#(settings.NOTE_SENDS_RESET[1], self.reset_send_2),
				#(settings.NOTE_SENDS_RESET[2], self.reset_send_3),
				#(settings.NOTE_SENDS_RESET[3], self.reset_send_4)
			],
			CC_STATUS: [
				(settings.CC_VOLUME, self.increase_volume_by),
				(settings.CC_PAN, self.increase_pan_by),
				# for backwards-compatibility
				(settings.CC_VOLUME_BC, self.increase_volume_by),
				(settings.CC_PAN_BC, self.increase_pan_by)
			]
		}
		
		# use helper-functions to set up callback via lambda-functions
		# a closure inside the lambda-functions is needed, so i is always the current i
		for i in range(len(settings.NOTE_SENDS_RESET)):
			#self.midi_callbacks.get(NOTEON_STATUS).append((settings.NOTE_SENDS_RESET[i], lambda velocity : self.reset_send(i)))
			self.setup_send_reset(i)
		
		for i in range(len(settings.CC_SENDS)):
			#self.midi_callbacks[CC_STATUS].append((settings.CC_SENDS[i], lambda d_value : self.increase_send_by(i, d_value)))
			self.setup_send_increase(i)
		
		
		# register callbacks on selected_track_controller
		for status, callbacks in self.midi_callbacks.items():
			for (key, callback) in callbacks:
				selected_track_controller.register_midi_callback(status, key, callback)

	def disconnect(self):
		pass
		#self.song.view.remove_selected_track_listener(self.on_track_selected_callback)
	
	
	def setup_send_reset(self, i):
		self.midi_callbacks.get(NOTEON_STATUS).append((settings.NOTE_SENDS_RESET[i], lambda velocity : self.reset_send(i)))
	def setup_send_increase(self, i):
		self.midi_callbacks[CC_STATUS].append((settings.CC_SENDS[i], lambda d_value : self.increase_send_by(i, d_value)))

#	def on_track_selected(self):
#		#self.track_selected = 1
#		#log("SelectedTrackMixerControl track selected")
#		#self.c_instance.request_rebuild_midi_map()
#		pass
	


#	# this gets called first from Live
#	def build_midi_map(self, script_handle, midi_map_handle):
#		log("SelectedTrackMixerControl::build_midi_map")
#		
#		channel = settings.MIDI_CHANNEL
#		
#		for note in [\
#			settings.NOTE_ARM, \
#			settings.NOTE_ARM_EXCLUSIVE, \
#			settings.NOTE_SOLO, \
#			settings.NOTE_SOLO_EXCLUSIVE, \
#			settings.NOTE_MUTE, \
#			settings.NOTE_MUTE_EXCLUSIVE, \
#			settings.NOTE_PAN_CENTER, \
#			settings.NOTE_VOLUME_RESET, \
#			settings.NOTE_SWITCH_MONITORING \
#			]:
#			Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, channel, note)
#		
#		# map controls manually as remapping everything on switching tracks is very performance-intensive
#		# alternative would be to just remap the CCs, but that would need an extra control interface
#		for cc in [\
#			settings.CC_VOLUME, \
#			settings.CC_PAN \
#			]:
#			Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc)
#		
#		
#		mode = Live.MidiMap.MapMode.relative_two_compliment
#		mixer_device = self.song.view.selected_track.mixer_device
#		
#		# map volume
#		parameter = mixer_device.volume
#		cc = settings.CC_VOLUME
#		Live.MidiMap.map_midi_cc(midi_map_handle,
#								parameter, channel, cc,
#								mode, True)
#		
#		# map pan relative
#		parameter = mixer_device.panning
#		cc = settings.CC_PAN
#		Live.MidiMap.map_midi_cc(midi_map_handle,
#								parameter, channel, cc,
#								mode, True)
#		
#		
#		# setup sends
#		sends = mixer_device.sends
#		for i in range(4):
#			if len(sends) > i:
#				Live.MidiMap.map_midi_cc(midi_map_handle,
#										sends[i], channel, settings.CC_SENDS[i],
#										mode, True)
#
#		for slot in dir(Live.MidiMap.MapMode):
#			try:
#				attr = getattr(obj, slot)
#			except:
#				attr = 'no_attr'
#			log(attr+", "+slot)
		#log(getattr(Live.MidiMap.MapMode, '__doc__', None) or 'no documentation')

	
	def get_tracks(self):
		return self.song.tracks + self.song.return_tracks
	
	
	
	
	
	
	def toggle_arm_track(self, track, exclusive):
		if track.can_be_armed:
			track.arm = not track.arm
		if exclusive: # arm exclusive
			for t in self.get_tracks():
				if not t == track and t.can_be_armed:
					t.arm = False
	def toggle_arm(self, velocity):
		# toggle exclusive depending on settings
		self.toggle_arm_track(self.song.view.selected_track, self.song.exclusive_arm)
	def toggle_arm_exclusive(self, velocity):
		# toggle exclusive depending on settings
		self.toggle_arm_track(self.song.view.selected_track, (not self.song.exclusive_arm))
	
	def toggle_solo_track(self, track, exclusive):
		track.solo = not track.solo
		if exclusive: # solo exclusive
			for t in self.get_tracks():
				if not t == track:
					t.solo = False
	def toggle_solo(self, velocity):
		# toggle exclusive depending on settings
		self.toggle_solo_track(self.song.view.selected_track, self.song.exclusive_solo)
	def toggle_solo_exclusive(self, velocity):
		# toggle exclusive depending on settings
		self.toggle_solo_track(self.song.view.selected_track, (not self.song.exclusive_solo))
	
	
	def toggle_mute_track(self, track, exclusive):
		track.mute = not track.mute
		if exclusive: # mute exclusive
			for t in self.get_tracks():
				if not t == track:
					t.mute = False
	def toggle_mute(self, velocity):
		self.toggle_mute_track(self.song.view.selected_track, False)
	def toggle_mute_exclusive(self, velocity):
		self.toggle_mute_track(self.song.view.selected_track, True)
		
	
	
	
	
	
	def increase_volume_by(self, d_value):
		param = self.song.view.selected_track.mixer_device.volume
		param.value = max(0.0, min(1.0, param.value + (d_value/200.0)))
	
	def reset_volume(self, velocity):
		self.song.view.selected_track.mixer_device.volume.value = settings.VOLUME_DEFAULT
	
	
	def increase_pan_by(self, d_value):
		param = self.song.view.selected_track.mixer_device.panning
		param.value = max(0.0, min(1.0, param.value + (d_value/100.0)))
	
	def reset_pan(self, velocity):
		self.song.view.selected_track.mixer_device.panning.value = settings.PAN_CENTER_VALUE
	
	
	def increase_send_by(self, i, d_value):
		#log("increase send %s by %s" % (i, d_value))
		param = self.song.view.selected_track.mixer_device.sends[i]
		if param:
			param.value = max(0.0, min(1.0, param.value + (d_value/100.0)))
	
	def reset_send(self, i):
		param = self.song.view.selected_track.mixer_device.sends[i]
		if param:
			param.value = 0.0
	
	
	def switch_monitoring(self, velocity):
		track = self.song.view.selected_track
		if (hasattr(track, "current_monitoring_state")):
			track.current_monitoring_state = (track.current_monitoring_state + 1) % len(track.monitoring_states.values)

