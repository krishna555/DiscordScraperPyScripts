import json
from collections import defaultdict
from Utils import Utils
import sys
"""
Input Path is the file where the chat history for a channel has been processed and stored.
Output Path is the file where keyword aggregated messages are extracted and stored.
"""
class ProcessedChatSearchUtil:
	def __init__(self, input_path, keywords):
		self.input_path = input_path
		self.keywords = keywords
		self.fname = self.input_path.split("/")[-1]

	def read_input(self):
		with open(self.input_path, "r") as f:
			data = json.loads(f.read())
		return data


	def search(self, data):
		res = defaultdict(list)
		for obj in data:
			for keyword in self.keywords:
				content = obj["content"].lower()
				if keyword in content:
					res[keyword].append(obj)

		return res

	def writeToFile(self, res):
		with open(f"../outputs/search/{self.fname}", "w") as f:
			json.dump(res, f)


	def run(self):
		extracted_data = self.read_input()
		processed_data = self.search(extracted_data)
		self.writeToFile(processed_data)

keywords = Utils.readKeywords()

if len(sys.argv) != 2:
	print("Run python3 ProcessedChatSearchUtil.py <INPUT_PATH>")
	exit(1)
input_path = sys.argv[1]

obj = ProcessedChatSearchUtil(input_path, keywords)
obj.run()



