import hotchocolate.worldobjects
import yaml

f = open("rooms/rooms.yaml")
r = yaml.load(f)
print(r)
print(r.items)
