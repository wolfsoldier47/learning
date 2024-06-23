import argparse
import sys
import re
TOKENS_SPECIFICATION =[
    ('LBRACE', r'\{'),           # {
    ('RBRACE', r'\}'),           # }
    ('COLON', r':'),             # :
    ('COMMA', r','),             # ,
    ('STRING', r'"([^"\\]*(?:\\.[^"\\]*)*)"'),  # "key" or "value" (handles escape sequences)
    ('BOOL',r'true|false'),
    ('NULL',r'null'),
    ('NUMBER',r'\b\d+(\.\d+)?\b'),
    ('WHITESPACE', r'\s+'), 
]

TOKENS = [(name, re.compile(pattern)) for name, pattern in TOKENS_SPECIFICATION]



class JsonLexer:
    def __init__(self,text):
        self.text = text
        self.position = 0
        self.brace_balance = 0

    def tokenize(self):
        tokens = []
        while self.position < len(self.text):
            match = None
            for token_spec in TOKENS:
                pattern_name, pattern = token_spec
                match = pattern.match(self.text, self.position)
                if match:
                    if pattern_name == 'LBRACE':
                        self.brace_balance += 1
                    elif pattern_name == 'RBRACE':
                        self.brace_balance -= 1
                        if self.brace_balance < 0:
                            raise Exception(f"Unmatched closing brace at position {self.position + 1}")
                    if pattern_name != 'WHITESPACE':
                        token = (pattern_name,match.group())
                        tokens.append(token)
                    self.position = match.end()
                    break
            if not match:
                raise Exception(f"Illegal character at position {self.position +1 }")
        print(tokens)
        return tokens

def parse_arguments():
    parser = argparse.ArgumentParser(description="Json parser")
    parser.add_argument('file', nargs='?',type=str, help="Path to the file or cat <filename> | python json_parser.py")
    # parser.add_argument('-h','--help',help="print helps",action='help')
    return parser.parse_args()

def validate_token(tokens):
    state = "START"
    for token in tokens:
        token_type, token_value = token
        if state == "START":
            if token_type == "LBRACE":
                state = "KEY"
            else:
                raise Exception("Invalid start of JSON: {token_value}")
        elif state == "KEY":
            if token_type == 'STRING':
                state = 'COLON'
            # elif token_type == 'RBRACE':
            #     state = 'END'
            else:
                raise Exception(f"Expected a string or closing brace after opening brace, got: {token_value}")
        elif state == "COLON":
            if token_type == "COLON":
                state = 'VALUE'
            else:
                raise Exception(f"Expected a colon after key, got: {token_value}")
        elif state == 'VALUE':
            if token_type == 'STRING' or token_type == 'BOOL' or token_type == 'NUMBER' or token_type == 'NULL':
                state = 'COMMA_OR_END'
            else:
                raise Exception(f"Expected a value after colon, got: {token_value}")
        elif state == 'COMMA_OR_END':
            if token_type == 'COMMA':
                state = 'KEY'
            elif token_type == 'RBRACE':
                state = 'END'
            else:
                raise Exception(f"Expected a comma or closing brace after value, got: {token_value} ")
        elif state == "END":
            raise Exception(f"Extra data after end of JSON object: {token_value}")
    if state != 'END':
        raise Exception("JSON object ended prematurely")
    print("All good")

def main():
    args = parse_arguments()

    if args.file:
        try:
            with open(args.file,'r') as file:
                content = file.read()
        except IOError:
            print(f"couldnt read the file: {args.file}")
            sys.exit(1)
    elif sys.stdin:
        try:
            content = sys.stdin.read()
        except IOError:
            print(f"couldnt read the file: {args.file}")
            sys.exit(1)      
    if content == "":
        print("Empty file")
    else:
        lexer = JsonLexer(content)
        try:
            tokens = lexer.tokenize()
            validate_token(tokens)
        except ValueError as e:
            print("Invalid JSON")
            sys.exit(1)

if __name__ == "__main__":
    main()