from bs4 import BeautifulSoup
import requests as req
import re


def get_beautifulsoup(url, sessionID):
    resp = req.get(url, cookies={'MoodleSession': sessionID})
    return BeautifulSoup(resp.content, 'html.parser')


def get_choices_and_right_answer(bs4_doc, nth):
    ans = 'No Answer.'
    choices = bs4_doc.select(
        "#q{} > div.content > div.formulation.clearfix > div.ablock > div.answer > div > label".format(nth))
    correct_ans = bs4_doc.select("#q{} > div.content > div.outcome.clearfix > div > div.rightanswer".format(nth))

    if len(correct_ans) > 0:
        ans = correct_ans[0].text
    else:  # if there is no right answer, check if the choice is corrected.
        for choice in bs4_doc.select(
                "#q{} > div.content > div.formulation.clearfix > div.ablock > div.answer > div".format(nth)):
            if choice.select('input')[0].get('checked') == 'checked':  # choosen answer
                gradetxt = bs4_doc.select('#q{} > div.info > div.grade'.format(nth))[0].text
                marks = re.findall('\d{1,}\.\d{1,}', gradetxt)
                if marks[0] == marks[1]:
                    ans = 'The correct answer is: ' + choice.select('label')[0].text
                    break
    return (choices, ans, (ans == 'No Answer.'))


def make_questions_answers(url_list, sessionID):
    results = {}  # {"question": {"choices":[], "right answer": "", "is_answer_corrected" : True | Flase }}

    # get all questions and their correct answer from urls
    for url in url_list:

        # get beutifulsoup
        doc = get_beautifulsoup(url, sessionID)
        for i in range(len(doc.find_all("div", {"class", "qtext"}))):
            question = doc.select("#q{} > div.content > div.formulation.clearfix > div.qtext".format(i + 1))[0].text
            if question not in results.keys() or not results[question][
                'is_answer_corrected']:  # this question has been answered correctly

                # answers and choices
                choices, ans, is_answer_corrected = get_choices_and_right_answer(doc, i + 1)

                # process a question
                a_question = {}  # the dict in 'results' variable
                temp_list = []  # list to store choices

                a_question["is_answer_corrected"] = is_answer_corrected
                a_question["right answer"] = ans

                for c in range(len(choices)):
                    temp_list.append(choices[c].text)
                a_question['choices'] = temp_list

                # post process
                results[question] = a_question
    return results


def add_to_file(questions, filename):
    f = open('{}.txt'.format(filename), 'a+', encoding='utf-8')
    tmp_questions = list(questions.keys())
    for i in range(len(tmp_questions)):
        f.write('{}) {}\n'.format(i + 1, tmp_questions[i]))
        f.write(' {}\n'.format('\n '.join(questions[tmp_questions[i]]['choices'])))
        f.write(questions[tmp_questions[i]]['right answer'] + '\n\n')
    f.write('\n------------------------------\n')
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