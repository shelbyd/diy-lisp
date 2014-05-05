# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_list(ast):
        operator = ast[0]
        evaled = map(lambda expr: evaluate(expr, env), ast[1:])

        if operator == "quote":
            return evaled[0]
        elif operator == "atom":
            return is_atom(evaled[0])
        elif operator == "eq":
            if not is_atom(evaled[0]) or not is_atom(evaled[1]):
                return False
            return evaled[0] ==evaled[1] 
        elif operator in ["+", "-", "/", "*", "mod", ">"]:
            return evaluate_math(operator, evaled[0], evaled[1])
    return ast

def evaluate_math(operator, left, right):
    try:
        left = int(left)
        right = int(right)
        if operator == "+": return left + right
        elif operator == "-": return left - right
        elif operator == "/": return left / right
        elif operator == "*": return left * right
        elif operator == "mod": return left % right
        elif operator == ">": return left > right
    except:
        raise LispError
