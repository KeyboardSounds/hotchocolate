import yaml

USE_OXFORD_COMMA = True
VOWEL_SET = set(["a","e","i","o","u"])
SEE_INTRODUCTION = "You can see "
DEFINITE_ARTICLE = "the"

class Item():
	"""
	Represents an item that exists in the game world.

	:param name: the name of the item
	:type name: string
	:param description: a written description of the item
	:type description: string
	:param lised: ``True`` if the item should be listed when a room's items are
		printed
	:type listed: boolean
	:param plural: ``True`` if the item is plural, ie. when there are more
		than one of it (eg. "apples")
	:type article: string
	"""
	def __init__(self, name, description, listed=True, plural=False, article="a", useDefiniteArticle=False):
		self.name = name
		self.description = description
		self.listed = listed
		self.plural = plural
		self.useDefiniteArticle = useDefiniteArticle
		if self.useDefiniteArticle:
			self.article = DEFINITE_ARTICLE
		else:
			self.article = article

	def __repr__(self):
		return self.name

# Constructor for YAML
def itemConstructor(loader, node) :
	fields = loader.construct_mapping(node)
	return Item(**fields)

yaml.add_constructor('!Item', itemConstructor)

class Room():
	"""
	Represents a room that exists in the game world.

	:param name: the name of the room
	:type name: string
	:param description: a written description of the room
	:type description: string
	:param hideName: ``True`` if the name of the room should be hidden when
		outputting the room as text
	:type hideName: boolean
	:param hideDescription: ``True`` if the description of the room should be hidden
		when outputting the room as text
	:type hideDescription: boolean
	:param items: a list of items in the room
	:type items: list(Item)
	:param exits: a list of the exits that this room has
	:type exits: list(Exit)
	"""
	def __init__(self,
				name,
				description,
				hideItems=False,
				hideName=False,
				hideDescription=False,
				items=[],
				exits=[]
				):
		self.name = name
		self.description = description
		self.hideItems = hideItems
		self.hideName = hideName or False
		self.hideDescription = hideDescription
		self.items = items
		self.exits = exits

	def __repr__(self):
		return self.name

	def outputText(self):
		"""
		:return: a text representation of the room and its contents
		:rtype: string
		"""
		text = ""
		if not self.hideName:
			text += self.name + "\n"
		if not self.hideDescription:
			text += self.description + "\n"
		if not self.hideItems:
			text += self.listItems() + "\n"
		return text

	def listItems(self):
		"""
		:return: a sentence that lists the items in the room that are marked as
			listable
		:rtype: text
		"""
		# figure out which items we should list
		listedItems = []
		for i in self.items:
			if i.listed == True:
				listedItems.append(i)

		# construct the list
		text = SEE_INTRODUCTION
		if len(listedItems) == 0:
			return ""

		# add first item - no comma before it
		i = listedItems[0]
		text += i.article + " " + i.name

		# add all the remaining items except the last one
		if len(listedItems) == 1:
			return text + "."
		else:
			for i in listedItems[1:-1]:
				text += ", " + i.article + " " + i.name

		# add last item - we need to put an and before it
		if USE_OXFORD_COMMA:
			text += ","

		i = listedItems[-1]
		text += " and " + i.article + " " + i.name + "."

		return text

# Constructor for YAML
def roomConstructor(loader, node) :
	fields = loader.construct_mapping(node)
	return Room(**fields)

yaml.add_constructor('!Room', roomConstructor)

class Exit():
	"""
	Represents a portal or doorway to a room. Unidirectional.
	:param direction: the direction of the exit
	:type direction: string
	:param roomName: the name of the room the exit leads to.
	:type roomName: string
	"""
	def __init__(self, direction, roomName):
		self.direction = direction
		self.roomName = roomName

	def __repr__(self):
		return "{}: {}".format(self.direction, self.roomName)

# Constructor for YAML
def exitConstructor(loader, node) :
	fields = loader.construct_mapping(node)
	return Exit(**fields)

yaml.add_constructor('!Exit', exitConstructor)
