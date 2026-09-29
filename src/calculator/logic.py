import re
import math

FUNCTIONS = ("sin", "cos", "tan", "log", "ln")
OPERATORS = "+-*/√^"

def filter_user_input(user_input):
    """
    Filters the user input to only allow valid characters.
    """
    allowed_chars = "0123456789().e=,π" + OPERATORS
    final_input = "".join([char for char in user_input if char in allowed_chars])
    final_input = final_input.replace(",", ".")
    return final_input

def calc_result(expression):
    """
    Calculates the result of the expression in the display.
    """
    expression = force_multiplication(expression)
    try:
        expression = symbol_cleanup(expression)
        if expression.count("(") != expression.count(")"):
            ## Ensures that the number of opening and closing parentheses match.
            expression += ")" * (expression.count("(") - expression.count(")"))
        expression = expression.replace("^", "**")
        expression = expression.replace("√", "math.sqrt")
        for function_name in ("sin", "cos", "tan"):
            expression = re.sub(
                rf"(?<!\.)\b{function_name}\(([^()]*)\)",
                rf"math.{function_name}(math.radians(\1))",
                expression,
            )
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("ln", "math.log")
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        result = eval(expression)
        if float(result).is_integer():
            result = int(result)
    except ZeroDivisionError:
        result = "Error: Can't divide by zero."
    except Exception as e:
        result = f"Error: {str(e)}"
    return result

def ensure_proper_input(old_expression, new_char):
    """
    Ensures the user doesn't make a syntax error by entering an improper expression.
    """
    if new_char in FUNCTIONS + ("√", "^"):
        new_char += "("
    if new_char == ".":
        if not old_expression or old_expression[-1] in OPERATORS + "(":
            new_char = "0."
        else:
            for char in reversed(old_expression):
                if char in OPERATORS + "(":
                    break
                if char == ".":
                    return old_expression
    if new_char == ")":
        if old_expression.count("(") <= old_expression.count(")"):
            return old_expression
    if new_char in OPERATORS:
        if not old_expression or old_expression[-1] in OPERATORS + "(.":
            return old_expression
    if new_char == "0" and old_expression and old_expression[-1] == "0":
        if len(old_expression) == 1 or old_expression[-2] in OPERATORS + "(":
            return old_expression
    if new_char.isdigit() and old_expression and old_expression[-1] == "0":
        if len(old_expression) == 1 or old_expression[-2] in OPERATORS + "(":
            return old_expression[:-1] + new_char
    return old_expression + new_char

def force_multiplication(expression):
    """
    Forces multiplication in the expression where necessary.
    """
    final_expression = ""
    index = 0
    function_names = sorted(FUNCTIONS, key=len, reverse=True)

    while index < len(expression):
        function_name = next(
            (name for name in function_names if expression.startswith(name, index)),
            ""
        )
        token = function_name or expression[index]
        previous_char = final_expression[-1:]
        value_ends = previous_char and (
            previous_char.isdigit() or previous_char in "πe)"
        )

        if value_ends and (token in FUNCTIONS or token in "eπ("):
            final_expression += "*"

        final_expression += token
        index += len(token)
    return final_expression

def symbol_cleanup(expression):
    """
    Cleans up the expression right before evaluation by removing any unnecessary symbols.
    """
    while expression[-1] in tuple(FUNCTIONS) + tuple(OPERATORS) or expression[-1] in "(.":
        expression = expression[:-1]
    return expression
