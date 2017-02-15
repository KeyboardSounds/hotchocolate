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
			print("foo")
			self.commandDict[verb](self.game, verb)
		else:
			args = wordList[verbIdx+1:]
			self.commandDict[verb](self.game, verb, args)

class BasicCommands():
	"""
	Container class for implementations of some basic, core commands.
	"""

	def look(game, verb):
		"""
		Displays the room text

		:param game: the object representing the game
		:type game: Game
		:param verb: the verb the command was called with
		:type verb: string
		"""
		if not game.isRunning():
			raise GameNotRunningException()
		else:
			game.displayCurrentRoom()

	def go(game, verb, args=[]):
		"""
		Moves the player into an adjacent room

		Can be called with ``go <direction>`` or just ``<direction>``.
		Also recognises common abbreviations of directions like "ne" (northeast)
		and "d" (down).

		:param game: the object representing the game
		:type game: Game
		:param verb: the verb the command was called with
		:type verb: string
		:param args: the arguments the command was called with
		:type args: list(string)
		"""
		if not game.isRunning():
			raise GameNotRunningException()

		if verb == "go": # there is a "go" in front of the direction
			if len(args) > 1:
				game.ui.displayText("I understood that as far as you wanting to"
					"go somewhere, but I didn't recognise the direction.")
				return
			else:
				direction = args[0]
		else: # the input was just a direction
			direction = verb
			if len(args) > 0:
				game.ui.displayText("I understood that as far as you wanting to"
					"go {}, but I didn't understand what you said after that."
					" Try just typing in \"{}\"".format(direction))
				return

		if direction == "n":
			direction = "north"
		elif direction == "s":
			direction = "south"
		elif direction == "e":
			direction = "east"
		elif direction == "w":
			direction = "west"
		elif direction == "ne":
			direction = "northeast"
		elif direction == "se":
			direction = "southeast"
		elif direction == "sw":
			direction = "southwest"
		elif direction == "ne":
			direction = "northeast"
		elif direction == "u":
			direction = "up"
		elif direction == "d":
			direction = "down"

		roomName = ""
		for e in game.currentRoom.exits:
			if e.direction == direction:
				roomName = e.roomName

		if roomName == "":
			game.ui.displayText("You can't go that way.")
			return
		else:
			game.currentRoom = game.rooms[roomName]
			game.displayCurrentRoom()

	def examine(game, verb, args):
		if not game.isRunning():
			raise GameNotRunningException()

		itemName = " ".join(args)
		item = game.getItem(itemName)

		if item is None:
			game.ui.displayText("That isn't here.")
		else:
			game.ui.displayText(item.outputText())

	def take(game, verb, args):
		if not game.isRunning():
			raise GameNotRunningException()

		itemName = " ".join(args)

		if itemName == "all":
			# we're going to be removing items from this dictionary, so we need
			# to copy it so we can iterate through them safely
			items = game.currentRoom.items.copy()
			for name, item in items.items():
				if item.takeable:
					game.currentRoom.removeItem(name)
					game.addToInventory(item)
			game.ui.displayText("Taken.")
			return

		item = game.getItem(itemName)
		if item is None:
			game.ui.displayText("That isn't here.")
		elif item.name in game.inventory:
			game.ui.displayText("You're already carrying that.")
		elif item.takeable == False:
			game.ui.displayText("You can't take that.")
		else:
			game.removeItem(item.name)
			game.addToInventory(item)
			game.ui.displayText("Taken.")

	basicCommandDict = {"look": look,
				"l": look,
				"north": go,
				"n": go,
				"east": go,
				"e": go,
				"south": go,
				"s": go,
				"west": go,
				"w": go,
				"northeast": go,
				"ne": go,
				"southeast": go,
				"se": go,
				"southwest": go,
				"sw": go,
				"northwest": go,
				"nw": go,
				"up": go,
				"u": go,
				"down": go,
				"d": go,
				"go": go,
				"examine": examine,
				"x": examine,
				"take": take
				}
