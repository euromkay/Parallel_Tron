import threading

def moveUp(mixer):
	threading.Thread(target = play, args = [mixer]).start()
	

def moveDown(mixer):
	threading.Thread(target = play, args = [mixer]).start()


def moveLeft(mixer):
	threading.Thread(target = play, args = [mixer]).start()

def moveRight(mixer):
	threading.Thread(target = play, args = [mixer]).start()

def play(mixer):
  sound = './assets/changedirec.wav'
  mixer.music.load(sound)
  mixer.music.play()