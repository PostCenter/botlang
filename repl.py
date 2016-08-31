from botlang import Evaluator
from botlang.interpreter import BotlangSystem
from botlang.parser import Parser


class BotlangREPL(object):

    def exit_function(self):
        def repl_exit():
            self.active = False

        return repl_exit

    def __init__(self):

        self.active = True
        self.dsl = BotlangSystem()
        self.dsl.environment.add_primitives(
            {'exit': self.exit_function()}
        )

    @classmethod
    def input(cls, prompt):
        '''
        Disgusting trick, because of python's decision of renaming raw_input
        to input in version 3
        '''
        if hasattr(__builtins__, 'raw_input'):
            return raw_input(prompt)
        else:
            return input(prompt)

    def eval(self, code_string):
        try:
            ast_seq = Parser.parse(code_string)
            return BotlangSystem.interpret(
                ast_seq,
                Evaluator(),
                self.dsl.environment
            )
        except Exception as e:
            name = e.__class__.__name__
            message = e.args[0]
            return '{0}: {1}'.format(name, message)

    @classmethod
    def run(cls):
        print('Welcome to the BotCenter REPL\n')
        runtime = BotlangREPL()
        line_breaks = 0
        code_input = ''

        while runtime.active:

            if line_breaks == 0:
                prompt = '>> '
            else:
                prompt = '\t'

            code_input += cls.input(prompt)
            balanced, fail_index = Parser.balanced_parens(code_input)
            if not balanced and fail_index == len(code_input):
                line_breaks += 1
                continue

            value = runtime.eval(code_input)
            if value is not None:
                print(value)
            line_breaks = 0
            code_input = ''


if __name__ == '__main__':
    BotlangREPL.run()