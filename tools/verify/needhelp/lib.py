# -*- coding: utf-8 -*-
"""Simulators used to machine-check the guided courses ("צריך עזרה?").

Everything here is brute force and independent of the course text: DFA / NFA runs, subset construction,
epsilon removal, minimization (Moore), product automata, a regular-expression parser (course syntax:
`+` union, `*` star, juxtaposition = concatenation, `ε`, `∅`, `Σ`), a CFG language enumerator (fixpoint over
strings of bounded length) with leftmost-derivation counting, a PDA runner with the course's acceptance
convention (accepting state AND empty stack), Nerode-class estimation from a membership predicate, and a
pumping-lemma game solver for a fixed constant.

Strings are Python str; the empty string is "".
"""
from itertools import product
from functools import lru_cache
import re

MAXLEN = 8
LOG = {"rx": [], "dfa": [], "nfa": [], "cfg": [], "pda": []}   # every machine built, for the cross-checks in common.py


def words(alpha, n=MAXLEN):
    """all strings over `alpha` of length 0..n, shortest first"""
    out = [""]
    layer = [""]
    for _ in range(n):
        layer = [w + a for w in layer for a in alpha]
        out += layer
    return out


# ----------------------------------------------------------------------------- DFA
class DFA:
    def __init__(self, alpha, delta, start, acc):
        """delta: dict {(state, letter): state} -- must be total over the states it mentions"""
        self.alpha = tuple(alpha)
        self.delta = dict(delta)
        self.start = start
        self.acc = frozenset(acc)
        LOG["dfa"].append(self)
        self.states = {start} | {q for (q, _) in self.delta} | set(self.delta.values()) | set(self.acc)
        for q in self.states:
            for a in self.alpha:
                if (q, a) not in self.delta:
                    raise ValueError(f"DFA is not total: no move from {q!r} on {a!r}")

    def run(self, w):
        q = self.start
        for c in w:
            q = self.delta[(q, c)]
        return q

    def accepts(self, w):
        return self.run(w) in self.acc

    def reachable(self):
        seen, todo = {self.start}, [self.start]
        while todo:
            q = todo.pop()
            for a in self.alpha:
                r = self.delta[(q, a)]
                if r not in seen:
                    seen.add(r); todo.append(r)
        return seen

    def complement(self):
        return DFA(self.alpha, self.delta, self.start, self.states - self.acc)

    def product(self, other, mode):
        """mode: 'and' | 'or' | 'xor' | 'minus'"""
        assert self.alpha == other.alpha
        f = {"and": lambda x, y: x and y, "or": lambda x, y: x or y,
             "xor": lambda x, y: x != y, "minus": lambda x, y: x and not y}[mode]
        delta, acc = {}, set()
        for p in self.states:
            for q in other.states:
                for a in self.alpha:
                    delta[((p, q), a)] = (self.delta[(p, a)], other.delta[(q, a)])
                if f(p in self.acc, q in other.acc):
                    acc.add((p, q))
        return DFA(self.alpha, delta, (self.start, other.start), acc)

    def is_empty(self):
        return not any(q in self.acc for q in self.reachable())

    def equiv(self, other):
        return self.product(other, "xor").is_empty()

    def minimize(self):
        """Moore partition refinement on the reachable part -> a DFA whose states are class numbers"""
        reach = sorted(self.reachable(), key=repr)
        cls = {q: (q in self.acc) for q in reach}
        while True:
            sig = {q: (cls[q],) + tuple(cls[self.delta[(q, a)]] for a in self.alpha) for q in reach}
            names = {}
            new = {}
            for q in reach:
                new[q] = names.setdefault(sig[q], len(names))
            if len(set(new.values())) == len(set(cls.values())):
                cls = new
                break
            cls = new
        delta = {(cls[q], a): cls[self.delta[(q, a)]] for q in reach for a in self.alpha}
        return DFA(self.alpha, delta, cls[self.start], {cls[q] for q in reach if q in self.acc})

    def n_min(self):
        return len(self.minimize().states)

    def lang(self, n=MAXLEN):
        return {w for w in words(self.alpha, n) if self.accepts(w)}


