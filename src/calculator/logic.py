import math
import re

FUNCTIONS = ("sin", "cos", "tan", "log", "ln")
OPERATORS = "+-*/√^"
TOGETHER = FUNCTIONS + tuple(OPERATORS)


def filter_user_input(user_input: str) -> str:
    """
    Filters the user input to only allow valid characters.
    """
    allowed_chars = "0123456789().e=,π" + OPERATORS
    final_input = "".join([char for char in user_input if char in allowed_chars])
    final_input = final_input.replace(",", ".")
    return final_input


def calc_result(expression: str) -> int | float | str:
    """
    Calculates the result of the expression in the display.
    """
    if expression.count(".") == 1 and not any(item in expression for item in TOGETHER):
        ## Ensures that if the user presses "=" after entering a single decimal, the decimal doesn't get rounded.
        return float(expression)
    expression = force_multiplication(expression)
    try:
        expression = symbol_cleanup(expression)
        if expression.count("(") != expression.count(")"):
            ## Ensures that the number of opening and closing parentheses match.
            expression += ")" * (expression.count("(") - expression.count(")"))
        expression = expression.replace("^", "**")
        expression = expression.replace("√", "math.sqrt")
        expression = expression.replace("π", str(math.pi))
        expression = expression.replace("e", str(math.e))
        expression = evaluate_functions(expression)
        if re.search(
            r"(?<![\d.])\(?0+(?:\.0*)?\)?\*\*\(?0+(?:\.0*)?\)?(?![\d.])",
            expression,
        ):
            raise ValueError("0^0 is undefined")
        result = eval(expression)
        if float(result).is_integer():
            result = int(result)
        else:
            result = round_float(float(result), expression)
    except ZeroDivisionError:
        result = "Division by zero is undefined"
    except ValueError as e:
        result = str(e)
    except Exception as e:
        result = "Unknown error. View console."
        print(expression)
        print("Error: ", e)
    return result


def evaluate_functions(expression: str) -> str:
    """
    Evaluates functions and parenthesized expressions before arithmetic evaluation.
    """
    function_pattern = re.compile(r"\b(sin|cos|tan|log|ln)\(([^()]*)\)")
    square_root_pattern = re.compile(r"\bmath\.sqrt\(([^()]*)\)")
    parentheses_pattern = re.compile(
        r"(?<!math\.sqrt)\(((?:[^()]|\([-+]?(?:\d+(?:\.\d*)?|\.\d+)\))*)\)"
    )
    function_map = {
        "sin": lambda value: math.sin(math.radians(value)),
        "cos": lambda value: math.cos(math.radians(value)),
        "tan": lambda value: math.tan(math.radians(value)),
        "log": math.log10,
        "ln": math.log,
    }

    while True:
        if match := function_pattern.search(expression):
            function_name, argument = match.groups()
            argument_result = eval(argument, {"__builtins__": {}}, {"math": math})
            replacement = str(round(function_map[function_name](argument_result), 15))
        elif match := square_root_pattern.search(expression):
            argument_result = eval(match.group(1), {"__builtins__": {}}, {"math": math})
            if argument_result < 0:
                raise ValueError("Square root of a negative number is undefined")
            replacement = str(round(math.sqrt(argument_result), 15))
        elif match := parentheses_pattern.search(expression):
            if not any(operator in match.group(1) for operator in "+-*/^"):
                break
            replacement = (
                "("
                + str(eval(match.group(1), {"__builtins__": {}}, {"math": math}))
                + ")"
            )
        else:
            break
        expression = (
            expression[: match.start()] + replacement + expression[match.end() :]
        )
    return expression


def round_float(result: float, expression: str) -> float:
    """
    Ensures the displayed result has the appropriate number of decimal places to avoid precision errors.
    """
    i = 1
    max_decimals = 0
    while i < len(expression):
        if expression[i] == ".":
            decimal_count = 0
            j = i + 1
            while j < len(expression) and (
                expression[j].isdigit()
                or (
                    expression[j] == "*"
                    and (j + 1 >= len(expression) or expression[j + 1] != "*")
                )
            ):
                if expression[j].isdigit():
                    decimal_count += 1
                    j += 1
                else:
                    decimal_count, j = multiplication_decimal_places(expression, i, j)
            max_decimals = max(max_decimals, decimal_count)
            i = j + 1
            continue
        i += 1
    return round(result, max_decimals)


