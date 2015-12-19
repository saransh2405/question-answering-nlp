import os
import glob
from nltk import tokenize
import subprocess
import nltkChecker

def convertToASCII():
	quetionfile = open("questions.txt","r")
	corpusfile = open("corpus.txt","r")
	questions = quetionfile.read()
	corpus = corpusfile.read()
	questions = questions.decode('utf-8')
	corpus = corpus.decode('utf-8')
	corpus = tokenize.sent_tokenize(corpus)
	quetionfile.close()
	corpusfile.close()
	
	quetionfile = open("questions.txt","w")
	corpusfile = open("tempcorpus.txt","w")
	quetionfile.write(questions)
	for item in corpus:
  		corpusfile.write("%s\n" % item)
	quetionfile.close()
	corpusfile.close()
	return questions.split("\n")

def runQuestions(question):
	quetionfile = open("tempquestion.txt","w")
  	quetionfile.write(question)
	quetionfile.close()
	proc = subprocess.Popen(["./answer corpus.txt tempquestion.txt"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	if os.path.isfile("tempquestion.txt"):
		os.remove("tempquestion.txt")
	return out


def deleteTempFiles():
	filenames = ["tempcorpus.txt","NUL","corpus.parse","corpus.sst","tempquestion.txt"]
	for filename in filenames:
		if os.path.isfile(filename):
			os.remove(filename)


def main():
	questions = convertToASCII()
	for question in questions:
		print
		answer = runQuestions(question)
		nltkChecker.checkIfCorrectAnswer(question, answer)
	deleteTempFiles()

if __name__ == '__main__':
	main()