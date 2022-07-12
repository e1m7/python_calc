
"""

	Часть 1: создание лексера
	=========================

01) Основная задача: создать простой интерпретатор типа калькулятор

	>>> 5 + 5 = 10.0
	>>> 8 / 2 = 4.0
	>>> 2 + 3 * 4 - 5 = 9.0
	>>> (2 + 3) * 4 - 5 = 15.0

02) Интерпретатор будет состоять из нескольких файлов, работающих вместе

	- main.py
	- lexer.py
	- tokens.py

03) Лексер группирует входную строку на сегменты (токены), которые имеют смысл
04) Если пользователь ввел строку "123.02 + 34 * 272", то лексер определит

	Type: Number     Value: 123.02    = токен 1
	Type: Plus       Value: N/A       = токен 2
	Type: Number     Value: 34        = токен 3
	Type: Multiply   Value: N/A       = токен 4
	Type: Number     Value: 272       = токен 5

05) В результате работы лексера из строки "123.02 + 34 * 272" мы получим массив

	[
		[Type:Number,   Value:123.02],
		[Type:Plus,     Value:N/A],
		[Type:Number,   Value:34],
		[Type:Multiply, Value:N/A],
		[Type:Number,   Value:272]
	]

06) В файле tokens.py будут хранится токены, которые может определить лексер

	NUMBER       = число
	PLUS         = сложение
	MINUS        = вычитание
	MULTILPY     = умножение
	DIVIDE       = деление
	LPAREN       = левая скобка
	RPAREN       = правая скобка

"""

# tokens.py
# tokens.py
# tokens.py

"""
	1) Подключаем модуль Enum, он позволяет описывать тип данных Enum (перечисления)
	2) То есть мы можем описать класс, который состоит из нескольких переменых
	3) Каждая переменная имеет имя (name) и значение (value). Пример использования

		import enum

		class MyStatus(enum.Enum):
	    new = 7
	    error = 6

		print('Status name: {}'.format(MyStatus.new.name)) 
		print('Status value: {}'.format(MyStatus.new.value))

	4) Подключаем модуль dataclasses, а из него подключаем библиотеку dataclass
	5) Это декоратор, если его написать перед классом, то не надо писать __init__
	6) Это удобно, если класс очень простой по типу: self.a=a, self.b=b
	7) В нашем случае создаем класс Token, который состоит из двух полей

		а) type : элемент типа TokenType, у которого есть type.name, type.value
		б) value : элемент типа любой, значение по-умолчанию = None

	8) Напишем функцию __repr__, чтобы выводить на печать токен Token
	9) Ничего особенного, просто текст формата "{}:{}" (имя, значение)
"""

from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
	NUMBER       = 0
	PLUS         = 1
	MINUS        = 2
	MULTIPLY     = 3
	DIVIDE       = 4
	LPAREN       = 5
	RPAREN       = 6

@dataclass
class Token:
	type: TokenType
	value: any = None

	def __repr__(self):
		return "{} : {}".format(self.type.name, self.value)

# tokens.py
# tokens.py
# tokens.py





# lexer.py
# lexer.py
# lexer.py

"""
	1) Cложная программа, которая получает строку "1 + 2", а возвращает массив токенов
	2) Подключаем из файла tokens.py два класса Token, TokenType (оба класса нужны)
	3) Определяем константу WHITESPACE = все пробельные символы, которые есть
	4) Определяем константу DIGITS = все цифровые символы 0-1-2-3-4-5-6-7-8-9
"""

from tokens import Token, TokenType

WHITESPACE = ' \t\n'
DIGITS = '0123456789'

"""
	1) Определяем класс Lexer (получает текст, который мы ввели в главной программе)
	2) У него одно поле данных = text, который сразу пропускается через функцию iter()
	3) В результате text = итератор для введенного текста, а у него есть метод next()
	4) При применении next() к итератору мы получаем новый элемент, таким образом

		text = iter("1+2")
		next(text) даст нам "1"
		next(text) даст нам "+"
		next(text) даст нам "2"

	5) Тут же вызываем функцию advance(), она кладет в self.current_char очередной символ
	6) Она делает это не просто так, а через try...except, чтобы обработать конец строки

		а) если функция next() дала новый символ, то кладем его в self.current_char
		б) если была ошибка, то перехватили ошибку и self.current_char = None
"""

