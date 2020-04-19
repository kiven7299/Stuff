from bs4 import BeautifulSoup
import requests as req
import re

def get_beautifulsoup(url, sessionID):
	resp = req.get(url, cookies={'MoodleSession': sessionID})
	return BeautifulSoup(resp.content, 'html.parser')


def make_questions_answers(url_list, sessionID):
	results = [] # [{"question": "", "choices":[], "right answer": "" }]
	all_questions = set()

	# get all questions and their correct answer from urls
	for url in url_list:

		# get beutifulsoup
		doc = get_beautifulsoup(url, sessionID)
		questions = doc.find_all("div", {"class", "qtext"})
		for i in range(len(questions)):
			question = questions[i].text
			if question not in all_questions:

				# get question, answers and choices
				choices = doc.select("#q{} > div.content > div.formulation.clearfix > div.ablock > div.answer > div > label".format(i + 1))
				ans = doc.select("#q{} > div.content > div.outcome.clearfix > div > div.rightanswer".format(i + 1))
				

				# process a question
				a_question = {} #the dict in 'results' variable
				temp_list = [] #list to store choices

				a_question["question"] = question
				if len(ans) == 0:
					a_question["right answer"] = "No answer."
				else:
					a_question["right answer"] = ans[0].text
				
				for c in range(len(choices)):
					temp_list.append(choices[c].text)
				a_question['choices'] = temp_list

				# post process
				all_questions.add(question) # add the question to all_question set
				results.append(a_question)


	return results


def add_to_file(questions, filename):
	f = open('{}.txt'.format(filename), 'a+', encoding='utf-8')
	for i in range(len(questions)):
		f.write('{}) {}\n'.format(i + 1, questions[i]['question']))
		f.write(' {}\n'.format('\n '.join(questions[i]['choices'])))
		f.write(questions[i]['right answer'] + '\n\n')
	f.close()


def get_url_list():
	return re.split(r'\s{0,},\s{0,}', input('Enter url(s) to LMS quizzes [delimeter by \',\']: '))


def main():
	url_list = get_url_list()
	sessionID = input('Enter the MoodleSession cookie: ')
	fileDes = input('Enter filename to save: ')

	# try:		
	# 	questions = make_questions_answers(url_list, sessionID)
	# 	add_to_file(questions, fileDes)
	# 	print("Done!")
	# except Exception as e:
	# 	print('Error(s) occured: ' + str(e))

	questions = make_questions_answers(url_list, sessionID)
	add_to_file(questions, fileDes)
	print("Done!")


main()