"""cli.py - command line interface"""
import argparse
from analyzer import analyze
from wordlist_gen import generate_tokens, save_wordlist

def cmd_analyze(args):
    res = analyze(args.password)
    import json
    print(json.dumps(res, indent=2))

def cmd_gen(args):
    years = None
    if args.years:
        if '-' in args.years:
            s,e = args.years.split('-',1)
            years = [str(y) for y in range(int(s), int(e)+1)]
        else:
            years = [y.strip() for y in args.years.split(',') if y.strip()]
    dates = [d.strip() for d in args.dates.split(',')] if args.dates else None
    extras = [e.strip() for e in args.extras.split(',')] if args.extras else None
    wl = generate_tokens(name=args.name, pet=args.pet, dates=dates, extras=extras, years=years, max_tokens=args.max)
    out = save_wordlist(wl, args.out)
    print(f"Wrote {len(wl)} candidates to {out}")

def main():
    p = argparse.ArgumentParser(prog="PasswordTool", description="Password Analyzer and Wordlist Generator")
    sub = p.add_subparsers(dest='cmd')

    a = sub.add_parser('analyze', help='Analyze a password')
    a.add_argument('--password', '-p', required=True)

    g = sub.add_parser('gen', help='Generate custom wordlist')
    g.add_argument('--name', type=str, help='Name or username')
    g.add_argument('--pet', type=str, help='Pet name')
    g.add_argument('--dates', type=str, help='Comma separated dates e.g. 1990,12-05-2005')
    g.add_argument('--extras', type=str, help='Comma separated extra tokens')
    g.add_argument('--years', type=str, help='Years e.g. 2018-2025 or 2018,2019')
    g.add_argument('--max', type=int, default=2000, help='Maximum candidates')
    g.add_argument('--out', type=str, default='wordlist.txt', help='Output file path')

    args = p.parse_args()
    if args.cmd == 'analyze':
        cmd_analyze(args)
    elif args.cmd == 'gen':
        cmd_gen(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
