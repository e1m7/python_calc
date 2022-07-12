

"""

	Часть 2: создание парсера
	=========================

01) Парсер просматривает последовательность токенов и выясняет имеют ли они смысл

	а) 1 + 2 + 3 = да, это верная запись
	б) 6 ** 4 = нет, это не верная запись

02) Как надо интерпретировать запись 1 + 2 * 3 = ? 
03) Постройте сами как интерпретировать запись (1 + 2) * 3 = ?
04) Есть определения, которые используются в таких записях

	а) FACTOR (фактор), это конкретное значение (в данном случае число)
	б) TERMIN (термин), это операция * или /, операция с высоким приоритетом
	в) EXPRESSION (выражение), это операция + или -, операция с низким приоритетом

05) Допустим, у нас есть выражение: 8 + 5 * 22, как оно будет записано?
06) Если парсер нашел фактор, то его надо вычислить
07) Если парсер нашел термин, то слева и справа от него должны стоять факторы
08) Если парсер нашел выражение, то слева и справа от него должны стоять термины
09) И все же 6-8 пункты не совсем верные, так как

	а) выражение может состоять из одного-единственного фактора (4)
	б) термин может не быть окружен факторами (+4, -4)

10) Парсер должен создать такое дерево, чтобы учесть все варианты
11) Если дерево создано верно, то интерпрератор просто обойдет его снизу и вычислит
12) Еще раз задачи каждого узла

	а) лексер = анализирует строку и выделяет токены
	б) парсер = анализирует токены и делает AST
	в) интерпретатор = исполняет AST и получает результат

13) Сейчас у нас в проекте три файла

	- main.py
	- lexer.py
	- tokens.py

14) Добавим еще два файла

	- nodes.py (определение всех узлов будущего AST-дерева)
	- parser_.py (файл с подчеркиванием, чтобы не было конфликта)

15) Подправим главный файл main.py

"""





# nodes.py
# nodes.py
# nodes.py

"""
	1) В этом файле мы перечисляем все узлы, которые понимает парсер
	2) Каждый узел простой: либо это число, либо операция над числами
	3) Каждому узлу (ноде) мы прописываем __repr__, чтобы выводить на экран
	4) Узлов получилось

		1. NumberNode (число)
		2. AddNode (сложение)
		3. SubtractNode (вычитание) 
		4. MultiplyNode (умножение) 
		5. DivideNode (деление)
		6. PlusNode (одиночный плюс)
		7. MinusNode (одиночный минус)

	5) Скобки это не ноды, это просто указание в какую сторону идти

"""

from dataclasses import dataclass

@dataclass
class NumberNode:
	value: float

	def __repr__(self):
		return "{}".format(self.value)

@dataclass
class AddNode:
	node_a: any
	node_b: any

	def __repr__(self):
		return "({} + {})".format(self.node_a, self.node_b)

@dataclass
class SubtractNode:
	node_a: any
	node_b: any

	def __repr__(self):
		return "({} - {})".format(self.node_a, self.node_b)

@dataclass
class MultiplyNode:
	node_a: any
	node_b: any

	def __repr__(self):
		return "({} * {})".format(self.node_a, self.node_b)

@dataclass
class DivideNode:
	node_a: any
	node_b: any

	def __repr__(self):
		return "({} / {})".format(self.node_a, self.node_b)

@dataclass
class PlusNode:
	node: any

	def __repr__(self):
		return "(+{})".format(self.node)

@dataclass
class MinusNode:
	node: any

	def __repr__(self):
		return "(-{})".format(self.node)

# nodes.py
# nodes.py
# nodes.py





# parser_.py
# parser_.py
# parser_.py

"""
	1) Это сложный код, парсер: получает список токенов, возвращает AST
	2) Для работы парсера подключаем класс TokenType и все из файла nodes
	3) При инициализации берем список токенов и делаем их итерируемыми
	4) После этого вызывает функцию advance(), current_token = 1-ый в списке
"""

