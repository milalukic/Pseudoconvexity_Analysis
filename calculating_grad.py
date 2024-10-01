import ast
from interval import Interval

def evaluate_string_expression(expr, variables):
    """Evaluate a mathematical expression involving custom Interval objects."""
    try:
        tree = ast.parse(expr, mode='eval')
        return _eval_node(tree.body, variables)
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {expr}. Reason: {e}")

def _eval_node(node, variables):
    if isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]  # Return the interval for the variable
        else:
            raise ValueError(f"Variable '{node.id}' not found.")
    
    elif isinstance(node, ast.Constant):
        return Interval(node.value, node.value)  # Return constant as an interval

    elif isinstance(node, ast.UnaryOp):
        operand_value = _eval_node(node.operand, variables)  # Evaluate the operand
        if isinstance(node.op, ast.UAdd):
            return operand_value  # Unary plus: return the operand (no change)
        elif isinstance(node.op, ast.USub):
            return -operand_value  # Unary minus: negate the operand

    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left, variables)
        right = _eval_node(node.right, variables)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right
        elif isinstance(node.op, ast.Pow):  # Handle exponentiation
            return left ** right  # Use the __pow__ method in your Interval class

    # Raise an error for unsupported node types
    raise ValueError(f"Unsupported operation for node: {ast.dump(node)}")

# Example of usage in your evaluate function
def evaluate_expression(expression, intervals, symbols):
    """Wrapper function to evaluate a mathematical expression with intervals."""
    variables = dict(zip(symbols, intervals))
    evaluated = evaluate_string_expression(expression, variables)
    return evaluated