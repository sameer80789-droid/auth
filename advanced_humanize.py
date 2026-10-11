import re
import random

# ============================================================
# ACADEMIC FLUFF KILLER
# Targets the exact phrases in your highlights
# ============================================================
ACADEMIC_FLUFF = {
    r"\bThe rapid proliferation of\b": "The fast growth of",
    r"\bhas basically altered\b": "has changed",
    r"\bshow an uncanny ability to\b": "are very good at",
    r"\bremains poorly understood\b": "is still a mystery",
    r"\bsits at the intersection of\b": "mixes",
    r"\bintersection of several disciplines\b": "mix of different fields",
    r"\bRecent real-world research has begun to map this terrain\b": "Recent studies are starting to show this",
    r"\bThese models are trained on vast corpora of\b": "These models learn from huge amounts of",
    r"\bdrawing on existing real-world studies\b": "using real-world studies",
    r"\bthe theoretical framework combines insights from\b": "the theory pulls from",
    r"\bfocusing on three dimensions:\b": "It looks at three things:",
    r"\bThis chapter sets up the background of the study, articulates the research problem, outlines the goals and research questions, discusses the significance of the study and delimits its\b": "This chapter covers the background. It explains the problem, the goals, and the research questions. It also talks about why this study matters and what it doesn't cover.",
    r"\boffers teaching-related implications for teaching literature in the age of AI\b": "shows what this means for teaching literature in the age of AI",
    r"\bwhat's the nature of the fine-tuning vulnerability and what does it reveal about the stability of LLM literary memory\b": "What is this fine-tuning problem? And what does it say about how stable LLM literary memory really is",
    r"\bWhat are the implications of these findings for\b": "So what does this mean for",
    r"\bFrequency refers to how often a given text or\b": "Frequency is how often a text or",
    r"\bAnd kind of, it encodes patterns\b": "It also encodes patterns",
    r"\bSo studies have shown that\b": "Studies show that",
    r"\blike, Llama 3.1 70B has been found to\b": "For example, Llama 3.1 70B can",
    r"\bThis selectivity isn't random. Also, it follows a logic that this study seeks to uncover\b": "This selectivity isn't random. It follows a logic this study wants to uncover.",
    r"\bthe boundary between\b": "the line between",
    r"\bbecomes dangerously blurred\b": "gets very blurry",
    r"\bthe relationship between human readers and literary texts\b": "how humans read books",
    r"\bYet the nature of their\b": "But how they handle",
    r"\bof literature remains poorly understood\b": "of books is still a mystery",
}

# ============================================================
# AI CLICHÉ KILLERS
# ============================================================
AI_CLICHES = {
    r"\bit is (important|worth|crucial|essential|vital|necessary) to note that\b": "",
    r"\bit should be noted that\b": "",
    r"\bit should be mentioned that\b": "",
    r"\bit is (widely|generally|commonly) (known|believed|accepted|recognized) that\b": "",
    r"\bit goes without saying that\b": "",
    r"\bneedless to say,?\b": "",
    r"\bin today's (world|day and age|society|landscape)\b": "today",
    r"\bin this day and age\b": "today",
    r"\bwith the advent of\b": "with",
    r"\bin the realm of\b": "in",
    r"\bin the field of\b": "in",
    r"\bin the context of\b": "in",
    r"\bat the end of the day\b": "really",
    r"\bwhen all is said and done\b": "really",
    r"\ball things considered\b": "overall",
    r"\bfor all intents and purposes\b": "basically",
    r"\bthe fact of the matter is( that)?\b": "truth is",
    r"\bwhat's more\b": "also",
    r"\bmore often than not\b": "usually",
    r"\bin the majority of cases\b": "usually",
    r"\bthe vast majority of\b": "almost all",
    r"\ba significant (number|amount|portion) of\b": "many",
    r"\bplay a (significant|crucial|key|vital|major|critical) role in\b": "matter for",
    r"\bshed light on\b": "explain",
    r"\bpave the way for\b": "set up",
    r"\bcome to terms with\b": "accept",
    r"\btake into account\b": "consider",
    r"\bbear in mind\b": "remember",
    r"\bwith that (being )?said\b": "still",
    r"\bthat (being )?said\b": "still",
    r"\bhaving said that\b": "still",
    r"\bwith this in mind\b": "so",
    r"\bin this respect\b": "here",
    r"\bin this regard\b": "here",
    r"\bconversely,?\b": "on the flip side",
    r"\bas opposed to\b": "unlike",
    r"\bvis-à-vis\b": "about",
}

# ============================================================
# REDUNDANT PAIRS
# ============================================================
REDUNDANT = {
    r"\bvery unique\b": "unique",
    r"\bcompletely (destroy|destroyed|eliminate|eliminated)\b": r"\1",
    r"\bvery (essential|necessary|vital|crucial)\b": r"\1",
    r"\bbasic fundamentals\b": "fundamentals",
    r"\bfinal outcome\b": "outcome",
    r"\bfinal result\b": "result",
    r"\bpast history\b": "history",
    r"\bclose proximity\b": "closeness",
    r"\bnew innovation\b": "innovation",
    r"\beach and every\b": "every",
    r"\bfirst and foremost\b": "first",
    r"\bvarious different\b": "different",
    r"\bgeneral consensus\b": "consensus",
    r"\bvery (large|big|small|tiny)\b": r"\1",
    r"\bvery (good|bad|nice|great)\b": r"\1",
    r"\bquite (good|bad|nice|great)\b": r"\1",
    r"\b(extremely|incredibly|amazingly|remarkably) (good|bad|nice|great|large|big|small)\b": r"\1",
    r"\bkind of (like|similar)\b": "like",
    r"\bcompletely (different|unique|new|separate)\b": r"\1",
    r"\bhighly (unlikely|likely|probable|improbable)\b": r"\1",
    r"\bstrongly (believe|feel|think)\b": r"\1",
    r"\bcarefully (consider|examine|study|analyze|review)\b": r"\1",
}

# ============================================================
# ROBOTIC STARTERS
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

NATURAL_STARTERS = [
    "Also,", "Plus,", "And", "So", "But", "Now",
    "Still,", "Even so,", "Then again,", "Then,",
    "Meanwhile,", "At the same time,", "On top of that,",
]

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
        r"__P\d+__",  # Protect placeholders like __P1__
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
        escaped = re.escape(starter.rstrip(","))
        pattern = r"(^|(?<=[.!?])\s+)" + escaped + r",?\s+"
        def repl(m):
            if random.random() < 0.6:
                new = random.choice(NATURAL_STARTERS)
                return m.group(1) + new + " "
            return m.group(1)
        text = re.sub(pattern, repl, text)
    return text

def _vary_sentence_rhythm(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for s in sentences:
        words = s.split()
        if len(words) >= 25:
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
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for s in sentences:
        if len(s.split()) > 22 and " and " in s:
            idx = s.find(" and ")
            before = s[:idx]
            after = s[idx + 5:].strip()
            if after and after[0].islower():
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

    # 1. Kill academic fluff (the highlighted parts!)
    text = _apply_dict(text, ACADEMIC_FLUFF)

    # 2. Kill AI clichés
    text = _apply_dict(text, AI_CLICHES)

    # 3. Trim redundant pairs
    text = _apply_dict(text, REDUNDANT)

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
