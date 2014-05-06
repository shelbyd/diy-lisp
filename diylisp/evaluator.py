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

        if is_closure(operator):
            params = dict()
            if len(ast) != len(operator.params)+1:
                raise LispError("wrong number of arguments, expected %d got %d" % (len(operator.params), len(ast)-1))
            arg_index = 1
            for param in operator.params:
                params[param] = evaluate(ast[arg_index], env)
                arg_index += 1
            return evaluate(operator.body, operator.env.extend(params)) 

        # Part that does not evaluate arguments necessarily
        if operator == "quote":
            return ast[1] 
        elif operator == "if":
            if evaluate(ast[1], env):
                return evaluate(ast[2], env)
            else:
                return evaluate(ast[3], env)
        elif operator == "define":
            if len(ast) == 3:
                if is_symbol(ast[1]):
                    return env.set(ast[1], evaluate(ast[2], env))
                else:
                    raise LispError("non-symbol")
            else:
                raise LispError("Wrong number of arguments")
        elif operator == "lambda":
            if is_list(ast[1]):
                if len(ast) == 3:
                    return Closure(env, ast[1], ast[2]) 
                else:
                    raise LispError("number of arguments")
            else:
                raise LispError

        # Part that always evaluates arguments
        evaled = map(lambda expr: evaluate(expr, env), ast[1:])
        if operator == "atom":
            return is_atom(evaled[0])
        elif operator == "eq":
            if not is_atom(evaled[0]) or not is_atom(evaled[1]):
                return False
            return evaled[0] ==evaled[1] 
        elif operator in ["+", "-", "/", "*", "mod", ">"]:
            return evaluate_math(operator, evaled[0], evaled[1])
        else:
            if is_symbol(operator):
                # operator is possibly a function name
                block = [env.lookup(ast[0])]
            elif is_closure(evaluate(operator, env)):
                block = [evaluate(operator, env)]
            else:
                raise LispError("not a function")
            block.extend(ast[1:])
            return evaluate(block, env)

    try:
        return env.lookup(ast)
    except Exception as e:
        if is_symbol(ast):
            raise e
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
