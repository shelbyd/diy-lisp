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
    evaluator = build_evaluator(ast)
    return evaluator.evaluate(env)

def evaluate_math(operator, left, right):
    try:
        left = int(left)
        right = int(right)
        if operator == "+": return left + right
        if operator == "-": return left - right
        if operator == "/": return left / right
        if operator == "*": return left * right
        if operator == "mod": return left % right
        if operator == ">": return left > right
    except:
        raise LispError

class Evaluator:
    def __init__(self, ast=[]):
        self.ast = ast

    def evaluate(self, env):
        if is_list(self.ast):
            if is_symbol(self.ast[0]):
                # self.ast[0] is possibly a function name
                block = [env.lookup(self.ast[0])]
            if is_closure(evaluate(self.ast[0], env)):
                block = [evaluate(self.ast[0], env)]
            else:
                raise LispError("not a function")
            block.extend(self.ast[1:])
            return evaluate(block, env)

        try:
            return env.lookup(self.ast)
        except Exception as e:
            if is_symbol(self.ast):
                raise e
            return self.ast

class ClosureEvaluator(Evaluator):
    def evaluate(self, env):
        params = dict()
        if len(self.ast) != len(self.ast[0].params)+1:
            raise LispError("wrong number of arguments, expected %d got %d" % (len(self.ast[0].params), len(self.ast)-1))
        arg_index = 1
        for param in self.ast[0].params:
            params[param] = evaluate(self.ast[arg_index], env)
            arg_index += 1
        return evaluate(self.ast[0].body, self.ast[0].env.extend(params)) 

class QuoteEvaluator(Evaluator):
    def evaluate(self, env):
        return self.ast[1]

class IfEvaluator(Evaluator):
    def evaluate(self, env):
        if evaluate(self.ast[1], env):
            return evaluate(self.ast[2], env)
        else:
            return evaluate(self.ast[3], env)
        
class DefineEvaluator(Evaluator):
    def evaluate(self, env):
        if len(self.ast) == 3:
            if is_symbol(self.ast[1]):
                return env.set(self.ast[1], evaluate(self.ast[2], env))
            else:
                raise LispError("non-symbol")
        else:
            raise LispError("Wrong number of arguments")

class LambdaEvaluator(Evaluator):
    def evaluate(self, env):
        if is_list(self.ast[1]):
            if len(self.ast) == 3:
                return Closure(env, self.ast[1], self.ast[2]) 
            else:
                raise LispError("number of arguments")
        else:
            raise LispError

class AtomEvaluator(Evaluator):
    def evaluate(self, env):
        return is_atom(evaluate(self.ast[1], env))

class EqEvaluator(Evaluator):
    def evaluate(self, env):
        if not is_atom(evaluate(self.ast[1], env)) or not is_atom(evaluate(self.ast[2], env)):
            return False
        return evaluate(self.ast[1], env) ==evaluate(self.ast[2], env) 

class MathEvaluator(Evaluator):
    def evaluate(self, env):
        return evaluate_math(self.ast[0], evaluate(self.ast[1], env), evaluate(self.ast[2], env))

class ConsEvaluator(Evaluator):
    def evaluate(self, env):
        l = [evaluate(self.ast[1], env)]
        l.extend(evaluate(self.ast[2], env))
        return l

class HeadEvaluator(Evaluator):
    def evaluate(self, env):
        try:
            return evaluate(self.ast[1], env)[0]
        except IndexError:
            raise LispError("head called on empty list")

class TailEvaluator(Evaluator):
    def evaluate(self, env):
        return evaluate(self.ast[1], env)[1:]

class EmptyEvaluator(Evaluator):
    def evaluate(self, env):
        return len(evaluate(self.ast[1], env)) == 0


def build_evaluator(ast):
    if is_list(ast):
        if is_closure(ast[0]):
            return ClosureEvaluator(ast)
        if ast[0] == "quote":
            return QuoteEvaluator(ast)
        if ast[0] == "if":
            return IfEvaluator(ast)
        if ast[0] == "define":
            return DefineEvaluator(ast)
        if ast[0] == "lambda":
            return LambdaEvaluator(ast)
        if ast[0] == "atom":
            return AtomEvaluator(ast)
        if ast[0] == "eq":
            return EqEvaluator(ast)
        if ast[0] in ["+", "-", "/", "*", "mod", ">"]:
            return MathEvaluator(ast)
        if ast[0] == "cons":
            return ConsEvaluator(ast)
        if ast[0] == "head":
            return HeadEvaluator(ast)
        if ast[0] == "tail":
            return TailEvaluator(ast)
        if ast[0] == "empty":
            return EmptyEvaluator(ast)
    return Evaluator(ast)