def dfa_table(alpha, rows, start, acc):
    """rows: {state: 'next-on-a next-on-b ...'}  (letters in the order of `alpha`)"""
    delta = {}
    for q, nxt in rows.items():
        for a, r in zip(alpha, nxt.split()):
            delta[(q, a)] = r
    return DFA(alpha, delta, start, acc)


def _is_infinite(self):
    """exact: some reachable state on a cycle can reach an accepting state"""
    R = self.reachable()
    def reach(q):
        seen, todo = {q}, [q]
        while todo:
            x = todo.pop()
            for a in self.alpha:
                y = self.delta[(x, a)]
                if y not in seen:
                    seen.add(y); todo.append(y)
        return seen
    for q in R:
        on_cycle = any(q in reach(self.delta[(q, a)]) for a in self.alpha)
        if on_cycle and any(r in self.acc for r in reach(q)):
            return True
    return False


DFA.is_infinite = _is_infinite


def all_dfas(n, alpha="01", start_fixed=True):
    """every DFA with states 0..n-1, start 0, every transition table and every accepting set"""
    from itertools import product as P
    states = [str(i) for i in range(n)]
    keys = [(q, a) for q in states for a in alpha]
    for tgt in P(states, repeat=len(keys)):
        delta = dict(zip(keys, tgt))
        for mask in range(1 << n):
            d = DFA(alpha, delta, "0", {states[i] for i in range(n) if mask >> i & 1})
            LOG["dfa"].pop()      # exhaustive enumeration is not part of the cross-check log
            yield d


def cyc_dfa(n, f, alpha="ab"):
    """n states 0..n-1 (letter a advances cyclically, the others stay), the first f states accepting"""
    delta = {}
    for i in range(n):
        for k, a in enumerate(alpha):
            delta[(str(i), a)] = str((i + 1) % n) if k == 0 else str(i)
    return DFA(alpha, delta, "0", {str(i) for i in range(f)})


# ----------------------------------------------------------------------------- NFA
class NFA:
    def __init__(self, alpha, delta, start, acc):
        """delta: {(state, letter-or-''): set(states)}; '' is an epsilon move"""
        self.alpha = tuple(alpha)
        self.delta = {k: set(v) for k, v in delta.items()}
        self.start = start
        self.acc = frozenset(acc)
        LOG["nfa"].append(self)
        self.states = {start} | set(self.acc) | {q for (q, _) in self.delta} | {r for v in self.delta.values() for r in v}

    def eclose(self, S):
        S = set(S); todo = list(S)
        while todo:
            q = todo.pop()
            for r in self.delta.get((q, ""), ()):
                if r not in S:
                    S.add(r); todo.append(r)
        return S

    def step(self, S, a):
        out = set()
        for q in self.eclose(S):
            out |= self.delta.get((q, a), set())
        return self.eclose(out)

    def accepts(self, w):
        S = self.eclose({self.start})
        for c in w:
            S = self.step(S, c)
            if not S:
                return False
        return bool(S & self.acc)

    def lang(self, n=MAXLEN):
        return {w for w in words(self.alpha, n) if self.accepts(w)}

    def remove_eps(self):
        """the course algorithm: add accepting states, add edges q -e*-> p -a-> p', delete eps moves and unreachable states"""
        acc = {q for q in self.states if self.eclose({q}) & self.acc}
        delta = {}
        for q in self.states:
            for a in self.alpha:
                t = set()
                for p in self.eclose({q}):
                    t |= self.delta.get((p, a), set())
                if t:
                    delta[(q, a)] = t
        n = NFA(self.alpha, delta, self.start, acc)
        # keep reachable only
        seen, todo = {n.start}, [n.start]
        while todo:
            q = todo.pop()
            for a in n.alpha:
                for r in n.delta.get((q, a), ()):
                    if r not in seen:
                        seen.add(r); todo.append(r)
        d2 = {k: v for k, v in n.delta.items() if k[0] in seen}
        return NFA(n.alpha, d2, n.start, {q for q in n.acc if q in seen})

    def to_dfa(self):
        """subset construction (reachable subsets only); the empty set is the sink and is kept"""
        start = frozenset(self.eclose({self.start}))
        delta, seen, todo = {}, {start}, [start]
        while todo:
            R = todo.pop()
            for a in self.alpha:
                T = frozenset(self.step(R, a))
                delta[(R, a)] = T
                if T not in seen:
                    seen.add(T); todo.append(T)
        return DFA(self.alpha, delta, start, {R for R in seen if R & self.acc})


