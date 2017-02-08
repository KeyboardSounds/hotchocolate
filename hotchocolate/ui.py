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
