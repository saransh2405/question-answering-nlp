import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

def questionType(question):
    if question.startswith("Who "):
        return "PERSON"
    elif question.startswith("When "):
        return "DATE"
    elif question.startswith("Where "):
        return "LOCATION"
    elif question.startswith("What "):
        return "NOUN"
    elif question.startswith(("Why ", "How ")):
        return "PHRASE"
    elif question.startswith("How many "):
        return "NUMERAL"
    elif question.startswith(("Is ", "Was ", "Will ", "Are ", "Were ", "Do ", "Does ", "Did ", "Have ", "Has ", "Can ")):
        return "BOOLEAN"
    else:
        return "UNKOWN"


def findABetterAns(question, prevLevel):
	corpusFile = open("tempcorpus.txt","r")
	data = corpusFile.read()
	corpusFile.close()

	data = data.split("\n")

	linedata = []
	questionParts = make_min(question,"q")


	confidenceLevels = []
	for sent in data:
		confidenceLevel = []
		matched = 0
		answerParts = make_min(sent, "a")
		for each in questionParts:
			if each in answerParts:
				matched += 1

		confidenceLevel.append(sent)
		confidenceLevel.append(matched*100/len(questionParts))
		confidenceLevels.append(confidenceLevel)

	potentialAns = []
	for ans in sorted(confidenceLevels, key=lambda x: x[1], reverse=True):
		if ans[1] > prevLevel:
			if questionType(question) == "PERSON" or questionType(question) == "NOUN":
				return ans
			tags = check(ans[0])
			ps = PorterStemmer()
			for tag in tags:
				if ps.stem(tag[0].upper()) in questionParts and "VB" in tag[1]:
					if questionType(question) == "DATE":
						index = [ans[0].upper().split().index(tag[0].upper())] if type(ans[0].upper().split().index(tag[0].upper())) is int else ans[0].upper().split().index(tag[0].upper())
						for eachindex in index:
							if eachindex+1 < len(ans[0].upper().split()):
								if ans[0].upper().split()[eachindex+1] == "ON":
									return ans
					elif questionType(question) == "LOCATION":
						index = [ans[0].upper().split().index(tag[0].upper())] if type(ans[0].upper().split().index(tag[0].upper())) is int else ans[0].upper().split().index(tag[0].upper())
						for eachindex in index:
							if eachindex+1 < len(ans[0].upper().split()):
								if ans[0].upper().split()[eachindex+1] == "IN":
									return ans

			
	return "none",0


def process(question):
    if question.lower().startswith(("who ","when ","where ","what ","why ")):
        return 2
    elif question.lower().startswith(("how ","is ", "was ", "will ", "are ", "were ", "do ", "does ", "did ", "have ", "has ", "can ")):
    	return 1
    elif question.lower().startswith("how many "):
        return 2
    else:
        return 0

def make_min(sentence,Qtype):
	sentence = sentence.upper()
	sentence = ' '.join([word for word in sentence.split() if word not in (stopwords.words('english'))])
	sentenceParts = []
	ps = PorterStemmer()
	if Qtype == "q":
		for i in range(process(sentence),len(sentence.strip("?").split())):
			sentenceParts.append(ps.stem(sentence.strip("?").split()[i]))
	else:
		for each in sentence.strip("?").split():
			sentenceParts.append(ps.stem(each))

	return sentenceParts


def checkIfCorrectAnswer(question, answer):
	questionParts = make_min(question, "q")
	answerParts = make_min(answer, "a")
	matched = 0
	for each in questionParts:
		if each in answerParts:
			matched += 1

	if matched == len(questionParts):
		print "100"+"%"+" confidence"
		print "Q",question
		print "Ans",answer
	else:
		if questionType(question) == "DATE" or questionType(question) == "LOCATION" or questionType(question) == "PERSON" or questionType(question) == "NOUN":
			print question
			reply = findABetterAns(question,matched*100/len(questionParts))
			if reply[1] > 0:
				print reply[0]
				print str(reply[1]) + "%" + " confidence"
			else:
				print "Only low confidence answer found"
				print "Ans",answer
				print str(matched*100/len(questionParts)) +"% "+ "confidence"
		else:
			print "Q",question
			print "Ans",answer
			print str(matched*100/len(questionParts)) +"% "+ "confidence"
	

def check(sentence):
	sentence = sentence.strip("?")
	text = word_tokenize(sentence)
	return nltk.pos_tag(text)

def main():
	checkIfCorrectAnswer("s","q")
	#check("d","d")
if __name__ == '__main__':
	main()

