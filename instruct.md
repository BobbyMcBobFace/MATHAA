## AI Instruction Set for Generating TI-BASIC Graph Code (TI-84 Plus CE)

### General Requirements

1. **Use only Y₀ through Y₉.** Do not use Y₁₀ or higher.
2. **Limit to 10 Y-vars per code block.** If more are needed, split into separate blocks.
3. **Use `piecewise(` only when a domain is present.** If no domain is provided, use direct assignment:
   ```
   "expression"→Y₀
   ```
4. **Equations must be explicit.** Do not use implicit or parametric forms such as `x² + y² = 1`.
5. **Only `X` may be used in domain conditions.** If a range is given for `Y`, convert it to an equivalent range for `X`.

### Expression Normalization Rules

6. **Use `0-` before any negated number or expression.**
   - Correct: `0-5.1`
   - Incorrect: `-5.1`

7. **Sin/Cos/Tan expressions must be formatted as `Afunction(C)±B`:**
   - No space between the coefficient and the function (e.g., `2cos(...)`)
   - Always enclose the function argument (`C`) in parentheses.
   - If it’s unclear whether the argument is a number or a fraction, clarify or use `1/(...)`.

8. **± expressions must be split into two separate equations, assigned to two Y-vars:**
   - Example:
     ```
     "piecewise(A+√(...),domain)"→Y₀
     "piecewise(A-√(...),domain)"→Y₁
     ```

9. **Convert `x=` and `y=` equations to explicit `y=` form:**
   - For sideways parabolas (e.g., `x = a(y+b)^2 + c`), solve for `y` and express with ± branches if needed.
   - Translate all `Y` domains into `X` domains.
   - Example:
     ```
     x = 1.5(y+5.1)² + 6.7, x ≤ 8.1
     → y = 0-5.1 ± √((X−6.7)/1.5), X ≤ 8.1
     ```

### Syntax and Formatting Rules

10. **Use proper TI-BASIC syntax and symbols:**
    - Replace ASCII symbols with calculator-native versions:
      - `<=` → `≤`, `>=` → `≥`, `!=` → `≠`, `->` → `→`

11. **Avoid unnecessary spaces:**
    - No space after commas in `piecewise(`.
    - No space between function names and parentheses.
    - In domain ranges:
      - `-5≤X and X≤3` is correct.
      - Do not format as `-5 ≤ X and X ≤ 3`.

12. **Wrap all equations in quotes when assigning to Y-vars:**
    - Even without `piecewise(`, quotes are required.
    - Example: `"X²+1"→Y₁`

13. **Add a `GraphColor` command after each Y-var assignment:**
    - Format: `GraphColor(index,color)`
    - Example: `GraphColor(0,22)`

14. **End every code block with cleanup and graph commands:**
    ```
    DispGraph
    RecallPic 0
    StorePic 0
    ClrDraw
    DelVar Y₀
    DelVar Y₁
    ...
    DelVar Y₉
    ```
