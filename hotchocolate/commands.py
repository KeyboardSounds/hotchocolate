from hotchocolate.game import *

class CommandInterpreter():
	"""
	Parses user input and executes appropriate command, if any.
	:param game: object representing currently running game
	:type game: Game
	:param commandDict: map from a command's text to the function that text
		should trigger. Will use the commands implemented in BasicCommands by
		default.
	:type commandDict: dict(string, function)
	"""
	def __init__(self, game, commandDict=None):
		self.game = game
		if commandDict is None:
			self.commandDict = BasicCommands.basicCommandDict
		else:
			self.commandDict = commandDict

	def parse(self, inp):
		"""
		Very simple parser for commands. Will look for a known command at the
			beginning of the input, and execute the corresponding function (if
			this exists) with the remaining input as arguments
		:param inp: the input to parser
		:type inp: string
		"""
		wordList = inp.split()

		verbSoFar = ""
		verbIdx = -1
		for word in wordList:
			if verbSoFar + word not in self.commandDict:
				break
			verbSoFar += word
			verbIdx += 1

		if verbIdx == -1:
			# didn't recognise verb
			self.game.ui.displayText("I couldn't understand that.")
			return

		verb = verbSoFar

		if verbIdx == (len(wordList) -1):
			# no words apart from verb in command, so no command has no
			# arguments that need to be passed to its parser function
			self.commandDict[verb](self.game, verb)
		else:
			args = wordList[verbIdx+1:]
			self.commandDict[verb](self.game, verb, args)

class BasicCommands():
	"""
	Implementations of some basic, core commands
	"""

	def look(game, verb):
		"""
		Displays the room text
		:param game: the game object to get
		"""
		print("run")
		if not game.isRunning():
			raise GameNotRunningException()
		else:
			game.displayCurrentRoom()

	basicCommandDict = {"look": look,
				"l": look}