def multiplication_decimal_places(
    expression: str, starting_index: int, ending_index: int
) -> tuple[int, int]:
    """
    In multiplication, the result is rounded to the sum of the decimal places of the numbers being multiplied.
    """
    ## Traverses the expression backwards to detect the integer part of the first number being multiplied.
    ## starting_index always represents the index of the decimal point of the first number being multiplied.
    ## ending_index always represents the index of the last decimal in the first number being multiplied.
    numbers_to_multiply = []
    i = starting_index - 1
    while i >= 0 and expression[i].isdigit():
        i -= 1
    first_number = float(expression[i + 1 : ending_index])
    numbers_to_multiply.append(first_number)
    new_num_starting_index = 0
    expression = expression[ending_index + 1 :]
    for j, char in enumerate(expression):
        if char.isdigit() or char == ".":
            number = expression[new_num_starting_index : j + 1]
        elif char == "*":
            numbers_to_multiply.append(float(number))
            new_num_starting_index = j + 1
        elif char in "/^":
            continue
        else:
            numbers_to_multiply.append(float(number))
            break
    final_index = j + ending_index + 1
    result = 1
    for n in numbers_to_multiply:
        result *= n
    result_str = str(result)
    if result_str.endswith(".0"):
        return (0, final_index)
    else:
        return (len(result_str.split(".")[1]), final_index)


def ensure_proper_input(old_expression: str, new_char: str) -> str:
    """
    Ensures the user doesn't make a syntax error by entering an improper expression.
    """
    if (
        old_expression
        and old_expression[-1] == "."
        and (new_char in TOGETHER or new_char in "()πe")
    ):
        return old_expression
    if new_char == "^":
        if old_expression:
            if old_expression[-1] in OPERATORS + "(":
                return old_expression
        else:
            return old_expression
    if new_char in FUNCTIONS + ("√", "^"):
        new_char += "("
    if new_char == ".":
        if not old_expression or old_expression[-1] in OPERATORS + "(":
            new_char = "0."
        if old_expression and old_expression[-1] in ")πe":
            return old_expression
        else:
            for char in reversed(old_expression):
                if char in OPERATORS + "(":
                    break
                if char == ".":
                    return old_expression
    if new_char == ")" and (
        not old_expression
        or (
            old_expression[-1] == "("
            or old_expression.count("(") <= old_expression.count(")")
        )
    ):
        return old_expression
    if new_char == "-":
        if not old_expression:
            return new_char
        elif old_expression[-1] == "(":
            return old_expression + new_char
    if new_char in OPERATORS and (
        not old_expression or old_expression[-1] in OPERATORS + "(."
    ):
        return old_expression
    if (
        new_char == "0"
        and old_expression
        and old_expression[-1] == "0"
        and (len(old_expression) == 1 or old_expression[-2] in OPERATORS + "(")
    ):
        return old_expression
    if new_char == "(" and old_expression:
        if old_expression[-1] == "0":
            if len(old_expression) == 1:
                return new_char
            if old_expression[-2] in OPERATORS + "(":
                return old_expression[:-1] + new_char
        elif old_expression[-1] == ".":
            return old_expression
    if (
        new_char.isdigit()
        and old_expression
        and old_expression[-1] == "0"
        and (len(old_expression) == 1 or old_expression[-2] in OPERATORS + "(")
    ):
        return old_expression[:-1] + new_char
    return old_expression + new_char


def force_multiplication(expression: str) -> str:
    """
    Forces multiplication in the expression where necessary.
    """
    final_expression = ""
    index = 0
    function_names = sorted(FUNCTIONS, key=len, reverse=True)

    while index < len(expression):
        function_name = next(
            (name for name in function_names if expression.startswith(name, index)), ""
        )
        token = function_name or expression[index]
        previous_char = final_expression[-1:]
        value_ends = previous_char and (
            previous_char.isdigit() or previous_char in "πe)"
        )

        if value_ends and (
            token in FUNCTIONS
            or token in "eπ("
            or (token.isdigit() and previous_char == ")")
        ):
            final_expression += "*"

        final_expression += token
        index += len(token)
    return final_expression


def symbol_cleanup(expression: str) -> str:
    """
    Cleans up the expression right before evaluation by removing any unnecessary symbols.
    """
    while expression[-1] in TOGETHER or expression[-1] in "(.":
        expression = expression[:-1]
    return expression
