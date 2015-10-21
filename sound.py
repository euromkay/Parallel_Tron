def play(sound, player):
	channel = sound.play(loops = 0, maxtime = 0, fade_ms = 0)
	pos = player.location[0]/165.0
	channel.set_volume(pos, 1-pos)