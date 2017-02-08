from hotchocolate.game import Game
import yaml
import os

roomFilePath = os.path.abspath("rooms/rooms.yaml")
game = Game(roomFilePath)
game.run()
