import re
from typing import List, Tuple, Optional

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Input
from textual.reactive import reactive

# ---------------- Equation Processor -------------------

class EquationProcessor:
    """Handles reading, validating, and formatting equations."""

    def __init__(self, input_file: str = "input.txt") -> None:
        self.input_file = input_file
        self.valid_equations: List[Tuple[str, str]] = []
        self.invalid_equations: List[str] = []
        self.color_mapping: List[Optional[str]] = []  # Color mapping for each equation
        self.colors: dict[int, str] = {}  # Store colors for equations (indexed by their number)
        self.load_equations()

    def load_equations(self) -> None:
        """Reads and validates equations from input file."""
        with open(self.input_file, "r") as file:
            for line in file:
                cleaned = line.strip()
                if not cleaned:
                    continue
                if not self.is_valid_equation(cleaned):
                    self.invalid_equations.append(cleaned)
                    continue
                match = re.match(r'\s*(y)\s*=\s*(?P<expression>[^{]+)\s*({(?P<constraints>[^}]+)})?', cleaned)
                expression = match.group("expression").strip()
                constraints = match.group("constraints") or ""
                self.valid_equations.append((expression, constraints))
                self.color_mapping.append(None)  # Initialize color slots

        # Write invalid equations to badeqn.txt immediately
        with open("badeqn.txt", "w") as bad_file:
            for eq in self.invalid_equations:
                bad_file.write(eq + "\n")

    @staticmethod
    def is_valid_equation(equation: str) -> bool:
        """Validates if the equation matches the expected format."""
        pattern = r'\s*(y)\s*=\s*([^{{]+)\s*({[^}]+})?'
        return re.match(pattern, equation) is not None

    @staticmethod
    def format_piecewise(expression: str, constraints: str, color: str, y_index: int) -> str:
        """Formats a TI-BASIC piecewise line with color."""
        expression = expression.replace("x", "X").replace("y", "Y")
        constraints = constraints.replace("x", "X").replace("y", "Y")

        # Format constraint if in "a <= x <= b" form
        match_range = re.match(r'(-?\d*\.?\d*)\s*<=\s*(X|Y)\s*<=\s*(-?\d*\.?\d*)', constraints)
        if match_range:
            lower, var, upper = match_range.groups()
            constraints = f"{lower}<={var} and {var}<={upper}"

        return f"\"piecewise({expression},{constraints})\"->Y{y_index}\nGraphColor(Y{y_index},{color})"

    def generate_program_files(self) -> None:
        """Generates programX.txt files based on collected equations and colors."""
        program_count = 0

        for i in range(0, len(self.valid_equations), 10):
            chunk = self.valid_equations[i:i+10]
            color_chunk = self.color_mapping[i:i+10]    
            lines = []

            for j, ((expression, constraints), color) in enumerate(zip(chunk, color_chunk)):
                # Default to a placeholder color if skipped
                assigned_color = color if color is not None else "BLACK"
                lines.append(self.format_piecewise(expression, constraints, assigned_color, j))

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


# ---------------- TUI App -------------------

class EquationConverterApp(App):
    """Textual TUI App for mapping colors to equations."""

    CSS_PATH = "converter.tcss"  # No custom CSS, pure code-based layout
    BINDINGS = [
        ("ctrl+b", "undo", "Undo"),
        ("ctrl+n", "skip", "Next"),
        ("ctrl+l", "produce", "Generate Piecewise"),
        ("ctrl+o", "submit_color", "Submit Color"),
    ]

    current_index = reactive(0)

    def __init__(self, processor: EquationProcessor) -> None:
        super().__init__()
        self.processor = processor
        self.current_color: str = ""  # Initial color is empty

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            self.eq_display = Static("")
            self.piecewise_display = Static("")
            self.counter_display = Static("")
            yield self.eq_display
            yield self.piecewise_display
            yield self.counter_display
            self.color_input = Input(placeholder="Enter color code here", name="color_input", valid_empty=True)
            yield self.color_input
        yield Footer()

    def on_mount(self) -> None:
        """Setup when app starts."""
        self.update_displays()

    def update_displays(self) -> None:
        """Refreshes the displayed equation, piecewise output, and counter."""
        if self.current_index < len(self.processor.valid_equations):
            expr, constraint = self.processor.valid_equations[self.current_index]

            # Try to fetch saved color if exists, else use "<color>"
            saved_color = self.processor.colors.get(self.current_index)
            color = saved_color if saved_color is not None else "color"

            y_idx = self.current_index % 10  # TI-BASIC resets Y0-Y9 every 10 equations
            piecewise = EquationProcessor.format_piecewise(expr, constraint, color, y_idx)

            self.eq_display.update(f"Equation: y = {expr} {{{constraint}}}")
            self.piecewise_display.update(f"TI-BASIC: {piecewise}")
            self.counter_display.update(f"Equation {self.current_index + 1} of {len(self.processor.valid_equations)}")

            # Only clear input if not already filled (for editing convenience)
            self.color_input.value = "" if saved_color is None else str(saved_color)

        else:
            self.eq_display.update("All equations processed.")
            self.piecewise_display.update("")
            self.counter_display.update("")

    def action_submit_color(self) -> None:
        """Handles Ctrl+O key: saves color and moves forward."""
        if self.current_index < len(self.processor.valid_equations):
            color = self.color_input.value.strip().upper() or "BLACK"
            self.processor.color_mapping[self.current_index] = color  # Store color
            self.processor.colors[self.current_index] = color  # Store color in the 'colors' dictionary
            self.current_index += 1  # Move to the next equation
            self.update_displays()  # Update UI after color submission
            self.set_focus(None)  # Remove focus from the input field

    def action_undo(self) -> None:
        """Handles Ctrl+B key: undo last color entry."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_displays()

    def action_skip(self) -> None:
        """Handles Ctrl+N key: skip setting color."""
        if self.current_index < len(self.processor.valid_equations):
            self.current_index += 1
            self.update_displays()

    def action_produce(self) -> None:
        """Handles Ctrl+L key: generates final output files."""
        self.processor.generate_program_files()
        self.notify("program files generated")

# ---------------- Main Entry -------------------

if __name__ == "__main__":
    processor = EquationProcessor()
    app = EquationConverterApp(processor)
    app.run()
