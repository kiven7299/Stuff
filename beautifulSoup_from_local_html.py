from bs4 import BeautifulSoup

def make_questions_answers(file):
	results = [] # [{"question": "", "right answer": "" }]

	with open(file, "r", encoding="utf-8") as f:
		doc = BeautifulSoup(f, 'html.parser')

	# get all questions and their correct answer
	questions = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-definitionText > span")
	ans = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-wordText > span")


	# for each question, get all choices + add to results
	for i in range(len(questions)):
		a_question = {} #the dict in 'results' variable
		tmp = questions[i].text.replace('\r\n', '\n')
		a_question["question"] = tmp

		tmp = ans[i].text.replace('\r\n', '\n')
		a_question["right answer"] = tmp
		results.append(a_question)

	return results


def add_to_file(questions, filename):
	f = open(filename, 'a+', encoding="utf-8")
	for i in range(len(questions)):
		f.write('{}) {}\n'.format(i + 1, questions[i]['question']))
		f.write('Answer:' + questions[i]['right answer'] + '\n\n')
	f.close()


def main():
	reviewsFilePath = ["quizlet.html"]
	fileDes = "quizlet.txt"

	for file in reviewsFilePath:
		questions = make_questions_answers(file)
		add_to_file(questions, fileDes)


main()



		
