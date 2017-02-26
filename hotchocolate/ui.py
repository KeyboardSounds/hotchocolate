from abc import ABC, abstractmethod

class AbstractUI(ABC):
	"""
	An abstract class outlining the services that hotchocolate user interfaces
	must provide.
	"""
	@abstractmethod
	def getUserInput(self):
		"""
		:return: the user's input text
		:rtype: string
		"""
		pass

	@abstractmethod
	def displayText(self, text):
		"""
		Used to print out story text and room descriptions.
		:param text: the text to display
		:type text: string
		"""
		pass

	def askYesNo(self, question):
		"""
		Asks the player a yes or no question and gets their response
		:param question: the question to ask the player
		:type question: string
		:return: True if player says yes, False otherwise
		:rtype: boolean
		"""
		pass

class CommandLineUI(AbstractUI):
	"""
	Command line implementation of abstract class AbstractUI.
	"""
	def __init__(self):
		self.prompt = "> "

	def getUserInput(self):
		return input(self.prompt)

	def displayText(self, text):
		print(text)

	def askYesNo(self, question):
		while True:
			self.displayText(question + " (Y/N)")
			inp = self.getUserInput().lower()
			if inp == "y" or inp == "yes":
				return True
			elif inp == "n" or inp == "no":
				return False
			else:
				self.displayText("Please type yes or no.")
