import re

# Check if equation is explicit
# Stopped matching for X equations and add it to invalid_equations
def is_valid_equation(equation):
    pattern = r'\s*(y)\s*=\s*(?P<expression>[^{{]+)\s*({(?P<constraints>[^}]+)})?'
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

# Turn the expression + constraints into TI-BASIC compatible syntax (for file output)
def generate_tibasic_code(expression, constraints, y_index):
    expression = expression.replace("x", "X").replace("y", "Y")
    constraints = constraints.replace("x", "X").replace("y", "Y")

    # Fix range: A <= X <= B to A<=X and X<=B
    # Stopped matching for X equations and add it to invalid_equations
    match_range = re.match(r'(-?\d*\.?\d*)\s*<=\s*(X|Y)\s*<=\s*(-?\d*\.?\d*)', constraints)
    if match_range:
        lower, var, upper = match_range.groups()
        constraints = f"{lower}<={var} and {var}<={upper}"

    return f"\"piecewise({expression},{constraints})\"->Y{y_index}\nGraphColor(Y{y_index}, <color>)"

# storage
valid_equations = []
invalid_equations = []

# Read from input.txt
with open("input.txt", "r") as input_file:
    for line in input_file:
        cleaned_line = line.strip()
        print("Current Equation Is: " + cleaned_line)
        if not cleaned_line:
            continue
        if not is_valid_equation(cleaned_line):
            print("Line Invalid! Add Manually.\n")
            invalid_equations.append(cleaned_line)
            continue

        print("Line Valid! Proceeding.\n")
        match = re.match(r'\s*(y|x)\s*=\s*(?P<expression>[^{{]+)\s*({(?P<constraints>[^}]+)})?', cleaned_line)
        expression = match.group("expression").strip()
        constraints = match.group("constraints") if match.group("constraints") else ""
        valid_equations.append((expression, constraints))

# Write bad equations
with open("badeqn.txt", "w") as bad_file:
    for eq in invalid_equations:
        bad_file.write(eq + "\n")

# Write valid output in groups of 10
program_count = 0
for i in range(0, len(valid_equations), 10):
    chunk = valid_equations[i:i+10]
    lines = []

    for j, (expression, constraints) in enumerate(chunk):
        lines.append(generate_tibasic_code(expression, constraints, j))

    lines.append("DispGraph")
    lines.append("RecallPic 0")
    lines.append("StorePic 0")
    lines.append("ClrDraw")
    for k in range(10):
        lines.append(f"DelVar Y{k}")

    with open(f"program{program_count + 1}.txt", "w") as out_file:
        out_file.write("\n".join(lines))

    program_count += 1

print(f"Done. Created {program_count} files.")
