from pylatexenc.latex2text import LatexNodes2Text
import re

def latex_to_pieces(latex_str):
    """
    Converts a LaTeX string into plaintext and then into pieces suitable for TI-Basic.
    
    Args:
    latex_str (str): A LaTeX string in the format "equation\ range"
    
    Returns:
    list: A list of tuples (expression, condition) suitable for TI-Basic piecewise function.
    """
    # Use LatexNodes2Text to convert LaTeX to plaintext
    converter = LatexNodes2Text()
    
    try:
        # Split the LaTeX string into equation and range
        equation, range_str = latex_str.split('\\left{')
    except ValueError:
        raise ValueError(f"Invalid LaTeX format: {latex_str}")
    
    # Strip unwanted characters and convert LaTeX equation to plaintext
    equation = equation.strip().rstrip('\\')
    equation = converter.latex_to_text(equation.strip())
    
    # Remove any backslashes and equals sign from equation
    equation = equation.replace('\\', '').replace('=', '')
    
    # Extract range conditions using regex
    match = re.match(r'([<>]=?)([\d.+-]+)<([<>]=?)([\d.+-]+)', range_str)
    if not match:
        raise ValueError(f"Invalid range format: {range_str}")
    
    less_op, less_val, more_op, more_val = match.groups()
    
    # Convert LaTeX range to TI-Basic condition
    # Example: "-4.5<x<=-4.15" becomes "X>-4.5 and X<=-4.15"
    if less_op == '<':
        less_op = '>'
    elif less_op == '<=':
        less_op = '>='
    
    if more_op == '<':
        more_op = '<'
    elif more_op == '<=':
        more_op = '<='
    
    condition = f"X{less_op}{less_val} and X{more_op}{more_val}"
    
    return [(equation, condition)]

def convert_file_to_tibasic(input_file, output_file):
    """
    Converts the contents of a file containing LaTeX strings into TI-Basic piecewise functions.
    
    Args:
    input_file (str): The path to the input file containing LaTeX strings.
    output_file (str): The path to the output file to write the TI-Basic commands.
    """
    tibasic_lines = []
    
    with open(input_file, 'r') as infile:
        for line in infile:
            try:
                latex_pieces = latex_to_pieces(line.strip())
                if latex_pieces:
                    piecewise_cmd = "piecewise("
                    for expression, condition in latex_pieces:
                        piecewise_cmd += f"{expression}, {condition}, "
                    # Remove trailing comma and space
                    piecewise_cmd = piecewise_cmd.rstrip(', ') + ")"
                    tibasic_lines.append(piecewise_cmd)
            except ValueError as e:
                print(f"Error processing line: {line.strip()}. Reason: {e}")
    
    with open(output_file, 'w') as outfile:
        for line in tibasic_lines:
            outfile.write(line + '\n')

# Example usage
convert_file_to_tibasic('input.txt', 'output.txt')

# Test debug
with open('output.txt', 'r') as debugfile:
    for line in debugfile:
        print(line.strip())
