import requests
import time
import json
import sys
from Utils import Utils
# Insert Keywords to be searched here.
keywords = Utils.readKeywords()

n = len(keywords)

i = 0

data = {}
for i in range(n):
	keyword = keywords[i]
	data[keyword] = []
	print(keyword)
	for cnt in range(0, 5001, 25):
		time.sleep(5)
		url = f"https://discord.com/api/v9/guilds/{channel_id}/messages/search?content={keyword}&offset={cnt}"
		headers = {
			"authorization": auth_token,
			"referer": channel_url
		}
		try:
			response = requests.get(url, headers=headers, timeout=10)
		except:
			print("[Failed]: Tried to scrape URL:", url)
			continue
		all_extracted = []
		parsed_data = json.loads(response.text)
		if (parsed_data is not None and "messages" in parsed_data):
			for message in parsed_data["messages"]:
				message = message[0]
				if message["content"] != "":
					obj = {
						"message_id": message["id"],
						"content": message["content"],
						"channel_id": message["channel_id"],
						"author": {
							"id": message["author"]["id"],
							"user_name": message["author"]["username"]
						},
						"pinned": message["pinned"],
						"ts": message["timestamp"]
					}
					obj["mentions"] = []
					for mention in message["mentions"]:
						obj["mentions"].append(mention["username"])

					all_extracted.append(obj)
				else:
					print(message)
			data[keyword].extend(all_extracted)
		else:
			# No more responses, Break
			# print(len(data[keyword]))
			break
		# print(len(data[keyword]))

if len(sys.argv) != 4:
	print("Run python3 KeywordMetadataExtractor.py <AUTH_TOKEN> <CHANNEL_URL> <OUTPUT_PATH>")
	exit(1)

auth_token = sys.argv[1]
channel_url = sys.argv[2]
channel_id = channel_url.split("/")[-1]
# Strip Trailing Slash if any.
if channel_id[-1] == "/":
	channel_id = channel_id[:-1]
output_path = sys.argv[3]
with open(output_path, "w") as of:
	json.dump(data, of)

