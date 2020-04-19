from bs4 import BeautifulSoup
import requests as req
import re

def get_beautifulsoup(url):
	resp = req.get(url, headers={"User-Agent":"Chrome/80.0.3987.163"})
	return BeautifulSoup(resp.content, 'html.parser')


def process_beautifulsoup(beautiful_soup_html):
	results = [] # [{"question": "", "right answer": "" }]
	doc = beautiful_soup_html	

	# get all questions and their correct answer
	questions = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-definitionText > span")
	ans = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-wordText > span")

	# for each question, get all choices + add to results
	for i in range(len(questions)):
		a_question = {} #the dict in 'results' variable
		a_question["question"] = re.sub(r'^\d+\. ', '', questions[i].get_text('\n'))
		a_question["right answer"] = ans[i].get_text('\n')
		results.append(a_question)

	return results


def make_questions_answers(url):
	return process_beautifulsoup(get_beautifulsoup(url))


def add_to_file(questions, filename):
	f = open('{}.txt'.format(filename), 'a+', encoding='utf-8')
	for i in range(len(questions)):
		f.write('{}) {}\n'.format(i + 1, questions[i]['question']))
		f.write('Answer:' + questions[i]['right answer'] + '\n\n')
	f.close()


def main():
	url = input('Enter quizlet url: ')
	fileDes = input('Enter filename to save: ')

	try:		
		questions = make_questions_answers(url)
		add_to_file(questions, fileDes)
		print("Done!")
	except Exception as e:
		print('Error(s) occured: ' + str(e))


main()



		
