
INTEGER, PLUS, MINUS, MUL, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV','EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, int(self.integer()))

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, self.current_char)

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, self.current_char)

            if self.current_char == '*':
                self.advance()
                return Token(MUL, self.current_char)

            if self.current_char == '/':
                self.advance()
                return Token(DIV, self.current_char)

            self.error()
        return Token(EOF, None)


    def factor(self):
        self.eat(INTEGER)

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                self.factor()

        self.current_token = self.get_next_token()

        result = self.term()
        # while self.current_token.type in (PLUS, MINUS):
        #     token = self.current_token
        #     if token.type == PLUS:
        #         self.eat(PLUS)
        #         result = result + self.term()
        #     elif token.type == MINUS:
        #         self.eat(MINUS)
        #         result = result - self.term()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.term()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.term()


        # left = self.current_token
        # self.eat(INTEGER)
        #
        # op = self.current_token
        # if op.type == PLUS:
        #     self.eat(PLUS)
        # elif op.type == MINUS:
        #     self.eat(MINUS)
        # elif op.type == MUL:
        #     self.eat(MUL)
        # elif op.type == DIV:
        #     self.eat(DIV)
        #
        # right = self.current_token
        # self.eat(INTEGER)
        #
        # if op.type == PLUS:
        #     result = left.value + right.value
        # elif op.type == MINUS:
        #     result = left.value - right.value
        # elif op.type == MUL:
        #     result = left.value * right.value
        # elif op.type == DIV:
        #     result = left.value / right.value
        return result

def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
