import random
import tkinter
from tkinter import messagebox
import concurrent.futures
import main.fuzzing_vars as fv
from lxml.html import fromstring
from bs4 import BeautifulSoup
import requests
import time
from requests import cookies
import collections
import re
from main import crawl_links
from main.pdf_Generator import write_to_pdf
import time
from main.Mutators import MultipleMutation
from main.DB import DatabaseConnection


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


'''  This function s vulnerables links '''
successful_headers = list()
error_headers = list()
successful_texts = list()

req_Session = requests.session()


class FuzzEngine:
    def __init__(self, url, port, cookie, module, save_results, payloads, check_crawl_links, shell_file, check_head,
                 quite_mode, gui_proxy, threads_no, method, username, password, header_list, request_time, auth_data,
                 auth_check, user_agent, depth_no, mutator_value,check_rfi_bool):

        # Variables for  PDF PLOTS#
        self.plot_mutators = list()
        self.plot_mutators_count = int(0)
        self.plot_depth = int(0)
        self.plot_payload = list()
        self.plot_payload_count = int(0)
        self.plot_others = list()
        self.plot_all_y = list()
        self.plot_all_count = int(0)
        self.request_statuses = list()
        self.req_values = list()
        for i in range(10):
            self.req_values.append(0)


        #Fuzzing Variables
        self.status_interested_in = [200, 301, 302, 400, 403, 500]
        self.url = url
        self.check_rfi_b = check_rfi_bool
        self.pdf_url = str()
        self.http_headers = header_list
        self.dbConn = DatabaseConnection()
        self.plot_x = []  # time
        self.plot_y = []  # founded vulnerabilties
        self.plot_y_attempts = []
        self.time_per_request = 0.3
        self.request_time = request_time
        self.start = int(round(time.time()))
        self.attempts = int(0)
        self.port = port
        self.mutator_box = mutator_value
        # self.cookie = self.set_cookies(cookie)
        self.cookie = self.set_cookie_for_DWVA()
        self.payloads = payloads
        self.check_head = check_head
        self.method = list()
        self.auth_data_list = auth_data
        self.method.append(method)
        self.check_headf()
        self.threads_no = threads_no
        self.proxy = gui_proxy
        self.payload_content = list()  # list of strings for every payload file
        self.faults = int(0)
        self.admin = username
        self.user_agent = user_agent
        self.depth_no = depth_no
        self.rfi_check = bool(False)

        self.password = password
        self.responses_list = list()
        self.dots_exploitable = fv.dots_exploitable
        self.slashes_exploitable = fv.slashes_exploitable
        self.Special_Prefix_Patterns = fv.Special_Prefix_Patterns
        self.Special_Prefixes = fv.Special_Prefixes
        self.Special_Mid_Patterns = fv.Special_Mid_Patterns
        self.Special_Sufixes = fv.Special_Sufixes
        self.Special_Patterns = fv.Special_Patterns

        self.proxy_path = "proxy-list/proxy-list.txt"
        # self.payload_def_path = "Payloads/File Inclusion/Intruders/List_Of_File_To_Include_NullByteAdded.txt"
        self.payload_def_path = "Payloads/File Inclusion/Intruders/Web-files.txt"
        self.max_directories_depth = 5

        self.port = port
        self.module = module
        self.save_results_bool = save_results
        self.payloads_files = payloads
        self.check_craw_links = check_crawl_links
        self.shell_file = shell_file
        self.check_quite_mode = quite_mode
        self.full_url = self.get_full_url(self.url, self.module)
        self.fuzzer_paused = False
        self.fuzz_counter = 0
        self.check_timer()
        if auth_check:
            self.set_auth()

    def set_auth(self):
        global req_Session
        # U                 [user,                   pass]
        req_Session.auth = {self.auth_data_list[0], self.auth_data_list[1]}

    def set_user_agent(self):
        global req_Session
        if len(self.user_agent) > 2:
            user_agent_h = {'User-Agent': self.user_agent}
            req_Session.headers.update(user_agent_h)

    def check_headf(self):
        if self.check_head == 1:
            self.method.append("HEAD")

    def check_timer(self):
        if self.request_time > 0:
            self.time_per_request = self.request_time

    def get_url_indexes_to_inject(self, url, crawl=0):
        indexes = list()
        regex = re.compile('file=|page=|index.php|image=|home.php')
        match = regex.search(url)
        if crawl == 0:
            try:
                if match.end(0) != -1:
                    if "file=" or "page=" in url:# length of "page=" is 5 and teh match.end return the start of regex
                        indexes.append(match.end(0) + 5)
                    if "home.php" in url:#
                        indexes.append(match.end(0) + 8)
                    if "image=" in url:# length of "page=" is 5 and teh match.end return the start of regex
                        indexes.append(match.end(0) + 6)
                    if "index.php=" in url:
                        indexes.append(match.end(0) + 9)
            finally:
                indexes.append(len(url))
                return indexes
        else:
            try:
                if match.end(0) != -1:
                    return url
                else:
                    return ""
            except Exception as e:
                return ""
            finally:
                pass

    def extract_payloads(self):
        for payload_path in self.payloads:  # self.payloads its a list of filenames containing the malitious input
            if payload_path != '':
                if payload_path == "Default Payload":
                    payload_path = self.payload_def_path
                with open(payload_path, encoding='utf-8') as f:
                    content = f.readlines()
                content = [x.strip() for x in content]
                self.payload_content.append(content)
            else:
                messagebox.showerror(title="Bad payload", message="Please select valid payload path!")

    def pause_fuzzing(self):
        self.fuzzer_paused = True

    def resume(self, root):
        self.fuzzer_paused = False
        self.get_request_status(self.full_url, self.method, root)

    def start_fuzzing(self, root):
        # rand_proxy = args.randproxy
        # cookie = set_cookie_for_DWVA(cookie)
        self.extract_payloads()
        self.set_user_agent()
        self.write_crawl_links()# it may take too long, for big websites, like google for example
        # if rand_proxy is True:
        # proxy = get_rand_proxy, module)
        login_to_Site()
        self.set_http_headers()
        if self.check_rfi_b:
            self.check_rfi(root)
        self.fuzz_Engine(root)
        if self.save_results_bool:
            write_to_pdf(self.plot_x, self.plot_y, self.plot_payload_count, self.plot_mutators_count, self.plot_depth,
                         self.plot_all_count, self.attempts, self.faults, self.full_url, self.req_values,
                         self.request_statuses, self.rfi_check, self.pdf_url)
        self.dbConn.my_cursor.close()
        self.dbConn.connection.close()
        messagebox.showinfo("Info", "Fuzzing proccess ended!")
        # copy_db_to_android()

    def getFaults(self):
        return self.faults

    def add_depth(self, url, payload):
        bad_urls = list()
        if self.depth_no > 0:
            for i in range(self.depth_no):
                for prefix in fv.Special_Prefixes:
                    for mid in fv.Special_Mid_Patterns:
                        for suffix in fv.Special_Sufixes:
                            bad_url = url + prefix + mid * (i + 1) + payload + suffix
                            bad_urls.append(bad_url)
                            bad_url = url + mid * (i + 1) + payload  # + suffix
                            bad_urls.append(bad_url)
        return bad_urls

    def check_rfi(self, root):
        url_list = list()
        url_list.append("http://www.google.ro/")
        url_list.append("https://www.google.ro/")
        url_list.append("HTTP://WWW.GOOGLE.RO/")
        url_list.append("HTTPS://WWW.GOOGLE.RO/")
        for url in url_list:
            fuzzed = str(self.full_url[:-1] + url)
            status = self.send_request("GET", fuzzed)
            root.addrow("GET", status, fuzzed, 0)
            if status in self.status_interested_in:
                self.rfi_check = True
        return url_list

    def inject_dt(self, full_url):
        full_url = full_url.partition("\n")[0]
        indexes = self.get_url_indexes_to_inject(full_url, crawl=0)
        payloads = flatten(self.payload_content)
        url_vulnerables = list()
        for index in indexes:
            if index != -1:
                for payLoad in payloads:
                    url_bad = full_url[:index + 5] + payLoad
                    url_vulnerables.append(url_bad)
                    self.plot_payload_count = self.plot_payload_count + 1
                    if self.depth_no > 0:
                        url_depths = self.add_depth(full_url, payLoad)
                        url_vulnerables += url_depths
                        self.plot_depth += len(url_depths)
                    if self.mutator_box:
                        multObj = MultipleMutation(payLoad, 5)
                        res = multObj.fuzz_elem()
                        number_of_res = len(res)
                        self.plot_mutators_count += number_of_res
                        for ind in res:
                            url_bad = full_url[:index + 5] + ind
                            # url_vulnerables.append(url_bad)
                            # self.plot_mutators_count = self.plot_mutators_count + 1
                            url_vulnerables.append(url_bad)
        return url_vulnerables

    def send_request(self, method, url):
        global req_Session
        self.attempts = self.attempts + 1
        # self.plot_x.append(int(round(time.time())) - self.start)
        req = requests.Request
        try:
            if method == "GET":
                req = req_Session.get(url, cookies=self.cookie, proxies=self.proxy, timeout=self.time_per_request)
                # req = req_Session.get(url)#, cookies=self.cookie)

            elif method == "POST":
                req = req_Session.post(url, cookies=self.cookie, proxies=self.proxy, timeout=self.time_per_request)

            elif method == "HEAD":
                req = req_Session.head(url, cookies=self.cookie, proxies=self.proxy, timeout=self.time_per_request)

            else:  # default get
                req = req_Session.get(url, cookies=self.cookie, proxies=self.proxy, timeout=self.time_per_request)

            successful_headers.append(req.url + "\n" + str(req.headers))
            successful_texts.append(url + "\n" + req.text)

            # if req_Session.status_code in self.status_interested_in :

            # successful_headers.append(str(req_Session.url) + "\n" + str(req_Session.headers))
            # error_headers.append(str(req_Session.url) + "\n" + str(req_Session.headers))

            # if req.status_code not in self.status_interested_in:
            # if req_text.find("Failed opening") > 0 or req_text.find("such") > 0 or req_text.find("Error") > 0:
            # self.faults = self.faults + 1
            # self.plot_x.append(self.faults)
            # self.plot_y.append(int(round(time.time())) - self.start)
            # return req_Session.status_code
            al = req.text

            title = str((al[al.find('<title>') + 7: al.find('</title>')]))
            if title.find("Not found") > 0 or title.find("File not found") > 0 or title.find("404 Not Found") > 0:
                # 204 request but actually a 404
                self.plot_x.append(self.attempts)
                self.plot_y.append(self.faults)
                return 404

            if req.status_code in self.status_interested_in:
                text = req.text
                if text.find("No such file or directory in") > 0 or text.find("not found") > 0 or text.find(
                        "Failed opening") > 0 or text.find("This page isn't available") and url.find(
                    "http") < 0 and url.find("HTTP") < 0:
                    self.plot_x.append(self.attempts)
                    self.plot_y.append(self.faults)

                    return 404
                else:
                    self.pdf_url += url + '\n'
                    self.faults = self.faults + 1
                    self.plot_y.append(self.faults)
                    self.plot_x.append(self.attempts)
                    return 200
            # if req_text not in self.responses_list:
            #   #self.responses_list.append(req_text)
            # else:
            #   return 404
            # return req.status_code

        except ConnectionError as e:
            print("error at request" + str(e))
        except requests.Timeout as req_timeout:
            print("Coneection Timeout !!" + str(req_timeout))

        self.plot_x.append(self.attempts)
        self.plot_y.append(self.faults)
        return req.status_code

    def write_crawl_links(self):
        time_in_sec = time.time()
        full_url = self.get_full_url(self.url, self.module)
        if self.check_craw_links == 1:
            crawled_links = crawl_links.getAllUrl(full_url, time_in_sec)# maxim 30 seconds for this operation

            with open('crawl_links', 'w') as f:
                for link in crawled_links:
                    ans = self.get_url_indexes_to_inject(link, crawl=1)
                    if len(ans) > 2: # or not equal to ""
                        f.write("%s\n" % link)

    def fuzz_Engine(self, root):
        full_url = self.get_full_url(self.url, self.module)
        fuzzed_urls = self.inject_dt(full_url)
        # all_urls = mutator_list + fuzzed_urls
        ##fuzzed_urls = [fuzzed_urls, mutator_list]
        for method in self.method:
            self.get_request_status(fuzzed_urls, method, root)
            self.fuzz_counter = 0

    def get_request_status(self, fuzzed_urls, method, root):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads_no) as executor:
            url_list = {executor.submit(self.send_request, method, url): url for url in
                        fuzzed_urls[self.fuzz_counter:]}
            for future in concurrent.futures.as_completed(url_list):
                fuzzed = url_list[future]
                try:
                    status = future.result()
                    if status not in self.request_statuses:
                        self.request_statuses.append(status)
                        self.req_values[self.request_statuses.index(status)] = 1
                    else:
                        self.req_values[self.request_statuses.index(status)] += 1

                    if not self.fuzzer_paused:
                        self.fuzz_counter = self.fuzz_counter + 1
                        self.dbConn.send_values([self.full_url, fuzzed, status, len(fuzzed)])
                        if self.check_quite_mode == 0:
                            root.addrow(method, status, fuzzed, len(fuzzed))

                            tkinter.Frame.update(root)
                        elif self.check_quite_mode == 1 and status in self.status_interested_in:
                            root.addrow(method, status, fuzzed, len(fuzzed))
                            tkinter.Frame.update(root)
                        else:
                            break
                    else:
                        break

                except Exception as e:
                    if "timed out" in str(e):
                        status = 408
                        root.addrow(method, status, fuzzed, len(fuzzed))
                        self.fuzz_counter = self.fuzz_counter + 1
                        self.dbConn.send_values([self.full_url, fuzzed, status, len(fuzzed)])
                        tkinter.Frame.update(root)
                    else:
                        print("Error here at rquest status: " + str(e))
            del executor

    def get_full_url(self, url, module):
        if len(self.port) < 2:
            if url.find("http:") == -1:
                return module + "://" + self.url
            else:
                return self.url
        else:
            if url.find("http:") == -1:
                return module + "://" + self.url + ":" + str(self.port) + "/"
            else:
                return self.url + ":" + str(self.port) + "/"

    '''Set cookies params from a long string by splitting it '''

    def set_cookies(self, string):
        keys_and_values = string.split()
        self.cookie = requests.cookies.RequestsCookieJar()
        for k in keys_and_values:
            self.cookie.set(k.split('=')[0], k.split('=')[1])
        return self.cookie

    @staticmethod
    def set_cookie_for_DWVA():
        cookie = requests.cookies.RequestsCookieJar()
        security = 'security'
        security_value = 'low'
        session = 'PHPSESSID'
        # response = requests.post('http://127.0.0.1/dvwa/login.php',
        #                        data={'username': 'admin', 'password': 'password', 'Login': 'Login'})
        session_value = 'k54r976mqr4qqe28s679tfitua'
        cookie.set(security, security_value)
        cookie.set(session, session_value)
        return cookie

    ''' Generate random proxy from list'''

    def get_rand_proxy(self):
        rand = random.randrange(10, 310)
        with open(self.proxy_path) as f:
            lines = f.readlines()
            line_proxy = lines[rand + 1]
        proxyDict = {"http": self.module + "://" + line_proxy.split()[0],
                     "https": self.module + "://" + line_proxy.split()[0]
                     }
        return proxyDict

    def set_http_headers(self):
        global req_Session
        headers_tuple = {}
        for tuple_ in self.http_headers:
            headers_tuple[tuple_[0]] = tuple_[1]
        req_Session.headers = headers_tuple


def get_iplist_from_file(filename):
    with open(filename) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    return content


def write_response(req, filename):
    with open(filename, "w") as f:
        f.write(str(req, 'utf8'))
        f.write('\n\n\n')
        f.close()

def signal_handler(signum, frame):
    raise Exception("Timed out!")

def login_to_Site():
    global req_Session
    login_payload = {'username': 'admin', 'password': 'password', 'Login': 'Login'}
    try:
        response = req_Session.get('http://127.0.0.1:8080/DVWA-master/login.php')
        token = re.search("user_token'\s*value='(.*?)'", response.text).group(1)
        login_payload['user_token'] = token
        p = req_Session.post('http://127.0.0.1:8080/DVWA-master/login.php', data=login_payload)
    except:
        print("cannot log in")
    finally:
        pass
