
from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter
from termcolor import colored

while True:
	try:
		text = input("calc > ")
		lexer = Lexer(text)
		tokens = lexer.generate_tokens()
		parser = Parser(tokens)
		tree = parser.parse()
		if not tree: continue
		inter = Interpreter()
		value = inter.visit(tree)
		print(colored('{}'.format(value), 'green', attrs=['reverse', 'blink']))
	except Exception as e:
		print(colored('{}'.format(e), 'red', attrs=['reverse', 'blink']))