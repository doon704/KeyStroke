from sys import *

tokens = []
num_stack = []

def open_file(filename):
	data = open(filename, "r").read()
	data += "<EOF>"
	return data

def lexer(file_contents):
	file_contents = list(file_contents)
	token = ""
	state = 0
	string = ""
	expression = ""
	n = ""
	is_expression = 0
	for char in file_contents:
		token += char
		if token == "":
			token = ""
		if token == " ":
			if state == 0:
				token = ""
			else:
				token = " "
		elif token == "\n" or token == "<EOF>":
			if expression != "" and is_expression == 1:
				tokens.append("EXPR:" + expression)
				expression = ""
			elif expression != "" and is_expression == 0:
				tokens.append("NUM:" + expression)
				expression = ""
			token = ""
		elif token == "say":
			tokens.append("say")
			token = ""
		elif token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
			expression += token
			token = ""
		elif token == "+" or token == "-" or token == "*" or token == "/" or token == "(" or token == ")":
			is_expression = 1
			expression += token
			token = ""
		elif token == "\"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("STRING:" + string)
				string = ""
				state = 0
				token = ""
		elif state == 1:
			string += token
			token = ""

	return tokens

def evaluate_expression(expression):
	expression = "," + expression
	i = len(expression) - 1
	a = 0
	num1 = ""

	while i >= 0:
		if expression[i] == "+" or expression[i] == "-" or expression[i] == "*" or expression[i] == "/":
			num1 = num1[::-1]
			num_stack.append(num1)
			num_stack.append(expression[i])
			num1 = ""
		elif expression[i] == ",":
			num1 = num1[::-1]
			num_stack.append(num1)
			num1 = ""
		else:
			num1 += expression[i]
		i-=1

	while a < len(num_stack):
		if num_stack[a] == "+":
			ans = int(num_stack[a+1]) + int(num_stack[a-1])
			del num_stack[0:]
			return ans
		elif num_stack[a] == "-":
			ans = int(num_stack[a+1]) - int(num_stack[a-1])
			del num_stack[0:]
			return ans
		elif num_stack[a] == "*":
			ans = int(num_stack[a+1]) * int(num_stack[a-1])
			del num_stack[0:]
			return ans
		elif num_stack[a] == "/":
			ans = int(num_stack[a+1]) / int(num_stack[a-1])
			del num_stack[0:]
			return ans
		a+=1

def parse(toks):
	i = 0
	while i < len(toks):
		if toks[i] + " " + toks[i+1][0:6] == "say STRING" or toks[i] + " " + toks[i+1][0:3] == "say NUM" or toks[i] + " " + toks[i+1][0:4] == "say EXPR":
			if toks[i+1][0:6] == "STRING":
				print toks[i+1][8:]
			elif toks[i+1][0:3] == "NUM":
				print toks[i+1][4:]
			elif toks[i+1][0:4] == "EXPR":
				print evaluate_expression(toks[i+1][5:])
			i+=2

def run():
	data = open_file(argv[1])
	toks = lexer(data)
	parse(toks)

run()