def nfa_from_edges(alpha, edges, start, acc):
    """edges: list of (p, letter-or-'', q)"""
    d = {}
    for p, a, q in edges:
        d.setdefault((p, a), set()).add(q)
    return NFA(alpha, d, start, acc)


# ----------------------------------------------------------------------------- regular expressions
class Rx:
    """course syntax: letters, ε, ∅, Σ, + (union), * (star), concatenation, parentheses.
    `x?` is NOT course syntax and is rejected."""

    def __init__(self, text, alpha="01"):
        self.text = text.replace(" ", "")
        self.alpha = tuple(alpha)
        self.pos = 0
        LOG["rx"].append(self)
        self.ast = self._union()
        if self.pos != len(self.text):
            raise ValueError(f"bad regex {text!r} at {self.pos}")
        self._dfa = None

    # grammar: union := cat ('+' cat)* ; cat := star+ ; star := atom '*'* ; atom := letter | ε | ∅ | Σ | '(' union ')'
    def _peek(self):
        return self.text[self.pos] if self.pos < len(self.text) else ""

    def _union(self):
        parts = [self._cat()]
        while self._peek() == "+":
            self.pos += 1
            parts.append(self._cat())
        return parts[0] if len(parts) == 1 else ("u", parts)

    def _cat(self):
        parts = []
        while self._peek() and self._peek() not in "+)":
            parts.append(self._star())
        if not parts:
            raise ValueError("empty concatenation in " + self.text)
        return parts[0] if len(parts) == 1 else ("c", parts)

    def _star(self):
        a = self._atom()
        while self._peek() == "*":
            self.pos += 1
            a = ("s", a)
        return a

    def _atom(self):
        c = self._peek()
        if c == "(":
            self.pos += 1
            r = self._union()
            if self._peek() != ")":
                raise ValueError("missing ) in " + self.text)
            self.pos += 1
            return r
        if c in ("ε", "∅"):
            self.pos += 1
            return ("e",) if c == "ε" else ("z",)
        if c == "Σ":
            self.pos += 1
            return ("u", [("l", a) for a in self.alpha])
        if c and (c.isalnum()):
            if c not in self.alpha:
                raise ValueError(f"letter {c!r} is not in the alphabet {self.alpha} ({self.text})")
            self.pos += 1
            return ("l", c)
        raise ValueError(f"bad symbol {c!r} in {self.text}")

    def to_nfa(self):
        cnt = [0]

        def new():
            cnt[0] += 1
            return cnt[0]
        edges = []

        def build(n):
            s, t = new(), new()
            k = n[0]
            if k == "l":
                edges.append((s, n[1], t))
            elif k == "e":
                edges.append((s, "", t))
            elif k == "z":
                pass
            elif k == "u":
                for p in n[1]:
                    a, b = build(p)
                    edges.append((s, "", a)); edges.append((b, "", t))
            elif k == "c":
                cur = s
                for p in n[1]:
                    a, b = build(p)
                    edges.append((cur, "", a)); cur = b
                edges.append((cur, "", t))
            elif k == "s":
                a, b = build(n[1])
                edges.extend([(s, "", a), (b, "", a), (b, "", t), (s, "", t)])
            return s, t
        s, t = build(self.ast)
        return nfa_from_edges(self.alpha, edges, s, {t})

    def dfa(self):
        if self._dfa is None:
            self._dfa = self.to_nfa().to_dfa()
        return self._dfa

    def accepts(self, w):
        return self.dfa().accepts(w)

    def lang(self, n=MAXLEN):
        return self.dfa().lang(n)

    def equiv(self, other):
        return self.dfa().equiv(other.dfa())

    def subset(self, other):
        return self.dfa().product(other.dfa(), "minus").is_empty()


