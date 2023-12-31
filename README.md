# DiscordScraperPyScripts

1. This package provides scripts to scrape Discord Servers for Discord Chat messages.

There are two techniques proposed in this package. You are free to choose either one that fits best your use-case:
1. DiscordChatExporter
2. Discord GET Request Endpoints

## Comparison between Techniques

(To Be Done) Use DiscordChatExporter Scripts in general. Responses from Discord GET Request Endpoints are prone to being stalled by the Discord Servers.

## How to run DiscordChatExporter Scripts

1. Setup [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) CLI on your machine.
2. We will essentially try to get the entire chat history for a channel. Then, we will use python scripts to filter out messages relevant to keywords of interest.
3. To get the entire chat history of a channel use the following command of DiscordChatExporter.

`dotnet <INSTALLATION_PATH>/DiscordChatExporter.Cli.dll export -c <CHANNEL_ID> -o <OUTPUT_PATH> -f Json -t <DISCORD_USER_TOKEN>`
   1. Here, <CHANNEL_ID> is the Discord Channel Id in a URL of the form `https://discord.com/channels/<SERVER_ID>/<CHANNEL_ID>`.
   2. <DISCORD_USER_TOKEN> is the token associated with your Discord account. To retrieve this token you may follow the steps mentioned in the [DiscordChatExporter Docs](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md#in-chrome).
   3. <OUTPUT_PATH> is the path where the chat history of the Discord Channel will be logged to.
**Note**: [Automating user accounts violates Discord's terms of service](https://support.discord.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-) and may result in account termination. Use at your own risk.
4. Now, we will create a minified view of every message containing only fields that are relevant to our task. Our script in this package currently generates the following minified metadata from each message representation of DiscordChatExporter.

```
[{
	"id": "(String) Message Id",
	"content": "(String) Message",
	"author": {
		"name": "(String) User Name",
		"id": "(String) User Id"
	},
	"pinned": "(Boolean) Was the message Pinned? (True or False).",
	"ts": "(String) Timestamp",
	"mentions": [{
		"id": "(String) Message Id referenced in the current message",
		"name": "(String) User name of the message referenced in the current message",
		"discriminator": "(String) Discord User Id ex: abcd#1234 implies discriminator is 1234",
		"nickname": "(String) User name alias of the Discord User",
		"color": "(String) Color",
		"isBot": "(String) Boolean is the the Discord User a Bot",
		"avatarUrl": "(String) URL of the Discord Profile User"
	}],
	"reactions": [{
		"emoji": {
			"name": "(String) Reaction Name",
			"id": "(String) Reaction Id",
			"code": "(String) Reaction Code",
			"imageUrl": "(String) URL containing emoji",
			"animated": "(String) Boolean is the emoji animated"
		},	
		"count": "(Integer) Number of users who upvoted the reaction."
	}],
	"attachments": [{
		"url": "(String) URL of attached links in the message",
		"fileName": "(String) File name of the URL ex: file:///a/b/c/d.json implies file name is d.json"
	}]
}]
```
5. To create the above minified representation, run the command `python3 DiscordChannelPostProcess.py /path/to/input` where `/path/to/input` is the `<OUTPUT_PATH>` in the Dotnet command in step 3.
6. Fill keywords.txt with the keywords to be searched for in the message history such that each line contains one keyword.
7. Run `python3 ProcessedChatSearchUtil.py /path/to/input` is the output path of step 5 i.e.., `../outputs/ChatExport/{CHANNEL_ID}_{CHANNEL_NAME}.json`
8. The filtered output is in `../outputs/search/{CHANNEL_ID}_{CHANNEL_NAME}.json`
9. **Note:** The above set of python processing scripts may fail if the JSON generated by DiscordChatExporter is huge. (Ex: #general-chat of Discord channels can have size in ~10-20GB ranges for ~20Million messages). In this case, you would like to use the package [LargeDiscordChatExporter](https://github.com/krishna555/LargeDiscordChatExportProcessor). This package uses GSON streaming processing to read and process a single Discord message JSON object in memory at a time. This makes processing a large number of messages extremely efficient.

## How to run Discord GET Request Endpoint Scripts.

Fill keywords.txt with the keywords to be searched for in the message history such that each line contains one keyword.

### Crawl Entire Chat History and filter for keywords
1. Run `python3 ChatHistoryExporter.py <CHANNEL_ID> <DISCORD_USER_TOKEN> <DISCORD_CHANNEL_URL>`.
   1. Here, <CHANNEL_ID> is the Discord Channel Id in a URL of the form `https://discord.com/channels/<SERVER_ID>/<CHANNEL_ID>`.
   2. <DISCORD_USER_TOKEN> is the token associated with your Discord account. To retrieve this token you may follow the steps mentioned in the [DiscordChatExporter Docs](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md#in-chrome).
   3. <DISCORD_CHANNEL_URL> is the URL of the Discord Channel URL of the form `https://discord.com/channels/<SERVER_ID>/<CHANNEL_ID>`.
2. The above command will extract all messages scraping 100 messages at a time, taking a 5s sleep and repeating the same until it retrieves all messages.
**Note:** Sometimes, Discord GET endpoint does not return messages for a request. Currently, the upper bound for time limit has been set to 1 day in which case, we may not be able to retrieve any more messages from the point of failure. This is because this technique relies on picking the 100th oldest message as an offset id to retrieve the next 100 older messages. So, it is synchronous in nature and can fail if the Discord GET endpoint fails.

### Use Discord's search feature for keyword.
1. This implementation has an important limitation. It can only return 5025 messages corresponding to a keyword. Hence, this may be the least interesting technique. But this is the exact behaviour of how Discord works when you navigate to Discord and search a keyword in the search box. Although, you may see a larger number of messages in Discord when you try to navigate to the >= 5026th message, it will fail on the UI as well.
2. Run `python3 KeywordMetadataExtractor.py <AUTH_TOKEN> <CHANNEL_URL> <OUTPUT_PATH>`  

   1. Here, <AUTH_TOKEN> is the token associated with your Discord account. To retrieve this token you may follow the steps mentioned in the [DiscordChatExporter Docs](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md#in-chrome).

   2. <CHANNEL_URL> is the URL of the Discord Channel URL of the form `https://discord.com/channels/<SERVER_ID>/<CHANNEL_ID>`.
   3. <OUTPUT_PATH> is the output path where the generated JSON will be stored.