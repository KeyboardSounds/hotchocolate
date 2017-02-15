import yaml

USE_OXFORD_COMMA = True
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
	def __init__(self,
				name,
				description,
				listed=True,
				plural=False,
				article="a",
				useDefiniteArticle=False,
				takeable=True):
		self.name = name
		self.description = description
		self.listed = listed
		self.plural = plural
		self.takeable = takeable
		self.useDefiniteArticle = useDefiniteArticle
		if self.useDefiniteArticle:
			self.article = DEFINITE_ARTICLE
		else:
			self.article = article

	def __repr__(self):
		return self.name

	def outputText(self):
		return self.description

# Constructor for YAML
def itemConstructor(loader, node) :
	fields = loader.construct_mapping(node)
	return Item(**fields)

yaml.add_constructor('!Item', itemConstructor, yaml.SafeLoader)

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
				items=None,
				exits=None
				):
		self.name = name
		self.description = description


	def setValues(self,
				hideItems=False,
				hideName=False,
				hideDescription=False,
				items=None,
				exits=None):

		self.hideItems = hideItems
		self.hideName = hideName
		self.hideDescription = hideDescription

		if exits is None:
			self.exits = []
		else:
			self.exits = exits
		self.items = {}

		if items is not None:
			# construct dictionary from item list
			for i in items:
				self.items[i.name] = i

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
		for name, item in self.items.items():
			if item.listed == True:
				listedItems.append(item)

		# construct the list
		text = SEE_INTRODUCTION
		if len(listedItems) == 0:
			return ""

		# add first item - no comma before it
		i = listedItems[0]
		text += i.article + " " + i.name


		if len(listedItems) == 1:
			return text + "."
		else:
			# add all the remaining items except the last one
			for i in listedItems[1:-1]:
				text += ", " + i.article + " " + i.name

		# add last item - we need to put an 'and' before it
		if USE_OXFORD_COMMA:
			text += ","

		i = listedItems[-1]
		text += " and " + i.article + " " + i.name + "."

		return text

	def getItem(self, itemName):
		"""
		:param itemName: the name of the item to return
		:type itemName: string
		:return: item with name itemName or None if no such item exists
		:rtype: Item
		"""
		if itemName in self.items:
			return self.items[itemName]
		else:
			return None

	def removeItem(self, itemName):
		if itemName in self.items:
			del self.items[itemName]

# Constructor for YAML
def roomConstructor(loader, node) :
	fields = loader.construct_mapping(node)
	room = Room(fields.pop("name"), fields.pop("description"))
	yield room
	room.setValues(**fields)

yaml.add_constructor('!Room', roomConstructor, yaml.SafeLoader)

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
		return "{}: {}".format(self.direction, self.roomName, yaml.SafeLoader)

# Constructor for YAML
def exitConstructor(loader, node) :
	fields = loader.construct_mapping(node)
	return Exit(**fields)

yaml.add_constructor('!Exit', exitConstructor, yaml.SafeLoader)
