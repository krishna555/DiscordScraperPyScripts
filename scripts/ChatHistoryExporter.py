"""
Python Class to export the entire chat history of a channel.
"""
import time
import json
import requests

class ChatExporter:
	def __init__(self, channel_id):
		self.channel_id = channel_id
		self.extracted_data = []
		self.base_url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"

	def extractView(self, obj):
		data = {
			"message_id": obj["id"],
			"content": obj["content"],
			"channel_id": obj["channel_id"],
			"author": {
				"id": obj["author"]["id"],
				"user_name": obj["author"]["username"]
			},
			"pinned": obj["pinned"],
			"ts": obj["timestamp"]                          
		}
		data["mentions"] = []
		for mention in obj["mentions"]:
			data["mentions"].append(mention["username"])
		return data

	def call_discord(self, url):
		headers = {
			"Authorization": auth_token,
			"Referer": channel_url
		}
		try:
			response = requests.get(url,headers=headers, timeout=86400)
		except:
			print(f"[ERROR]: Failed to scrape URL: {url}")
			return None
		return response

	def get_first_obj(self):
		
		url = f"{self.base_url}?limit=50"
		response = self.call_discord(url)
		if not response:
			return Exception(f"No Messages found for channelId : {self.channel_id}")

		data = json.loads(response.text)
		if (data is not None):
			for i in range(len(data)):
				obj = self.extractView(data[i])
				self.extracted_data.append(obj)

	def get_next_page(self, id_val):

		url = f"{self.base_url}?before={id_val}&limit=100"
		response = self.call_discord(url)

		if not response:
			return False

		data = json.loads(response.text)
		if (data is not None):
			for i in range(len(data)):
				obj = self.extractView(data[i])
				self.extracted_data.append(obj)
			return True

		return False

	def write(self, output_path):
		with open(output_path, "w") as of:
			json.dump(self.extracted_data)

	def run(self, output_path):

		self.get_first_obj()
		count = len(self.extracted_data)
		status = True
		start = time.time()
		while status:
			last_id = self.extracted_data[-1]["message_id"]
			time.sleep(5)
			status = self.get_next_page(last_id)
			print(len(self.extracted_data))
			
		end = time.time()
		print(f"Total Execution Time: {end - start}")
		self.write(output_path)

if len(sys.argv) != 4:
	print("Run python3 ChatExporter.py <CHANNEL_ID> <DISCORD_AUTHORIZATION_TOKEN> <DISCORD_CHANNEL_URL>")
	exit(1)

channel_id = sys.argv[1]
auth_token = sys.argv[2]
channel_url = sys.argv[3]
output_path = f"../outputs/ChatExport/{channel_id}"
chat_exp_obj = ChatExporter(channel_id)
chat_exp_obj.run(output_path)


