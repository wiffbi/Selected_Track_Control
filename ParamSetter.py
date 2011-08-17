import Live

import MIDI
import settings
from Logging import log







# general device parameter setter
def general_device(song, device, param, value, mode, status):
	param_range = param.max - param.min
	#log("set %s (%s): %s - %s" % (param.name, param.value, param.min, param.max))
	if param.is_quantized:
		if status == MIDI.CC_STATUS and mode == MIDI.ABSOLUTE:
			# absolute CC
			param.value = round(param_range*value/127.0 + param.min)
		else:
			# relative CC or NOTE
			if param_range == 1 or status == MIDI.NOTEON_STATUS:
				# circle through quantized values
				p_value = param.value + value
				if p_value > param.max:
					# values can be bigger than one => take overlap and add it min
					p_value = param.min + (p_value % (param_range + 1))
				elif p_value < param.min:
					p_value = param.max - ((p_value - 1) % (param_range + 1))
				param.value = p_value
			else:
				# range is bigger than on/off and we have relative CC
				# => do NOT circle through quantized values
				param.value = max(param.min, min(param.max, param.value + value))
	else:
		if mode == MIDI.ABSOLUTE:
			param.value = param_range*value/127.0 + param.min
		else:
			#param.value = max(param.min, min(param.max, param.value + (value/100.0)))
			if param_range > 4:
				param.value = max(param.min, min(param.max, param.value + value))
			else:
				param.value = max(param.min, min(param.max, param.value + param_range*value/127.0))

def looper(song, device, param, value, mode, status):
	if not param.name == "State":
		general_device(song, device, param, value, mode, status)
		return
	# get current state:
	# 1 - record; 0 - stop; 2 - play; 3 - overdub;
	if not value:
		return
	
	# floor value to a stepping value
	if param.value == 3:
		# if "overdub" is active, step back to "play"
		value = -1
	else:
		value = 1
	
	if param.value == 0:
		# enable play for record to work
		song.continue_playing()
	
	param.value = param.value + value
	
	#general_device(song, device, param, value, mode, status)











setters = {
	"Looper": looper
}

def get(device):
	if device.name in setters:
		return setters[device.name]
	return general_device