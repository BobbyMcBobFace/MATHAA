import re

# Check if equation is explicit
def is_valid_equation(equation):
    pattern = r'\s*(y|x)\s*=\s*(?P<expression>[^{{]+)\s*({(?P<constraints>[^}]+)})?'
    return re.match(pattern, equation) is not None

# guessing what type of function it is lols (prob the worst way to do so but it works)
def identify_function_type(expression):
    expression = expression.lower()
    if "sin" in expression or "cos" in expression or "tan" in expression:
        return "Trigonometric"
    if "^2" in expression:
        return "Quadratic"
    if "log" in expression:
        return "Logarithmic"
    if "sqrt" in expression or "?" in expression:
        return "Radical"
    if "^" in expression:
        return "Exponential"
    return "Linear"

# Turn the expression + constraints into TI-BASIC compatible syntax (need to ask discord for this)
def generate_tibasic_code(expression, constraints):
    expression = expression.replace("x", "X").replace("y", "Y")
    constraints = constraints.replace("x", "X").replace("y", "Y")

    # Fix range: A <= X <= B to X>=A and X<=B (need to ask discord for this too)
    match_range = re.match(r'(-?\d*\.?\d*)\s*<=\s*(X|Y)\s*<=\s*(-?\d*\.?\d*)', constraints)
    if match_range:
        lower, var, upper = match_range.groups()
        constraints = f"{var}>={lower} and {var}<={upper}"

    # Quote the entire expression for debug purposes (debug purposes = satisfying purposes)
    return f":\"piecewise({expression},{constraints})\"?Y"


# Main processing function per equation
def process_equation_line(equation_line):
    if not is_valid_equation(equation_line):
        print("Format Incorrect! Please Manually Add\n")
        invalid_equation_file.write(equation_line + "\n")
        return

    print("Format correct! Proceeding")
    match = re.match(r'\s*(y|x)\s*=\s*(?P<expression>[^{{]+)\s*({(?P<constraints>[^}]+)})?', equation_line)

    expression = match.group("expression").strip()
    constraints = match.group("constraints") if match.group("constraints") else ""

    print("Expression:", expression)
    print("Constraints:", constraints + "\n")

    valid_equation_file.write(equation_line + "\n")
    valid_equation_file.write(expression + "\n")
    valid_equation_file.write(constraints + "\n\n")

    # Write TI-BASIC code with type label
    function_type = identify_function_type(expression)
    tibasic_code = generate_tibasic_code(expression, constraints)
    tibasic_file.write(f"# {function_type}\n{tibasic_code}\n\n")

# Run the script on all input lines
with open("input.txt", "r") as input_file, \
     open("badeqn.txt", "w") as invalid_equation_file, \
     open("goodeqn.txt", "w") as valid_equation_file, \
     open("tibasic.txt", "w") as tibasic_file:

    for raw_line in input_file:
        cleaned_line = raw_line.strip()
        if not cleaned_line:
            continue
        print("Current Equation Is:", cleaned_line)
        process_equation_line(cleaned_line)
