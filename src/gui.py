"""gui.py - simple Tkinter GUI"""
import tkinter as tk
from tkinter import messagebox, filedialog
from analyzer import analyze
from wordlist_gen import generate_tokens, save_wordlist

def analyze_click():
    pwd = pw_entry.get()
    if not pwd:
        messagebox.showwarning("Input required", "Enter a password to analyze")
        return
    res = analyze(pwd)
    z = res.get('zxcvbn', {})
    score = z.get('score') if isinstance(z, dict) else None
    entropy = res.get('entropy_bits')
    txt = f"zxcvbn score: {score}\\nEstimated entropy (bits): {entropy:.2f}"
    result_var.set(txt)

def gen_click():
    name = name_entry.get().strip() or None
    pet = pet_entry.get().strip() or None
    dates = [d.strip() for d in dates_entry.get().split(',')] if dates_entry.get().strip() else None
    years = years_entry.get().strip() or None
    years_arg = None
    if years:
        if '-' in years:
            s,e = years.split('-',1)
            years_arg = [str(y) for y in range(int(s), int(e)+1)]
        else:
            years_arg = [y.strip() for y in years.split(',') if y.strip()]
    wl = generate_tokens(name=name, pet=pet, dates=dates, years=years_arg, max_tokens=5000)
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
    if path:
        save_wordlist(wl, path)
        messagebox.showinfo("Saved", f"Wrote {len(wl)} entries to {path}")

root = tk.Tk()
root.title("Password Strength Analyzer")

tk.Label(root, text="Password:").grid(row=0, column=0, sticky="e")
pw_entry = tk.Entry(root, width=30, show="*")
pw_entry.grid(row=0, column=1)

tk.Button(root, text="Analyze Password", command=analyze_click).grid(row=0, column=2, padx=5)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, justify="left").grid(row=1, column=0, columnspan=3, sticky="w")

tk.Label(root, text="Name:").grid(row=2, column=0, sticky="e")
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=2, column=1)

tk.Label(root, text="Pet:").grid(row=3, column=0, sticky="e")
pet_entry = tk.Entry(root, width=30)
pet_entry.grid(row=3, column=1)

tk.Label(root, text="Dates (comma):").grid(row=4, column=0, sticky="e")
dates_entry = tk.Entry(root, width=30)
dates_entry.grid(row=4, column=1)

tk.Label(root, text="Years (e.g. 2018-2025 or 2019,2020):").grid(row=5, column=0, sticky="e")
years_entry = tk.Entry(root, width=30)
years_entry.grid(row=5, column=1)

tk.Button(root, text="Generate Wordlist", command=gen_click).grid(row=6, column=1, pady=10)

root.mainloop()
