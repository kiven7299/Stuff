from bs4 import BeautifulSoup
import requests as req
import re

def get_beautifulsoup(url, sessionID):
	resp = req.get(url, cookies={'MoodleSession': sessionID})
	return BeautifulSoup(resp.content, 'html.parser')


def get_choices_and_right_answer(bs4_doc, nth, is_ans_available):
	ans = ''
	choices = bs4_doc.select("#q{} > div.content > div.formulation.clearfix > div.ablock > div.answer > div > label".format(nth))
	
	if is_ans_available:
		ans = bs4_doc.select("#q{} > div.content > div.outcome.clearfix > div > div.rightanswer".format(nth))
	else: # if there is no right answer, check if the choice is corrected.
		ans = 'No Answer.'
		for choice in bs4_doc.select("#q{} > div.content > div.formulation.clearfix > div.ablock > div.answer > div".format(nth)):
			if choice.select('input')[0].get('value') == '1': # choosen answer
				gradetxt = bs4_doc.select('#q{} > div.info > div.grade'.format(nth))[0].text
				marks = s = re.findall('\d{1,}\.\d{1,}', gradetxt)
				if marks[0] == marks[1]:
					ans = choice.select('label')[0].text
					break
	return (choices, ans)


def make_questions_answers(url_list, sessionID, is_ans_available):
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
				choices, ans = get_choices_and_right_answer(doc, i + 1, is_ans_available)
				
				# process a question
				a_question = {} #the dict in 'results' variable
				temp_list = [] #list to store choices

				a_question["question"] = question
				a_question["right answer"] = 'Answer: ' + ans
				
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
	f.write('\n------------------------------\n')
	f.close()


def get_url_list():
	return re.split(r'\s{0,},\s{0,}', input('Enter url(s) to LMS quizzes [delimeter by \',\']: '))


def main():
	url_list = get_url_list()
	sessionID = input('Enter the MoodleSession cookie: ')
	is_ans_available = (input('Answer avaiable? [y|others]: ') == 'y')
	fileDes = input('Enter filename to save: ')	

	try:		
		questions = make_questions_answers(url_list, sessionID, is_ans_available)
		add_to_file(questions, fileDes)
		print("Done!")
	except Exception as e:
		print('Error(s) occured: ' + str(e))

main()
