import os
import requests


def check_url(_dir):
    _dir = _dir.split("joomla\\")[1]
    url = "http://localhost:8072/joomla/"
    url = url + _dir
    url = url.replace("\\","/")
    r = requests.get(url)
    if "D:\\xampp" in r.text:
    	print url
        return 1

def check_jexec(dirss):
    for root, dirs, files in os.walk(dirss):
         for file in files:
            if "vendor" not in root:
                score = 0
                if file.endswith(".php"):
                    content = open(root + "\\" + file,'r').read()
                    if "defined('_JEXEC') or die" not in content:
                        score+= 1
                    if "require_once" in content or "require" in content or "include_once" in content or "include" in content or "use" in content:
                        score+= 1
                if score == 2:
                    #print "score: %d" % score
                    if check_url(root + "\\" + file) == 1:
                        print "In %s" % root
                        print "-> %s" % file

_dir = "D:\\xampp\\htdocs\\joomla\\"

check_jexec(_dir)