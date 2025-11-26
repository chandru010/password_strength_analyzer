# utils.py - helper functions
import itertools

def unique_preserve_order(seq):
    seen = set()
    out = []
    for s in seq:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

def year_range(start, end):
    return [str(y) for y in range(int(start), int(end)+1)]
