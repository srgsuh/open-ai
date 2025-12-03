from typing import Callable
import regular_expressions as reg_expr
import operator
from re import Pattern, compile

__operations: dict[str, Callable[[float, float], float]] = {
    '**': operator.pow,
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def get_operation(operation_sign: str) -> Callable[[float, float], float]:
    operation_function = __operations.get(operation_sign)
    if operation_function is None:
        raise ValueError(f"Unsupported operation: {operation_sign}.")
    return operation_function

__UNSIGNED_NUMBER_PATTERN: str = reg_expr.unsigned_float_number_pattern()
__SIGNED_NUMBER_PATTERN: str = reg_expr.float_number_pattern()
__OPERATION_PATTERN: str = reg_expr.iterable_items_pattern(__operations)
__EXPR_PATTERN: str = reg_expr.ltr_expression(__UNSIGNED_NUMBER_PATTERN, __OPERATION_PATTERN)
__INNER_EXPR_PATTERN: str = reg_expr.inner_expression()
__BLANK_PATTERN: str = r"\s+"


ltr_pattern: Pattern = compile(__EXPR_PATTERN)
inner_pattern: Pattern = compile(__INNER_EXPR_PATTERN)
operation_pattern: Pattern = compile(__OPERATION_PATTERN)
signed_num_pattern: Pattern = compile(__SIGNED_NUMBER_PATTERN)
blank_pattern: Pattern = compile(__BLANK_PATTERN)