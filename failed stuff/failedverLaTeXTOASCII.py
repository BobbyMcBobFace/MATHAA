import re
from pylatexenc.latex2text import LatexNodes2Text

def latex_to_text(latex_code):
    """Convert LaTeX code to plaintext."""
    return LatexNodes2Text().latex_to_text(latex_code)

def parse_latex_equation(latex_code):
    """Parse the LaTeX equation and return a list of expressions and conditions."""
    # Simplistic heuristic to parse LaTeX equations
    # This is a basic parser and may not handle all cases
    expressions = []
    conditions = []
    for line in latex_code.split('\n'):
        if line.strip() and not line.startswith('%'):
            parts = line.split('=')
            if len(parts) == 2:
                expressions.append(parts[0].strip())
                conditions.append(parts[1].strip())
    return expressions, conditions

def convert_to_ti_basics(expressions, conditions):
    """Convert a list of expressions and conditions to TI-BASIC piecewise syntax."""
    ti_basics = []
    for expr, cond in zip(expressions, conditions):
        ti_basics.append(f'piecewise({expr}, {cond})')
    return ti_basics

def main():
    # Read the LaTeX file
    with open('input.txt', 'r') as file:
        latex_code = file.read()

    # Convert LaTeX to plaintext
    plaintext_equations = latex_to_text(latex_code)

    # Parse the plaintext equations
    expressions, conditions = parse_latex_equation(plaintext_equations)

    # Convert to TI-BASIC piecewise syntax
    ti_basics = convert_to_ti_basics(expressions, conditions)

    # Output the TI-BASIC piecewise syntax
    for ti_basic in ti_basics:
        print(f"{ti_basic}")

if __name__ == "__main__":
    main()