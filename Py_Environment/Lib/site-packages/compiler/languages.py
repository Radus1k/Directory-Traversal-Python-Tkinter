import os
# import subprocess
from subprocess import PIPE, Popen

class Language(object):
    _FORMAT = None

    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.path, _ = os.path.split(fullpath)

    @classmethod
    def format(cls):
        if cls._FORMAT:
            return cls._FORMAT

    def parse_path(self):
        return os.path.split(self.fullpath)

    def run(self, command):
        '''run command'''
        # with Popen(command, shell=True, stdout=PIPE, stderr=PIPE) as p:
        #     stdout, errors = p.communicate()
        p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
        stdout, errors = p.communicate()
        p.stdout.close()

        return stdout, errors

    def compile(self):
        '''compile 接口'''
        raise NotImplementedError('The inheritance class must implement {} interface'.format('compile'))

    def show(self, stdout, errors):
        '''show result message'''
        if stdout:
            print(str(stdout, encoding='utf-8'))
        if errors:
            print(str(errors, encoding='utf-8'))

class Python(Language):
    _FORMAT = '*.py'

    def compile(self):
        stdout, errors = self.run('/usr/bin/python {}'.format(self.fullpath))

        self.show(stdout, errors)


class Cpp(Language):
    _FORMAT = '*.cpp'

    def compile(self):
        path, filename = self.parse_path()

        files = [f.lower() for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        if 'makefile' in files:
            makefile = Makefile(self.fullpath)
            return makefile.compile()
        else:
            name_without_ext, _ = os.path.splitext(filename)
            stdout, errors = self.run('clang++ -g -Wall {} -o {}'.format(filename, name_without_ext))
            self.show(stdout, errors)
            cstdout, cerrors = self.run('{}'.format(name_without_ext))
            self.show(cstdout, cerrors)

class Makefile(Language):
    _FORMAT = 'Makefile'

    def compile(self):
        print("Compile Makefile")
