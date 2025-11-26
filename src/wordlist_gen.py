"""wordlist_gen.py
Generate custom wordlists from user-provided tokens with common variations.
"""
from utils import unique_preserve_order, year_range
import itertools

# Common leet substitutions
LEET_MAP = {
    'a': ['@','4'],
    'b': ['8'],
    'e': ['3'],
    'i': ['1','!','|'],
    'l': ['1','|'],
    'o': ['0'],
    's': ['5','$'],
    't': ['7'],
}

COMMON_YEARS = [str(y) for y in range(1980, 2031)]

def apply_leet(token):
    """Return a set of leet variations for token (simple, not exhaustive)."""
    variations = set()
    variations.add(token)
    lower = token.lower()
    # single-char substitutions
    for i, ch in enumerate(lower):
        if ch in LEET_MAP:
            for sub in LEET_MAP[ch]:
                v = lower[:i] + sub + lower[i+1:]
                variations.add(v)
    # add case variations
    variations.update({token.lower(), token.upper(), token.capitalize()})
    return variations

def generate_tokens(name=None, pet=None, dates=None, extras=None, years=None, max_tokens=5000):
    tokens = []
    base = []
    if name:
        base.append(name)
    if pet:
        base.append(pet)
    if dates:
        base.extend([d for d in dates])
    if extras:
        base.extend(extras)
    # include individual words split by non-alpha
    split_words = []
    for b in base:
        split_words.extend([''.join(filter(str.isalnum, part)) for part in b.replace('_',' ').split() if part])
    if not split_words:
        split_words = ['password','admin','user']
    # apply leet and simple transforms
    variants = set()
    for s in split_words:
        variants.update(apply_leet(s))
    # append years
    years_list = years if years else COMMON_YEARS
    # combine pairs and singles
    candidates = set()
    for v in variants:
        candidates.add(v)
        for y in years_list:
            candidates.add(v + y)
            candidates.add(y + v)
    # combine pairs
    for a,b in itertools.permutations(list(variants), 2):
        candidates.add(a + b)
    # limit size
    final = unique_preserve_order(list(candidates))
    return final[:max_tokens]

def save_wordlist(list_tokens, path):
    with open(path, 'w', encoding='utf-8') as f:
        for t in list_tokens:
            f.write(t + "\\n")
    return path

if __name__ == "__main__":
    # quick demo
    wl = generate_tokens(name="Alice", pet="Rex", dates=["1990"], years=["2018","2019"], max_tokens=500)
    save_wordlist(wl, "examples/sample_wordlist.txt")
    print("Sample wordlist written to examples/sample_wordlist.txt")
