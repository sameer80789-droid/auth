#!/usr/bin/env python3
"""
ADVANCED HUMANIZER - Second Pass
Runs AFTER humanize() to clean up what it missed.
- Kills AI clichés
- Varies sentence rhythm
- Removes redundant phrases
- Fixes robotic starts
- Adds natural flow
"""

import re
import random


# ============================================================
# AI CLICHÉ KILLERS (whole phrases -> removed or shortened)
# ============================================================
AI_CLICHES = {
    r"\bit is (important|worth|crucial|essential|vital|necessary) to note that\b": "",
    r"\bit is (important|worth|crucial|essential|vital|necessary) to (mention|remember|consider) that\b": "",
    r"\bit should be noted that\b": "",
    r"\bit should be mentioned that\b": "",
    r"\bit is (widely|generally|commonly) (known|believed|accepted|recognized) that\b": "",
    r"\bit goes without saying that\b": "",
    r"\bneedless to say,?\b": "",
    r"\bin today's (world|day and age|society|landscape)\b": "today",
    r"\bin this day and age\b": "today",
    r"\bin the modern era\b": "today",
    r"\bin recent years\b": "lately",
    r"\bin recent times\b": "lately",
    r"\bwith the advent of\b": "with",
    r"\bwith the dawn of\b": "with",
    r"\bwith the rise of\b": "as",
    r"\bin the realm of\b": "in",
    r"\bin the field of\b": "in",
    r"\bin the world of\b": "in",
    r"\bin the context of\b": "in",
    r"\bin the sphere of\b": "in",
    r"\bin the arena of\b": "in",
    r"\bin the domain of\b": "in",
    r"\bat the end of the day\b": "really",
    r"\bwhen all is said and done\b": "really",
    r"\ball things considered\b": "overall",
    r"\bfor all intents and purposes\b": "basically",
    r"\bthe fact of the matter is( that)?\b": "truth is",
    r"\bthe truth of the matter is( that)?\b": "truth is",
    r"\bwhat's more\b": "also",
    r"\bwhat is more\b": "also",
    r"\bnot only that,? but\b": "also",
    r"\bmore often than not\b": "usually",
    r"\bin the majority of cases\b": "usually",
    r"\bin a (significant|large) number of cases\b": "often",
    r"\bthe vast majority of\b": "almost all",
    r"\ba significant (number|amount|portion) of\b": "many",
    r"\ba considerable (number|amount|portion) of\b": "many",
    r"\ba substantial (number|amount|portion) of\b": "many",
    r"\bplay a (significant|crucial|key|vital|major|critical) role in\b": "matter for",
    r"\bplay an important role in\b": "matter for",
    r"\bshed light on\b": "explain",
    r"\bsheds light on\b": "explains",
    r"\bshedding light on\b": "explaining",
    r"\bpave the way for\b": "set up",
    r"\bpaves the way for\b": "sets up",
    r"\bpaving the way for\b": "setting up",
    r"\bcome to terms with\b": "accept",
    r"\bcomes to terms with\b": "accepts",
    r"\btake into account\b": "consider",
    r"\btakes into account\b": "considers",
    r"\btaking into account\b": "considering",
    r"\btake into consideration\b": "consider",
    r"\bbear in mind\b": "remember",
    r"\bbears in mind\b": "remembers",
    r"\bkeep in mind\b": "remember",
    r"\bkeeps in mind\b": "remembers",
    r"\bwith that (being )?said\b": "still",
    r"\bthat (being )?said\b": "still",
    r"\bhaving said that\b": "still",
    r"\bthat having been said\b": "still",
    r"\bthis (being )?said\b": "still",
    r"\bwith this in mind\b": "so",
    r"\bwith that in mind\b": "so",
    r"\bin this respect\b": "here",
    r"\bin this regard\b": "here",
    r"\bin this sense\b": "here",
    r"\bin this vein\b": "here",
    r"\balong these lines\b": "similarly",
    r"\bin a similar vein\b": "similarly",
    r"\bin much the same way\b": "similarly",
    r"\bby the same token\b": "similarly",
    r"\bin like manner\b": "similarly",
    r"\bin the same manner\b": "similarly",
    r"\bconversely,?\b": "on the flip side",
    r"\boppositely,?\b": "on the flip side",
    r"\bby way of contrast\b": "in contrast",
    r"\bby way of comparison\b": "compared",
    r"\bin stark contrast\b": "very differently",
    r"\bin direct contrast\b": "very differently",
    r"\bas opposed to\b": "unlike",
    r"\bas distinct from\b": "unlike",
    r"\bas compared to\b": "compared to",
    r"\bvis-à-vis\b": "about", r"\bvis-a-vis\b": "about",
}