def rx(text, alpha="01"):
    return Rx(text, alpha)


def rx_vs_rx(r1, r2, alpha="01"):
    """'eq' | 'lt' (L1 strictly inside L2) | 'gt' | 'none'"""
    a, b = rx(r1, alpha), rx(r2, alpha)
    ab, ba = a.subset(b), b.subset(a)
    return "eq" if ab and ba else "lt" if ab else "gt" if ba else "none"


# ----------------------------------------------------------------------------- CFG
class CFG:
    """rules: 'S -> aSb | ε ; T -> ...'  (single capital letters are variables, 'ε' = empty)"""

    def __init__(self, text, start="S", alpha=None):
        self.rules = {}
        for part in re.split(r"[;\n]", text):
            part = part.strip()
            if not part:
                continue
            lhs, rhs = part.split("->")
            lhs = lhs.strip()
            for alt in rhs.split("|"):
                alt = alt.strip().replace(" ", "")
                alt = "" if alt in ("ε", "") else alt
                self.rules.setdefault(lhs, []).append(alt)
        self.start = start
        LOG["cfg"].append(self)
        self.vars = set(self.rules)
        self._cache = {}
        for alts in self.rules.values():
            for alt in alts:
                for c in alt:
                    if c.isupper() and c not in self.vars:
                        raise ValueError(f"variable {c!r} has no rule in: {text}")

    def lang_of(self, n=MAXLEN):
        """fixpoint: for each variable, all terminal strings of length <= n it derives"""
        if n in self._cache:
            return self._cache[n]
        L = {v: set() for v in self.vars}
        changed = True
        while changed:
            changed = False
            for v, alts in self.rules.items():
                for alt in alts:
                    cur = {""}
                    for sym in alt:
                        opts = L[sym] if sym in self.vars else {sym}
                        cur = {x + y for x in cur for y in opts if len(x) + len(y) <= n}
                        if not cur:
                            break
                    new = cur - L[v]
                    if new:
                        L[v] |= new
                        changed = True
        self._cache[n] = L
        return L

    def lang(self, n=MAXLEN, var=None):
        return self.lang_of(n)[var or self.start]

    def derives(self, w, var=None):
        return w in self.lang(max(len(w), 1), var)

    def count_trees(self, w, depth=14, limit=3):
        """number of distinct leftmost derivations of w (capped); >=2 means ambiguous on w. Bounded search."""
        results = [0]
        seen = set()

        def go(form, d):
            if results[0] >= limit:
                return
            # prune: terminal prefix must match w
            i = 0
            while i < len(form) and form[i] not in self.vars:
                i += 1
            if not w.startswith(form[:i]):
                return
            if i == len(form):
                if form == w:
                    results[0] += 1
                return
            term = sum(1 for c in form if c not in self.vars)
            if term > len(w) or d > depth:
                return
            A = form[i]
            for alt in self.rules[A]:
                go(form[:i] + alt + form[i + 1:], d + 1)
        go(self.start, 0)
        return results[0]

    def height_of_derivation(self, w):
        raise NotImplementedError


