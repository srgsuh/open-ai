from typing import Iterable
import re

def unsigned_float_number_pattern() -> str:
    """Define a pattern for the unsigned float number"""
    return r"(?:(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"

def float_number_pattern() -> str:
    """Define a pattern for the signed float number"""
    ufn_format: str = unsigned_float_number_pattern()
    return rf"(?:[+-]?{ufn_format})"

def iterable_items_pattern(iterable: Iterable) -> str:
    return rf"(?:{'|'.join([re.escape(str(k)) for k in iterable])})"

def arithmetic_operations_pattern() -> str:
    """"Define a pattern that matches any of the following arithmetic operations: +, -, /, * and **"""
    return iterable_items_pattern(['**','*','/','+','-'])

def ltr_no_parentheses_expr(num_pattern: str, op_pattern: str) -> str:
    """Define a pattern for the valid arithmetic expression that does not contain parentheses
    with binary operations defined in the `op_pattern` and numbers in the format defined by the `num_pattern`
    """
    return rf"(?:{num_pattern}{op_pattern})*{num_pattern}"

def ltr_expression(number_pattern: str, operation_pattern: str) -> str:
    """Define a pattern that matches arithmetical expression, containing parentheses,
    numbers in a format defined by the `number_pattern` and a set of operations,
    defined by the `operation_pattern`. Expression does not check parentheses pairing.
    """
    openings_and_blanks: str = r"(?:\s*(?:\(\s*)*)"
    closings_and_blanks: str = r"(?:\s*(?:\)\s*)*)"
    operand: str = rf"(?:{openings_and_blanks}{number_pattern}{closings_and_blanks}\)*)"
    return rf"(?:{operand}(?:{operation_pattern}{operand})*)"

def inner_expression() -> str:
    """Define an expression inside the parentheses, that does not itself contains any parentheses"""
    return r"\([^()]+\)"