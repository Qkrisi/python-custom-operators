import inspect
import importlib.util
import tempfile
import os
import re

from enum import Enum
from collections.abc import Iterable

import CustomOperators.operator_handler

class ArgumentError(Exception):pass

Imports = []

def GetModuleByPath(name, path):
	spec = importlib.util.spec_from_file_location(name, path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

ends = [
	'|',
	'/',
	'*',
	'+',
	'-',
	'=',
	'%',
	'>',
	'<',
	'&',
	'^',
	'~'
]
escape = "\\"

CreateJoin = lambda: '|'.join(f' ?{escape}{x} ?' for x in ends+[op for op in CustomOperators.operator_handler.Operators])
GenerateRegEx = lambda operator : f"((.*)(\(|^| |{CreateJoin()})((?!\)).*?){escape+escape.join(c for c in operator)}((?!\().*?)(\)|$| |{CreateJoin()})(.*))"

def ImportModule(name):
	module = inspect.getmodule(inspect.stack()[1][0])
	if name in Imports:raise ImportError("Module is already imported")
	Imports.append(name)
	if not name.endswith(".py"):name=f"{name}.py"
	path = os.path.join(os.path.dirname(os.path.abspath(module.__file__)), name)
	if not os.path.exists(path):
		path = name
		if not os.path.exists(path):raise ModuleNotFoundError("Module doesn't exist")
	TempPath = os.path.join(tempfile.gettempdir(), f"{os.path.basename(path).replace('.py', '')}_temp.py")
	with open(path, "r") as ReadFile:
		with open(TempPath, "w", encoding="utf-8") as WriteFile:
			WriteFile.write("import CustomOperators.operator_handler\n")
			for line in ReadFile.readlines():
				l = line
				ident = ""
				while len(l)>0 and l[0].isspace():
					ident+=l[0]
					l = "".join(l[1:])
				AddAfter = []
				for operator in CustomOperators.operator_handler.Operators:
					for pattern in re.finditer(GenerateRegEx(operator), l):
						groups = pattern.groups()
						LeftValue = groups[3].replace('Â', '')
						RightValue = groups[4]
						HasLeft = LeftValue.strip()!=""
						HasRight = RightValue.strip()!=""
						if not HasLeft and not HasRight:raise ArgumentError("Operator used without any operands!")
						val = 0
						if HasLeft:val+=1
						if HasRight:val+=2
						apply = Apply(val)
						if operator in CustomOperators.operator_handler.OperatorRules:
							for rule in CustomOperators.operator_handler.OperatorRules[operator]:
								if not apply in rule.apply:continue
								cmd = ident+rule.Command.format(LeftValue, RightValue)+"\n"
								if rule.Before:WriteFile.write(cmd)
								else:AddAfter.append(cmd)
						l = l.replace(groups[0], f"{''.join(groups[1:3])}CustomOperators.operator_handler.Operators[\"{operator}\"]({LeftValue}{', ' if HasLeft and HasRight else ''}{RightValue}){''.join(groups[5:])}")
				WriteFile.write(ident+l)
				for after in AddAfter:WriteFile.write("\n" if not l.endswith("\n") else "" + after)
	FullName = os.path.basename(name).replace(".py", "")
	setattr(module, FullName, GetModuleByPath(FullName, TempPath))
	os.remove(TempPath)
	
class CustomOperator:
    def __init__(self, func, strict):
        self.Func = func
        self.Strict = strict
        argspec = inspect.getfullargspec(self.Func)
        if not len(argspec.args) in [1, 2]: raise ArgumentError("Operator function should only have 1 or 2 arguments")
        self.ArgNum = len(argspec.args)
        ind = 0
        for arg in argspec.args:
            ind+=1
            setattr(self, f"Type{ind}", argspec.annotations[arg] if arg in argspec.annotations else None)

    def Validate(self, *args):
        if(len(args)!=self.ArgNum):return False
        ind = 0
        for arg in args:
            ind+=1
            attr = getattr(self, f"Type{ind}")
            if not (attr==None or ((self.Strict and type(arg)==attr) or (not self.Strict and isinstance(arg, attr)))):return False
        return True

class OperatorBatch:
    def __init__(self, symbol):
        self.Operators = []
        self.Symbol = symbol
    def __call__(self, *args):
        for operator in self.Operators:
            if operator.Validate(*args):return operator.Func(*args)
        if(len(args)==1):args = ["",args[0]]
        return eval(f"{args[0]} {self.Symbol} {args[1]}")

def Operator(symbol, strict = False):
    def CreateOperator(func):
        if not symbol in CustomOperators.operator_handler.Operators:CustomOperators.operator_handler.Operators[symbol]=OperatorBatch(symbol)
        CustomOperators.operator_handler.Operators[symbol].Operators.append(CustomOperator(func, strict))
    return CreateOperator

class Apply(Enum):
	Left = 1
	Right = 2
	Both = 3

class OpRule:
	def __init__(self, command, before, _apply):
		self.Command = command
		self.Before = before
		self.apply = _apply

def AddRule(symbol, apply, command, before = True):
	if not isinstance(apply, Iterable):apply = [apply]
	if not symbol in CustomOperators.operator_handler.OperatorRules:CustomOperators.operator_handler.OperatorRules[symbol] = []
	CustomOperators.operator_handler.OperatorRules[symbol].append(OpRule(command, before, apply))