# ----------------------------------------------------------------------------- PDA
class PDA:
    """edges: list of (p, a, pop, q, push) -- a, pop, push are a single symbol or '' (epsilon / nothing).
    Acceptance (course convention): consume the whole input, end in an accepting state, with an EMPTY stack."""

    def __init__(self, edges, start, acc):
        self.edges = edges
        self.start = start
        LOG["pda"].append(self)
        self.acc = frozenset(acc)
        self.by_state = {}
        for e in edges:
            self.by_state.setdefault(e[0], []).append(e)

    def accepts(self, w, max_stack=None, require_empty=True):
        max_stack = max_stack if max_stack is not None else 2 * len(w) + 6
        start = (self.start, 0, "")
        seen, todo = {start}, [start]
        while todo:
            q, i, st = todo.pop()
            if i == len(w) and q in self.acc and (st == "" or not require_empty):
                return True
            for (_, a, pop, r, push) in self.by_state.get(q, ()):
                if a:
                    if i >= len(w) or w[i] != a:
                        continue
                    j = i + 1
                else:
                    j = i
                if pop:
                    if not st or st[-1] != pop:
                        continue
                    ns = st[:-1]
                else:
                    ns = st
                if push:
                    ns = ns + push
                if len(ns) > max_stack:
                    continue
                c = (r, j, ns)
                if c not in seen:
                    seen.add(c); todo.append(c)
        return False

    def lang(self, alpha, n=MAXLEN, **kw):
        return {w for w in words(alpha, n) if self.accepts(w, **kw)}


# ----------------------------------------------------------------------------- Nerode / Rank estimation
def classes(pred, alpha, plen=6, slen=8):
    """partition of all prefixes of length <= plen by their behaviour on all suffixes of length <= slen.
    Returns a list of classes (each a list of strings, shortest first)."""
    suff = words(alpha, slen)
    sig = {}
    for x in words(alpha, plen):
        s = tuple(pred(x + z) for z in suff)
        sig.setdefault(s, []).append(x)
    return list(sig.values())


def rank_est(pred, alpha, plen=6, slen=8):
    return len(classes(pred, alpha, plen, slen))


def rank_stable(pred, alpha, slen=9, plen_range=(4, 5, 6)):
    """Rank estimate that is stable as the prefix length grows (finite Rank), else None"""
    vals = [rank_est(pred, alpha, p, slen) for p in plen_range]
    return vals[-1] if len(set(vals)) == 1 else None


def separable(pred, x, y, alpha, slen=8):
    """a separating suffix z (xz in L xor yz in L), or None"""
    for z in words(alpha, slen):
        if pred(x + z) != pred(y + z):
            return z
    return None


def is_separating_set(pred, T, alpha, slen=8):
    T = list(T)
    return all(separable(pred, T[i], T[j], alpha, slen) is not None for i in range(len(T)) for j in range(i + 1, len(T)))


def max_separating_size(pred, alpha, plen=6, slen=8):
    """largest separating set = number of classes (finite Rank); equals rank_est"""
    return rank_est(pred, alpha, plen, slen)


# ----------------------------------------------------------------------------- pumping lemma (regular) game
def pump_breaks(pred, w, n, ipow=range(0, 7)):
    """True iff for EVERY split w = xyz with y != '' and |xy| <= n there is an i in ipow with x y^i z not in L
    (the prover wins with this word for this constant n)"""
    if not pred(w) or len(w) < n:
        return False
    for a in range(0, n + 1):
        for b in range(a + 1, min(n, len(w)) + 1):
            x, y, z = w[:a], w[a:b], w[b:]
            if all(pred(x + y * i + z) for i in ipow):
                return False
    return True


def pump_word_works(pred, word_of_n, ns=range(2, 8), ipow=range(0, 7)):
    """the word family works for every constant in ns"""
    return all(pump_breaks(pred, word_of_n(n), n, ipow) for n in ns)


def pump_adversary_split(pred, w, n, ipow=range(0, 7)):
    """a split (x, y, z) that survives all pumps, or None"""
    for a in range(0, n + 1):
        for b in range(a + 1, min(n, len(w)) + 1):
            x, y, z = w[:a], w[a:b], w[b:]
            if all(pred(x + y * i + z) for i in ipow):
                return (x, y, z)
    return None


