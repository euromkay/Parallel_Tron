# middle ware for passing network data to the game
# import network as n
import cPickle
class MiddleWare():
  """ Handles all of the networking communication between the game and the 
  network. Pass it the game object that will be used."""
  def __init__(self, game, server):
    self.server = server
    self.game = game

  def process_request(pickled_data):
    data = cPickle.loads(pickled_data)
    self.game.update(data)

  def run_server(self):
    """runs the server, should be called before anythin"""
    # server=n.broadcastServer( ( '10.10.0.1', 20000 ), n.requestHandler )
    self.server.serve_forever()