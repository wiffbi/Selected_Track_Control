import MIDI
import settings
#from Logging import log

from Control import Control

class SessionControl(Control):
#	__module__ = __name__
	__doc__ = "Session parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		
		self.auto_arm = settings.auto_arm
		
		# each callback is (mapping, callback)
		# mappings are taken from settings.midi_mapping
		m = settings.midi_mapping
		self.midi_callbacks = (
			(m["play_selected_scene"], self.fire_selected_scene),
			(m["play_next_scene"], self.fire_next_scene),
			(m["play_prev_scene"], self.fire_previous_scene),
			
			(m["first_scene"], self.select_first_scene),
			(m["last_scene"], self.select_last_scene),
			
			(m["play_selected_clip"], self.fire_selected_clip_slot),
			(m["play_next_clip"], self.fire_next_clip_slot),
			(m["play_prev_clip"], self.fire_previous_clip_slot),
			(m["play_next_available_clip"], self.fire_next_available_clip_slot),
			(m["play_prev_available_clip"], self.fire_previous_available_clip_slot),
			
			(m["toggle_mute_selected_clip"], self.toggle_mute_selected_clip),
			
			(m["stop_selected_track"], self.stop_selected_track),
			(m["toggle_auto_arm"], self.toggle_auto_arm),
			
			(m["first_track"], self.select_first_track),
			(m["last_track"], self.select_last_track),
			
			(m["scroll_scene"], self.scroll_scenes_by),
			(m["scroll_track"], self.scroll_tracks_by)
		)
		
		# register midi_callbacks via parent
		self.register_midi_callbacks()
	
	
	def disconnect(self):
		pass
	
	
	
	
	def get_all_tracks(self):
		return self.song.tracks + self.song.return_tracks + (self.song.master_track, )
	
	# helper function to go from one track to the other
	def get_track_by_delta(self, track, d_value):
		tracks = self.get_all_tracks()
		max_tracks = len(tracks)
		for i in range(max_tracks):
			if track == tracks[i]:
				return tracks[max((0, min(i+d_value, max_tracks-1)))]
	
	# helper function to go from one scene to the other
	def get_scene_by_delta(self, scene, d_value):
		scenes = self.song.scenes
		max_scenes = len(scenes)
		for i in range(max_scenes):
			if scene == scenes[i]:
				return scenes[max((0, min(i+d_value, max_scenes-1)))]
	
	
	
	
	
	def toggle_mute_selected_clip(self, value, mode):
		clip_slot = self.song.view.highlighted_clip_slot
		if clip_slot.has_clip():
			clip_slot.clip.muted = not clip_slot.clip.muted
	
	def fire_selected_scene(self, value, mode):
		self.song.view.selected_scene.fire()
	
	def fire_next_scene(self, value, mode):
		scene = self.get_scene_by_delta(self.song.view.selected_scene, 1)
		scene.fire()
		self.song.view.selected_scene = scene
		
	def fire_previous_scene(self, value, mode):
		scene = self.get_scene_by_delta(self.song.view.selected_scene, -1)
		scene.fire()
		self.song.view.selected_scene = scene
	
	
	def scroll_scenes_by(self, value, mode):
		if mode == MIDI.ABSOLUTE:
			# note: absolute mode does not make any sense here!
			pass
		else:
			self.song.view.selected_scene = self.get_scene_by_delta(self.song.view.selected_scene, value)
	def select_first_scene(self, value, mode):
		self.song.view.selected_scene = self.song.scenes[0]
	def select_last_scene(self, value, mode):
		self.song.view.selected_scene = self.song.scenes[len(self.song.scenes)-1]
	
	
	def scroll_tracks_by(self, value, mode):
		if mode == MIDI.ABSOLUTE:
			# note: absolute mode does not make any sense here!
			pass
		else:
			self.song.view.selected_track = self.get_track_by_delta(self.song.view.selected_track, value)
			if self.auto_arm:
				track = self.song.view.selected_track
				if track.can_be_armed:
					track.arm = True
				for t in self.song.tracks:
					if not t == track and t.can_be_armed:
						t.arm = False
	
	def toggle_auto_arm(self, value, mode):
		self.auto_arm = not self.auto_arm
		
		track = self.song.view.selected_track
		if track.can_be_armed:
			track.arm = self.auto_arm
		
		if self.auto_arm:
			for t in self.song.tracks:
				if not t == track and t.can_be_armed:
					t.arm = False
	
	
	
	
	def select_first_track(self, value, mode):
		tracks = self.song.tracks
		if self.song.view.selected_track == self.song.master_track:
			self.song.view.selected_track = tracks[len(tracks)-1]
		else:
			self.song.view.selected_track = tracks[0]
	
	def select_last_track(self, value, mode):
		if self.song.view.selected_track == self.song.master_track:
			return
		
		tracks = self.song.tracks
		# mimics Live's behaviour: if last track is selected, select master-track
		if self.song.view.selected_track == tracks[len(tracks)-1]:
			self.song.view.selected_track = self.song.master_track
		else:
			self.song.view.selected_track = tracks[len(tracks)-1]
	
	def stop_selected_track(self, value, mode):
		for clip_slot in self.song.view.selected_track.clip_slots:
			if clip_slot.has_clip and clip_slot.clip.is_playing:
				clip_slot.clip.stop()
				break
	
	
	
	
	
	def fire_selected_clip_slot(self, value, mode):
		self.song.view.highlighted_clip_slot.fire()
	
	
	def get_clip_slot_by_delta_bool(self, current_clip_slot, track, d_value, bool_callable):
		clip_slots = track.clip_slots
		max_clip_slots = len(clip_slots)
		
		found = False
		if d_value > 0:
			the_range = range(max_clip_slots)
		else:
			the_range = range(max_clip_slots-1, -1, -1)
		
		for i in the_range:
			clip_slot = clip_slots[i]
			if found and bool_callable(clip_slot):
				return clip_slot
			
			if clip_slot == current_clip_slot:
				found = True
		
		
	
	def fire_clip_slot_by_delta(self, d_value, available):
		current_clip_slot = self.song.view.highlighted_clip_slot
		track = self.song.view.selected_track
		
		if available:
			if track.arm:
				clip_slot = self.get_clip_slot_by_delta_bool(current_clip_slot, track, d_value, lambda x: x.has_stop_button and not x.has_clip)
			else:
				clip_slot = self.get_clip_slot_by_delta_bool(current_clip_slot, track, d_value, lambda x: x.has_clip)
		else:
			clip_slot = self.get_clip_slot_by_delta_bool(current_clip_slot, track, d_value, lambda x: True)
		
		clip_slot.fire()
		self.song.view.highlighted_clip_slot = clip_slot
	
	
	def fire_next_clip_slot(self, value, mode):
		self.fire_clip_slot_by_delta(1, False)
		
	def fire_next_available_clip_slot(self, value, mode):
		self.fire_clip_slot_by_delta(1, True)
	
	def fire_previous_clip_slot(self, value, mode):
		self.fire_clip_slot_by_delta(-1, False)
		
	def fire_previous_available_clip_slot(self, value, mode):
		self.fire_clip_slot_by_delta(-1, True)
