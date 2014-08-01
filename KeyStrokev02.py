from sys import *
import os

tokens = []
num_stack = []
variable_stack = []
variables = {}

global if_statement
if_statement = False

global if_executed
if_executed = True

def open_file(filename):
	data = open(filename, "r").read()
	data += "~EOF~"
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
		elif token == "\n" or token == "~EOF~":
			if expression != "" and is_expression == 1:
				tokens.append("EXPR:" + expression)
				expression = ""
			elif expression != "" and is_expression == 0:
				tokens.append("NUM:" + expression)
				expression = ""
			token = ""

		elif token == "clear":
			tokens.append("clear")
			token = ""

		elif token == "if":
			tokens.append("if")
			token = ""
		elif token == "endif":
			tokens.append("endif")
			token = ""

		elif token == "else":
			tokens.append("else")
			token = ""
		elif token == "endelse":
			tokens.append("endelse")
			token = ""
		# say commands
		elif token == "say":
			tokens.append("say")
			token = ""
		elif token == "string":
			tokens.append("varstring")
			token = ""
		elif token == "number":
			tokens.append("varnum")
			token = ""
		elif token == "input":
			tokens.append("varinput")
			token = ""
		elif token == "0" or token == "1" or token == "2" or token == "3" or token == "4" or token == "5" or token == "6" or token == "7" or token == "8" or token == "9":
			expression += token
			token = ""
		elif token == "+" or token == "-" or token == "*" or token == "/":
			is_expression = 1
			expression += token
			token = ""
		elif token == "()":
			tokens.append("()")
			token = ""
		elif token == "=":
			tokens.append("=")
			token = ""
		elif token == ">":
			tokens.append(">")
			token = ""
		elif token == "<":
			tokens.append("<")
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

def set_var(name, value):
	variables[name] = value

def is_valid_var(name):
	if name in variables:
		return True
	return False

def evaluate_if_statement(value1, operator, value2):
	a = 0
	if is_valid_var(value1):
		variable_stack.append(value1)
		variable_stack.append(operator)
		variable_stack.append(value2)

		while a < len(variable_stack):
			if variable_stack[a] == "=":
				if str(variable_stack[a+1]) == str(variables[variable_stack[a-1]]):
					ans = True
					del variable_stack[0:]
					return ans
				else:
					del variable_stack[0:]
					return False
			elif variable_stack[a] == ">":
				if int(variables[variable_stack[a-1]]) > int(variable_stack[a+1]):
					ans = True
					del variable_stack[0:]
					return ans
				else:
					del variable_stack[0:]
					return False
			elif variable_stack[a] == "<":
				if int(variables[variable_stack[a-1]]) < int(variable_stack[a+1]):
					ans = True
					del variable_stack[0:]
					return ans
				else:
					del variable_stack[0:]
					return False
			a+=1
	else:
		print "Value1 does not exist!"

def parse(toks):
	i = 0
	global  if_statement
	if_statement = False
	global if_executed
	if_executed = False

	while i < len(toks):
		if toks[i] == "clear":
			if if_statement == False:
				os.system("cls")
			i+=1
		elif toks[i] == "else":
			if_statement = True
			if toks[i-2] == "endif":
				if if_executed == False:
					if if_statement == True:
						if_statement = False
						if_executed = True
			else:
				pass
			i+=1
		elif toks[i] + " " + toks[i+1][0:6] == "say STRING" or toks[i] + " " + toks[i+1][0:3] == "say NUM" or toks[i] + " " + toks[i+1][0:4] == "say EXPR" or toks[i] + " " + toks[i+1][0:6] == "varinput STRING" or toks[i] + " " + toks[i+1][0:6] == "endif ()" or toks[i] + " " + toks[i+1][0:6] == "endelse ()":
			if if_statement == False:
				if toks[i] + " " + toks[i+1][0:6] == "say STRING":
					print toks[i+1][8:]
				elif toks[i+1][0:3] == "NUM":
					print toks[i+1][4:]
				elif toks[i+1][0:4] == "EXPR":
					print evaluate_expression(toks[i+1][5:])
				elif toks[i] + " " + toks[i+1][0:6] == "varinput STRING":
					input_val = raw_input()
					set_var(toks[i+1][8:], input_val)
			elif toks[i] + " " + toks[i+1][0:6] == "endif ()" or toks[i] + " " + toks[i+1][0:6] == "endelse ()":
				if toks[i] == "endif":
					if_statement = False
				elif toks[i] == "endelse":
					if_statement = False

			i+=2

		elif toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] == "say varstring STRING":
			if if_statement == False:
				if is_valid_var(toks[i+2][8:]):
					print variables[toks[i+2][8:]]
			i+=3
		elif toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] == "say varnum STRING":
			if is_valid_var(toks[i+2][8:]):
				print variables[toks[i+2][8:]]
			i+=3
		elif toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] == "say varinput STRING":
			if is_valid_var(toks[i+2][8:]):
				print variables[toks[i+2][8:]]
			i+=3
		elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2] + " " + toks[i+3][0:6] == "varstring STRING = STRING" and toks[i-1] != "if":
			if if_statement == False:
				set_var(toks[i+1][8:], toks[i+3][8:])
			i+=4
		elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2] + " " + toks[i+3][0:3] == "varnum STRING = NUM":
			set_var(toks[i+1][8:], toks[i+3][4:])
			i+=4

		elif toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:6] == "if varstring STRING = STRING" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:6] == "if varinput STRING = STRING" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:3] == "if varnum STRING = NUM" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:3] == "if varnum STRING > NUM" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:3] == "if varnum STRING < NUM" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:3] == "if varinput STRING > NUM" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:3] == "if varinput STRING > NUM" or toks[i] + " " + toks[i+1] + " " + toks[i+2][0:6] + " " + toks[i+3] + " " + toks[i+4][0:3] == "if varinput STRING < NUM":
			if_statement = True
			if if_executed == False:
				if toks[i+1] == "varnum":
					if evaluate_if_statement(toks[i+2][8:], toks[i+3], toks[i+4][4:]):
						if_statement = False
						if_executed = True
					else:
						if_statement = True
						if_executed = False
				else:
					if_statement = True
					if evaluate_if_statement(toks[i+2][8:], toks[i+3], toks[i+4][8:]):
						if_statement = False
						if_executed = True

					else:
						if_statement = True
						if_executed = False
			i+=5

def run():
	data = open_file(argv[1])
	toks = lexer(data)
	parse(toks)
run()
