import argparse
import os
import languages
import inspect
import re

class NotSupportFormat(Exception):
    pass

class Compile(object):
    def __init__(self):
        self.args = self.parseArgs()
        self.format, self.obj = self.analyzeFile()

    def parseArgs(self):
        parser = argparse.ArgumentParser(description='auto compile code file')
        parser.add_argument('fullpath', metavar='File', type=str, help='File name of current document with full path.')
        return parser.parse_args()

    def analyzeFile(self):
        '''Analyze file types'''
        path, filename = os.path.split(self.args.fullpath)
        _, ext = os.path.splitext(filename)
        clsmembers = inspect.getmembers(languages, inspect.isclass)

        for name, obj in clsmembers:
            # 排除 Language 类和没有继承自 Language 的类
            if hasattr(obj, 'format') is False or obj.format() is None:
                continue

            format_ = obj.format()

            # this is a python bug
            # see https://stackoverflow.com/questions/3675144/regex-error-nothing-to-repeat
            if format_[0] == '*':
                format_ = format_.replace(format_[0], '[a-zA-Z0-9]*')

            obj_re = re.compile(r'{}'.format(format_))
            if obj_re.match(filename):
                # 返回类名称与实例对象
                return name, obj(self.args.fullpath)

        return ext,None

    def compile(self):
        if self.obj is None:
            raise NotSupportFormat('the format:{} is not support'.format(self.format))

        return self.obj.compile()


if __name__ == '__main__':
    compile = Compile()
    compile.compile()
    # compile()
