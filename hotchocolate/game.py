import hotchocolate.ui as ui
import hotchocolate.worldobjects as worldobjects
import hotchocolate.commands as commands
import yaml

class _Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class Game(metaclass=_Singleton):
	running = False
	def __init__(self, roomFilePath, uiClass=ui.CommandLineUI):
		self.currentRoom = None
		self.rooms = {}
		self.ui = uiClass()
		self.roomFilePath = roomFilePath
	@staticmethod
	def isRunning():
		return Game.running

	def getInstance(self):
		return self

	def loadData(self):
		f = open(self.roomFilePath)
		roomsAsList = yaml.load(f)

		# make a dictionary from the room list, with the room name as the key
		for room in roomsAsList:
			self.rooms[room.name] = room

		self.currentRoom = roomsAsList[0] #TODO: make this configurable from file

	def mainLoop(self):
		while True:
			inp = self.ui.getUserInput()
			self.commandInterpreter.parse(inp)

	def displayCurrentRoom(self):
		roomDesc = self.currentRoom.outputText()
		self.ui.displayText(roomDesc)

	def run(self):
		Game.running = True
		self.commandInterpreter = commands.CommandInterpreter(self)
		self.loadData()
		self.displayCurrentRoom()
		self.mainLoop()

class GameNotRunningException(Exception):
	def __init__(self, msg=None):
		if msg is None:
			msg = "A Game instance is not currently running."
		super(GameNotRunningException, self).__init__(msg)