class Lexer:
	def __init__(self, text):
		self.text = iter(text)
		self.advance()

	def advance(self):
		try:
			self.current_char = next(self.text)
		except StopIteration:
			self.current_char = None

"""
	1) Сложный кусок кода, функция generate_tokens(), генерация токенов
	2) Она вызывается извне, из основной программы и она, собственно, суть лексера
	3) Сначала отрабатывает __init__() и один раз advance(), а потом идет вызов функции
	4) Начинается цикл до тех пор, пока current_char != None (не дойдем до конца строки)

			5) если символ == точка или символ == цифры...
			6) ...идем создавать Token типа Number, т.к. перед нами число
			7) причем, мы возвращаем токен не через return, а через yield

	Замечание: чем yield отличается от return? Да, это сложное понятие
	Замечание: ответ вернется откуда вызвали и функция продолжит выполнение
	Замечание: причем, она будет выполнена "дальше по ходу", а не заново

			8) если символ == +, то прочитали следующий и вернули токен PLUS
			9) ... MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN
			10) если просмотрели все, но нет варианта, который есть у нас, то ошибка
			11) выбрасываем исключение с сообщением об ошибке + этот странный символ
"""

	def generate_tokens(self):
		while self.current_char != None:
			if self.current_char in WHITESPACE:
				self.advance()
			elif self.current_char == '.' or self.current_char in DIGITS:
				yield self.generate_number()
			elif self.current_char == '+':
				self.advance()
				yield Token(TokenType.PLUS)
			elif self.current_char == '-':
				self.advance()
				yield Token(TokenType.MINUS)
			elif self.current_char == '*':
				self.advance()
				yield Token(TokenType.MULTIPLY)
			elif self.current_char == '/':
				self.advance()
				yield Token(TokenType.DIVIDE)
			elif self.current_char == '(':
				self.advance()
				yield Token(TokenType.LPAREN)
			elif self.current_char == ')':
				self.advance()
				yield Token(TokenType.RPAREN)
			else:
				raise Exception("Illegal character {}".format(self.current_char))

"""
	1) Сложный кусок кода, функция generate_number(), мы определяем число
	2) В числе может быть одна точка, заведем decimal_point_count (счетчик точек)
	3) Само число будем собирать в number_str = первому символу + вызов следующего символа
	4) Дальше запускаем цикл, пока символ != None и он == точка или цифра
	5) Как только получим конец строки или что-то, отличное от точки или цифры, то выход
	6) Внутри цикла склеиваем число и следим, чтобы не было две точки

			7) если символ == точка, то увеличиваем decimal_point_count
			8) если он, decimal_point_count > 1, т.е. 2, то выход из цикла
			9) если дошли до этого места, то приклеиваем символ и берем новый

	10) Когда вышли из цикла, то надо проанализировать что мы получили
	11) Пользователь любит писать коротко, а потому может быть такой число

			а) 10.15    = не надо трогать, все ок, 10.15
			б) .15      = надо доклеить впереди 0, получится 0.15
			в) 10.      = надо доклеить сзади 0, получится 10.0

	12) Последний шаг = возвращаем токен Token с типом NUMBER, значением float(number_str)
"""

	def generate_number(self):
		decimal_point_count = 0
		number_str = self.current_char
		self.advance()
		
		while self.current_char != None and (self.current_char == '.' or self.current_char in DIGITS):
			if self.current_char == '.':
				decimal_point_count += 1
				if decimal_point_count > 1:
					break
			number_str += self.current_char
			self.advance()

		if number_str.startswith('.'):
			number_str = '0' + number_str
		if number_str.endswith('.'):
			number_str += '0'

		return Token(TokenType.NUMBER, float(number_str))

# lexer.py
# lexer.py
# lexer.py





# main.py
# main.py
# main.py

from lexer import Lexer

while True:
	text = input("calc > ")
	lexer = Lexer(text)
	tokens = lexer.generate_tokens()
	print(list(tokens))

# main.py
# main.py
# main.py