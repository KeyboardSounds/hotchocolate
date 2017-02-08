commandMap = {"look": look
			"look at": look
			"l": look}

def tokenize(command):
	wordList = command.split()

	verbSoFar = ""
	for word in wordList:
		verbSoFar += word
		if verbSoFar not in commandMap:
			break

	verb = verbSoFar

def look(gameState, args):
	pass
