import tkinter
from tkinter import Text
import webbrowser
import re
from main.Fuzzer import successful_headers, successful_texts

url_global = str()

def create_request_model(host, page, full_url):
    headers = "GET " + host + " HTTP/1.1\n" \
              "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0\n" \
              "Host: " + page + "\n" \
              "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\n" \
              "Accept-Language: en-US,en;q=0.5\n" \
              "Accept-Encoding: gzip, deflate\n" \
              "Referer: " + full_url + "\n" \
              "Content-Type: application/x-www-form-urlencoded\n" \
              "Connection: keep-alive\n" \
              "Upgrade-Insecure-Requests: 1\n"
    return headers


class FancyEntry(tkinter.Entry):
    def __init__(self, parent, url, parent_notebook, notebook_tools, tab_tools, tab5, resp_table, tab_comparer, comp_table1, comp_table2, *args, **kwargs):
        tkinter.Entry.__init__(self, parent, *args, **kwargs)
        self.full_url = url
        self.configure(background='#414550', cursor="hand2")
        self.parent = parent
        self.tab_tools = tab_tools
        self.parent_notebook = parent_notebook
        self.notebook_tools = notebook_tools
        self.tab5_par = tab5
        self.tab_comparer = tab_comparer
        self.comp_table1 = comp_table1
        self.comp_table2 = comp_table2
        self.request_table = resp_table
        self.popup_menu = tkinter.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="See in Web",
                                    command=self.open_in_browser)
        self.popup_menu.add_command(label="Send to requester creator",
                                    command=self.send_to_request)
        self.popup_menu.add_command(label="Send content to comparer",
                                    command=self.send_to_comparer)

        self.bind("<Button-3>", self.popup)  # Button-2 on Aqua
        self.bind("<Button-1>", self.popup)  # Button-2 on Aqua

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def open_in_browser(self):
        webbrowser.open(self.full_url, new=2)

    def get_host_only(self):
        result = re.search('//[^/]*', self.full_url)
        host = result.group(0)[2:]
        return host

    def get_link(self, host):
        poz = self.full_url.rfind(host)
        return self.full_url[len(host) + poz:]

    def get_url(self):
        global url_global
        url_global = self.full_url
        return url_global

    def send_to_comparer(self):
        print("SENT")
        for req in successful_texts:
            if req.find(self.full_url) != -1:
                if len(self.comp_table1.get('1.0', tkinter.END)) ==1 and len(self.comp_table2.get('1.0', tkinter.END)) == 1:
                    self.comp_table1.insert('1.0', req)

                elif len(self.comp_table1.get('1.0', tkinter.END)) >1 and len(self.comp_table2.get('1.0', tkinter.END)) == 1:
                    self.comp_table2.insert('1.0', req)

                elif len(self.comp_table1.get('1.0', tkinter.END)) > 1 and len(self.comp_table2.get('1.0', tkinter.END)) > 1:
                    self.comp_table1.delete('1.0', tkinter.END)
                    self.comp_table1.insert('1.0', req)

                else:
                    self.comp_table2.delete('1.0', tkinter.END)
                    self.comp_table2.insert('1.0', req)

                self.parent_notebook.select(self.tab_tools)
                self.notebook_tools.select(self.tab_comparer)

    def send_to_request(self):
        for request_header in successful_headers:
            if request_header.find(self.full_url) != -1:
                host = self.get_host_only()
                link = self.get_link(host)
                global url_global
                url_global = self.get_url()
                headers = create_request_model(link, host, self.full_url)
                self.request_table.insert('1.0', headers)
                self.parent_notebook.select(self.tab_tools)
                self.notebook_tools.select(self.tab5_par)
