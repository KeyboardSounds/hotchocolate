import hotchocolate.worldobjects
import yaml

f = open("rooms/rooms.yaml")
r = yaml.load(f)
print(r.outputText())
print(r.items)
