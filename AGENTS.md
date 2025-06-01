Style guide:
* Follow PEP 8.
* Type hints mandatory for every public function or method.
  Use from __future__ import annotations.
* Google-style triple-quoted docstrings for public functions.
  Private helpers (_internal) may omit docstrings if the code is trivial.

Comments:
* Include a top-of-file comment stating the file’s purpose.
* Use comments only when intent or reasoning is not obvious from names.
* No “translation” comments (like “increment i”).
* No comment banners.

Granularity:
* Keep functions short and single-purpose.
* 40–60 lines per function before splitting into smaller helpers.
* Prefer multiple helper functions over large, complex functions.

Data interchange:
* Pass simple scalars or tuples (tuple[int, ...]) for dice.
* For complex data bundles, use dataclasses (e.g., Combination, TurnResult).
* Avoid passing raw dictionaries unless their structure is obvious and documented.

Logging vs. Prints
* Use the built-in logging module instead of print statements for:
  * Complex operations.
  * Long-running processes.
  * Debugging and tracing internal logic.
* Simple or short-lived scripts may still use print() if logging adds unnecessary complexity

Error handling:
* Do not add unnecessary validation checks for obvious preconditions.
* Only validate inputs explicitly when preconditions are non-obvious, easy to misuse, or have no crash fallback.
* Allow Python to raise built-in exceptions (like TypeError, IndexError) naturally.
  Use the traceback to debug issues as they occur.
* Clearly describe expected preconditions in docstrings without enforcing them explicitly in code.
* Use try-except blocks only when truly recovering, such as in long-running simulations or I/O operations.

Tests:
* No formal tests; rely instead on manual smoke tests and logging.
* Write simple scripts under analysis/ to quickly spot-check key behaviors.
* Maintain a minimal tests/ folder, executed locally with pytest.
* Focus on 3-4 canonical truths (e.g. expectation_one_throw(5) ≈ 28.289).
* Console output is welcome: feel free to print() or use logging.
* Run with pytest -q -s so the captured output is shown.

Commit messages:
* Use present-tense imperative style: "Add scoring for triples", "Fix bust detection".

Additional project rules:
* No global state. Pass a seeded random.Random into functions when determinism matters.
* Reproducible plots. Save figures with informative names (ev_by_dice.png) and reference them in insights.md.
* Avoid premature optimization. Clarity > microseconds. Optimize only after profiling proves it's worth it.
* Use JSON for storing structured simulation data (e.g., turn logs, strategy outputs, roll histories).