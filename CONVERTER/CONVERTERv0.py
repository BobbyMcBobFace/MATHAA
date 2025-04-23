import re

# Function to check if equation is of type y = mx + c {a <= y <= b}
def check_is_equation_ymxc(eqn):
    pattern = r'\s*(y|x)\s*=\s*(?P<expr>[^{{]+)\s*({(?P<constraints>[^}]+)})?'
    if re.match(pattern, eqn):
        return True
    else:
        return False

# Function to check for non-implicit equation
def utility_function(eqn):
    if check_is_equation_ymxc(eqn) != True:
        print("Format Incorrect! Please Manually Add" + "\n")
        badeqn.write(eqn + "\n")
        return
    else:
        print("Format correct! Proceeding")
        match = re.match(r'\s*(y|x)\s*=\s*(?P<expr>[^{{]+)\s*({(?P<constraints>[^}]+)})?', eqn)
        expr = match.group("expr").strip()
        constraints = match.group("constraints") if match.group("constraints") else ""
        print("Expression:", expr)
        print("Constraints:", constraints + "\n")
        goodeqn.write(eqn + "\n")
        goodeqn.write(expr + "\n")
        goodeqn.write(constraints + "\n" + "\n")   

# Main
f = open("input.txt", "r")
badeqn = open("badeqn.txt", "w")
goodeqn = open("goodeqn.txt", "w")

for x in f:
    x = x.strip()
    if not x:
        continue
    print("Current Equation Is:", x)
    utility_function(x)
    
f.close()
badeqn.close()
goodeqn.close()


