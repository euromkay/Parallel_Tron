import tron_render, tron_master
import sys, platform, time
from multiprocessing import Process

local = (len(sys.argv) == 3)

p = None 
if local:
	ip = '0.0.0.0'
	port = 5000
	scale = 7

	Process(target = tron_master.start, args = [ip, port]).start()
	time.sleep(2)
	for x in range(5):
		for y in range (3):
			coords = (x * 300, y * 200)
			Process(target = tron_render.display, args=[ip, port, x, y, scale, coords]).start()

else:
	ip = '10.0.0.10'
	port = 5000
	scale = 30
	name = platform.node()
	if name == 'master':
		tron_master.start(ip, port)
	else:
		xcoord = int(name[5])
		ycoord = int(name[7])
		tron_render.display(ip, port, xcoord, ycoord, 60)
	
