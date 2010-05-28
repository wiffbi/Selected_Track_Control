#import Live

from consts import *
import settings
#from Logging import log

class SessionControl:
	__module__ = __name__
	__doc__ = "Session parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		#log("SessionControl::__init__")
		self.c_instance = c_instance
		if c_instance:
			self.song = c_instance.song()
		
		
		self.midi_callbacks = {
			NOTEON_STATUS: (
				(settings.NOTE_PLAY_SELECTED_SCENE, self.fire_selected_scene),
				(settings.NOTE_PLAY_NEXT_SCENE, self.fire_next_scene),
				(settings.NOTE_PLAY_PREV_SCENE, self.fire_previous_scene),
				
				(settings.NOTE_FIRST_SCENE, self.select_first_scene),
				(settings.NOTE_LAST_SCENE, self.select_last_scene),
				
				(settings.NOTE_PLAY_SELECTED_CLIP, self.fire_selected_clip_slot),
				(settings.NOTE_PLAY_NEXT_CLIP, self.fire_next_clip_slot),
				(settings.NOTE_PLAY_PREV_CLIP, self.fire_previous_clip_slot),
				(settings.NOTE_PLAY_NEXT_AVAILABLE_CLIP, self.fire_next_available_clip_slot),
				(settings.NOTE_PLAY_PREV_AVAILABLE_CLIP, self.fire_previous_available_clip_slot),
				
				(settings.NOTE_FIRST_TRACK, self.select_first_track),
				(settings.NOTE_LAST_TRACK, self.select_last_track)
			),
			CC_STATUS: (
				(settings.CC_SCENE_SCROLL, self.scroll_scenes_by),
				(settings.CC_TRACK_SCROLL, self.scroll_tracks_by)
			)
		}
		
		
		# register callbacks on selected_track_controller
		for status, callbacks in self.midi_callbacks.items():
			for (key, callback) in callbacks:
				selected_track_controller.register_midi_callback(status, key, callback)

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
	
	
	
	
	
	def fire_selected_scene(self, velocity):
		self.song.view.selected_scene.fire()
	
	def fire_next_scene(self, velocity):
		scene = self.get_scene_by_delta(self.song.view.selected_scene, 1)
		scene.fire()
		self.song.view.selected_scene = scene
		
	def fire_previous_scene(self, velocity):
		scene = self.get_scene_by_delta(self.song.view.selected_scene, -1)
		scene.fire()
		self.song.view.selected_scene = scene
	
	
	def scroll_scenes_by(self, d_value):
		self.song.view.selected_scene = self.get_scene_by_delta(self.song.view.selected_scene, d_value)
	def select_first_scene(self, velocity):
		self.song.view.selected_scene = self.song.scenes[0]
	def select_last_scene(self, velocity):
		self.song.view.selected_scene = self.song.scenes[len(self.song.scenes)-1]
	
	
	def scroll_tracks_by(self, d_value):
		self.song.view.selected_track = self.get_track_by_delta(self.song.view.selected_track, d_value)
	
	def select_first_track(self, velocity):
		tracks = self.song.tracks
		if self.song.view.selected_track == self.song.master_track:
			self.song.view.selected_track = tracks[len(tracks)-1]
		else:
			self.song.view.selected_track = tracks[0]
	
	def select_last_track(self, velocity):
		if self.song.view.selected_track == self.song.master_track:
			return
		
		tracks = self.song.tracks
		# mimics Live's behaviour: if last track is selected, select master-track
		if self.song.view.selected_track == tracks[len(tracks)-1]:
			self.song.view.selected_track = self.song.master_track
		else:
			self.song.view.selected_track = tracks[len(tracks)-1]
	
	
	
	
	
	
	def fire_selected_clip_slot(self, velocity):
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
	
	
	def fire_next_clip_slot(self, velocity):
		self.fire_clip_slot_by_delta(1, False)
		
	def fire_next_available_clip_slot(self, velocity):
		self.fire_clip_slot_by_delta(1, True)
	
	def fire_previous_clip_slot(self, velocity):
		self.fire_clip_slot_by_delta(-1, False)
		
	def fire_previous_available_clip_slot(self, velocity):
		self.fire_clip_slot_by_delta(-1, True)