def pump_breaks_cf(pred, w, p, ipow=range(0, 5)):
    """pumping lemma for CFL: every split w = u v x y z with |vxy| <= p and |vy| >= 1 has some i that leaves L"""
    if not pred(w) or len(w) < p:
        return False
    n = len(w)
    for a in range(n + 1):
        for b in range(a, min(n, a + p) + 1):
            for c in range(b, min(n, a + p) + 1):
                for d in range(c, min(n, a + p) + 1):
                    u, v, x, y, z = w[:a], w[a:b], w[b:c], w[c:d], w[d:]
                    if not v and not y:
                        continue
                    if all(pred(u + v * i + x + y * i + z) for i in ipow):
                        return False
    return True


# ----------------------------------------------------------------------------- language predicates (handy)
def eq_lang(pred, S, alpha, n=MAXLEN):
    """pred agrees with the finite set S on all strings up to length n"""
    return all(pred(w) == (w in S) for w in words(alpha, n))


def same_pred(p1, p2, alpha, n=MAXLEN):
    return all(p1(w) == p2(w) for w in words(alpha, n))


def count(w, c):
    return w.count(c)


def is_pal(w):
    return w == w[::-1]


# ----------------------------------------------------------------------------- language classification certificates
def sep_infinite(pred, gen, zs, n=8):
    """the first n words gen(0), gen(1), ... of an infinite family are pairwise separable by some z in zs"""
    T = [gen(k) for k in range(n)]
    return all(any(pred(x + z) != pred(y + z) for z in zs) for i, x in enumerate(T) for y in T[i + 1:])


def rank_growing(pred, alpha, plens=None, slen=None):
    """the number of Nerode classes among prefixes of length <= p keeps growing with p (evidence of Rank = infinity)"""
    big = len(alpha) > 2
    plens = plens or ((2, 3, 4) if big else (3, 5, 7))
    slen = slen or (7 if big else 9)
    vals = [rank_est(pred, alpha, p, slen) for p in plens]
    return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


def classify_cert(pred, alpha, cert, n=9):
    """Verify a classification certificate and return 'finite' | 'reg' | 'cfl' | 'noncfl'.
      ('finite', B)          every word of L has length <= B (checked up to length 12) and L is non-empty
      ('reg', regex)         the regex equals L on all words <= n, exactly DFA-infinite
      ('cfl', grammar)       the grammar equals L on all words <= n, and the Nerode class count keeps growing (not regular)
      ('noncfl', wordfun)    the CFL pumping game is won with wordfun(p) for p = 2, 3, 4 (and L is not regular: classes keep growing)
    Raises AssertionError when the certificate does not check out."""
    kind = cert[0]
    W = words(alpha, n)
    if kind == "finite":
        B = cert[1]
        assert any(pred(w) for w in W), "empty language"
        assert not any(pred(w) for w in words(alpha, 12) if len(w) > B), "a word longer than the bound"
        return "finite"
    if kind == "reg":
        r = rx(cert[1], alpha)
        assert all(pred(w) == r.accepts(w) for w in W), "regex differs from the language: " + cert[1]
        assert r.dfa().is_infinite(), "not infinite"
        return "reg"
    if kind == "cfl":
        g = CFG(cert[1])
        L = g.lang(n)
        assert all(pred(w) == (w in L) for w in W), "grammar differs from the language"
        assert rank_growing(pred, alpha), "classes do not keep growing: maybe regular"
        return "cfl"
    if kind == "noncfl":
        f = cert[1]
        for p in (2, 3, 4):
            assert pump_breaks_cf(pred, f(p), p), f"pumping word fails for p={p}"
        assert rank_growing(pred, alpha), "classes do not keep growing"
        return "noncfl"
    raise ValueError(kind)


CLASS_LABELS = [("finite", "סופית"), ("reg", "רגולרית ואינסופית"), ("cfl", "חסרת הקשר ולא רגולרית"), ("noncfl", "לא חסרת הקשר")]
