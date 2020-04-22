from bs4 import BeautifulSoup
import requests as req
import re

def get_beautifulsoup(url):
	resp = req.get(url, headers={"User-Agent":"Chrome/80.0.3987.163"})
	return BeautifulSoup(resp.content, 'html.parser')

'''
	Crawl from single link
'''
# def process_beautifulsoup(beautiful_soup_html):
# 	results = [] # [{"question": "", "right answer": "" }]
# 	doc = beautiful_soup_html	

# 	# get all questions and their correct answer
# 	ans = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-definitionText > span")
# 	questions = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-wordText > span")

# 	# for each question, get all choices + add to results
# 	for i in range(len(questions)):
# 		a_question = {} #the dict in 'results' variable
# 		a_question["question"] = re.sub(r'^\d+\. ', '', questions[i].get_text('\n'))
# 		a_question["right answer"] = ans[i].get_text('\n')
# 		results.append(a_question)

# 	return results


'''
	Crawl from multiple links
'''
def make_questions_answers(url_list):
	results = [] # [{"question": "", "choices":[], "right answer": "" }]
	all_questions = set()

	# get all questions and their correct answer from urls
	for url in url_list:

		# get beutifulsoup
		doc = get_beautifulsoup(url)

		# get all questions and their correct answer
		questions = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-definitionText > span")
		ans = doc.select("div.SetPageTerm-side > div > a.SetPageTerm-wordText > span")
		
		# for each question, get all choices + add to results
		for i in range(len(questions)):
			question = re.sub(r'^\d+\. ', '', questions[i].get_text('\n'))
			if question not in all_questions:
				a_question = {} #the dict in 'results' variable
				a_question["question"] = question
				a_question["right answer"] = ans[i].get_text('\n')

				# post process
				all_questions.add(question) # add the question to all_question set
				results.append(a_question)

	return results



def add_to_file(questions, filename):
	f = open('{}.txt'.format(filename), 'a+', encoding='utf-8')
	for i in range(len(questions)):
		f.write('{}) {}\n'.format(i + 1, questions[i]['question']))
		f.write('Answer:' + questions[i]['right answer'] + '\n\n')
	f.close()


def get_url_list():
	return re.split(r'\s{0,},\s{0,}', input('Enter url(s) to LMS quizzes [delimeter by \',\']: '))


def main():
	url_list = get_url_list()
	fileDes = input('Enter filename to save: ')

	try:		
		questions = make_questions_answers(url_list)
		add_to_file(questions, fileDes)
		print("Done!")
	except Exception as e:
		print('Error(s) occured: ' + str(e))
		

if __name__ == '__main__':
	main()
