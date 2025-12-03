def is_parentheses_pairing(expr: str) -> bool:
    opened_count: int = 0
    for c in expr:
        opened_count += 1 if c == '(' else (-1 if c == ')' else 0)
        if opened_count < 0:
            break
            
    return opened_count == 0