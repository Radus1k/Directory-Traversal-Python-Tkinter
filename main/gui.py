import time
import webbrowser
from datetime import datetime
import requests
from requests import cookies

from tkinter import *  # filedialog, Button, IntVar, Text, Menu, Frame ,Scale, PhotoImage, StringVar, Scale, Tk, Label
from tkinter import messagebox, ttk, filedialog
from tkinter.font import Font

from PyQt5.QtWidgets import QApplication

import main.fuzzing_vars as fv
from main.Encoding import Encoder
from main.Fuzzer import FuzzEngine
from main.RequestBuilder import RequestBuilder
from main.monitoring_table import SimpleTable

entry_var = None
app = None


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.arrow = PhotoImage(file=r"images/arrow.png")
        self.arrow_ph = self.arrow.subsample(10, 10)

        self.int_proxy = IntVar()
        self.method = "GET"
        self.bool_quite_mode = IntVar()
        self.bool_crawl_links = IntVar()
        self.head_box = IntVar()
        self.save_fuzzing_results = IntVar()
        self.treads_no = Scale()
        self.mutators_box = BooleanVar()
        self.timeout_Value = Text()
        self.request_model = fv.request_model
        self.style = ttk.Style()
        self.style.configure("BW.TLabel", foreground="black", background="white")
        self.myFont = Font(family="Helvetica", size=15)
        self.myFont_italic = Font(family="Helvetica", size=15, slant="italic")
        self.tab_parent = ttk.Notebook(self, width=1500, height=800)
        self.payloads_files = []
        self.proxyDict = dict()
        self.isPaused = False
        self.black = "#282c36"
        self.grey = "#414550"
        self.user_agent_boolean = BooleanVar()
        self.blue_btn_color = "#9fb4bf"
        self.cookie_data_file = str()
        self.user_agent_str = str()

        # Import the Notebook.tab element from the default theme
        noteStyler = ttk.Style()
        noteStyler.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {"configure": {"padding": [100, 100]}, }})
        noteStyler.element_create('Plain.Notebook.tab', "from", 'default')
        # Redefine the TNotebook Tab layout to use the new element
        noteStyler.layout("TNotebook.Tab",
                          [('Plain.Notebook.tab', {'children':
                                                       [('Notebook.padding', {'side': 'top', 'children':
                                                           [('Notebook.focus', {'side': 'top', 'children':
                                                               [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                                                                'sticky': 'nswe'})],
                                                                              'sticky': 'nswe'})],
                                                   'sticky': 'nswe'})])

        # noteStyler.configure('Plain.Notebook.tab', settings={
        #    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        #    "TNotebook.Tab": {"configure": {"padding": [100, 10],
        #                                    "font": ('URW Gothic L', '11', 'bold')}}})

        noteStyler.configure("TNotebook", background=self.black, borderwidth=0)
        noteStyler.configure("TNotebook.Tab", background=self.blue_btn_color, foreground=self.black,
                             lightcolor="#0000FF", borderwidth=2, font="Helvetica 13")

        self.tab2 = ttk.Frame(self.tab_parent)
        self.tab3 = ttk.Frame(self.tab_parent, style="BW.TLabel", width=1200, height=1500)
        self.tab4 = ttk.Frame(self.tab_parent)
        self.tab_help = ttk.Frame(self.tab_parent)
        self.tab6 = ttk.Frame(self.tab_parent)
        self.tab_tools = ttk.Frame(self.tab_parent)

        self.tools_notebook = ttk.Notebook(self.tab_tools, width=1500, height=700)

        self.tab_comparer = ttk.Frame(self.tools_notebook)
        self.tab_decoder = ttk.Frame(self.tools_notebook)
        self.tab5 = ttk.Frame(self.tools_notebook)

        self.advanced = ttk.Notebook(self.tab4)

        self.cookies = ttk.Frame(self.advanced)
        self.payloads = ttk.Frame(self.advanced)
        self.authentification = ttk.Frame(self.advanced)
        self.http_settings = ttk.Frame(self.advanced)

        ''' Initialize TABS'''

        self.menubar = Menu(self)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.restart_app)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.donothing)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.tree = ttk.Treeview(self.http_settings)

        self.master.config(menu=self.menubar)

        self.start_time = time.time()
        # self.cookie_Entry = Entry(self.tab4, font=self.myFont, text="Format: var=value", state=DISABLED).grid(row=4, column=0)
        self.iterations = int(0)
        self.grid()
        self.create_main()
        self.director = ""
        self.tableRows = 0  # count the rows of the table

    ''' Create 2 Frames(Tables), pack them left / LEFT '''

    def restart_app(self):
        # self.destroy()c
        # run()
        print("wroking on it")

    # def go_to_requests(self):
    #    self.tab_tools.select(self.tab5)

    def go_to_comparer(self):
        self.tab_parent.select(self.tab_comparer)

    def create_Comparer(self):
        self.tab_comparer.configure(style='Black.TLabelframe')

        self.comp_button = Button(self.tab_comparer, text="Compare", command=self.comparer_compare, font="Helvetica 15"
                                  , fg='black', bg=self.blue_btn_color, width=10).pack(side=TOP, anchor=CENTER,
                                                                                       pady=(10, 10),
                                                                                       padx=(240, 240))

        tabs_Frame = Frame(self.tab_comparer)
        self.comp_button = Button(tabs_Frame, text="Paste", command=self.paste_to_comp1, font="Helvetica 15"
                                  , fg='black', bg=self.blue_btn_color, width=10).pack(side=LEFT, anchor=N)

        self.compare_Table1 = Text(tabs_Frame, height=20, width=60, borderwidth=2, relief="groove", bg=self.grey,
                                   fg=self.blue_btn_color)
        self.compare_Table1.pack(side=LEFT, padx=(20, 20), anchor=N)

        self.compare_Table2 = Text(tabs_Frame, height=20, width=60, borderwidth=2, relief="groove", bg=self.grey,
                                   fg=self.blue_btn_color)
        self.compare_Table2.pack(side=LEFT, padx=20, anchor=N)

        self.comp2_button = Button(tabs_Frame, text="Paste", command=self.paste_to_comp2, font="Helvetica 15"
                                   , fg='black', bg=self.blue_btn_color, width=10).pack(side=LEFT, anchor=N)

        tabs_Frame.configure(background='#282c36', borderwidth=2)
        tabs_Frame.pack()

        self.back_button = Button(self.tab_comparer, text="Back to Monitoring", command=self.back_to_monitoring,
                                  font="Helvetica 15", width=100,
                                  fg='black', bg=self.blue_btn_color).pack(side=BOTTOM, expand=True)

    def back_to_monitoring(self):
        self.tab_parent.select(self.tab3)

    def paste_to_comp1(self):
        try:
            clipboard_str = self.clipboard_get()
            self.compare_Table1.insert(END, clipboard_str)
        except:
            messagebox.showwarning("Warning", "Empty Clipboard")

    def paste_to_comp2(self):
        try:
            clipboard_str = self.clipboard_get()
            self.compare_Table2.insert(END, clipboard_str)
        except:
            messagebox.showwarning("Warning", "Empty Clipboard")

    def comparer_compare(self):
        print("comparing")

        table1_Str = self.compare_Table1.get('1.0', END)
        table2_Str = self.compare_Table2.get('1.0', END)

        table1_list = table1_Str.splitlines()
        table2_list = table2_Str.splitlines()

        equal_Texts = bool(True)

        for x in range(len(table1_list)):
            if table1_list[x] != table2_list[x]:
                # print("conflict at line " + str(x))
                messagebox.showinfo(title="Not matching!", message="conflict at line " + str(x + 1))
                equal_Texts = False
                break
        if equal_Texts:
            messagebox.showinfo(title="Matching!", message="Texts are equal!")

    def donothing(self):
        print("nothing")

    def send_Request(self):
        from main.Mon_Properties import url_global
        module = self.get_gui_module()
        all_request = self.request_Table.get('1.0', END)
        request_type = self.request_Table.get('1.0', '1.3')
        port = self.get_gui_Port()
        full_url = url_global
        aux_url = self.get_gui_Port()
        if len(aux_url) > 1:
            pass
            # full_url = aux_url

        self.response_Table.delete('1.0', END)
        builder = RequestBuilder(all_request, module, port, request_type, full_url)
        response = builder.get_response()

        self.response_Table.insert('1.0', response.headers)
        self.response_Table.insert(END, "\n\n")
        self.response_Table.insert(END, response.content)

    def create_Requests(self):
        self.tab5.configure(style='Black.TLabelframe')
        self.create_two_tabels("Request", "Response",
                               "Send", "See Response On Web", self.tab5, self.myFont, self.send_Request)

    def see_on_browser(self):
        html_content = self.response_Table.get('1.0', END)
        f = open("response.html", "wb")
        f.write(html_content.encode())
        webbrowser.open_new_tab('response.html')

    def delete_payload(self):
        selection = self.listBox.curselection()
        if selection:
            self.listBox.delete(selection)
        else:
            messagebox.showinfo("Eroare", "Niciun payload selectat!")

    def create_Advanced(self):
        self.payloads.configure(style='Black.TLabelframe')
        # self.payloads.configure(background=self.black, highlightbackground="white", highlightthickness=2)
        self.payload_Title = Label(self.payloads, text="Payloads", font="Helvetica 15", fg=self.blue_btn_color,
                                   bg=self.grey)
        self.payload_Title.grid(row=0, column=0, padx=50, pady=(20, 5), sticky=NW, columnspan=2)

        self.listBox = Listbox(self.payloads, highlightthickness=3, highlightbackground=self.blue_btn_color,
                               highlightcolor=self.blue_btn_color,
                               fg=self.blue_btn_color, bg=self.grey, font=self.myFont, selectmode=SINGLE)

        self.listBox.config(width=90, height=10)
        self.listBox.xview_moveto(1)
        #self.listBox.insert(ACTIVE, "Default Payload")
        self.listBox.grid(row=1, column=0, sticky=W, padx=50)

        # Label(payloads_Frame, text="Add/Delete a payload:", font=self.myFont, fg=self.blue_btn_color, bg=self.grey).grid(row=1,column=0, sticky=W,padx=50, pady=10)

        self.add_img = PhotoImage(file=r"images/plus.png")
        self.add_ph = self.add_img.subsample(20, 20)

        self.del_img = PhotoImage(file=r"images/minus.png")
        self.del_ph = self.del_img.subsample(10, 10)

        self.save = PhotoImage(file=r"images/save.png")
        self.save_ph = self.save.subsample(8, 8)

        add_button = Button(self.payloads, font="Helvetica 10", text="Add Payload", compound=LEFT, image=self.add_ph,
                            command=self.browse_button, bg=self.blue_btn_color, width=130)
        add_button.grid(row=1, column=0, sticky=NW, padx=1048)

        delete_button = Button(self.payloads, font="Helvetica 10", text="Delete Payload", compound=LEFT,
                               image=self.del_ph, command=self.delete_payload, bg=self.blue_btn_color, width=130)
        delete_button.grid(row=1, column=0, sticky=NW, padx=1048, pady=40)  # pady=(100, 0)
        # payloads_Frame.grid(row=0, column=0, sticky=NSEW)

        ''' add cookies'''

        self.cookies.configure(style='Black.TLabelframe')
        self.cookie_var = IntVar()
        self.Cookie_Table = Label(self.cookies, text="Cookies", font="Helvetica 15", fg=self.blue_btn_color,
                                  bg=self.grey)
        self.Cookie_Table.grid(padx=50, pady=(20, 5), sticky=NW)

        self.cookie_Check = Checkbutton(self.cookies, text="Use specific cookie", font=self.myFont,
                                        variable=self.cookie_var, command=self.enable_entry, fg=self.blue_btn_color,
                                        bg=self.grey)

        self.cookie_Check.grid(row=1, column=0, columnspan=2, padx=50, pady=10, sticky=NW)

        global entry_var
        entry_var = StringVar()

        self.cookie_Entry = Entry(self.cookies, textvariable=entry_var, font=self.myFont_italic, fg=self.blue_btn_color,
                                  bg=self.grey,
                                  disabledforeground=self.blue_btn_color, disabledbackground=self.grey)

        entry_var.set("Format: var=value, var=value")

        self.cookie_Entry.grid(row=2, column=0, sticky=W, padx=50, pady=(0, 30))
        self.cookie_browse = IntVar()
        self.shell_var = IntVar()
        self.cookie_Label = Checkbutton(self.cookies, text="Use a file containing the cookie", font=self.myFont,
                                        variable=self.cookie_browse, command=self.toogle_browse, fg=self.blue_btn_color,
                                        bg=self.grey)
        self.cookie_Label.grid(row=3, column=0, columnspan=2, sticky=W, pady=(10, 0), padx=50)
        self.cookie_Label.grid(row=3, column=0, columnspan=2, sticky=W, pady=(10, 0), padx=50)

        self.browsing_button = Button(self.cookies, font=self.myFont, state=NORMAL, text="Upload Cookie",
                                      command=self.browse_cookie, fg='black', bg=self.blue_btn_color).grid(row=4,
                                                                                                           column=0,
                                                                                                           sticky=NW,
                                                                                                           pady=10,
                                                                                                           padx=50)

        self.entry_user_var = StringVar()
        self.entry_password_var = StringVar()
        self.cookie_label_var = StringVar()
        self.php_label_var = StringVar()

        self.entr_cookie = Entry(self.cookies, font="Helvetica 15", width=40, textvariable=self.cookie_label_var,
                                 fg=self.blue_btn_color, bg=self.grey, state=DISABLED,
                                 disabledforeground=self.blue_btn_color,
                                 disabledbackground=self.grey)
        self.entr_cookie.xview_moveto(1)

        self.entr_cookie.config(width=20)
        self.php_var = IntVar()
        self.domain_var = StringVar()
        self.entr_cookie.grid(row=5, column=0, sticky=NW, pady=10, padx=50)

        rfi_Frame = Frame(self.tab4)

        self.authentification.configure(style='Black.TLabelframe')

        self.login_Title = Label(self.authentification, text="Http Authentication", font="Helvetica 15",
                                 fg=self.blue_btn_color, bg=self.grey)
        self.login_Title.configure(anchor=CENTER)
        self.login_Title.grid(padx=50, pady=(20, 5), sticky=NW, columnspan=2)

        self.auth_var = BooleanVar()
        self.auth_check = Checkbutton(self.authentification, text="Use HTTP Authentication", font=self.myFont,
                                      variable=self.auth_var, command=self.auth_func, fg=self.blue_btn_color,
                                      bg=self.grey)

        self.auth_check.grid(row=1, column=0, pady=10, sticky=W, padx=50)
        self.user_Entry = Entry(self.authentification, font=self.myFont_italic, width=20,
                                textvariable=self.entry_user_var,
                                fg=self.blue_btn_color, bg=self.grey, disabledforeground=self.blue_btn_color,
                                disabledbackground=self.grey)
        self.user_Entry.bind("<Button-1>", self.clear_entry)

        self.user_Entry.insert(0, 'add username ')

        self.password_Entry = Entry(self.authentification, font=self.myFont_italic, width=20,
                                    textvariable=self.entry_password_var,
                                    fg=self.blue_btn_color, bg=self.grey, disabledforeground=self.blue_btn_color,
                                    disabledbackground=self.grey)

        self.password_Entry.insert(0, 'add password')
        self.password_Entry.bind("<Button-1>", self.clear_pass_entry)

        self.user_Entry.grid(row=2, column=0, pady=10, sticky=W, padx=50)
        self.password_Entry.grid(row=3, column=0, pady=10, sticky=W, padx=50)

        self.php_check = Checkbutton(rfi_Frame, text="Use PHP Shell Exploit", font=self.myFont,
                                     variable=self.php_var, command=self.exploit_func, fg=self.blue_btn_color,
                                     bg=self.grey)
        self.php_check.grid(row=1, column=0, padx=50, sticky=W, pady=(0, 20))
        # self.cookie_Label.grid(row=9, column=0, sticky=W, padx=10)

        self.php_button = Button(rfi_Frame, font=self.myFont, text="Upload Shell", command=self.upload_func,
                                 fg='black', bg=self.blue_btn_color)
        self.php_button.grid(row=2, column=0, sticky=W, pady=(10, 0), padx=50)

        self.entr_php = Entry(rfi_Frame, width=20, font="Helvetica 15", textvariable=self.php_label_var,
                              fg=self.blue_btn_color,
                              bg=self.grey)
        self.entr_php.grid(row=3, column=0, sticky=W, padx=50)

        save_button = Button(self.tab4, text="Save Settings", font=self.myFont, compound=LEFT, image=self.arrow_ph,
                             fg='black', bg=self.blue_btn_color, command=self.save_fuzzer_context)
        # save_button.grid(row=5, column=0, columnspan=3, sticky=S, pady=70, padx=50)
        save_button.config(height=30, width=700)

        self.http_settings.configure(style='Black.TLabelframe')

        ip_Text = Label(self.http_settings, font=self.myFont,
                        text="Timeout per request( seconds)",
                        fg=self.blue_btn_color, background='#282c36')
        ip_Text.grid(row=1, column=0, sticky=W, pady=(20, 5), padx=50)

        self.timeout_Value = Text(self.http_settings, font=self.myFont, height=1, width=10, bg=self.grey,
                                  fg=self.blue_btn_color)
        self.timeout_Value.grid(row=2, column=0, sticky=W, padx=50)

        self.tree = ttk.Treeview(self.http_settings)

        http_style = ttk.Style(self.http_settings)
        http_style.theme_use("clam")
        http_style.configure("Treeview", background=self.grey,
                             fieldbackground=self.grey, foreground=self.blue_btn_color)

        self.tree["columns"] = ("one", "two")
        self.tree.column("#0", width=1, minwidth=1, stretch=NO)
        self.tree.column("one", width=150, minwidth=150, stretch=NO)
        self.tree.column("two", width=350, minwidth=350, stretch=NO)

        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("one", text="HTTP Header", anchor=W)
        self.tree.heading("two", text="Value", anchor=S)

        ip_Text = Label(self.http_settings, font=self.myFont,
                        text="Http Headers",
                        fg=self.blue_btn_color, background='#282c36')
        ip_Text.grid(row=3, column=0, sticky=W, pady=(50, 0), padx=50)

        self.tree.grid(row=4, column=0, sticky=W, padx=50, pady=10)

        self.header_add = Button(self.http_settings, text="Add Header", command=self.add_tree, image=self.add_ph,
                                 compound=LEFT, width=100)
        self.header_add.grid(row=4, column=0, padx=(555, 0), sticky=NW, pady=(10, 0))

        self.header_del = Button(self.http_settings, text="Delete Header", command=self.delete_tree, image=self.del_ph,
                                 compound=LEFT, width=100)
        self.header_del.grid(row=4, column=0, padx=(555, 0), sticky=NW, pady=(50, 0))

        self.fake_user_checkbox = Checkbutton(self.http_settings, text="Use Fake User Agent", command=self.check_user_agent,
                                              variable=self.user_agent_boolean,font=self.myFont, fg=self.blue_btn_color, background='#282c36')
        self.fake_user_checkbox.grid(row=5, column=0, sticky=NW, pady=(50, 0), padx=(50, 0))

    '''Advanced end here'''

    def check_user_agent(self):
        if self.user_agent_boolean.get():
            from main.useragent import genUA
            self.user_agent_str = genUA()

    def add_tree(self):
        self.new_win = Toplevel()
        center(self.new_win)
        self.header_var_ = StringVar()
        self.value_var_ = StringVar()
        header_label = Label(self.new_win, text="Header", font=self.myFont,
                             fg=self.blue_btn_color, background=self.grey)
        value_label = Label(self.new_win, text="Value", font=self.myFont,
                            fg=self.blue_btn_color, background=self.grey)
        self.header_Entry_ = Entry(self.new_win, textvariable=self.header_var_, font=self.myFont,
                                   fg=self.blue_btn_color, bg=self.grey,
                                   disabledforeground=self.blue_btn_color, disabledbackground=self.grey, width=40)
        self.value_Entry_ = Entry(self.new_win, textvariable=self.value_var_, font=self.myFont, fg=self.blue_btn_color,
                                  bg=self.grey,
                                  disabledforeground=self.blue_btn_color, disabledbackground=self.grey, width=40)
        header_label.grid(row=0, column=0, pady=10)
        self.header_Entry_.grid(row=0, column=1, pady=10)
        value_label.grid(row=1, column=0, pady=10)
        self.value_Entry_.grid(row=1, column=1, pady=10)
        b = ttk.Button(self.new_win, text="Save", command=self.add_tree_data)
        b.grid(row=2, sticky=S)

    def add_tree_data(self):
        if self.header_var_.get() not in fv.request_headers:
            messagebox.showerror("Error!", "Incorrect `HTTP header` type!\n Here are all the options avialable: \n" + str(
                fv.request_headers))
            self.add_tree()
        else:
            self.new_win.destroy()
            self.tree.insert('', 'end', values=(self.value_var_.get(), self.header_var_.get()))

    def delete_tree(self):
        selected_item = self.tree.selection()[0]  ## get selected item
        self.tree.delete(selected_item)

    def clear_entry(self, event):
        self.user_Entry.configure(font="Helvetica 15")
        self.user_Entry.delete(0, END)

    def clear_pass_entry(self, event):
        self.password_Entry.delete(0, END)
        self.password_Entry.delete(0, END)

        self.password_Entry.configure(show="*")

    def clear_rep_entry(self, event):
        #self.domain_entry.delete(0, END)
        #self.domain_entry.delete(0, END)
        pass

    def check_head_requests(self):
        #if self.use_headreq_button.
        pass

    def upload_func(self):
        self.php_file = filedialog.askopenfilename(initialdir="./",
                                                   filetypes=(("py files", "*.py"), ("txt files", "*.txt")))
        self.php_label_var.set(self.php_file)

    def save_advanced_settings(self):
        print(self.listBox.index(0))

    def auth_func(self):
        if not self.auth_var.get():
            #self.domain_entry.config(state=DISABLED)
            self.password_Entry.config(state=DISABLED)
            self.user_Entry.config(state=DISABLED)
        else:
            #self.domain_entry.config(state=NORMAL)
            self.password_Entry.config(state=NORMAL)
            self.user_Entry.config(state=NORMAL)

    def exploit_func(self):
        if self.php_var.get() == 1:
            self.php_button.config(state=NORMAL)
            self.entr_php.config(state=NORMAL)
        else:
            # self.php_button.config(state=DISABLED)
            pass
            # self.entr_php.config(state='readonly')

    def browse_cookie(self):
        self.cookie_file = filedialog.askopenfilename(initialdir="./",
                                                      filetypes=(("py files", "*.py"), ("txt files", "*.txt")))

        with open(self.cookie_file, 'r') as file:
            self.cookie_data_file = file.read().replace('\n', '')
            if "=" not in self.cookie_data_file:
                messagebox.showwarning("File", message="This file may not be a cookie valid syntax!")
            self.cookie_label_var.set(self.cookie_file)
            self.entr_cookie.xview_moveto(1)

    def toogle_browse(self):
        if self.cookie_browse.get() == 1:
            self.cookie_Label.config(state=NORMAL)
            self.entr_cookie.config(state=NORMAL)
            self.cookie_Check.config(state=DISABLED)
        elif self.cookie_browse.get() == 0 and self.cookie_Check['state'] == 'NORMAL':
            self.cookie_Check.config(state=NORMAL)
            self.cookie_Label.config(state=NORMAL)

        elif self.cookie_browse.get() == 0:
            self.cookie_Check.config(state=NORMAL)

    def enable_entry(self):
        global entry_var
        if self.cookie_var.get() == 1:
            self.entr_cookie.config(text=DISABLED)
            self.entr_cookie.config(state=DISABLED)
            self.cookie_Entry.config(state=NORMAL)
            entry_var.set("")
            self.cookie_Label.config(state=DISABLED)

        elif self.cookie_var.get() == 0:  # whenever unchecked
            self.cookie_Entry.config(state=DISABLED)
            self.cookie_Label.config(state=NORMAL)
            entry_var.set("Format: var=value, var=value")

    def create_main(self):

        self.tab_parent.add(self.tab2, text="Basic Configuration")
        self.tab_parent.add(self.tab3, text="Monitoring")
        self.tab_parent.add(self.tab4, text="Advanced")
        self.tab_parent.add(self.tab_tools, text="Tools")
        # self.tab_parent.add(self.tab_help, text="Help")

        self.tools_notebook.add(self.tab5, text="Requests")
        self.tools_notebook.add(self.tab_comparer, text="Comparer")
        self.tools_notebook.add(self.tab_decoder, text="Decoder")

        self.advanced.add(self.cookies, text="Cookies")
        self.advanced.add(self.payloads, text="Payloads")
        self.advanced.add(self.authentification, text="Authentification Options")
        self.advanced.add(self.http_settings, text="Http Options")

        self.tab_parent.pack(expand=1, fill='both', padx=10)
        self.tools_notebook.pack(expand=1, fill='both', padx=10)
        self.advanced.pack(expand=1, fill='both')

        # self.tab_parent.hide(self.tab_comparer)

        self.create_Home()
        self.create_Advanced()
        self.create_basicConf()
        self.create_Requests()
        self.create_Comparer()
        self.create_Help()
        self.table = SimpleTable(self.tab3, self.tab_parent, self.tools_notebook, self.tab_tools, self.tab5,
                                 self.request_Table, self.tab_comparer,
                                 self.compare_Table1, self.compare_Table2)

        self.create_Monitoring()
        self.create_Decoder()

    def create_Home(self):

        self.create_basicConf()

    def on_field_encode(self, index=None, value=None, op=None):
        given_str = self.decode_Table1.get('1.0', END)
        EncObj = Encoder(given_str)
        EncObj.set_Results_encoded(self.encode_value.get(), self.decode_Table2)

    def on_field_decode(self, index=None, value=None, op=None):
        given_str = self.decode_Table1.get('1.0', END)
        EncObj = Encoder(given_str)
        EncObj.set_Results_decoded(self.encode_value.get(), self.decode_Table2)

    def create_Decoder(self):
        self.tab_decoder.configure(style='Black.TLabelframe')
        self.encode_value = StringVar()
        self.dec_Frame = Frame(self.tab_decoder, background='#282c36')
        self.encode_value.trace('w', self.on_field_encode)

        self.decode_Table1 = Text(self.dec_Frame, height=10, width=120, borderwidth=2, relief="groove", bg=self.grey,
                                  fg=self.blue_btn_color)
        self.decode_Table1.pack(side=TOP, padx=(10, 10), anchor=W)

        self.decode_Table2 = Text(self.dec_Frame, height=10, width=120, borderwidth=2, relief="groove", bg=self.grey,
                                  fg=self.blue_btn_color)
        self.decode_Table2.pack(side=TOP, padx=(10, 10), pady=20, anchor=W)

        self.dec_Frame.pack(side=LEFT, anchor=NW, pady=10)
        self.encode_button = Button(self.tab_decoder, text="Encode as", fg='black', bg=self.blue_btn_color,
                                    command=self.on_field_encode, font=self.myFont).pack(padx=10, pady=(10, 0),
                                                                                         anchor=W)

        values_to_encode = ["URL", "Base64", "Text", "Hex", "Binary"]
        self.encode_list = ttk.Combobox(self.tab_decoder, values=values_to_encode, textvariable=self.encode_value)

        self.encode_list.current(0)
        self.encode_list.pack(pady=(20, 100), anchor=W)
        self.decode_button = Button(self.tab_decoder, text="Decode as", fg='black', bg=self.blue_btn_color,
                                    command=self.on_field_decode, font=self.myFont).pack(padx=10,
                                                                                         pady=(10, 0),
                                                                                         anchor=W)

        values_to_decode = ["URL", "HTML", "Base64", "Text", "Hex", "Binary"]
        self.decode_value = StringVar()
        self.decode_value.trace('w', self.on_field_decode)
        self.decode_list = ttk.Combobox(self.tab_decoder, values=values_to_decode, textvariable=self.decode_value)
        self.decode_list.current(0)
        self.decode_list.pack(pady=(20, 0), anchor=W)

    def switch_tabs(self):
        self.tab_parent.select(self.tab2)

    def activate_check(self):
        if self.int_proxy.get() == 1:
            self.proxyEntry.config(state=NORMAL)
        elif self.int_proxy.get() == 0:  # whenever unchecked
            self.proxyEntry.config(state=DISABLED)

    def create_basicConf(self):

        self.tab2.configure(style='Black.TLabelframe')

        intro_label = Label(self.tab2, text="Setup the Configuration Settings", font="Helvetica 20 ",
                            fg=self.blue_btn_color, background='#282c36')
        intro_label.configure(anchor=CENTER)
        intro_label.grid(row=0, columnspan=3, pady=20)

        ip_Text = Label(self.tab2, font=self.myFont,
                        text="Enter the target URL (example: http://google.ro:80/)",
                        fg=self.blue_btn_color, background='#282c36')
        ip_Text.grid(row=1, column=0, columnspan=4, sticky=W, pady=5, padx=200)

        self.ipValue = Text(self.tab2, font=self.myFont, height=1, width=100, bg=self.grey, fg=self.blue_btn_color)
        self.ipValue.grid(row=2, column=0, columnspan=4, sticky=W, pady=10, padx=200, ipadx=10)
        self.ipValue.insert(END, 'http://127.0.0.1:8080/DVWA-master/vulnerabilities/fi/?page=', "center")

        #self.portIP = Label(self.tab2, font=self.myFont, fg=self.blue_btn_color, text="Enter the port IP (default: 80)",
        #                    background='#282c36')
        #self.portIP.grid(row=3, column=0, columnspan=4, sticky=W, pady=5, padx=200)

        #self.portValue = Text(self.tab2, bg=self.grey, fg=self.blue_btn_color, height=1, width=100, font=self.myFont)
        #self.portValue.grid(row=4, column=0, columnspan=4, sticky=W, padx=200, ipadx=10)

        self.button_Proxy = Checkbutton(self.tab2, fg=self.blue_btn_color, background='#282c36',
                                        text="Use a proxy server (Recommended to avoid banning/blacklist..)",
                                        variable=self.int_proxy, font=self.myFont)
        self.button_Proxy.grid(row=5, column=0, columnspan=4, sticky=W, pady=5, padx=200)

        self.proxyEntry_Adress = Text(self.tab2, bg=self.grey, fg=self.blue_btn_color, height=1, width=30,
                                      font="Helvetica 15 italic")
        self.proxyEntry_Adress.insert('1.0', "enter proxy here")
        self.proxyEntry_Adress.grid(row=6, column=0, sticky=W, pady=5, ipadx=10, padx=(200, 0))

        self.proxy_ChooseList = ttk.Combobox(self.tab2, font=self.myFont, width=50, height=30)
        self.choose_proxy_sv()
        self.proxy_ChooseList.current(0)
        self.proxy_ChooseList.grid(row=6, column=0, columnspan=2, sticky=W, pady=10, padx=(600, 0))
        self.proxy_ChooseList.bind("<<ComboboxSelected>>", self.set_proxy_entry)

        # selectModule = Label(self.tab2, background='#282c36', fg=self.blue_btn_color, font=self.myFont,
        #                     text="Select the Module for the fuzzing")
        # selectModule.grid(row=7, sticky=W, column=0, pady=(30, 5), padx=30)

        # self.box_value = StringVar()
        self.moduleBox = ttk.Combobox()

        # stil = ttk.Style()
        # stil.configure('MyStyle.TCombobox', foreground=self.grey)
        # self.moduleBox = ttk.Combobox(self.tab2, textvariable=self.box_value, state='readonly')
        # self.moduleBox.configure(style='MyStyle.TCombobox', font=self.myFont)
        # self.moduleBox.bind("<<ComboboxSelected>>", self.get_gui_module())
        # self.moduleBox['values'] = ('http', 'http-Url', 'FTP', 'Payload')
        # self.moduleBox.current(0)
        # self.moduleBox.grid(row=8, column=0, sticky=W, padx=30, pady=5)

        threads_label = Label(self.tab2, text="Set the number of threads for the fuzzing session", font=self.myFont,
                              fg=self.blue_btn_color, background='#282c36')
        threads_label.grid(row=7, column=0, sticky=W, padx=30)
        self.treads_no = Scale(self.tab2, from_=1, to=20, orient=HORIZONTAL, length=200, background='#282c36', fg=self.blue_btn_color)
        self.treads_no.set(value=4)
        self.treads_no.grid(row=8, column=0, sticky=W, padx=30)

        self.save_Results_button = Checkbutton(self.tab2, fg=self.blue_btn_color,
                                               text="Save fuzzing results and statistics into a PDF file",
                                               variable=self.save_fuzzing_results, background='#282c36',
                                               font=self.myFont)
        self.save_Results_button.grid(row=8, column=1, sticky=W, padx=10, pady=5)

        self.button_Crawl = Checkbutton(self.tab2, fg=self.blue_btn_color, font=self.myFont,
                                        text="Generate crawl link txt file (write  all links from the website that may be vulnerable to input data)",
                                        background='#282c36',
                                        variable=self.bool_crawl_links)
        self.button_Crawl.grid(row=9, sticky=W, padx=30, pady=20)

        self.button_Quite = Checkbutton(self.tab2, text="Quite Mode(doesn't show any attempts)", font=self.myFont,
                                        variable=self.bool_quite_mode, fg=self.blue_btn_color, background='#282c36')
        # self.button_Quite.configure()1
        self.button_Quite.grid(row=9, column=1, sticky=W, pady=5, padx=10)

        self.use_headreq_button = Checkbutton(self.tab2, fg=self.blue_btn_color, font=self.myFont,
                                            text="Send  HEAD requests instead (May obtain faster results)",
                                            background='#282c36', variable=self.head_box)
        self.use_headreq_button.grid(row=7, column=1, sticky=W, padx=10, pady=(40, 5))

        depth_label = Label(self.tab2, text="Set the depth level search, 0 for disabled", font=self.myFont,
                              fg=self.blue_btn_color, background='#282c36')
        depth_label.grid(row=10, column=0, sticky=W, padx=30)
        self.depth_no = Scale(self.tab2, from_=0, to=10, orient=HORIZONTAL, length=200, background='#282c36',
                               fg=self.blue_btn_color)
        self.depth_no.set(value=0)
        self.depth_no.grid(row=11, column=0, sticky=W, padx=30)

        self.use_mutators_button = Checkbutton(self.tab2, fg=self.blue_btn_color, font=self.myFont,
                                            text="Generate mutators for payloads",
                                            background='#282c36', variable=self.mutators_box)
        self.use_mutators_button.grid(row=11, column=1, sticky=NW, padx=10)

        self.check_rfi_var = BooleanVar()
        self.check_rfi = Checkbutton(self.tab2, fg=self.blue_btn_color, font=self.myFont,
                                               text="Check Remote File Inclusion at the beggining of session",
                                               background='#282c36', variable=self.check_rfi_var)
        self.check_rfi.grid(row=12, column=1, sticky=NW, padx=10)

        fuzzing_button = Button(self.tab2, text="Start Fuzzing", font=self.myFont, compound=LEFT, image=self.arrow_ph,
                                fg='black', bg=self.blue_btn_color, command=self.start_fuzzing)
        fuzzing_button.grid(row=13, column=0, columnspan=3, sticky=S, pady=70)
        fuzzing_button.config(height=30, width=700)
        # self.proxyEntry.config(state=NORMAL)

    def set_proxy_entry(self, event):
        if len(self.proxyEntry_Adress.get('1.0', END)) > 0:
            self.proxyEntry_Adress.delete('1.0', END)
        self.proxyEntry_Adress.configure(font="Helvetica 15")
        self.proxyEntry_Adress.insert(END, str(self.proxy_ChooseList.get()))

    def choose_proxy_sv(self):
        filepath = "proxy-list/proxy-list.txt"
        with open(filepath) as fp:
            lines = fp.readlines()[7:]
            lines = [x.strip() for x in lines]
            for line in lines:
                if line not in self.proxy_ChooseList['values']:
                    self.proxy_ChooseList['values'] = (*self.proxy_ChooseList['values'], line)

    def get_elapsed_time_string(self):
        self.elapsed_time = time.time() - self.start_time
        return str(time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time)))

    def create_Monitoring(self):

        """Create The Dashboard and Top first"""

        """Also create a Frame for the dashboard info!"""
        self.tab3.configure(style='Black.TLabelframe')
        self.dashBoard = Frame(self.tab3, background='#282c36')
        font_Monitoring = Font(family="Helvetica", size=14)
        date_time = str(datetime.now())

        Label(self.dashBoard, borderwidth=2, font=font_Monitoring, fg=self.blue_btn_color, bg=self.grey,
              relief="groove",
              text='Start Time:' + date_time[0:19]).pack(side=LEFT, anchor=W, pady=2, padx=5)

        self.time_var = StringVar(value="Time Elapsed: " + self.get_elapsed_time_string())
        self.iter = StringVar(value="Attempts: " + str(self.iterations))

        try:
            faults = str(self.FuzzerObj.getFaults())  # Fuzzer may not be initialized yet
        except:
            faults = str(0)

        self.faults = StringVar(value="Total Faults: " + faults)

        self.label_time = Label(self.dashBoard, borderwidth=2, bg=self.grey, relief="groove", fg=self.blue_btn_color,
                                font=font_Monitoring,
                                textvariable=self.time_var).pack(side=LEFT, padx=5, pady=2)

        self.iterations = Label(self.dashBoard, borderwidth=2, bg=self.grey, relief="groove", font=font_Monitoring,
                                textvariable=self.iter, fg=self.blue_btn_color).pack(side=LEFT, padx=5, pady=2)

        self.Label_faults = Label(self.dashBoard, borderwidth=2, bg=self.grey, relief="groove", font=font_Monitoring,
                                  textvariable=self.faults, fg=self.blue_btn_color)

        self.Label_faults.pack(side=LEFT, padx=5, pady=2)
        self.dashBoard.grid(sticky='we')

        self.table.grid()

        self.pause_button = Button(self.dashBoard, text="Pause", font=font_Monitoring, command=self.pause_Fuzzing,
                                   bg=self.blue_btn_color)
        self.continue_button = Button(self.dashBoard, text="Continue", font=font_Monitoring,
                                      command=self.resume_Fuzzing,
                                      bg=self.blue_btn_color)
        self.stop_button = Button(self.dashBoard, text="Stop", font=font_Monitoring, command=self.stop_Fuzzing,
                                  bg=self.blue_btn_color)

        self.pause_button.pack(side=RIGHT, padx=20, pady=20)
        self.continue_button.pack(side=RIGHT, padx=20, pady=20)
        self.stop_button.pack(side=RIGHT, padx=20, pady=20)

    def create_Help(self):
        self.tab_help.configure(style='Black.TLabelframe')

        self.img = PhotoImage(file=r"images/photo.png")
        self.photoimage = self.img.subsample(10, 10)

        self.style_tab = ttk.Style()
        self.style_tab.configure('Black.TLabelframe', background='#282c36')

        introduction = "This program is a totally automatic tool able to scan and exploit Local File Inclusion vulnerabilities using many different methods of attack"
        Label(self.tab_help, text="Quick Introduction", fg=self.blue_btn_color, background='#282c36', padx=10,
              pady=20).pack(side="top", anchor=NW)
        Label(self.tab_help, padx=10, text=introduction, font="Helvetica 14", wraplength=800, pady=20).pack(side="top",
                                                                                                            anchor=NW)

        Button(self.tab_help, text="Back to Configuration!", image=self.photoimage, compound=LEFT,
               background=self.blue_btn_color,
               command=self.switch_tabs).pack(side=BOTTOM, pady=100)

    def pause_Fuzzing(self):
        self.FuzzerObj.pause_fuzzing()

    def resume_Fuzzing(self):
        self.FuzzerObj.resume(self)

    def stop_Fuzzing(self):
        self.FuzzerObj.pause_fuzzing()

    def addrow(self, method, status, content, length):
        if self.iterations is None:
            self.iterations = int(0)
        self.iterations = self.iterations + 1
        self.iter.set("Current Iteration: " + str(self.iterations))
        self.faults.set("Total Faults: " + str(self.FuzzerObj.getFaults()))
        self.time_var.set("Time Elapsed: " + str(self.get_elapsed_time_string()))
        Frame.update(self)
        self.table.add_row(method, status, content, length)

    def browse_button(self):
        self.filename = filedialog.askopenfilename(initialdir="./Payloads",
                                                   filetypes=(("txt files", "*.txt"), ("py files", "*.py")))
        if self.filename not in self.payloads_files:
            self.listBox.insert(END, self.filename)

        self.listBox.update()

    ''' Getters and Setters Section'''

    def get_gui_check_results(self):
        return self.save_fuzzing_results.get()

    def get_gui_proxy_server(self):
        if self.int_proxy.get() == 1:
            return self.get_gui_proxy_dict()
        else:
            return None

    def get_gui_check_crawlLinks(self):
        return self.bool_crawl_links.get()

    def get_gui_check_quite_mode(self):
        return self.bool_quite_mode.get()

    def get_gui_module(self):
        return self.moduleBox.get()

    def get_gui_IP(self):
        return self.ipValue.get('1.0', END)

    def get_gui_timeout(self):
        stringTimeout = self.timeout_Value.get('1.0', END)
        try:
            floatTimeout = float(stringTimeout)
            return floatTimeout
        except:
            return 0

    def get_gui_mutator(self):
        return self.mutators_box.get()

    def get_gui_Port(self):
        #return self.portValue.get('1.0', END)
        return ""

    def get_gui_check_HEAD(self):
        if self.head_box.get():
            self.method = "HEAD"

    def get_gui_auth_check(self):
        return self.auth_var.get()

    def get_gui_payloads(self):
        return self.listBox.get(0, END)

    def get_gui_threads_no(self):
        return int(self.treads_no.get())

    def get_gui_depth_no(self):
        return int(self.depth_no.get())

    def get_gui_cookie(self):
        if self.cookie_var.get() == 1:
            return self.cookie_Entry.get()
        else:  # we return the conent  of cookie file
            return self.cookie_data_file

    def get_gui_php_shell(self):
        return self.php_var

    def check_rfi_func(self):
        return self.check_rfi_var.get()

    def get_gui_http_atuh(self):
        ret_list = list()
        ret_list.append(self.entry_user_var.get())
        ret_list.append(self.entry_password_var.get())
        return  ret_list

    def get_gui_Treeview_childs(self):
        treeview_Childs = []
        for child in self.tree.get_children():
            treeview_Childs.append(self.tree.item(child)["values"])
        return treeview_Childs

    def create_two_tabels(self, text_label1, text_label2, button_text, response_text, frame, font, funct):
        tables_frame = Frame(frame)
        texts = Frame(frame)

        texts.configure(background='#282c36')
        tables_frame.configure(background='#282c36')

        self.request_Text = Label(texts, text=text_label1, bg=self.grey, fg=self.blue_btn_color, font=font).pack(
            side=LEFT,
            padx=150,
            pady=20)

        send_button = Button(texts, command=funct, text=button_text, fg='black', bg=self.blue_btn_color, font=font)
        send_button.pack(side=LEFT, padx=50, pady=20)

        Label(texts, text=text_label2, font=font, bg=self.grey, fg=self.blue_btn_color).pack(side=LEFT,
                                                                                             padx=(
                                                                                             280, 50))  # adx=(20, 200))
        texts.pack(side=TOP, anchor=NW)

        SeeResponseOnWeb = Button(texts, text=response_text, command=self.see_on_browser, fg='black',
                                  bg=self.blue_btn_color, font=font)
        SeeResponseOnWeb.pack(side=LEFT, padx=100, pady=20)

        self.ip_stuff = Frame(tables_frame)
        self.port_stuff = Frame(tables_frame)

        self.resp_ipVar = StringVar()
        self.resp_portVar = StringVar()

        self.request_ip = Entry(self.ip_stuff, textvariable=self.resp_ipVar, bg=self.grey, fg=self.blue_btn_color,
                                font="Helvetica 14", width=10)
        self.request_port = Entry(self.port_stuff, textvariable=self.resp_portVar, bg=self.grey, fg=self.blue_btn_color,
                                  font="Helvetica 14", width=10)

        Label(self.ip_stuff, text="Target URL", bg=self.grey, fg=self.blue_btn_color, font=self.myFont).pack(side=LEFT,
                                                                                                             padx=(
                                                                                                             20, 0))
        self.request_ip.pack(side=LEFT, padx=(10, 0))

        Label(self.port_stuff, text="Target Port", bg=self.grey, fg=self.blue_btn_color, font=self.myFont).pack(
            side=LEFT,
            padx=(20, 0))
        self.request_port.pack(side=LEFT, padx=(10, 0))

        self.port_stuff.configure(bg=self.grey)
        self.ip_stuff.configure(bg=self.grey)

        self.port_stuff.pack(side=TOP, anchor=W)
        self.ip_stuff.pack(side=TOP, anchor=W)

        self.request_Table = Text(tables_frame, height=30, width=60, borderwidth=2, relief="groove", bg=self.grey,
                                  fg=self.blue_btn_color)
        self.request_Table.pack(side=LEFT, padx=(300, 20))

        self.response_Table = Text(tables_frame, height=30, width=60, borderwidth=2, relief="groove", bg=self.grey,
                                   fg=self.blue_btn_color)
        self.response_Table.pack(side=LEFT)

        tables_frame.pack(side=LEFT, anchor=NW)

    def save_fuzzer_context(self):
        self.FuzzerObj = FuzzEngine(self.get_gui_IP(), self.get_gui_Port(), self.get_gui_cookie(),
                                    self.get_gui_module(),
                                    self.get_gui_check_results(), self.get_gui_payloads(),
                                    self.get_gui_check_crawlLinks(),
                                    self.get_gui_php_shell(), self.get_gui_check_HEAD(),
                                    self.get_gui_check_quite_mode()
                                    , self.get_gui_proxy_server(), self.get_gui_threads_no(), self.method, "admin",
                                    "password", self.get_gui_Treeview_childs(), self.get_gui_timeout(),
                                    self.get_gui_http_atuh(),self.get_gui_auth_check(), self.user_agent_str,
                                    self.get_gui_depth_no(), self.get_gui_mutator(), self.check_rfi_func())

    def get_gui_proxy_dict(self):
        proxyStr = self.proxyEntry_Adress.get(1.0, END)
        proxySplit = proxyStr.split()
        if len(proxyStr) > 0:
            self.proxyDict = {"http": "http://" + proxySplit[0],
                              "https": "https://" + proxySplit[0]}
            return self.proxyDict
        return ""

    def start_fuzzing(self):
        ipVal = self.get_gui_IP()
        if len(ipVal) == 1:
            messagebox.showerror("Error", "Necessary Field")
            return
        if "http" not in ipVal:
            messagebox.showerror("Error", "Bad format. Need \"http or https:\" !!")
            return

        if not self.listBox.size():
            messagebox.showerror(title="Empty Payload", message="You have not selected any payload")
            self.tab_parent.select(self.tab4)
            self.advanced.select(self.payloads)
            return

        messagebox.showinfo("Success", "Fuzzing process has begun!")
        self.tab_parent.select(self.tab3)
        self.check_head_requests()
        self.save_fuzzer_context()
        self.resp_ipVar.set(self.get_gui_IP())
        self.resp_portVar.set(self.get_gui_Port())


        FuzzEngine.start_fuzzing(self.FuzzerObj, self)


def center(toplevel):
    toplevel.update_idletasks()
    qt_app = QApplication([])
    screen_width = qt_app.desktop().screenGeometry().width()
    screen_height = qt_app.desktop().screenGeometry().height()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2
    toplevel.geometry("+%d+%d" % (x, y))


def run():
    root = Tk()
    root.title("Directory Traversal Fuzzer")
    root.resizable(0, 0)
    root.geometry("1500x800")
    root.option_add("*TCombobox*Listbox*Background", "#414550")
    root.option_add("*TCombobox*Listbox*Foreground", "#9fb4bf")
    Application(root)

    root.mainloop()
