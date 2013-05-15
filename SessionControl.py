import MIDI
import settings
from Logging import log

from Control import Control

class SessionControl(Control):
#	__module__ = __name__
	__doc__ = "Session parameters of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		if settings.auto_select_playing_clip:
			self.song.view.add_selected_track_listener(self.on_track_selected)
	
	def get_midi_bindings(self):
		return (
			("play_selected_scene", self.fire_selected_scene),
			("play_next_scene", self.fire_next_scene),
			("play_prev_scene", self.fire_previous_scene),
			
			("first_scene", self.select_first_scene),
			("last_scene", self.select_last_scene),
			
			("play_selected_clip", self.fire_selected_clip_slot),
			("toggle_selected_clip", self.toggle_selected_clip_slot),
			("play_next_clip", self.fire_next_clip_slot),
			("play_prev_clip", self.fire_previous_clip_slot),
			("play_next_available_clip", self.fire_next_available_clip_slot),
			("play_prev_available_clip", self.fire_previous_available_clip_slot),
			
			("select_playing_clip", self.select_playing_clip),
			("toggle_auto_select_playing_clip", self.toggle_auto_select_playing_clip),
			
			#("toggle_mute_selected_clip", self.toggle_mute_selected_clip),
			
			("stop_all_clips", self.stop_all_clips),
			("stop_selected_track", self.stop_selected_track),
			
			("first_track", self.select_first_track),
			("last_track", self.select_last_track),
			
			("scroll_scenes", self.scroll_scenes),
			("scroll_tracks", self.scroll_tracks),
			
			("select_scene", self.select_scene),
			("select_track", self.select_track),
			
			("prev_scene", lambda value, mode, status: self.scroll_scenes(-1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)),
			("next_scene", lambda value, mode, status: self.scroll_scenes(1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)),
			("prev_track", lambda value, mode, status: self.scroll_tracks(-1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)),
			("next_track", lambda value, mode, status: self.scroll_tracks(1, MIDI.RELATIVE_TWO_COMPLIMENT, MIDI.CC_STATUS)),
			
			("toggle_track_fold", self.toggle_track_fold)
		)
	
	
	def auto_arm_track(self, track):
		# fallback to auto-arm if no midi loopback is available
		if settings.auto_arm and not settings.has_midi_loopback:
			if track.can_be_armed:
				track.arm = True
			for t in self.song.tracks:
				if not t == track and t.can_be_armed:
					t.arm = False
	
	
	
	
	
	def on_track_selected(self):
		self.select_playing_clip(127, MIDI.ABSOLUTE, MIDI.NOTEON_STATUS)
	
	
	def select_playing_clip(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		
		for clip_slot in self.song.view.selected_track.clip_slots:
			if clip_slot.has_clip and clip_slot.clip.is_playing:
				self.song.view.highlighted_clip_slot = clip_slot
	
	
	def toggle_auto_select_playing_clip(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		
		settings.auto_select_playing_clip = not settings.auto_select_playing_clip
		
		if settings.auto_select_playing_clip:
			self.on_track_selected()
			self.song.view.add_selected_track_listener(self.on_track_selected)
		else:
			self.song.view.remove_selected_track_listener(self.on_track_selected)
	
	
	
	def stop_all_clips(self, value, mode, status):
		self.song.stop_all_clips()
	
	
	
	def get_all_tracks(self, only_visible = False):
		tracks = []
		for track in self.song.tracks:
			if not only_visible or track.is_visible:
				tracks.append(track)
				
		for track in self.song.return_tracks:
			tracks.append(track)
		tracks.append(self.song.master_track)
		return tracks
		
	
	# helper function to go from one track to the other
	def get_track_by_delta(self, track, d_value):
		tracks = self.get_all_tracks(only_visible = True)
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
	
	
	
	
	
	
	def toggle_track_fold(self, value, mode, status):
		# ignore CC toggles (like on LPD8)
		if status == MIDI.CC_STATUS and not value:
			return
		
		
		track = self.song.view.selected_track
		if not track.is_foldable:
			return
		
		if status == MIDI.NOTEON_STATUS:
			track.fold_state = not track.fold_state
		elif status == MIDI.CC_STATUS:
			if  mode == MIDI.ABSOLUTE:
				track.fold_state = value < 64
			else:
				track.fold_state = value < 0
	
#	def toggle_mute_selected_clip(self, value, mode):
#		log("toggle_mute_selected_clip")
#		clip_slot = self.song.view.highlighted_clip_slot
#		clip = self.song.view.detail_clip
#		#if clip_slot and clip_slot.has_clip():
#		#	clip_slot.clip.muted = not clip_slot.clip.muted
#		
#		if clip:
#			log("clip available")
#			for slot in dir(clip):
#				#try:
#				#	attr = getattr(clip, slot)
#				#except:
#				#	attr = 'no_attr'
#				#log(attr+", "+slot)
#				log(slot)
#			log(getattr(clip, '__doc__', None) or 'no documentation')
#		else:
#			log("no clip available")
#		
#		log("toggle_mute_selected_clip done")
	
	def fire_selected_scene(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.view.selected_scene.fire()
	
	def fire_next_scene(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		scene = self.get_scene_by_delta(self.song.view.selected_scene, 1)
		scene.fire()
		self.song.view.selected_scene = scene
		
	def fire_previous_scene(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		scene = self.get_scene_by_delta(self.song.view.selected_scene, -1)
		scene.fire()
		self.song.view.selected_scene = scene
	
	
	def scroll_scenes(self, value, mode, status):
		if mode == MIDI.ABSOLUTE:
			# invert value (127-value), somehow feels more natural to turn left to go fully down and right to go up
			# also when assigning this to a fader this is more natural as up is up and down is down
			index = int((127-value)/(128.0/len(self.song.scenes)))
			self.song.view.selected_scene = self.song.scenes[index]
		else:
			self.song.view.selected_scene = self.get_scene_by_delta(self.song.view.selected_scene, value)
	def select_first_scene(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.view.selected_scene = self.song.scenes[0]
	def select_last_scene(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.view.selected_scene = self.song.scenes[len(self.song.scenes)-1]
	
	
	def scroll_tracks(self, value, mode, status):
		if mode == MIDI.ABSOLUTE:
			tracks = self.get_all_tracks(only_visible = True)
			index = int(value/(128.0/len(tracks)))
			self.song.view.selected_track = tracks[index]
		else:
			self.song.view.selected_track = self.get_track_by_delta(self.song.view.selected_track, value)
		
		self.auto_arm_track(self.song.view.selected_track)
	
	
	
	def select_first_track(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		tracks = self.song.tracks
		if self.song.view.selected_track == self.song.master_track:
			self.song.view.selected_track = tracks[len(tracks)-1]
		else:
			self.song.view.selected_track = tracks[0]
		
		self.auto_arm_track(self.song.view.selected_track)
	
	def select_last_track(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		if self.song.view.selected_track == self.song.master_track:
			return
		
		tracks = self.song.tracks
		# mimics Live's behaviour: if last track is selected, select master-track
		if self.song.view.selected_track == tracks[len(tracks)-1]:
			self.song.view.selected_track = self.song.master_track
		else:
			self.song.view.selected_track = tracks[len(tracks)-1]
		
		self.auto_arm_track(self.song.view.selected_track)
	
	def stop_selected_track(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.view.selected_track.stop_all_clips()
	
	
	
	
	
	def select_scene(self, value, mode, status):
		scenes = self.song.scenes
		index = min(len(scenes)-1, value)
		self.song.view.selected_scene = scenes[index]
	
	def select_track(self, value, mode, status):
		tracks = self.song.tracks
		index = min(len(tracks)-1, value)
		self.song.view.selected_track = tracks[index]
	
	
	def fire_selected_clip_slot(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		if self.song.view.highlighted_clip_slot:
			self.song.view.highlighted_clip_slot.fire()
	
	def toggle_selected_clip_slot(self, value, mode, status):
		clip_slot = self.song.view.highlighted_clip_slot
		if clip_slot and clip_slot.has_clip and not (clip_slot.clip.is_playing or clip_slot.clip.is_triggered):
			self.fire_selected_clip_slot(value, mode, status)
		else:
			self.stop_selected_track(value, mode, status)
	
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
		
		if clip_slot:
			clip_slot.fire()
			self.song.view.highlighted_clip_slot = clip_slot
	
	
	def fire_next_clip_slot(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.fire_clip_slot_by_delta(1, False)
		
	def fire_next_available_clip_slot(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.fire_clip_slot_by_delta(1, True)
	
	def fire_previous_clip_slot(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.fire_clip_slot_by_delta(-1, False)
		
	def fire_previous_available_clip_slot(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.fire_clip_slot_by_delta(-1, True)
