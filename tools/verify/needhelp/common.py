# -*- coding: utf-8 -*-
"""Shared machinery of tools/verify/needhelp/<course>/check.py.

run(course) does three things:
  1. imports every level module of the course (tools/needhelp/<course>/<ID>.py). Importing IS the first check: every
     option of every question was computed by a simulator and nh.Q refuses to build unless exactly one option is true;
     the asserts inside the level files check the lesson's worked examples the same way.
  2. cross-validates the simulators that were used, against independent implementations, on all words up to length 6-8:
       regular expressions  vs Python's `re`
       NFA runs             vs subset construction and vs epsilon removal
       DFAs                 minimization keeps the language; Moore classes equal the Nerode-class estimate
       CFGs                 string fixpoint vs leftmost-derivation search
       PDAs                 configuration BFS vs an independent recursive search
  3. prints the statistics (own / bank questions, simulator-computed vs judged options).
"""
import importlib.util, pathlib, re, sys
from functools import lru_cache

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "needhelp"))
sys.path.insert(0, str(HERE))
import nh                      # noqa: E402
from lib import *              # noqa: E402,F401,F403
import lib                     # noqa: E402

PREFIX = {"fa": "F", "nerode": "N", "classify": "K", "cf": "G"}


def load_levels(course):
    out = []
    for f in sorted((ROOT / "tools" / "needhelp" / course).glob(PREFIX[course] + "[0-9][0-9].py")):
        spec = importlib.util.spec_from_file_location(f"chk_{course}_{f.stem}", f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        out.append(m.LEVEL)
    return out


def py_regex(r, alpha):
    out = []
    for c in r.text:
        out.append({"+": "|", "ε": "", "∅": "(?!)", "Σ": "[" + "".join(alpha) + "]"}.get(c, c))
    return "".join(out)


def check_rx():
    n = 0
    for r in list(lib.LOG["rx"]):
        pat = re.compile(py_regex(r, r.alpha))
        for w in words(r.alpha, 8):
            assert bool(pat.fullmatch(w)) == r.accepts(w), f"regex {r.text!r} differs from re on {w!r}"
        n += 1
    return n


def check_nfa():
    n = 0
    for a in list(lib.LOG["nfa"]):
        d, e = a.to_dfa(), a.remove_eps()
        for w in words(a.alpha, 7):
            assert a.accepts(w) == d.accepts(w) == e.accepts(w), f"NFA subset/epsilon-removal differs on {w!r}"
        n += 1
    return n


def check_dfa():
    """minimization keeps the language (every logged DFA with <= 40 states); for the small ones the Moore class
    count must equal the Nerode-class estimate (first 40 DFAs with <= 5 minimal states)"""
    n = est_n = 0
    for d in list(lib.LOG["dfa"]):
        if len(d.states) > 40:
            continue
        m = d.minimize()
        for w in words(d.alpha, 6):
            assert d.accepts(w) == m.accepts(w)
        k = len(m.states)
        if k <= 5 and est_n < 40 and len(d.alpha) <= 2:
            est = rank_est(d.accepts, d.alpha, 6, 8)
            assert est == k, f"Moore says {k} states, Nerode estimate {est}"
            est_n += 1
        n += 1
    return n


def derive_search(g, N, cap=300000):
    """independent: all terminal words of length <= N by exploring sentential forms (None when the search is too big)"""
    seen, todo, out = set(), [g.start], set()
    seen.add(g.start)
    while todo:
        f = todo.pop()
        i = next((k for k, c in enumerate(f) if c in g.vars), None)
        if i is None:
            if len(f) <= N:
                out.add(f)
            continue
        for alt in g.rules[f[i]]:
            nf = f[:i] + alt + f[i + 1:]
            if sum(1 for c in nf if c not in g.vars) > N or len(nf) > N + 4:
                continue
            if nf not in seen:
                seen.add(nf); todo.append(nf)
                if len(seen) > cap:
                    return None
    return out


def check_cfg():
    n = skipped = 0
    for g in list(lib.LOG["cfg"]):
        N = 5
        s = derive_search(g, N)
        if s is None:
            skipped += 1
            continue
        assert {w for w in g.lang(N) if len(w) <= N} == s, f"CFG fixpoint differs from derivation search: {g.rules}"
        n += 1
    return n, skipped


def pda_accepts_indep(p, w):
    cap = 2 * len(w) + 6
    seen = set()

    def go(q, i, st):
        key = (q, i, st)
        if key in seen:
            return False
        seen.add(key)
        if i == len(w) and q in p.acc and not st:
            return True
        for (a, rd, pop, b, push) in p.edges:
            if a != q:
                continue
            j = i
            if rd:
                if i >= len(w) or w[i] != rd:
                    continue
                j = i + 1
            s2 = st
            if pop:
                if not s2 or s2[-1] != pop:
                    continue
                s2 = s2[:-1]
            if push:
                s2 = s2 + (push,)
            if len(s2) > cap:
                continue
            if go(b, j, s2):
                return True
        return False
    import sys as _s
    _s.setrecursionlimit(10000)
    return go(p.start, 0, ())


def check_pda():
    n = 0
    for p in list(lib.LOG["pda"]):
        alpha = sorted({e[1] for e in p.edges if e[1]})
        for w in words(alpha, 6):
            assert p.accepts(w) == pda_accepts_indep(p, w), f"PDA runners differ on {w!r}"
        n += 1
    return n


def run(course):
    levels = load_levels(course)
    own = bank = sim = judged = 0
    for L in levels:
        for q in L.questions:
            if isinstance(q, nh.Bank):
                bank += 1
            else:
                own += 1
                for o in q.opts:
                    sim += o.kind == "sim"
                    judged += o.kind == "judged"
    print(f"{course}: {len(levels)} levels, {own} own questions + {bank} bank questions; "
          f"{sim} simulator-computed options, {judged} judged options (exactly one true option per question: enforced at import)")
    print(f"  cross-checks vs independent implementations: regexes vs re: {check_rx()}, NFAs: {check_nfa()}, DFAs: {check_dfa()}, "
          f"CFGs: {check_cfg()} (checked, skipped), PDAs: {check_pda()}")
    print(f"{course}: ALL CHECKS PASSED")
