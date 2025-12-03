import regular_expressions as reg_expr
from utils import is_parentheses_pairing
from ltr_constants import get_operation,blank_pattern,ltr_pattern,inner_pattern,signed_num_pattern

def __is_valid_expression(expr: str) -> bool:
    return is_parentheses_pairing(expr) and (ltr_pattern.fullmatch(expr) is not None)

def __compute_one(op1: float, op2: float, operation_sign: str) -> float:
    operation_function = get_operation(operation_sign)
    return operation_function(op1, op2)

def __eval_no_parentheses(expr: str) -> float:
    print(f"expression = {expr}")
    operations: list[str] = signed_num_pattern.split(expr)
    operands: list[str] = signed_num_pattern.findall(expr) # fix to work with sci-format (e.g. 1e-2)
    print(f"operation = {operations}, operand = {operands}")
    res = float(operands[0])
    for i in range(1, len(operands)):
        operation_sign = operations[i] if operations[i] else '+'
        res = __compute_one(res, float(operands[i]), operation_sign)
    return res

def eval(expr: str) -> float:
    if not __is_valid_expression(expr):
        raise ValueError(f"Invalid expression: {expr}")
    expr = blank_pattern.sub("", expr)
    while mo := inner_pattern.search(expr):
        inner = mo.group()[1:-1]
        value = __eval_no_parentheses(inner)
        expr = expr[:mo.start()] + str(value) + expr[mo.end():]

    return __eval_no_parentheses(expr)