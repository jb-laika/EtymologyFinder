from wiktionaryparser import WiktionaryParser

f = open("input.txt", "r")
text = f.read()
parser = WiktionaryParser()
body = ""

def clean(word):
	cleanedWord = word
	if word[-1] == ',' or word[-1] == '.' or word[-1] == ':' or word[-1] == ';':
			cleanedWord = word[:-1]
	return cleanedWord

def getEtymology(scrapedWord, word):
	etymologyFound = False
	bodyAddition = ''
	for i in range(len(scrapedWord)):
		if not etymologyFound:
			if "from french" in scrapedWord[i]["etymology"].lower() or "from old french" in scrapedWord[i]["etymology"].lower():
				etymologyFound = True
				bodyAddition += ("\n" + "<span style=\"color: royalblue\">" + word + "</span> ")
			elif "from old northern french" in scrapedWord[i]["etymology"].lower() or "from middle french" in scrapedWord[i]["etymology"].lower():
				etymologyFound = True
				bodyAddition += ("\n" + "<span style=\"color: royalblue\">" + word + "</span> ")
			elif "from latin" in scrapedWord[i]["etymology"].lower():
				etymologyFound = True
				bodyAddition += ("\n" + "<span style=\"color: firebrick\">" + word + "</span> ")
			elif "from old english" in scrapedWord[i]["etymology"].lower():
				etymologyFound = True
				bodyAddition += ("\n" + "<span style=\"color: slategray\">" + word + "</span> ")
			elif "from old norse" in scrapedWord[i]["etymology"].lower():
				etymologyFound = True
				bodyAddition += ("\n" + "<span style=\"color: lightblue\">" + word + "</span> ")
			elif "from middle english" in scrapedWord[i]["etymology"].lower():
				etymologyFound = True
				bodyAddition += ("\n" + "<span style=\"color: slategray\">" + word + "</span> ")

	return bodyAddition

for word in text.split():
	print(word)
	cleanWord = clean(word)

	checkWord = parser.fetch(cleanWord)

	resultEtymology = getEtymology(checkWord, word)

	if resultEtymology == '' and cleanWord[0].isupper():
		checkWord = parser.fetch(cleanWord.lower())
		resultEtymology = getEtymology(checkWord, cleanWord)
		print("Trying lowercase")

	if resultEtymology == '':
		checkFormsWord = checkWord
		for entry in range(len(checkWord)):
			for definitionNum in range(len(checkWord[entry]["definitions"])):
				for textNum in range(len(checkWord[entry]["definitions"][definitionNum]["text"])):

					if "participle of" in checkWord[entry]["definitions"][definitionNum]["text"][textNum]:
						newWord = clean(checkWord[entry]["definitions"][definitionNum]["text"][textNum].split())
						for breakdown in range(len(newWord)):
							if newWord[breakdown].lower() == "participle" and newWord[breakdown+1] == "of":
								print("Found root: " + clean(newWord[breakdown+2]))
								checkFormsWord = parser.fetch(clean(newWord[breakdown+2]))

					elif "plural of" in checkWord[entry]["definitions"][definitionNum]["text"][textNum]:
						newWord = clean(checkWord[entry]["definitions"][definitionNum]["text"][textNum].split())
						for breakdown in range(len(newWord)):
							if newWord[breakdown].lower() == "plural" and newWord[breakdown+1] == "of":
								print("Found singular: " + clean(newWord[breakdown+2]))
								checkFormsWord = parser.fetch(clean(newWord[breakdown+2]))

					elif "form of" in checkWord[entry]["definitions"][definitionNum]["text"][textNum]:
						newWord = clean(checkWord[entry]["definitions"][definitionNum]["text"][textNum].split())
						for breakdown in range(len(newWord)):
							if newWord[breakdown].lower() == "form" and newWord[breakdown+1] == "of":
								print("Found root: " + clean(newWord[breakdown+2]))
								checkFormsWord = parser.fetch(clean(newWord[breakdown+2]))

					elif "manner" in checkWord[entry]["definitions"][definitionNum]["text"][textNum]:
						newWord = clean(checkWord[entry]["definitions"][definitionNum]["text"][textNum].split())
						for breakdown in range(len(newWord)):
							if newWord[breakdown].lower() == "in" and newWord[breakdown+1] == "a":
								if newWord[breakdown+3] == "manner" or newWord[breakdown+3][:-1] == "manner":
									print("Found root: " + clean(newWord[breakdown+2]))
									checkFormsWord = parser.fetch(clean(newWord[breakdown+2]))


		checkWord = checkFormsWord

		resultEtymology = getEtymology(checkWord, cleanWord)

	if resultEtymology == '':
		body += word + " "
		print("Etymology not found")
	else:
		body += resultEtymology

print(body)

f = open('checkedtext.html','wb')

message = """<html>
<head></head>
<body><p>""" + body + """<br><br><span style=\"color: slategray\">Old English</span>
<br><span style=\"color: lightblue\">Old Norse</span>
<br><span style=\"color: royalblue\">French</span>
<br><span style=\"color: firebrick\">Latin</span>
<br>Other/Not Found</p></body>
</html>"""

message = message.encode('UTF-8')

f.write(message)
f.close()