# ============================================================
# REDUNDANT PAIRS (trim the weaker word)
# ============================================================
REDUNDANT = {
    r"\bvery unique\b": "unique",
    r"\breally unique\b": "unique",
    r"\bvery perfect\b": "perfect",
    r"\bcompletely perfect\b": "perfect",
    r"\bcompletely (destroy|destroyed|eliminate|eliminated)\b": r"\1",
    r"\btotally (destroy|destroyed|eliminate|eliminated)\b": r"\1",
    r"\bvery (essential|necessary|vital|crucial)\b": r"\1",
    r"\babsolutely (essential|necessary|vital|crucial)\b": r"\1",
    r"\bbasic fundamentals\b": "fundamentals",
    r"\bfinal outcome\b": "outcome",
    r"\bfinal result\b": "result",
    r"\bend result\b": "result",
    r"\bpast history\b": "history",
    r"\bfuture plans\b": "plans",
    r"\badvance planning\b": "planning",
    r"\badvance warning\b": "warning",
    r"\bclose proximity\b": "closeness",
    r"\bmutual cooperation\b": "cooperation",
    r"\bnew innovation\b": "innovation",
    r"\bnew invention\b": "invention",
    r"\barmed gunman\b": "gunman",
    r"\bfree gift\b": "gift",
    r"\badded bonus\b": "bonus",
    r"\beach and every\b": "every",
    r"\bfirst and foremost\b": "first",
    r"\bvarious different\b": "different",
    r"\bgeneral consensus\b": "consensus",
    r"\bsudden impulse\b": "impulse",
    r"\bunexpected surprise\b": "surprise",
    r"\bcompletely (surrounded|filled|covered)\b": r"\1",
    r"\bvery (large|big|small|tiny)\b": r"\1",
    r"\bvery (good|bad|nice|great)\b": r"\1",
    r"\breally (good|bad|nice|great)\b": r"\1",
    r"\bquite (good|bad|nice|great)\b": r"\1",
    r"\b(extremely|incredibly|amazingly|remarkably) (good|bad|nice|great|large|big|small)\b": r"\1",
    r"\bkind of (like|similar)\b": "like",
    r"\bsort of (like|similar)\b": "like",
    r"\ba bit (like|similar)\b": "like",
    r"\ba little (like|similar)\b": "like",
    r"\bcompletely (different|unique|new|separate)\b": r"\1",
    r"\btotally (different|unique|new|separate)\b": r"\1",
    r"\bfully (complete|finished|done)\b": r"\1",
    r"\bentirely (complete|finished|done)\b": r"\1",
    r"\bextremely (difficult|hard|easy|simple)\b": r"\1",
    r"\bhighly (unlikely|likely|probable|improbable)\b": r"\1",
    r"\bstrongly (believe|feel|think)\b": r"\1",
    r"\bdeeply (concerned|worried|troubled)\b": r"\1",
    r"\bheavily (criticized|criticised|criticized)\b": r"\1",
    r"\bsharply (criticized|criticised)\b": r"\1",
    r"\bwidely (regarded|considered|known)\b": r"\1",
    r"\bcarefully (consider|examine|study|analyze|review)\b": r"\1",
    r"\bthoroughly (investigate|examine|study|analyze)\b": r"\1",
}


# ============================================================
# ROBOTIC STARTERS TO SHAKE UP
# ============================================================
ROBOTIC_STARTERS = [
    "Additionally,", "Furthermore,", "Moreover,",
    "In addition,", "Similarly,", "Likewise,",
    "Consequently,", "Therefore,", "Thus,",
    "Hence,", "Accordingly,", "Subsequently,",
    "Conversely,", "On the contrary,", "Conversely,",
    "In conclusion,", "In summary,", "To summarize,",
    "In other words,", "That is to say,",
    "It is important to note that", "It should be noted that",
    "It is worth noting that", "Notably,",
    "Importantly,", "Interestingly,", "Significantly,",
    "Ultimately,", "Fundamentally,", "Essentially,",
    "Basically,", "In essence,", "In effect,",
    "In fact,", "Indeed,", "Actually,",
    "In particular,", "Specifically,", "Namely,",
]

# Natural replacements (used randomly)
NATURAL_STARTERS = [
    "Also,", "Plus,", "And", "So", "But", "Now",
    "Still,", "Even so,", "Then again,", "Then,",
    "Meanwhile,", "At the same time,", "On top of that,",
]


