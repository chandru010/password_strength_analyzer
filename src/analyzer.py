# src/analyzer.py
"""analyzer.py
Provides password strength analysis using zxcvbn plus a simple entropy calculation.
Sanitizes zxcvbn results so they are JSON-serializable (no timedelta objects).
"""
import math
import json
from datetime import timedelta

# Try import zxcvbn; if not available we will still run entropy calculation.
try:
    from zxcvbn import zxcvbn
    ZX_AVAILABLE = True
except Exception:
    ZX_AVAILABLE = False

def shannon_entropy(password: str) -> float:
    """Estimate entropy using Shannon formula (bits)."""
    if not password:
        return 0.0
    freq = {}
    for c in password:
        freq[c] = freq.get(c, 0) + 1
    entropy = 0.0
    length = len(password)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy * length  # bits

def _sanitize(obj):
    """
    Recursively convert objects that json.dumps cannot handle into serializable types:
    - timedelta -> total seconds (float)
    - bytes -> decode to str
    - other unknown objects -> str(obj)
    """
    # primitive types ok
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    if isinstance(obj, bytes):
        try:
            return obj.decode('utf-8', errors='ignore')
        except Exception:
            return str(obj)
    # lists/tuples/sets
    if isinstance(obj, (list, tuple, set)):
        return [_sanitize(x) for x in obj]
    # dicts: sanitize keys and values
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            # try to convert key to string (json requires string keys)
            try:
                ks = str(k)
            except Exception:
                ks = json.dumps(_sanitize(k))
            out[ks] = _sanitize(v)
        return out
    # fallback: try to convert to string
    try:
        return str(obj)
    except Exception:
        return repr(obj)

def analyze(password: str) -> dict:
    """Return analysis combining zxcvbn and entropy, sanitized for JSON."""
    entropy = shannon_entropy(password)
    zx = None
    if ZX_AVAILABLE:
        try:
            raw = zxcvbn(password)
            zx = _sanitize(raw)
        except Exception as e:
            zx = {"error": "zxcvbn error", "detail": str(e)}
    else:
        zx = {"error": "zxcvbn not installed"}

    result = {
        "password": password,
        "entropy_bits": entropy,
        "zxcvbn": zx
    }
    return result

if __name__ == "__main__":
    import sys
    pwd = sys.argv[1] if len(sys.argv) > 1 else input("Enter password: ")
    out = analyze(pwd)
    print(json.dumps(out, indent=2))
