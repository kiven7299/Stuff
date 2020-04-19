from bs4 import BeautifulSoup
import requests as req


def get_beautifulsoup(url, sessionID):
	resp = req.get(url, cookies={'MoodleSession': sessionID})
	return BeautifulSoup(resp.content, 'html.parser')


def process_beautifulsoup(beautiful_soup_html):
	results = [] # [{"question": "", "choices":[], "right answer": [] }]
	doc = beautiful_soup_html

	# get all questions and their correct answer
	questions = doc.find_all("div", {"class", "qtext"})
	ans = doc.find_all("div", {"class", "rightanswer"})

	# for each question, get all choices + add to results
	for i in range(len(questions)):
		a_question = {} #the dict in 'results' variable
		temp_list = [] #list to store choices

		a_question["question"] = questions[i].text
		if len(ans) == 0:
			a_question["right answer"] = "No answer."
		else:
			a_question["right answer"] = ans[i].text

		choices = doc.select("#q{} > div.content > div.formulation.clearfix > div.ablock > div.answer > div > label".format(i + 1))
		for c in range(len(choices)):
			temp_list.append(choices[c].text)
		a_question['choices'] = temp_list
		results.append(a_question)

	return results


def make_questions_answers(url, sessionID):
	return process_beautifulsoup(get_beautifulsoup(url, sessionID))


def add_to_file(questions, filename):
	f = open('{}.txt'.format(filename), 'a+')
	for i in range(len(questions)):
		f.write('{}) {}\n'.format(i + 1, questions[i]['question']))
		f.write(' {}\n'.format('\n '.join(questions[i]['choices'])))
		f.write(questions[i]['right answer'] + '\n\n')
	f.close()


def main():
	url = input('Enter url to review: ')
	sessionID = input('Enter the MoodleSession cookie: ')
	fileDes = input('Enter filename to save: ')

	try:		
		questions = make_questions_answers(url, sessionID)
		add_to_file(questions, fileDes)
		print("Done!")
	except Exception as e:
		print('Error(s) occured: ' + str(e))


main()