from settings import debug_mode

def log(msg):
	if not debug_mode:
		return
	f = open(__file__.replace('.pyc', '.py').replace('Logging.py','SelectedTrackControl.log'), 'a')
	f.write(msg+"\n")
	f.close()


def bin(x, digits=0): 
	oct2bin = ['000','001','010','011','100','101','110','111'] 
	binstring = [oct2bin[int(n)] for n in oct(x)] 
	return ''.join(binstring).lstrip('0').zfill(digits)