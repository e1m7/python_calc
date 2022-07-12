
"""

	Часть 3: создание интерпретатора
	================================

01) Мы сделали лексер, который проходит по строке и разбивает ее на токены
02) Мы сделали парсер, который проходит по токенам и разбирает их в AST-дерево
03) Теперь надо сделать интерпретатор, который вычисляет дерево

		а) lexer (разбивает строку на токены)
		б) parser_ (делает из токенов AST-дерево)
		в) tokens (список всех токенов)
		г) nodes (список всех узлов дерева)
		д) termcolor (раскрашивание ответа и ошибок)
		е) values (список токенов, котоыре возвращает интерпретатор)

04) В файле values.py мы определим класс данных, котоыре возвращает интерпретатор
05) Фактически, это класс чисел, т.к. результат работы калькулятора это число
06) Как будет работать исполнитель (интерпретатор)?

		а) он заходит в центральный узел
		б) он определяет по типу узла что это (+, -, *, /)
		в) он выполняет действие, и если слева или справа узел, то входит в него
		д) все узлы обходятся рекурсивно и потом собираются в один ответ

"""





# values.py
# values.py
# values.py

from dataclasses import dataclass

@dataclass
class Number:
	value: float

	def __repr__(self):
		return "{}".format(self.value)

# values.py
# values.py
# values.py





# interpreter.py
# interpreter.py
# interpreter.py

"""
	1) Подключаем файл values.py, чтобы указывать класс, который мы возвращаем
	2) В любом случае мы возвращает Number(), т.е. вычисленное число (или ошибку)
	3) Подключаем файл nodes (и все, что там лежит), чтобы вызывать его ноды для обхода
"""

from nodes import *
from values import Number

"""
	1) Сложный кусок кода: обход дерева для того, чтобы вычислить выражение
	2) Создаем метод visit(), которй получает ноду (изначально самую первую, корневую)
	3) Внутри метода определяем method_name = название ноды, которую мы получили
	4) Создаем ее имя как visit_ + имя ноды (NumberNode, AddNode и проч.)
	5) Вытаскиваем название свойства name ноды, чтобы использовать его
	6) Возвращаем из корня результат вызова полученной ноды
"""

class Interpreter:
	def visit(self, node):
		method_name = "visit_{}".format(type(node).__name__)
		method = getattr(self, method_name)
		return method(node)

"""
	1) Каждая нода, когда ее вызывали, возвращает число Number()
	2) Значение ноды будет складываться от того, что она обозначает
	3) Например, посещение ноды visit_AddNode(self, node)
			а) возьмет значение посещенной ноды левой части (node_a)
			б) возьмет значение посещенной ноды правой части (node_b)
			в) сложит их и вернет как новый объект класса Number()
"""

	def visit_NumberNode(self, node):
		return Number(node.value)

	def visit_AddNode(self, node):
		return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)

	def visit_SubtractNode(self, node):
		return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

	def visit_MultiplyNode(self, node):
		return Number(self.visit(node.node_a).value * self.visit(node.node_b).value)

	def visit_DivideNode(self, node):
		try:
			return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)
		except:
			raise Exception("Runtime Error")

	def visit_PlusNode(self, node):
		return self.visit(node.node)

	def visit_MinusNode(self, node):
		return Number(-self.visit(node.node).value)

# interpreter.py
# interpreter.py
# interpreter.py





# main.py
# main.py
# main.py


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

# main.py
# main.py
# main.py


