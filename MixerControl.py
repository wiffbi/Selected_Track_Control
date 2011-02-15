import MIDI
import settings
#from Logging import log

from Control import Control

class MixerControl(Control):
#	__module__ = __name__
	__doc__ = "Mixer parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		# each callback is (mapping, callback)
		# mappings are taken from settings.midi_mapping
		m = settings.midi_mapping
		self.midi_callbacks = (
			(m["arm"], self.toggle_arm),
			(m["arm_exclusive"], self.toggle_arm_exclusive),
			(m["solo"], self.toggle_solo),
			(m["solo_exclusive"], self.toggle_solo_exclusive),
			(m["solo_kill"], self.solo_kill),
			(m["mute"], self.toggle_mute),
			(m["mute_exclusive"], self.toggle_mute_exclusive),
			(m["mute_kill"], self.mute_kill),
			(m["mute_flip"], self.mute_flip),
			(m["reset_pan"], self.reset_pan),
			(m["reset_volume"], self.reset_volume),
			(m["switch_monitoring"], self.switch_monitoring),
			
			(m["volume"], self.set_volume),
			(m["pan"], self.set_pan)
		)
		
		
		# use helper-functions to set up callback via lambda-functions
		# a closure inside the lambda-functions is needed, so i is always the current i
		
		#if "reset_sends" in settings.midi_mapping:
		#	for i in range(len(settings.midi_mapping["reset_sends"])):
		#		self.setup_send_reset(i, settings.midi_mapping["reset_sends"][i])
		
		if "sends" in settings.midi_mapping:
			for i in range(len(settings.midi_mapping["sends"])):
				self.setup_send_set(i, settings.midi_mapping["sends"][i])
		
		
		# register midi_callbacks via parent
		self.register_midi_callbacks()
		
	def disconnect(self):
		pass
	
	
	def setup_send_reset(self, i, mappings):
		# always make sure mappings is a tuple
		if isinstance(mappings, MIDI.MIDICommand):
			mappings = (mappings,)
		
		callback = lambda value, mode : self.reset_send(i)
		
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
	
	def solo_kill(self, value, mode):
		for t in self.get_tracks():
			t.solo = False
	
	
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
		
	def mute_kill(self, value, mode):
		for t in self.get_tracks():
			t.mute = False
	
	def mute_flip(self, value, mode):
		for t in self.song.tracks:
			t.mute = not t.mute
	
	
	
	def set_volume(self, value, mode):
		param = self.song.view.selected_track.mixer_device.volume
		if mode == MIDI.ABSOLUTE:
			param.value = value/127
		else:
			param.value = max(0.0, min(1.0, param.value + (value/200.0)))
	
	def reset_volume(self, value, mode):
		self.song.view.selected_track.mixer_device.volume.value = settings.volume_default
	
	
	def set_pan(self, value, mode):
		param = self.song.view.selected_track.mixer_device.panning
		if mode == MIDI.ABSOLUTE:
			param.value = value-64/64
		else:
			param.value = max(-1.0, min(1.0, param.value + (value/100.0)))
	
	def reset_pan(self, value, mode):
		self.song.view.selected_track.mixer_device.panning.value = 0.0
	
	
	def set_send(self, i, value, mode):
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

