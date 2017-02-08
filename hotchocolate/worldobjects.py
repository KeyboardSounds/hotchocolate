import yaml

class Item(yaml.YAMLObject):
	"""
	Represents an item that exists in the game world.

	:param name: the name of the item
	:type name: string
	:param description: a written description of the item
	:type description: string
	"""
	yaml_tag = u'!Item'
	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return self.name

class Room(yaml.YAMLObject):
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
	"""
	yaml_tag = u'!Room'
	def __init__(self,
				name,
				description,
				hideName=False,
				hideDescription=False,
				items=[],
				exits=[]
				):
		self.name = name
		self.description = description
		self.hideName = hideName
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
		return text
