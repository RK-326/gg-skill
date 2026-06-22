# -*- coding: utf-8 -*-
"""
Fact-check a list of claims via the Perplexity API and save sources to JSON.

Usage:
    export PPLX_API_KEY=pplx-xxxxxxxx        # never commit the key
    python3 factcheck_perplexity.py

The API key is read from the PPLX_API_KEY environment variable, or from a local
.env file in the repo root (gitignored, never pushed). It is not committed.
Output (verdict + summary + top-3 source URLs per claim) is saved to OUT as JSON,
which you then turn into per-claim footnotes in the document (see build_docx.py).
"""
import os, json, re, time, urllib.request

def _load_dotenv():
    """Load KEY=VALUE pairs from a local .env (repo root or cwd). Gitignored, never committed."""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.join(here, "..", ".env"), os.path.join(here, ".env"), ".env"):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                line = line[7:] if line.startswith("export ") else line
                if "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            break

_load_dotenv()
KEY = os.environ.get("PPLX_API_KEY")
if not KEY:
    raise SystemExit("Set PPLX_API_KEY (env var or a local .env file) first.")

OUT = os.environ.get("FACTCHECK_OUT", "factcheck_perplexity.json")

# (id, short human label, the question to verify)
CLAIMS = [
    ("example_claim", "пример", "Is the CSS Profile financial aid application open on October 1 each cycle?"),
    # add your claims here ...
]

# Domains we trust most, ranked first when picking the 3 sources to keep.
PRIORITY = ("collegeboard", "satsuite", "cssprofile", "commonapp", "studentaid.gov",
            "wes.org", "ets.org", "ielts.org", "duolingo", ".gov", ".edu", "bigfuture")

def rank(url):
    u = url.lower()
    for i, p in enumerate(PRIORITY):
        if p in u:
            return i
    return len(PRIORITY)

def ask(question):
    body = json.dumps({
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Careful fact-checker. Prefer official primary "
             "sources (.edu, .gov, College Board, Common App, ETS, IELTS, CSS Profile). "
             "Answer in 2 sentences max: start with TRUE / PARTLY TRUE / FALSE, then why."},
            {"role": "user", "content": question},
        ],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request(
        "https://api.perplexity.ai/chat/completions", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)

def main():
    results = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    tokens = 0
    for cid, label, q in CLAIMS:
        if cid in results and "sources" in results[cid]:
            print("skip (already done):", cid); continue
        try:
            res = ask(q)
            content = res["choices"][0]["message"]["content"].strip()
            cites = res.get("citations") or [s.get("url") for s in res.get("search_results", [])]
            cites = [c for c in cites if c]
            top3 = sorted(dict.fromkeys(cites), key=rank)[:3]
            tokens += res.get("usage", {}).get("total_tokens", 0)
            v = re.match(r"\**\s*(TRUE|PARTLY TRUE|FALSE)", content, re.I)
            results[cid] = {"label": label,
                            "verdict": v.group(1).upper() if v else "?",
                            "summary": content, "sources": top3, "all_citations": cites}
            print(f"[{results[cid]['verdict']:11}] {label}")
        except Exception as e:
            print("ERROR", cid, e)
        time.sleep(1)
    json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("Saved:", OUT, "| approx tokens:", tokens)

if __name__ == "__main__":
    main()
