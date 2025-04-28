import re
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Header, Footer
from textual.containers import Vertical
from textual.reactive import reactive
from textual import events

# === Helper functions ===
def is_valid_equation(equation):
    pattern = r'\s*(y)\s*=\s*(?P<expression>[^{{]+)\s*({(?P<constraints>[^}]+)})?'
    return re.match(pattern, equation) is not None

def generate_tibasic_code(expression, constraints, y_index, color):
    expression = expression.replace("x", "X").replace("y", "Y")
    constraints = constraints.replace("x", "X").replace("y", "Y")
    match_range = re.match(r'(-?\d*\.?\d*)\s*<=\s*(X|Y)\s*<=\s*(-?\d*\.?\d*)', constraints)
    if match_range:
        lower, var, upper = match_range.groups()
        constraints = f"{lower}<={var} and {var}<={upper}"
    return f"\"piecewise({expression},{constraints})\"->Y{y_index}\nGraphColor(Y{y_index}, {color if color else '<color>'})"

# === Load input file ===
valid_equations = []
invalid_equations = []

with open("input.txt", "r") as input_file:
    for line in input_file:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        if not is_valid_equation(cleaned_line):
            invalid_equations.append(cleaned_line)
            continue
        match = re.match(r'\s*(y|x)\s*=\s*(?P<expression>[^{{]+)\s*({(?P<constraints>[^}]+)})?', cleaned_line)
        expression = match.group("expression").strip()
        constraints = match.group("constraints") if match.group("constraints") else ""
        valid_equations.append((cleaned_line, expression, constraints))

# === TUI App ===
class ConverterTUI(App):
    BINDINGS = [
        ("b", "action_go_back", "Back"),
        ("n", "action_next", "Next equation"),
        ("r", "action_generate_files", "Generate Files"),
        ("enter", "action_submit_color", "Submit color"),
    ]

    index = reactive(0)
    current_color = reactive("")
    input_value = reactive("")
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main"):
            yield Static("Current Equation:", classes="label")
            yield Static("", id="eq_display", classes="box")
            yield Static("TI-BASIC Output:", classes="label")
            yield Static("", id="pw_display", classes="box")
            yield Input(
                placeholder="Enter color (10–24)",
                id="color_input",
                tooltip="Type a number and press Enter!"
            )
        yield Footer()

    def update_display(self):
        eq, expr, constraint = valid_equations[self.index]
        color = self.current_color
        code = generate_tibasic_code(expr, constraint, self.index, color)
        self.query_one("#eq_display", Static).update(f"Equation {self.index + 1}: {eq}")
        self.query_one("#pw_display", Static).update(code)
        self.query_one("#color_input", Input).value = self.input_value

    def on_mount(self):
        self.update_display()

    def on_input_changed(self, event: Input.Changed):
        self.input_value = event.value

    def on_input_submitted(self, event: Input.Submitted):
        value = event.value.strip()
        if value.isdigit() and 10 <= int(value) <= 24:
            self.current_color = value
            self.input_value = ""  # Clear after submit
            self.action_next()
        else:
            self.query_one("#color_input", Input).tooltip = "❌ Only numbers 10–24 allowed!"
            self.input_value = ""  # Clear wrong input
        self.update_display()

    def on_key(self, event: events.Key):
        if event.key == "b":
            self.action_go_back()
        elif event.key == "n":
            self.action_next()
        elif event.key == "r":
            self.action_generate_files()

    def action_go_back(self):
        if self.index > 0:
            self.index -= 1
            self.current_color = ""
            self.input_value = ""
            self.update_display()

    def action_next(self):
        if self.index < len(valid_equations) - 1:
            self.index += 1
            self.current_color = ""
            self.input_value = ""
            self.update_display()

    def action_generate_files(self):
        program_count = 0
        for i in range(0, len(valid_equations), 10):
            chunk = valid_equations[i:i + 10]
            lines = []
            for j, (eq, expression, constraints) in enumerate(chunk):
                color = self.current_color
                lines.append(generate_tibasic_code(expression, constraints, j, color))

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

if __name__ == "__main__":
    ConverterTUI().run()
