# import sys
# import SocketServer, struct, threading, socket
# import cPickle

# SOCKET_DEL = '*ET*'

# class server():
#   amount_of_data = 81852
#   def __init__(self, ip_address, port, game):
#     """Server class that handles dealing with requests"""
#     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     self.socket.bind((ip_address, port))
#     self.game = game # will handle giving data back to the game
#     # self.tile = tile
#     # print " i'm at tile " + str(tile)

#   def open_connection(self):
#     self.socket.listen(1)
#     self.open_sock, addr = self.socket.accept()
#     print "connection made to " + str(addr)

#   def close_connection(self, msg):
#     self.open_sock.sendall( msg )
#     self.open_sock.close()

#   def recev_connection(self):
#     # todo return something to know if time to quit
#     data = self.get_whole_packet()
#     state_struct = self.process_request(data)
#     self.sync(state_struct)

#   def process_request(self, pickled_data):
#       data = cPickle.loads(pickled_data)
#       struct = self.game.update(data)
#       # print struct
#       if struct['state'] == 1:
#         self.close_connection(struct['msg'])
#         print struct['msg']
#         sys.exit()
#       return struct

#   def get_whole_packet(self):
#     data = ''
#     while True:
#       data += self.open_sock.recv(self.amount_of_data)
#       # print 'rdbuff is ' + rdbuf
#       split = data.split(SOCKET_DEL) # split at newline, as per our custom protocol
#       if len(split) != 2: # it should be 2 elements big if it got the whole message
#         pass
#       else:
#         return split[0] # returns just the pickled string 

#   def translate_to_local(self, data):
#     """translates the given data to the local node. Wrapper for call to game
#     """
#     return

#   def tanslate_to_global(self):
#     """tanstlates the data to the global data """
#     return

#   def sync(self, send_struct):
#     # send response back to connecting to say processing is complete
#     # print send_struct
#     x = cPickle.dumps(send_struct, cPickle.HIGHEST_PROTOCOL) + '*ET*'
#     self.open_sock.sendall( x )

