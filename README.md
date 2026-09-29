<h1>🔢 Simple Calculator 🔢</h1>

<h2>👋 Introduction 👋</h2>

This project is a small calculator which offers support for all basic arithmetic operations, as well as the basic trigonometric and logarithmic functions.
<br>
I built this calculator for fun within a day. Feel free to check it out and fork it however you want!

<h2>✅ Dependencies ✅</h2>

This project only uses the **PySimpleGUI** external library.

<h2>📝 Setup 📝</h2>

<h3><u>uv</u></h3>

Run the following commands in the starting directory of the project:

<h4>With virtual environment:</h4>

```bash
uv venv
uv sync
uv run simple-calculator
```

<h4>Without virtual environment:</h4>

```bash
cd src/calculator # Make sure you're under src/calculator for this command to work!
uv run __main__.py
```

<h3><u>pip</u></h3>

Alternatively, run the following commands in the starting directory of the project:

<h4>With virtual environment:</h4>

```bash
python -m venv .venv
# Run one of the following three commands:
source .venv/bin/activate    # On macOS/Linux.
venv\Scripts\activate.bat    # On Windows (CMD)
venv\Scripts\Activate.ps1    # On Windows (PowerShell)
# Afterwards:
pip install -e
python -m simple-calculator
```

<h4>Without virtual environment:</h4>

```bash
pip install --break-system-packages # To install PySimpleGUI globally.
# Alternatively, run pip install PySimpleGUI instead of the above command
python __main__.py # Make sure you're under src/calculator for this command to work!
```