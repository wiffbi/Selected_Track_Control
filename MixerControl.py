import MIDI
import settings
#from Logging import log

class MixerControl(Control):
	__module__ = __name__
	__doc__ = "Mixer parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		super(c_instance, selected_track_controller)
		
		# each callback is (key, callback)
		# key is a key in settings.midi_mapping
		self.midi_callbacks = (
			("arm", self.toggle_arm),
			("arm_exclusive", self.toggle_arm_exclusive),
			("solo", self.toggle_solo),
			("sole_exclusive", self.toggle_solo_exclusive),
			("mute", self.toggle_mute),
			("mute_exclusive", self.toggle_mute_exclusive),
			("reset_pan", self.reset_pan),
			("reset_volume", self.reset_volume),
			("switch_monitoring", self.switch_monitoring),
			
			("volume", self.set_volume),
			("pan", self.set_pan)
		)
		
		# register midi_callbacks via parent
		self.register_midi_callbacks()
		
		
		# use helper-functions to set up callback via lambda-functions
		# a closure inside the lambda-functions is needed, so i is always the current i
		if "reset_sends" in settings.midi_mapping
			for i in range(len(settings.midi_mapping["reset_sends"])):
				self.setup_send_reset(i, settings.midi_mapping["reset_sends"][i])
		
		if "sends" in settings.midi_mapping
			for i in range(len(settings.midi_mapping["reset_sends"])):
				self.setup_send_set(i, settings.midi_mapping["reset_sends"][i])
		
	def disconnect(self):
		pass
	
	
	def setup_send_reset(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda velocity : self.reset_send(i)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
		
	def setup_send_set(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode : self.set_send(i, value, mode)
		
		for m in mappings:
			self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
		
	
	
	
	
	
	
	
	
	
	def get_tracks(self):
		return self.song.tracks + self.song.return_tracks
	
	
	
	
	
	
	def toggle_arm_track(self, track, exclusive):
		if track.can_be_armed:
			track.arm = not track.arm
		if exclusive: # arm exclusive
			for t in self.get_tracks():
				if not t == track and t.can_be_armed:
					t.arm = False
	def toggle_arm(self, value, mode):
		# toggle exclusive depending on settings
		self.toggle_arm_track(self.song.view.selected_track, self.song.exclusive_arm)
	def toggle_arm_exclusive(self, value, mode):
		# toggle exclusive depending on settings
		self.toggle_arm_track(self.song.view.selected_track, (not self.song.exclusive_arm))
	
	def toggle_solo_track(self, track, exclusive):
		track.solo = not track.solo
		if exclusive: # solo exclusive
			for t in self.get_tracks():
				if not t == track:
					t.solo = False
	def toggle_solo(self, value, mode):
		# toggle exclusive depending on settings
		self.toggle_solo_track(self.song.view.selected_track, self.song.exclusive_solo)
	def toggle_solo_exclusive(self, value, mode):
		# toggle exclusive depending on settings
		self.toggle_solo_track(self.song.view.selected_track, (not self.song.exclusive_solo))
	
	
	def toggle_mute_track(self, track, exclusive):
		track.mute = not track.mute
		if exclusive: # mute exclusive
			for t in self.get_tracks():
				if not t == track:
					t.mute = False
	def toggle_mute(self, value, mode):
		self.toggle_mute_track(self.song.view.selected_track, False)
	def toggle_mute_exclusive(self, value, mode):
		self.toggle_mute_track(self.song.view.selected_track, True)
		
	
	
	
	
	
	def set_volume(self, value, mode):
		param = self.song.view.selected_track.mixer_device.volume
		if mode == MIDI.ABSOLUTE:
			param.value = value/127
		else:
			param.value = max(0.0, min(1.0, param.value + (value/200.0)))
	
	def reset_volume(self, value, mode):
		self.song.view.selected_track.mixer_device.volume.value = settings.VOLUME_DEFAULT
	
	
	def set_pan(self, value, mode):
		param = self.song.view.selected_track.mixer_device.panning
		if mode == MIDI.ABSOLUTE:
			param.value = value-64/64
		else:
			param.value = max(-1.0, min(1.0, param.value + (value/100.0)))
	
	def reset_pan(self, value, mode):
		self.song.view.selected_track.mixer_device.panning.value = settings.PAN_CENTER_VALUE
	
	
	def set_send(self, i, value, mode):
		#log("increase send %s by %s" % (i, d_value))
		param = self.song.view.selected_track.mixer_device.sends[i]
		if param:
			if mode == MIDI.ABSOLUTE:
				param.value = value/127
			else:
				param.value = max(0.0, min(1.0, param.value + (value/100.0)))
	
	def reset_send(self, i):
		param = self.song.view.selected_track.mixer_device.sends[i]
		if param:
			param.value = 0.0
	
	
	def switch_monitoring(self, value, mode):
		track = self.song.view.selected_track
		if (hasattr(track, "current_monitoring_state")):
			track.current_monitoring_state = (track.current_monitoring_state + 1) % len(track.monitoring_states.values)

