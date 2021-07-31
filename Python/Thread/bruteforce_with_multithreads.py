import concurrent.futures
import threading
import itertools
import logging
import time

pass_len= 5
password_lists= list(map(''.join, itertools.product('0123456789', repeat= pass_len)))
# correct_pass= '20199' # one of the worst cases
correct_pass= '36000' # one of the best cases
number_of_threads= 500
result=''
successful= False
simulate_request_delay_time= 0.3


def do_bruteforce(password_lists, event, thread_no):
    global result
    global successful
    global simulate_request_delay_time

    for password in password_lists:
        # if event.is_set() or successful:
        if successful:
            # logging.info("Thread no. {} receives event. Exiting.".format(thread_no))
            return

        elif password == '': # tránh trường hợp pass rỗng
            continue

        elif password == correct_pass:
            time.sleep(simulate_request_delay_time) # pretends it is delay time when making request
            logging.info("Correct pass!: {}".format(password))
            result= password
            successful= True
            return
        else:
            time.sleep(simulate_request_delay_time) # pretends it is delay time when making 
            # logging.info("Incorrect pass: {}".format(password))
            pass

    # logging.info("Thread no. {} has the correct pass. Raise event and exiting.".format(thread_no))
    # event.set()
    return


def split_list_parts(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def bruteforce_pass_with_threads(password_lists):
    global number_of_threads
    event = threading.Event() # event when getting corrected pass

    # open bruteforce threads
    #   We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        # Start worker threads, each handles a set of data
        logging.info('Open {} threads'.format(number_of_threads))
        thread_no = 0
        for chunked_list in split_list_parts(password_lists, number_of_threads):
            thread_no += 1
            # print(len(chunked_list))
            executor.submit(do_bruteforce, chunked_list, event, thread_no)


def bruteforce_pass_no_thread(password_lists):
    global result
    global successful

    for password in password_lists:
        if password == correct_pass:
            time.sleep(0.2) # pretends it is delate time when making request
            logging.info("Correct pass!: {}".format(password))
            result= password
            successful= True
            break
        else:
            time.sleep(0.2) # pretends it is delate time when making 
            # logging.info("Incorrect pass: {}".format(password))
            pass
    return


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    ## Brute with threads
    print('Bruteforce OTP with len of {}'.format(pass_len))
    print('Delay time between each request: {}s'.format(simulate_request_delay_time))
    logging.info('Start')
    bruteforce_pass_with_threads(password_lists
        )
    logging.info('End')
    
    ## Brute without threads
    # print('Bruteforce without threads')
    # logging.info('Start')
    # bruteforce_pass_no_thread(password_lists)
    # logging.info('End')

    if successful:
        print('\n--------\nCorrect pass: ' + result)
    else:
        print('\n--------\nBetter luck next time!')
