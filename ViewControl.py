import Live

import MIDI
import settings
from Logging import log

from Control import Control

class ViewControl(Control):
#	__module__ = __name__
	__doc__ = "Device control section of SelectedTrackControl"
	
	def __init__(self, c_instance, selected_track_controller):
		Control.__init__(self, c_instance, selected_track_controller)
		
		self.view = Live.Application.get_application().view
		self.views = self.view.available_main_views()
		
		
	
	def get_midi_bindings(self):
		return (
			("toggle_browser", lambda value, mode, status : self.toggle_view(value, mode, status, "Browser")),
			("toggle_session_arranger", lambda value, mode, status : self.toggle_view(value, mode, status, ["Session", "Arranger"])),
			("toggle_detail", lambda value, mode, status : self.toggle_view(value, mode, status, "Detail")),
			("toggle_detail_clip_device", lambda value, mode, status : self.toggle_detail(value, mode, status, ["Detail/Clip", "Detail/DeviceChain"])),
			
			("toggle_detail_clip", lambda value, mode, status : self.toggle_detail(value, mode, status, "Detail/Clip")),
			("toggle_detail_device", lambda value, mode, status : self.toggle_detail(value, mode, status, "Detail/DeviceChain")),
		)
	
	
	
	def toggle_view(self, value, mode, status, view):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		
		if status == MIDI.CC_STATUS and mode == MIDI.ABSOLUTE:
			if type(view) == type([]):
				index = len(view)*value / 128
				self.view.show_view(view[index])
				return
			else:
				if value < 64:
					self.view.hide_view(view)
				else:
					self.view.show_view(view)
			return
		
		
		if type(view) == type([]):
			for v in view:
				if self.view.is_view_visible(v):
					index = (view.index(v)+1) % len(view)
					self.view.show_view(view[index])
					return
		else:
			if self.view.is_view_visible(view):
				self.view.hide_view(view)
			else:
				self.view.show_view(view)
	
	
	
	
	
	def toggle_detail(self, value, mode, status, view):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		
		if status == MIDI.CC_STATUS and mode == MIDI.ABSOLUTE:
			if type(view) == type([]):
				if not self.view.is_view_visible("Detail"):
					self.view.show_view("Detail")
				else:
					index = len(view)*value / 128
					self.view.show_view(view[index])
					return
			else:
				if value < 64:
					self.view.hide_view("Detail")
				else:
					self.view.show_view("Detail")
					self.view.show_view(view)
			return
		
		
		
		if type(view) == type([]):
			# toggle between multiple DetailViews => make sure Detail is visible
			if not self.view.is_view_visible("Detail"):
				self.view.show_view("Detail")
			else:
				# detail is visible => toggle between views
				for v in view:
					if self.view.is_view_visible(v):
						index = (view.index(v)+1) % len(view)
						self.view.show_view(view[index])
						return
		else:
			if self.view.is_view_visible("Detail"):
				if self.view.is_view_visible(view):
					self.view.hide_view("Detail")
				else:
					self.view.show_view(view)
			else:
				self.view.show_view("Detail")
				self.view.show_view(view)
			






