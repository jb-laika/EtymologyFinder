from wiktionaryparser import WiktionaryParser
import json

text = " Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth."
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