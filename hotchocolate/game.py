import hotchocolate.ui as ui
import hotchocolate.worldobjects as worldobjects
import yaml

class Game():
	def __init__(self, roomFilePath, uiClass=ui.CommandLineUI):
		self.currentRoom = None
		self.roomList = None
		self.ui = uiClass()
		self.roomFilePath = roomFilePath

	def loadData(self):
		f = open(self.roomFilePath)
		self.roomList = yaml.load(f)
		self.currentRoom = self.roomList[0] #TODO: make this configurable from file

	def mainLoop(self):
		while True:
			roomDesc = self.currentRoom.outputText()
			self.ui.displayText(roomDesc)
			inp = self.ui.getUserInput()

	def run(self):
		self.loadData()
		self.mainLoop()
