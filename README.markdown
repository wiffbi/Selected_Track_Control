Selected Track Control for Ableton Live
=======================================

Current version is 1.3.6 – released July 25, 2014.  
Compatible with Live 7,8 and 9


Control the currently selected track via common MIDI messages
-------------------------------------------------------------

Selected Track Control is a *MIDI Remote Script* for Ableton Live, that gives access to common settings of the currently selected track (arm, mute, solo, volume, pan, etc.) as well as the currently selected device (on/off, parameters, banks) via common MIDI messages. Furthermore some global controls are instantly mapped as well, so no manual configuration of the Live-set is necessary and these mappings are instantly available to older Live-sets as well.

Among the mapped functionality is:

*	**arm** (record-enable), **solo** and **mute** the selected track
*	control **volume, pan** and **send 1-4** of the selected track
*	**toggle monitoring** from On, In, Off the selected track
*	**toggle metronom, overdub, punch-in, punch-out, record** without having to manually assign them
*	**in-/decrease tempo**
*	**navigate session-view** without it having focus (up/down, left/right, first/last)
*	**launch scenes and clips** (next/previous, next/previous available)
*	…

For full reference see [MIDI Implementation Chart.](http://stc.wiffbi.com/midi-implementation-chart.html)


**Note:** There is an accompanying app for Mac OS X called **![App-Icon](http://stc.wiffbi.com/img/icon-16.png) Kimidi**. This app transforms global keyboard shortcuts into MIDI messages, which are sent to Ableton Live (and this *MIDI Remote Script*) on a virtual MIDI-port (created by the app automatically itself). **This allows instant keyboard-control of lots of features in Ableton Live** that either would require prior, manual configuration of each Live-set or aren't possible at all (such as using the same keyboard shortcut for e.g. the mute button – but always on the selected track).

More information and the app itself can be found on the [project’s homepage.](http://stc.wiffbi.com/)



License
-------------------
This work is licensed under the "Simplified BSD License" / "FreeBSD License"
see License.txt

*The previous CC Attribution license did not make sense. I made this software, so you can use it, do whatever you want to it and especially have fun with it! To be nice: if you make something with it, let me know!*



System Requirements
-------------------
Ableton Live 7 (some features require 8 or 9)




Installation
------------

Either download the zip from [http://stc.wiffbi.com/](http://stc.wiffbi.com/) and unzip or get the source from github.

1.	Stop Live if it is running.
2.	Add *Selected_Track_Control* to Ableton Live's MIDI Remote Scripts

	The folder `Selected_Track_Control` contains the MIDI Remote Script. To install, open Finder and locate the Ableton Live-application, right click on Live and choose *show package contents*. In there go to the folder `Contents/App-Resources/MIDI Remote Scripts/` and move the folder `Selected_Track_Control` in there.

3.	Start Live.
4.	Enable **Selected Track Control** as a Control Surface in Live

	In Live’s Preferences go to the *MIDI Sync* tab and select *Selected Track Control* in the dropdown list of available Control Surfaces. As MIDI Input select your controller’s MIDI-port. A MIDI Output is not needed.
	






Customize MIDI messages
-----------------------

The MIDI message, which **Selected Track Control** reacts upon, are defined in settings.py

You can change them there to match your needs, but be careful not to use the same note- or CC-number twice as this might result in unexpected behaviour.








Changelog
---------

### Version 1.3.6 (released July 25, 2014) ###

Added Live 9 features
- toggle arrangement_overdub with Note(117)
- toggle session_automation_record with Note(118)


### Version 1.3.5 (released Nov 4, 2013) ###

Added arm flip (Note 115)
Added solo flip (Note 116)


### Version 1.3.4 (released Oct 31, 2013) ###

Added lock to device via MIDI (through GUI was always possible)
Added re-enable automation
Added nudge tempo
Added global groove amount


### Version 1.3.3 (released Oct 21, 2013) ###

Added compatibility for clip launch modes (especially "Gate")


### Version 1.3.2 (released Aug 9, 2013) ###

Fixed blue-hand for initial device selection


### Version 1.3.1 (released Aug 8, 2013) ###

Fixed blue-hand when changing tracks - it is now always the selected device


### Version 1.3.0 (released Aug 7, 2013) ###

Added Live 9 API-features such as create/duplicate/delete clip/track/scene


### Version 1.2.9 (released May 15, 2013) ###

Added compatibility for Live 9


### Version 1.2.8 (released Sept 26, 2012) ###

Added dedicated tart, stop and continue-playing commands - this is useful for e.g. hitting stop 3 times in row for MIDI panic functionality  
Fixed scrub/rewind bug


### Version 1.2.7 (released Mar 14, 2012) ###

Added select scene/track by number directly by MIDI value  
Added toggle selected clipslot play/stop


### Version 1.2.6 (released Feb 7, 2012) ###

Added support for back-to-arranger button.


### Version 1.2.5 (released Nov 18, 2011) ###

Added toggle to fold/unfold automation lane in Arrangement.


### Version 1.2.4 (released Nov 14, 2011) ###

Added crossfader assignment and control. Added cue volume.
Fixed tracks navigation when group track is folded.


### Version 1.2.3 (released Sept 29, 2011) ###

Added notes and absolute MIDI CC triggers for quantization control


### Version 1.2.2 (released Sept 27, 2011) ###

Added quantization control - control MIDI recording quantization and clip launch quantization via MIDI.


### Version 1.2.1 (released Aug 17, 2011) ###

Added View control - select which main views are visible in the GUI (Browser, Session/Arrangement, Detail Clip/Devices)
Added ParamSetter for custom Device-handlers. Currently only Looper has a custom handler for its "State"-parameter. Note though, that Looper’s API support is very limited. Using Looper via _MIDI Remote Scripts_ is only useful if you are already in play mode (so no set-tempo functionality) and if you record for a predefined length.


### Version 1.2 (released Aug 8, 2011) ###

Added Device selection and control


### Version 1.1.8 (released Jun 22, 2011)

Auto-arm track on selection now works when using the mouse! 
Added _scrubbing_ in Arrangement-View as well as _select playing clip-slot_ in Session-View.


### Version 1.1.7 (released Jun 16, 2011)

made CCs for toggled elements behave like Note (so ignore zero-values) – this is useful for pad-controllers, that also send CCs like the LPD8.
improved auto-arm on selection if STC.app is used – thanks to new MIDI-loopback functionality in STC.app, auto-arm now works when selecting the track via mouse too! As a default has\_midi\_loopback is deactivated.


### Version 1.1.6 (released Apr 21, 2011)

added global DEFAULT_CHANNEL to easily make STC listen on another MIDI channel


### Version 1.1.5 (released Apr 14, 2011)

made settings optional (so you don’t have to define all controls for Live – useful if you use STC for your own MIDI controller)


### Version 1.1.4 (released Mar, 2011)

no changes, just matching release number for Selected Track Control.app (which added support for only being active when Live is front-most app)


### Version 1.1.3 (released Feb 19, 2011)

Fixed and added some global controls (play/pause/play selection as well as undo/redo), added stop-controls to selected and all tracks


### Version 1.1.2 (released Feb 18, 2011)

Improved Session-Navigation:

*	Walk through tracks/scenes via MIDI Note-events (Notes 82-85)
*	Navigate tracks/scenes with absolut MIDI CC (tracks/scenes are distributed evenly across the whole range of 0-127)


### Version 1.1.1 (released Feb 17, 2011)

Small bugfix concerning absolute MIDI CC controlling volume, pan, etc.


### Version 1.1 (released Feb 16, 2011)

Added several new features such as:

*	**Auto-arm on selection** arms a track automatically when selected through STC
*	**Solo kill** deactivates any active soloing on any track independent of the track your on
*	**Mute flip** mutes active tracks and unmutes muted tracks
*	**Tap Tempo** (Live 8 only) instantly mapped – no previous manual mapping required

Made STC more versatile by supporting a wider range of MIDI commands (use it with your own MIDI controller!)

*	**Support for absolute and relative MIDI CC values** (7-bit only) – no more rel2comp-bindings; feel free to use STC with your custom MIDI controller! Some default MIDI CC bindings already pre-defined – for more info see MIDI Implementation Chart
*	**Unlimited sends** – control effect-level to as many sends as you need, you are only limited by your MIDI controller (using keyboard shortcuts only sends 1-4 are available)


### Version 1.0.1 (released June 7, 2010)

This is a maintenance release. The following items were fixed and/or added:

*	fixed panning issue (panning left was broken)
*	added version numbers and changelog


### Version 1.0 (released May 28, 2010)

First public release.
