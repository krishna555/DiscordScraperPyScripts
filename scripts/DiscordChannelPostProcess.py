import json
import sys
class DiscordChannelPostProcess:
	def __init__(self, input_path):
		self.input_path = input_path
		self.channel_id = None
		self.channel_name = None

	def read_input(self):
		with open(self.input_path, "r") as f:
			data = json.loads(f.read())

		self.channel_id = data["channel"]["id"]
		self.channel_name = "_".join(data["channel"]["name"].split(" "))

		data = data["messages"]

		return data

	def extractView(self, obj):
		data = {
			"id": obj["id"],
			"content": obj["content"],
			"author": {
				"id": obj["author"]["id"],
				"name": obj["author"]["name"]
			},
			"pinned": obj["isPinned"],
			"ts": obj["timestamp"]                
		}
		data["mentions"] = obj["mentions"]

		data["reactions"] = obj["reactions"]

		data["attachments"] = []
		for attachment in obj["attachments"]:
			data["attachments"].append({
					"url": attachment["url"],
					"fname": attachment["fileName"]
				})
		return data

	def extractMetadata(self, data):
		res = []
		for obj in data:
			res.append(self.extractView(obj))
		return res


	def writeToFile(self, data):

		with open(f"../outputs/ChatExport/{self.channel_id}_{self.channel_name}.json", "w") as of:
			json.dump(data, of)


	def run(self):
		extracted_data = self.read_input()
		processed_data = self.extractMetadata(extracted_data)
		self.writeToFile(processed_data)


if len(sys.argv) != 2:
	print("Run using command: python3 DiscordChannelPostProcess.py /path/to/input")
	exit(1)
obj = DiscordChannelPostProcess(sys.argv[1])
obj.run()
