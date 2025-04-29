import re
from typing import List, Tuple
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.containers import Vertical
from textual.widgets import Header, Footer, Static, Input

EQUATION_PATTERN = re.compile(r'\s*y\s*=\s*([^{]+)\s*(?:{([^}]+)})?')

class EquationProcessor:
    """Handles equation processing and TI-BASIC code generation."""
    
    def __init__(self, input_file: str = "input.txt") -> None:
        self.input_file = input_file
        self.valid_equations: List[Tuple[str, str]] = []
        self.colors: dict[int, str] = {}
        self._process_input()

    def _process_input(self) -> None:
        """Load and validate equations from input file."""
        with open(self.input_file, "r") as file:
            for idx, line in enumerate(file):
                if not (line := line.strip()):
                    continue
                if match := EQUATION_PATTERN.match(line):
                    expr, constraints = match.groups()
                    self.valid_equations.append((expr.strip(), (constraints or "").strip()))
                else:
                    with open("badeqn.txt", "a") as bad_file:
                        bad_file.write(line + "\n")

    @staticmethod
    def format_piecewise(expr: str, constraints: str, color: str, y_index: int) -> str:
        """Format TI-BASIC piecewise function."""
        expr = expr.replace("x", "X").replace("y", "Y")
        constraints = re.sub(r'(-?\d*\.?\d*)\s*<=\s*([XY])\s*<=\s*(-?\d*\.?\d*)',
                            r'\1<=\2 and \2<=\3', constraints or "")
        return f'"piecewise({expr},{constraints})"->Y{y_index}\nGraphColor(Y{y_index},{color})'

    def generate_programs(self) -> None:
        """Generate program files with equations and colors."""
        for prog_num, i in enumerate(range(0, len(self.valid_equations), 10), 1):
            chunk = self.valid_equations[i:i+10]
            lines = [
                self.format_piecewise(expr, constr, self.colors.get(i+j, "BLACK"), j)
                for j, (expr, constr) in enumerate(chunk)
            ]
            lines += [
                "DispGraph", "RecallPic 0", "StorePic 0", "ClrDraw", 
                *(f"DelVar Y{k}" for k in range(10))
            ]
            with open(f"program{prog_num}.txt", "w") as f:
                f.write("\n".join(lines))

class EquationConverterApp(App):
    """TUI for assigning colors to equations."""
    
    CSS = """
    #main-container {
        padding: 1;
        align: center middle;
    }
    
    #equation-display, #ti-display {
        border: heavy white;
        padding: 1 2;
        margin: 1 0;
    }
    
    #input-container {
        margin: 2 0;
    }
    
    #counter {
        width: 100%;
        content-align: center middle;
        text-align: center;
    }
    """
    
    BINDINGS = [
        ("ctrl+b", "undo", "Undo"),
        ("ctrl+n", "skip", "Skip"),
        ("ctrl+l", "generate", "Generate Programs"),
        ("ctrl+o", "submit_color", "Submit Color"),
    ]

    current_index = reactive(0)

    def __init__(self, processor: EquationProcessor) -> None:
        super().__init__()
        self.processor = processor
        self.total = len(processor.valid_equations)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main-container"):
            # Equation display with rounded corners
            self.eq_display = Static(id="equation-display")
            self.eq_display.styles.rounding = (1, 2)  # Rounded corners
            yield self.eq_display

            # TI-BASIC display with rounded corners
            self.ti_display = Static(id="ti-display")
            self.ti_display.styles.rounding = (1, 2)  # Rounded corners
            yield self.ti_display

            # Color input with rounded corners
            with Vertical(id="input-container"):
                self.color_input = Input(placeholder="Enter color code (any value)")
                self.color_input.styles.rounding = (1, 1)  # Rounded corners
                yield self.color_input

            # Centered counter
            self.counter = Static(id="counter")
            yield self.counter
        yield Footer()

    def on_mount(self) -> None:
        self.update_display()

    def update_display(self) -> None:
        """Update all display elements."""
        if self.current_index >= self.total:
            self.eq_display.update("All equations processed!")
            self.ti_display.update("")
            self.counter.update("")
            return

        expr, constr = self.processor.valid_equations[self.current_index]
        y_idx = self.current_index % 10
        color = self.processor.colors.get(self.current_index, "color")
        
        self.eq_display.update(f"Equation: y = {expr} {{{constr}}}")
        self.ti_display.update(f"TI-BASIC:\n{self.processor.format_piecewise(expr, constr, color, y_idx)}")
        self.counter.update(f"Equation {self.current_index + 1}/{self.total}")
        self.color_input.value = self.processor.colors.get(self.current_index, "")

    def action_submit_color(self) -> None:
        if self.current_index >= self.total:
            return
        color = self.color_input.value.strip().upper() or "BLACK"
        self.processor.colors[self.current_index] = color
        self.current_index += 1
        self.update_display()

    def action_undo(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

    def action_skip(self) -> None:
        if self.current_index < self.total:
            self.current_index += 1
            self.update_display()

    def action_generate(self) -> None:
        self.processor.generate_programs()
        self.notify("Program files generated!")

if __name__ == "__main__":
    EquationConverterApp(EquationProcessor()).run()
