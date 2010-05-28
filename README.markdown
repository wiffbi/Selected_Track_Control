Selected Track Control for Ableton Live
=======================================

Control the currently selected track via common MIDI messages
-------------------------------------------------------------

Selected Track Control is a *MIDI Remote Script* for Ableton Live, that gives access to common settings of the currently selected track (arm, mute, solo, volume, pan, etc.) via common MIDI messages. Furthermore some global controls are instantly mapped as well, so no manual configuration of the Live-set is necessary and these mappings are instantly available to older Live-sets as well.

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




Installation
------------

Either download the zip from [http://stc.wiffbi.com/](http://stc.wiffbi.com/) and unzip or get the source from github.

1.	Stop Live if it is running.
2.	Add *Selected_Track_Control* to Ableton Live's MIDI Remote Scripts

	The folder `Selected_Track_Control` contains the MIDI Remote Script. To install, open Finder and locate the Ableton Live-application, right click on Live and choose *show package contents*. In there go to the folder `Contents/App-Resources/MIDI Remote Scripts/` and move the folder `Selected_Track_Control` in there.

3.	Start Live.
4.	Enable **Selected Track Control** as a Control Surface in Live

	In Live’s Preferences go to the *MIDI Sync* tab and select *Selected Track Control* in the dropdown list of available Control Surfaces. As MIDI Input select your controller’s MIDI-port. A MIDI Output is not needed.
	
	**Note:** There is an accompanying App for Mac OS X called **![App-Icon](http://stc.wiffbi.com/img/icon-16.png) Selected Track Control**. This app transforms keyboard shortcuts into MIDI messages, which are sent on the virtual MIDI-port called *STC Virtual IN*.
	More information and the app itself are on the [project’s homepage.](http://stc.wiffbi.com/)


