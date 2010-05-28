from settings import DEBUG_MODE

def log(msg):
	if not DEBUG_MODE:
		return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py','SelectedTrackControl.log'), 'a')
	f.write(msg+"\n")
	f.close()
