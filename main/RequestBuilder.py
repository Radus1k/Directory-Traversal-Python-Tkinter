import requests
from requests import cookies
from main.Fuzzer import req_Session, login_to_Site

import re


class RequestBuilder:
    def __init__(self, all_request, module, port, request_type, full_url):

        self.full_url_true = full_url
        self.location = get_second_word(all_request)
        self.module = module
        self.port = port
        self.request_type = request_type

        self.first_line = all_request.partition('\n')[0]
        self.link = get_second_word(self.first_line)
        self.user_agent = extract_header(all_request, "User-Agent:", 14)
        self.accept = extract_header(all_request, "Accept:", 10)
        self.cookie_string = extract_header(all_request, "Cookie:", 10)
        self.accept_language = extract_header(all_request, "Accept-Language:", 19)
        self.referer = extract_header(all_request, "Referer:", 11)
        self.host = extract_header(all_request, "Host:", 8)
        self.content_type = extract_header(all_request, "Content-Type:", 16)
        self.content_length = extract_header(all_request, "Content-Length:", 18)
        self.accept_encoding = extract_header(all_request, "Accept-Encoding:", 19)
        self.connection = extract_header(all_request, "Connection", 14)
        self.upgrade_insecure = extract_header(all_request, "Upgrade-Insecure-Requests:", 33)
        self.proxy_authorization = extract_header(all_request, "Proxy-Authorization:", 22)
        self.from_req = extract_header(all_request, "from=", 7)
        self.via = extract_header(all_request, "Via:", 6)
        self.upgrade = extract_header(all_request, "Upgrade:", 10)
        self.accept_charset = extract_header(all_request, "Access-Control-Request-Method:", 32)
        self.access_CRH = extract_header(all_request, "Access-Control-Request-Headers:", 33)
        self.authorization = extract_header(all_request, "Authorization:", 16)
        self.cache_control = extract_header(all_request, "Cache-Control:", 15)
        self.warning = extract_header(all_request, "Warning:", 9)
        self.x_token = extract_header(all_request, "X-Requested-With", 18)

        self.headers = {"Accept-Language": self.accept_language,
                        "Accept": self.accept,
                        "Accept-Charset": self.accept_charset,
                        "User-Agent": self.user_agent,
                        "Accepting-Encoding": self.accept_encoding,
                        "Access-Control-Request-Headers": self.access_CRH,
                        "Authorization": self.authorization,
                        "Cache-Control": self.cache_control,
                        #"Cookie": self.cookie_string,
                        "Content-Type": self.content_type,
                        #"Content-Length": self.content_length, #AICI
                        "Connection": self.connection,
                        "Referer": self.referer,
                        "Host": self.host,
                        "Proxy-Authorization": self.proxy_authorization,#SAU AICI
                        "Upgrade": self.upgrade,
                        "Via": self.via,
                        "Warning": self.warning,
                        "Upgrade-Insecure-Requests": self.upgrade_insecure,
                        "X-Requested-With": self.x_token,
                        "From": self.from_req}

    def print_headers(self):
        print(self.user_agent + "\n" + self.accept + "\n" + self.referer + "\n" + self.accept_language + "\n" +
              self.content_type + "\n" + self.content_length + "\n" + self.accept_encoding + "\n"
              + self.connection + "\n" + self.upgrade_insecure + "\n" + self.from_req)

    def get_response(self):
        login_to_Site()
        self.full_url = "http://" + self.host + self.link
        self.cookie = self.set_cookies()
        if self.request_type != "GET" and self.request_type != "POST":
            print("error" + self.request_type)
            return None
        # port = self.get_gui_Port()

        try:
            if self.request_type == "GET":
                print("url: " + self.full_url)
                print(self.cookie)
                response = req_Session.get(self.full_url,  cookies=self.cookie)
                #response = req_Session.get(self.full_url, headers=self.headers, cookies=self.cookie)

            else:
                response = req_Session.post(self.full_url, headers=self.headers, cookies=self.cookie)
            return response
        except req_Session.exceptions.RequestException as e:
            print(e)

    def set_cookies(self):
        try:
            self.cookie_string = "security=medium PHPSESSID=0ndt9teo4bv2qteja0uo5fqkjs"
            keys_and_values = self.cookie_string.split(" ")
            self.cookie = requests.cookies.RequestsCookieJar()
            for k in keys_and_values:
                self.cookie.set(k.split('=')[0], k.split('=')[1])
                #print(k.split('=')[0] + "  " + k.split('=')[1] + "\n")
            #print(self.cookie)
            return self.cookie
        except:
            print("bad syntax ma man")
            return ""

def get_second_word(text):
    breakUp = text.split(" ")
    return breakUp[1]

def extract_header(big_string, header_name, index):
    matched_line = [line for line in big_string.split('\n') if header_name in line]
    matched = str(matched_line)
    final_str = matched[index:]
    return final_str[:-2]
