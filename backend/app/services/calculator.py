"""
CALCULATOR SERVICE
==================
Purpose: Perform accurate math calculations.
"""

import math

SAFE_MATH = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'log': math.log,
    'log10': math.log10,
    'pow': pow,
    'pi': math.pi,
    'e': math.e
}

def calculate(expression: str) -> dict:
    try:
        expr = expression.replace('^', '**')
        result = eval(expr, {"__builtins__": {}}, SAFE_MATH)
        return {"success": True, "result": result, "expression": expression}
    except Exception as e:
        return {"success": False, "error": str(e), "expression": expression}