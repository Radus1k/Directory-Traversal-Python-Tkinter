import sqlite3
import os
import shutil


sql_create_Stats_table = """ CREATE TABLE IF NOT EXISTS Stats (
                                       id integer PRIMARY KEY,
                                       host text NOT NULL,
                                       fuzzed_url text,
                                       status real,
                                       result_length real
                                   ); """

'''sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                   id integer PRIMARY KEY,
                                   name text NOT NULL,
                                   priority integer,
                                   status_id integer NOT NULL,
                                   project_id integer NOT NULL,
                                   begin_date text NOT NULL,
                                   end_date text NOT NULL,
                                   FOREIGN KEY (project_id) REFERENCES projects (id)
                               );"""'''

inserting_query = ''' INSERT INTO Stats(host, fuzzed_url, status, result_length)
                   VALUES(?,?,?, ?) '''

class DatabaseConnection:
    def __init__(self):
        self.dbName = "REST_API/fuzzing.sqlite"
        self.connection = sqlite3.connect(self.dbName)
        self.my_cursor = self.connection.cursor()
        self.create_stats_table()

    def create_stats_table(self):
        self.my_cursor.execute(sql_create_Stats_table)

    def send_values(self, data_list):
        self.my_cursor.execute(inserting_query, data_list)
        self.connection.commit()

def copy_db_to_android():
    root_src_dir = "D:\\Licenta Proiect Practic\\REST_API"
    root_dst_dir = "C:\\Users\\SICA\\AndroidStudioProjects\\Proiect\\app\\src\\main\\assets"

    src_file = os.path.join(root_src_dir, "fuzzing.sqlite")
    dst_file = os.path.join(root_dst_dir, "fuzzing.sqlite")
    if os.path.exists(dst_file):
                # in case of the src and dst are the same file
        if not os.path.samefile(src_file, dst_file):
            print("Overwrrite the db with succes!")
            os.remove(dst_file)
            shutil.copy(src_file, root_dst_dir)
    else:
        shutil.copy(src_file, root_dst_dir)