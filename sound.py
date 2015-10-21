def play(sound, player):
	channel = sound.play()
	pos = player.location[0]/165.0
	channel.set_volume(pos, 1-pos)