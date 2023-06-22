class Utils:
	@staticmethod
	def readKeywords():
		file = open("keywords.txt", "r")
		return [line.strip() for line in file.readlines()]
