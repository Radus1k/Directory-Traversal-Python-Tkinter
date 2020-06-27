from tkinter import *
from main.Mon_Properties import FancyEntry
from tkinter.font import Font
from copy import copy

class SimpleTable(Frame):
    def __init__(self, parent, notebook, tools_notebook, tab_tools, tab5, response_table, tab_comparer, comp_table1, comp_table2, rows=1, columns=4):
        Frame.__init__(self, parent)
        self.configure(background='#282c36')
        self.current_row = []
        self.tableFont = Font(family="Helvetica", size=14)
        self.notebook = notebook
        self.tab_tools = tab_tools,
        self.tab5 = tab5
        self.tool_notebook = copy(tools_notebook)
        self.resp_table = response_table
        self.tab_comparer = tab_comparer
        self.comp_table1 = comp_table1
        self.comp_table2 = comp_table2
        self.row = 1
        self.columns = columns
        canvas = Canvas(self,  background='#282c36', width=1450, height=1600, scrollregion=(0, 0, 5000, 120000))
        vbar = Scrollbar(self, orient=VERTICAL, background='#282c36')
        vbar.grid(row=1, column=1, sticky='nsw')
        vbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vbar.set)
        canvas.grid(row=1, column=0, sticky='news')
        self.table = Frame(canvas, width=700, height=100000, background='#282c36')
        canvas.create_window(0, 0, anchor='nw', height=100000, width=1600, window=self.table)

        self.label_ID = Label(self.table, text="Id", anchor='w',  relief='groove', font=self.tableFont, bg='#414550', fg='#9fb4bf').grid(row=0, column=1, sticky="nw", padx=2)
        self.label_Method = Label(self.table, text="Method", anchor='w', relief='groove', font=self.tableFont, bg='#414550',fg='#9fb4bf').grid(row=0, column=2, sticky="nw", padx=2)
        self.label_Url = Label(self.table, text="Status", anchor='w', relief='groove', font=self.tableFont, bg='#414550', fg='#9fb4bf').grid(row=0, column=3, sticky="nw", padx=2)
        self.label_Host = Label(self.table, text="Content", anchor='w', relief='groove', font=self.tableFont, bg='#414550', fg='#9fb4bf').grid(row=0, column=4, sticky="nw", padx=2)
        self.label_Status = Label(self.table, text="Length", anchor='w', relief='groove', font=self.tableFont, bg='#414550', fg='#9fb4bf').grid(row=0, column=5, sticky="nw")
        self.label_Length = Label(self.table, text="", anchor='w', relief='groove', font=self.tableFont, bg='#414550', fg='#9fb4bf').grid(row=0, column=6, sticky="nw")

        self.table.grid_columnconfigure(1, weight=1)
        self.table.grid_columnconfigure(2, weight=1)
        self.table.grid_columnconfigure(3, weight=1)
        self.table.grid_columnconfigure(4, weight=5)
        self.table.grid_columnconfigure(5, weight=1)
        self.table.grid_columnconfigure(6, weight=1)

    def add_row(self, method, status, url_vuln, length):
        self.row = self.row + 1
        row = self.row

        if status in [200, 301, 302, 400, 403, 500]:
            color = '#fd7037'
        else:
            color = "#9fb4bf"

        data_string = StringVar()
        len_var = IntVar()
        len_var.set(length)
        data_string.set(url_vuln)

        idLabel = Label(self.table, text=str(row), font=self.tableFont, fg=color,  borderwidth=2, relief="groove",  bg='#414550')

        methodLabel = Label(self.table, text=method, fg=color, borderwidth=2, relief="groove", bg='#414550',
                            font=self.tableFont)

        statusLabel = Label(self.table, text=status, fg=color,  borderwidth=2, relief="groove",  bg='#414550', font=self.tableFont)

        contentLabel = FancyEntry(self.table, url_vuln, self.notebook, self.tool_notebook,  self.tab_tools, self.tab5, self.resp_table, self.tab_comparer,
                                  self.comp_table1, self.comp_table2, fg=color, textvariable=data_string,
                                  borderwidth=2, relief="groove", font=self.tableFont)#state="readonly",

        contentLabel.xview_moveto(1)

        lengthLabel = Label(self.table, text=length,  fg=color,  borderwidth=2, relief="groove",  bg='#414550', font=self.tableFont)
        Label(self.table, text="", anchor='w', relief='groove', bg='#414550', fg='#9fb4bf').grid(row=0, column=5, sticky="nw")

        idLabel.grid(row=row, column=1, sticky="nsew")
        methodLabel.grid(row=row, column=2, sticky="nsew")
        statusLabel.grid(row=row, column=3, sticky="nsew")
        contentLabel.grid(row=row, column=4, sticky="nsew")
        lengthLabel.grid(row=row, column=5, sticky="nsew")

        self.table.grid_columnconfigure(1, weight=1)
        self.table.grid_columnconfigure(2, weight=1)
        self.table.grid_columnconfigure(3, weight=1)
        self.table.grid_columnconfigure(4, weight=3)
        self.table.grid_columnconfigure(5, weight=1)

        # invisible row after last row gets all extra space
