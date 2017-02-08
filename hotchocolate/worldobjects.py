import yaml

class Item(yaml.YAMLObject):
	yaml_tag = u'!Item'
	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return self.name

class Room(yaml.YAMLObject):
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
		text = ""
		if not self.hideName:
			text += self.name + "\n"
		if not self.hideDescription:
			text += self.description + "\n"
		return text
