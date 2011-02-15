#from settings import debug_mode

def log(msg):
	#if not debug_mode:
	#	return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py','SelectedTrackControl.log'), 'a')
	f.write(msg+"\n")
	f.close()
