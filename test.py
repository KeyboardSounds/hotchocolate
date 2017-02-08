import hotchocolate.worldobjects
import yaml

f = open("rooms/rooms.yaml")
roomList = yaml.load(f)
r = roomList[1]
print(r.outputText())
