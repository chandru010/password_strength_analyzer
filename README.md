# Password Strength Analyzer with Custom Wordlist Generator

**Objective:** Analyze password strength and generate custom wordlists for password-cracking/testing workflows. Designed for beginners.

## What’s included
- `src/` — Python source files:
  - `analyzer.py` — zxcvbn-based analysis + simple entropy calculation
  - `wordlist_gen.py` — generate custom wordlists from user inputs (names, dates, pets), leetspeak, years, and combinations
  - `cli.py` — command-line interface (argparse) to analyze and generate wordlists
  - `gui.py` — simple Tkinter GUI for interactive use
  - `utils.py` — helper functions
- `requirements.txt` — pip install dependencies
- `examples/` — example outputs
- `README.md` — this file
- `LICENSE` — MIT

## Quick setup (Beginner-friendly)
1. Install Python 3.8+.
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   - If you get errors installing `zxcvbn`, try `pip install zxcvbn-python`

4. (Optional) Download NLTK data used by the script:
   ```python
   python -c "import nltk; nltk.download('words')"
   ```

## How to use

### CLI
Analyze a password:
```bash
python src/cli.py analyze --password "P@ssw0rd123"
```

Generate a custom wordlist:
```bash
python src/cli.py gen --name "Alice" --pet "Rex" --dates "1990,2000" --years 2018-2025 --max 2000 --out wordlist.txt
```

### GUI
Run:
```bash
python src/gui.py
```
Use the fields, click **Generate Wordlist** and **Analyze Password**.

## File formats
- Wordlists are exported as plain `.txt` files (one candidate per line) and can be used with cracking tools (hashcat, john, etc).

## Notes for beginners
- `zxcvbn` provides a human-friendly score (0-4). Scripts also output estimated entropy.
- Wordlists generated include simple transformations and common patterns. They are not exhaustive but serve as a targeted starting point.
- Always use these tools responsibly and only on systems and accounts you own or have explicit permission to test.
