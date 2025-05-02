
## AI Instruction Set for Generating TI-BASIC Graph Code (TI-84 Plus CE)

### General Requirements

1. **Use only Y₀ through Y₉.** Do not use Y₁₀ or higher.
2. **Limit to 10 Y-vars per code block.** If more are needed, split into separate blocks.
3. **Use `piecewise(` only when a domain is present.** If no domain is provided, use direct assignment:

   ```basic
   "expression"→Y₀
   ```
4. **Equations must be explicit.** Do not use implicit or parametric forms such as `x² + y² = 1`.
5. **Only `X` may be used in domain conditions.** If a range is given for `Y`, convert it to an equivalent range for `X`.

---

### Expression Normalization Rules

6. **Distinguish between subtraction and negation:**

   * **Negation** must use `0-` before the value or expression.

     * Correct: `0-5.1`
   * **Subtraction** must be written as-is, e.g., `X-5`.

7. **Sin/Cos/Tan expressions must be formatted as `Afunction(C)±B`:**

   * No space between the coefficient and the function (e.g., `2cos(...)`)
   * Always enclose the function argument `C` in parentheses.
   * **Always ask for clarification** if unsure whether the argument is a simple number or a fraction — **do not automatically convert to `1/(...)`**.

8. **± expressions must be split into two separate equations, assigned to two Y-vars:**

   ```basic
   "piecewise(A+√(...),domain)"→Y₀
   "piecewise(A-√(...),domain)"→Y₁
   ```

9. **Convert all `x=` and `y=` equations to explicit `y=` form:**

   * For sideways parabolas (e.g., `x = a(y+b)^2 + c`), solve for `y` using algebra.
   * If this leads to a ± form, split it accordingly (see Rule 8).
   * Translate all `Y` domains into `X` domains.
   * Example:

     ```basic
     x = 1.5(y+5.1)² + 6.7, x≤8.1
     → y = 0-5.1±√((X−6.7)/1.5), X≤8.1
     ```

---

### Syntax and Formatting Rules

10. **Convert ASCII syntax to TI-native syntax:**

    * `<=` → `≤`, `>=` → `≥`, `!=` → `≠`, `->` → `→`

11. **Avoid unnecessary spaces:**

    * No space after commas in `piecewise(`:
      ✅ `piecewise(expr,X≤3)`
      ❌ `piecewise(expr, X≤3)`
    * No space between function names and parentheses.
    * In domain ranges, retain spacing around `and` only:
      ✅ `-8≤X and X≤-6.21`

12. **Wrap all equations in quotes when assigning to Y-vars:**

    * Required for valid TI-BASIC syntax.
    * Example: `"X²+1"→Y₁`

13. **Add a `GraphColor` command after each Y-var assignment:**

    * Do **not** use a closing parenthesis.
    * Format:

      ```basic
      GraphColor(index,color
      ```

14. **End every code block with cleanup and graph commands:**

    ```basic
    DispGraph
    RecallPic 0
    StorePic 0
    ClrDraw
    DelVar Y₀
    DelVar Y₁
    ...
    DelVar Y₉
    ```

