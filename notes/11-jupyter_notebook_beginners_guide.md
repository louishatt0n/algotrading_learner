# Jupyter Notebook Beginner's Guide

This guide is a practical "start here" reference for using Jupyter Notebook as a beginner.

---

## 1) What Jupyter Notebook Is

Jupyter Notebook is an interactive environment where you run code in small blocks called **cells**.

- You can mix:
  - **Code cells** (Python code)
  - **Markdown cells** (notes, headings, explanations)
  - Output (tables, plots, errors) inline below each cell

Think of it as: document + code + results in one place.

---

## 2) Core Concepts You Must Understand

### A) Kernel

The **kernel** is the live Python process executing your code.

- Restarting kernel clears all in-memory variables/imports.
- If things behave strangely, restart kernel and run all cells top-to-bottom.

### B) Cell Order Matters

Cells can run out of order. This causes confusion.

- A notebook may "work" only because hidden state is already in memory.
- Best practice: run in order from the top.

### C) Notebook State vs File on Disk

A notebook has:
- In-memory state (what you currently see while open)
- Saved file on disk (`.ipynb`)

If the same notebook is open in two places (e.g., browser + editor), one can overwrite the other.

---

## 3) Basic Workflow (Recommended)

1. Open notebook
2. Restart kernel
3. Run all cells in order
4. Make changes
5. Save frequently
6. Before finishing: restart + run all again to verify reproducibility

---

## 4) Essential Shortcuts

Two modes:
- **Command mode** (cell-level actions, press `Esc`)
- **Edit mode** (edit cell text, press `Enter`)

Useful shortcuts:
- `Shift + Enter`: Run cell and move to next
- `Ctrl + Enter`: Run cell and stay
- `A`: Insert cell above (command mode)
- `B`: Insert cell below (command mode)
- `M`: Convert to Markdown cell
- `Y`: Convert to Code cell
- `DD`: Delete cell

---

## 5) Project Structure Best Practices

For maintainability, keep:

- `notebooks/` or `strategies/` -> experiments and analysis
- `src/` -> reusable Python modules
- `tests/` -> tests for core logic

Put heavy logic in `.py` files, and keep notebooks focused on exploration and visualization.

---

## 6) Imports and ModuleNotFoundError (`No module named 'src'`)

This is one of the most common beginner issues.

### Why it happens
Python cannot find your project root in `sys.path`.

### Fix option 1 (best)
Start Jupyter from your project root directory.

### Fix option 2
Add root path in first cell:

```python
import sys
from pathlib import Path

cwd = Path.cwd().resolve()
project_root = next((p for p in [cwd, *cwd.parents] if (p / "src").exists()), cwd)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

---

## 7) Re-running Changed Python Modules

If you edit a `.py` file while notebook kernel is running, notebook may keep old code cached.

Use:

```python
import importlib
import src.data_loader as data_loader
importlib.reload(data_loader)
```

Or restart kernel and run all cells.

---

## 8) Debugging Errors in Notebooks

When you see an error:

1. Read the exception type and line number
2. Verify variables were defined earlier
3. Check execution order
4. Restart kernel and run all

For weird behavior:
- Clear all outputs
- Restart kernel
- Run all cells cleanly

---

## 9) Common Beginner Pitfalls

- Running cells out of order
- Depending on hidden state
- Not saving before closing
- Editing same notebook in multiple places
- Putting too much production logic in notebook cells
- Forgetting to restart/re-run after package or module changes

---

## 10) Notebook Hygiene (Very Important)

- Keep cells small and focused
- Use markdown headers to organize sections
- Name variables clearly
- Remove unused cells
- Clear huge outputs before committing to git
- Add brief markdown context for future you

---

## 11) Reproducibility Checklist

Before sharing/submitting:

- [ ] Kernel restarted
- [ ] Run all completed without errors
- [ ] No hidden dependencies on old state
- [ ] Data paths are relative and valid
- [ ] Notebook saved
- [ ] Environment/dependencies documented

---

## 12) Version Control Tips for `.ipynb`

Notebook files are JSON and can produce noisy git diffs.

Tips:
- Keep output minimal
- Use clear markdown structure
- Move stable logic to `.py` files
- Commit often with meaningful messages

---

## 13) When to Use Notebook vs `.py`

Use notebook for:
- Exploration
- Visualization
- Quick hypothesis testing
- Teaching/explanations

Use `.py` for:
- Reusable functions/classes
- Pipelines
- Production-ready logic
- Unit-tested code

Best combo: notebook calls clean functions from `src/`.

---

## 14) Quickly Update Original `.py` From Notebook

If you modify logic in a notebook and want to push it back into the original Python file, use one of these options.

### Option 1: `%%writefile` (fastest manual method)

Put full script content in one cell and write directly to the target file:

```python
%%writefile strategies/sma_crossover.py
# full python script content here
```

- Very fast for immediate overwrite.
- Best when you intentionally want notebook to be source of truth for that moment.
- Important: this overwrites the file on disk.

### Option 2: `nbconvert` export (checkpoint snapshot)

From project root in terminal:

```bash
jupyter nbconvert --to script strategies/sma_crossover.ipynb
```

- Exports notebook to a `.py` script snapshot.
- Good for periodic sync/checkpoints.
- One-way export, not a true two-way workflow.

### Option 3: Jupytext pairing (best long-term workflow)

Install once:

```bash
pip install jupytext
```

Pair a notebook with a script:

```bash
jupytext --set-formats ipynb,py:percent strategies/sma_crossover.ipynb
```

- Keeps notebook and `.py` paired.
- Better diffs and easier Git workflow.
- Most maintainable option for ongoing notebook + script development.

Recommended workflow for beginners:
- Use `%%writefile` for quick fixes today.
- Move to Jupytext pairing once workflow stabilizes.

---

## 15) Quick "Healthy Session" Starter Cell

```python
# 1) Path setup
import sys
from pathlib import Path

cwd = Path.cwd().resolve()
project_root = next((p for p in [cwd, *cwd.parents] if (p / "src").exists()), cwd)
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 2) Basic sanity info
print("cwd:", cwd)
print("project_root:", project_root)

# 3) Imports
from src.data_loader import df
print(df.head())
```

---

## 16) Final Advice

If your notebook gets fragile, that is normal.

The skill to build is:
- Keep notebook lightweight
- Move logic into `.py`
- Restart and run all often

That habit alone solves most beginner pain in Jupyter.