from tokens import TokenType
from nodes import *

class Parser:
	def __init__(self, tokens):
		self.tokens = iter(tokens)
		self.advance()

"""
	1) Основная функция parse() = распарсить список токенов по правилам
	2) Правил всего четыре:
			а) результат = expr()
			б) expr() = term() + или - term()
			в) term() = factor() * или / factor()
			г) factor() = число (или выражение в скобках)
	3) Вспомогательная функция raise_error() выбрасывает ошибку синтаксиса
	4) Вспомогательная функция advance() считывает следующий токен из списка
"""

	def raise_error(self):
		raise Exception("Invalid syntax")

	def advance(self):
		try:
			self.current_token = next(self.tokens)
		except StopIteration:
			self.current_token = None

"""
	1) Создание AST-дерева начинается тут, с этой функции
	2) Если текущий токен == None, то значит ничего не было введено
	3) Если что-то есть, то результат (вообще весь) = expr()
	4) Если после разбора результата остались токены, то это ошибка
	5) Иначе можно возвращать результат (вообще весь) в главную программу
"""

	def parse(self):
		if self.current_token == None:
			return None
		result = self.expr()
		if self.current_token != None:
			self.raise_error()
		return result

"""
	1) Как вычисляется expr()? Заводится результат = term()
	2) Выражение (expr) = это либо один термин, либо много через + или -
	3) Заводим цикл пока текущий токен != None и тип текущего токена = + или -
	4) Если это плюс, то считываем новый токен и делаем AddNode()
	5) AddNode(левая часть = текущему результату, правая часть = term())
	6) Все крутится в цикле пока не кончится поток + или - терминов
"""

	def expr(self):
		result = self.term()
		while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
			if self.current_token.type == TokenType.PLUS:
				self.advance()
				result = AddNode(result, self.term())
			elif self.current_token.type == TokenType.MINUS:
				self.advance()
				result = SubtractNode(result, self.term())
		return result

"""
	1) Как вычисляется term()? Заводим результат = factor()
	2) Термин (term) = это либо один фактор, либо много через * или /
	3) Заводим цикл и собираем набор факторов * или / в результат
	4) Возвращаем результат в expr()
"""

	def term(self):
		result = self.factor()
		while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
			if self.current_token.type == TokenType.MULTIPLY:
				self.advance()
				result = MultiplyNode(result, self.factor())
			elif self.current_token.type == TokenType.DIVIDE:
				self.advance()
				result = DivideNode(result, self.factor())
		return result

"""
	1) Как вычисляется factor()? Мы кладем в token текущий токен для анализа
	2) Если он == (, то надо создать result=expr() и убедится, что текущий токен = )
	3) Если это не так, то у нас ошибка парсинга, если так, то фактор вычислен
	4) Если он == числу, то читаем дальше, возвращаем NumberNode() числовую ноду
	5) Если он == +, то перед нами что-то типа +5
	6) Если он == -, то перед нами что-то типа -5
	7) Если ничего из вышеперечисленного, то это ошибка парсинга
"""

	def factor(self):
		token = self.current_token
		if token.type == TokenType.LPAREN:
			self.advance()
			result = self.expr()
			if self.current_token.type != TokenType.RPAREN:
				self.raise_error()
			self.advance()
			return result
		elif token.type == TokenType.NUMBER:
			self.advance()
			return NumberNode(token.value)
		elif token.type == TokenType.PLUS:
			self.advance()
			return PlusNode(self.factor())
		elif token.type == TokenType.MINUS:
			self.advance()
			return MinusNode(self.factor())
		self.raise_error()

# parser_.py
# parser_.py
# parser_.py





# main.py
# main.py
# main.py

from lexer import Lexer
from parser_ import Parser

while True:
	text = input("calc > ")
	lexer = Lexer(text)
	tokens = lexer.generate_tokens()
	parser = Parser(tokens)
	tree = parser.parse()
	print(tree)

# main.py
# main.py
# main.py
