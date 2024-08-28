import ast
from interval import Interval

def evaluate_string_expression(expr, variables):
    """
    Evaluate a mathematical expression involving custom Interval objects.
    
    :param expr: A string representing a mathematical expression.
    :param variables: A dictionary of variable names to Interval objects.
    :return: The result of the evaluated expression.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(expr, mode='eval')
        return _eval_node(tree.body, variables)
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {e}")

def _eval_node(node, variables):
    """
    Recursively evaluate an AST node using custom Interval class.
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, variables)
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        elif isinstance(op, ast.Sub):
            return left - right
        elif isinstance(op, ast.Mult):
            return left * right
        elif isinstance(op, ast.Div):
            return left / right
        elif isinstance(op, ast.Pow):
            if isinstance(right, Interval):
                return left ** right.start  # This handles Interval as the exponent
            else:
                return left ** right  # This handles a simple number as the exponent
        else:
            raise TypeError(f"Unsupported operation: {op}")
    elif isinstance(node, ast.Name):
        return variables[node.id]
    elif isinstance(node, ast.Num):
        return Interval(node.n, node.n)
    elif isinstance(node, ast.Constant):  # For Python 3.8 and later
        return Interval(node.value, node.value)
    elif isinstance(node, ast.UnaryOp):  # Handling Unary Operations
        operand = _eval_node(node.operand, variables)
        if isinstance(node.op, ast.USub):  # Negation
            return -operand
    else:
        raise TypeError(f"Unsupported node type: {type(node)}")



def evaluate_expression(expression, intervals, symbols):
    """
    Wrapper function to evaluate a mathematical expression with intervals.

    :param expression: A string representing the mathematical expression.
    :param intervals: A list of Interval objects corresponding to the symbols.
    :param symbols: A list of symbol names corresponding to the intervals.
    :return: The result of the evaluated expression.
    """
    variables = dict(zip(symbols, intervals))
    evaluated = evaluate_string_expression(expression, variables)

    return evaluated