# ============================================================
# PASSIVE-ISH PATTERNS (light rewrite)
# ============================================================
PASSIVE_FIXES = {
    r"\b(is|are|was|were|been|being) (used|utilized|employed) (to|for)\b": "helps",
    r"\b(is|are|was|were) (able|capable) (to|of)\b": "can",
    r"\bhas been shown to\b": "shows",
    r"\bhave been shown to\b": "show",
    r"\bit has been (observed|noted|shown|found|demonstrated) that\b": "",
    r"\bit can be (observed|noted|seen|argued) that\b": "",
    r"\bit may be (observed|noted|seen|argued) that\b": "",
    r"\bthere (is|are|was|were) (a|an|the)? ?(number|amount|variety|range) of\b": "",
}


# ============================================================
# HELPERS
# ============================================================
def _preserve_protected(text):
    store = {}
    counter = [0]
    patterns = [
        r'"[^"]*"',
        r"'[^']*'",
        r"\([^)]*\)",
        r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
        r"\b\d{4}\b",
        r"\b[A-Z]{2,}\b",
    ]
    def repl(m):
        key = "__P{}__".format(counter[0])
        counter[0] += 1
        store[key] = m.group(0)
        return key
    for p in patterns:
        text = re.sub(p, repl, text)
    return text, store


def _restore(text, store):
    for k, v in store.items():
        text = text.replace(k, v)
    return text


def _apply_dict(text, mapping):
    for pat, rep in mapping.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


def _strip_robotic_starters(text):
    for starter in ROBOTIC_STARTERS:
        # Match starter at the start of a sentence
        escaped = re.escape(starter.rstrip(","))
        pattern = r"(^|(?<=[.!?])\s+)" + escaped + r",?\s+"
        def repl(m):
            # 60% chance to replace with a natural starter
            if random.random() < 0.6:
                new = random.choice(NATURAL_STARTERS)
                return m.group(1) + new + " "
            return m.group(1)
        text = re.sub(pattern, repl, text)
    return text


def _vary_sentence_rhythm(text):
    """Split sentences longer than 25 words; leave short ones alone."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for s in sentences:
        words = s.split()
        if len(words) >= 25:
            # Find a comma in the middle third
            commas = [m.start() for m in re.finditer(r",", s)]
            if commas:
                mid = len(s) // 2
                best = min(commas, key=lambda c: abs(c - mid))
                if 20 < best < len(s) - 20:
                    first = s[:best].strip().rstrip(",;:") + "."
                    rest = s[best + 1:].strip()
                    if rest:
                        rest = rest[0].upper() + rest[1:]
                        out.append(first)
                        out.append(rest)
                        continue
        out.append(s)
    return " ".join(out)


def _break_and_run_ons(text):
    """Some paragraphs have sentences joined with 'and'. Break the worst ones."""
    # Only break when ' and ' is followed by a subject-ish word and sentence > 22 words
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for s in sentences:
        if len(s.split()) > 22 and " and " in s:
            idx = s.find(" and ")
            # Don't split if it's inside a list
            before = s[:idx]
            after = s[idx + 5:].strip()
            if after and after[0].islower():
                # check if it looks like a clause
                first_word = after.split()[0]
                if first_word not in ("the", "a", "an", "his", "her", "their", "its", "my", "your", "our"):
                    out.append(before.strip().rstrip(",;:") + ".")
                    out.append(after[0].upper() + after[1:])
                    continue
        out.append(s)
    return " ".join(out)


def _trim_double_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text.strip()


# ============================================================
# MAIN ADVANCED FUNCTION
# ============================================================
def advanced_humanize(text):
    if not text or not text.strip():
        return text

    text, store = _preserve_protected(text)

    # 1. Kill AI clichés
    text = _apply_dict(text, AI_CLICHES)

    # 2. Trim redundant pairs
    text = _apply_dict(text, REDUNDANT)

    # 3. Fix passive constructions
    text = _apply_dict(text, PASSIVE_FIXES)

    # 4. Strip robotic sentence starters
    text = _strip_robotic_starters(text)

    # 5. Vary sentence rhythm
    text = _vary_sentence_rhythm(text)

    # 6. Break run-ons
    text = _break_and_run_ons(text)

    # 7. Clean spacing
    text = _trim_double_spaces(text)

    # 8. Capitalize sentence starts
    parts = re.split(r"(?<=[.!?])\s+", text)
    parts = [p[0].upper() + p[1:] if p else p for p in parts]
    text = " ".join(parts)

    text = _restore(text, store)
    return text


# ============================================================
# PIPELINE - combines both passes
# ============================================================
def full_humanize(text):
    """Run base humanizer, then advanced pass."""
    try:
        from humanize import humanize as base_humanize
    except ImportError:
        base_humanize = None

    if base_humanize:
        text = base_humanize(text)

    text = advanced_humanize(text)
    return text
