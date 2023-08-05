from lib2to3 import fixer_base

class FixTest(fixer_base.BaseFix):

    explicit = True

    def match(self, node):
        return True

    def transform(self, node, results):
        print(repr(node))
