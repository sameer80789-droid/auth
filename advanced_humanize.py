#!/usr/bin/env python3
"""
ULTIMATE HUMANIZER v4
Offline. No API. No dependencies. Single file.

Rewrites stiff, formal or AI-sounding prose into plainer, more natural wording
without changing what it says.

What's new compared with the old versions
  * One-pass, case-preserving replacement: no cascades, no lost capitals,
    "Moreover," -> "Also," instead of "also,".
  * Placeholders can never leak into the output again (private-use characters,
    nested protection resolved correctly, single quotes vs apostrophes handled).
  * Only swaps that keep the meaning and the grammar. Words like "report",
    "religion", "position", "version", "knowledge" are no longer rewritten.
  * Contractions that would be wrong are skipped ("I know what it is.",
    "We had dinner.", "I have a dog.").
  * a/an is re-checked after every swap ("an good" can't happen).
  * Semicolon / long-sentence splitting only where both halves are real clauses.
  * Strength levels:  --level light | medium | strong
  * Meaning guard: warns if numbers, quotes or negations changed.
  * Protects URLs, e-mails, `code`, [1] citations, quotes, (brackets),
    Names, years and ACRONYMS, plus anything you pass with --keep.
  * Handles bullet lists, headings and paragraph breaks.

Usage
  python ultimate_humanizer.py                        # paste text, type END
  python ultimate_humanizer.py in.txt                 # -> in.humanized.txt
  python ultimate_humanizer.py in.txt -o out.txt --level strong --seed 7
  python ultimate_humanizer.py in.txt --report --diff
  type in.txt | python ultimate_humanizer.py -o -     # stdin -> stdout
"""

import argparse
import difflib
import random
import re
import sys
from collections import Counter
from pathlib import Path

STATS = Counter()

PUA_OPEN, PUA_CLOSE = "", ""
_DIGIT_BASE = 0xE100

_L = r"(?<![\w-])"
_R = r"(?![\w-])"


# ============================================================
# 0. HELPERS
# ============================================================
def match_case(src, rep):
    """Give `rep` the capitalisation of the text it replaces."""
    if not rep:
        return rep
    if len(src) > 1 and src.isupper():
        return rep.upper()
    if src[0].isupper():
        return rep[0].upper() + rep[1:]
    return rep


def expand(table):
    """
    {"a/b/c": "x/y/z"} -> {"a": "x", "b": "y", "c": "z"}.
    One replacement is reused for every key. Keys containing "iz" also get
    their British "is" spelling (utilization -> utilisation).
    """
    out = {}
    for olds, news in table.items():
        o = [x.strip().lower() for x in olds.split("/")]
        n = [x.strip() for x in news.split("/")]
        if len(n) == 1:
            n = n * len(o)
        if len(o) != len(n):
            raise ValueError(f"form count mismatch: {olds!r} -> {news!r}")
        for a, b in zip(o, n):
            out[a] = b
            if "iz" in a:
                out[a.replace("iz", "is")] = b
    return out


def _phrase_rx(key):
    return r"\s+".join(re.escape(w) for w in key.split())


def make_sub(mapping, tail="", stat="words"):
    """One regex pass; longest phrase wins; replacement text is never re-scanned."""
    keys = sorted(mapping, key=len, reverse=True)
    rx = re.compile(_L + "(?:" + "|".join(_phrase_rx(k) for k in keys) + ")" + _R + tail,
                    re.IGNORECASE)

    def sub(text):
        def repl(m):
            matched = m.group(0)
            STATS[stat] += 1
            return match_case(matched, mapping[re.sub(r"\s+", " ", matched.lower())])
        return rx.sub(repl, text)

    return sub


def make_rules(rules, stat):
    """Regex rules: (pattern, replacement-with-\\1-groups). Case follows the match."""
    comp = [(re.compile(_L + "(?:" + p + ")" + _R, re.IGNORECASE), r) for p, r in rules]

    def sub(text):
        for rx, rep in comp:
            def repl(m, rep=rep):
                STATS[stat] += 1
                return match_case(m.group(0), m.expand(rep))
            text = rx.sub(repl, text)
        return text

    return sub


# ============================================================
# 1. CONTRACTIONS
# ============================================================
NEGATIONS = {
    "do not": "don't", "does not": "doesn't", "did not": "didn't",
    "is not": "isn't", "are not": "aren't", "was not": "wasn't",
    "were not": "weren't", "have not": "haven't", "has not": "hasn't",
    "had not": "hadn't", "will not": "won't", "would not": "wouldn't",
    "cannot": "can't", "could not": "couldn't", "should not": "shouldn't",
    "must not": "mustn't", "shall not": "shan't",
}

# "it is" -> "it's" only when something follows: "I know what it is." stays.
_NOT_CLAUSE_END = r"(?!\s*(?:[.,;:!?)\]\"'’”]|$|))"

PRONOUN_AUX = {
    "i am": "I'm", "you are": "you're", "we are": "we're", "they are": "they're",
    "he is": "he's", "she is": "she's", "it is": "it's", "that is": "that's",
    "there is": "there's", "here is": "here's", "what is": "what's",
    "who is": "who's", "where is": "where's", "how is": "how's",
    "i will": "I'll", "you will": "you'll", "he will": "he'll", "she will": "she'll",
    "it will": "it'll", "we will": "we'll", "they will": "they'll",
    "there will": "there'll", "that will": "that'll",
    "i would": "I'd", "you would": "you'd", "he would": "he'd", "she would": "she'd",
    "it would": "it'd", "we would": "we'd", "they would": "they'd",
}

# "I have been" -> "I've been", never "I have a dog" -> "I've a dog".
HAVE_AUX = {"i have": "I've", "you have": "you've", "we have": "we've", "they have": "they've"}
_HAVE_TAIL = r"(?=\s+(?:been|always|never|already|ever|just)\b)"

# Deliberately never contracted: "I had", "he has", "it has" (main verbs),
# "this is", "these are", "there are" (non-standard).

CONTRACTION_SUBS = [
    make_sub(NEGATIONS, stat="contractions"),
    make_sub(PRONOUN_AUX, _NOT_CLAUSE_END, stat="contractions"),
    make_sub(HAVE_AUX, _HAVE_TAIL, stat="contractions"),
    make_sub({"let us": "let's"}, r"(?!\s+know\b)" + _NOT_CLAUSE_END, stat="contractions"),
]

# ============================================================
# 2. SENTENCE OPENERS (robotic starters -> natural ones)
# ============================================================
_ADD = ["Also,", "Plus,", "On top of that,"]

_OPENER_SPECS = [
    (r"however,\s*", lambda: "But "),
    (r"(?:additionally|furthermore|moreover|in addition),\s*",
     lambda: random.choice(_ADD) + " "),
    (r"(?:consequently|therefore|thus|hence|accordingly|as a result|for this reason),\s*",
     lambda: "So "),
    (r"(?:similarly|likewise),\s*", lambda: "In the same way, "),
    (r"conversely,\s*", lambda: "On the flip side, "),
    (r"(?:in conclusion|in summary|to summari[sz]e|to conclude|to sum up),\s*",
     lambda: "To wrap up, "),
    (r"ultimately,\s*", lambda: "In the end, "),
    (r"(?:notably|importantly|interestingly|significantly|fundamentally|essentially|"
     r"basically|in essence|indeed),\s*", lambda: ""),
    (r"(?:with that being said|that being said|with that said|that said|"
     r"having said that|that having been said),\s*", lambda: "Still, "),
    (r"with (?:this|that) in mind,\s*", lambda: "So "),
    (r"it is (?:clear|evident|apparent|obvious) that\s+", lambda: "Clearly, "),
    (r"it is possible that\s+", lambda: "Maybe "),
    (r"it is likely that\s+", lambda: "Probably "),
    (r"it is (?:necessary|essential|important|crucial|vital) to\s+", lambda: "We need to "),
]
_OPENERS = [(re.compile(r"^(\W*)(?:" + p + ")", re.IGNORECASE), fn) for p, fn in _OPENER_SPECS]


def apply_openers(s):
    for rx, fn in _OPENERS:
        m = rx.match(s)
        if m:
            STATS["openers"] += 1
            return m.group(1) + fn() + s[m.end():]
    return s


# ============================================================
# 3. AI CLICHES (regex)  - empty replacement = just drop the filler
# ============================================================
CLICHES_SUB = make_rules([
    (r"it (?:is|was) (?:important|worth|crucial|essential|vital|necessary|useful) to "
     r"(?:note|mention|remember|emphasi[sz]e|stress|highlight) that", ""),
    (r"it (?:should|must|can) be (?:noted|mentioned|emphasi[sz]ed|stressed|highlighted) that", ""),
    (r"it is (?:worth|interesting|noteworthy) (?:noting|mentioning|to note|to mention) that", ""),
    (r"it (?:goes|went) without saying that", ""),
    (r"it (?:has been|can be|may be|could be|is|was) (?:observed|noted|seen) that", ""),
    (r"needless to say,?", ""),
    (r"in today[’']s (?:world|day and age|society|landscape|fast-paced world)", "today"),
    (r"in this day and age", "today"),
    (r"in the modern (?:era|age|world)", "today"),
    (r"in recent (?:years|times|decades)", "lately"),
    (r"with the advent of", "with"),
    (r"in the (?:realm|field|world|sphere|arena|domain) of", "in"),
    (r"at the end of the day", "in the end"),
    (r"when all is said and done", "in the end"),
    (r"all things considered", "overall"),
    (r"for all intents and purposes", "basically"),
    (r"more often than not", "usually"),
    (r"a (?:significant|considerable|substantial|large) number of", "many"),
    (r"a (?:significant|considerable|substantial|large) (?:amount|portion|proportion|share) of",
     "a lot of"),
    (r"a growing (?:number|body|amount) of", "more and more"),
    (r"a (?:wide|broad|diverse) (?:range|variety|array) of", "many different"),
    (r"(play(?:s|ed|ing)?) an? (?:significant|crucial|key|vital|major|critical|important|"
     r"central|pivotal) role in", r"\1 a big part in"),
    (r"in (?:a|the) (?:similar|same) vein|along these lines|in much the same way|"
     r"by the same token|in like manner|in the same manner", "in the same way"),
    (r"in (?:stark|direct) contrast|by way of contrast", "in contrast"),
    (r"as opposed to", "rather than"),
    (r"as compared (?:to|with)", "compared to"),
    (r"as distinct from", "unlike"),
    (r"as a matter of fact", "in fact"),
    (r"as a (?:general rule|rule of thumb)", "usually"),
    (r"(?<=,)\s*(?:therefore|thus|hence|consequently),?", " so"),
], "cliches")

# ============================================================
# 4. REDUNDANT PAIRS
# ============================================================
REDUNDANT_SUB = make_sub(expand({
    "very unique": "unique", "basic fundamentals": "fundamentals",
    "final outcome": "outcome", "final result": "result", "end result": "result",
    "past history": "history", "future plans": "plans",
    "advance planning": "planning", "advance warning": "warning",
    "close proximity": "proximity", "mutual cooperation": "cooperation",
    "new innovation": "innovation", "new invention": "invention",
    "armed gunman": "gunman", "free gift": "gift", "added bonus": "bonus",
    "each and every": "every", "various different": "various",
    "general consensus": "consensus", "sudden impulse": "impulse",
    "unexpected surprise": "surprise", "revert back": "revert",
    "return back": "return", "repeat again": "repeat", "join together": "join",
    "combine together": "combine", "merge together": "merge",
    "collaborate together": "collaborate", "past experience": "experience",
    "in my personal opinion": "in my opinion", "the reason why": "the reason",
    "refer back to": "refer to", "absolutely essential": "essential",
    "very essential": "essential", "completely eliminate": "eliminate",
    "completely eliminated": "eliminated", "completely surrounded": "surrounded",
    "fully complete": "complete", "entirely complete": "complete",
}), stat="redundant")

# ============================================================
# 5. FORMAL PHRASES -> PLAIN PHRASES  (longest phrase wins)
# ============================================================
PHRASES_SUB = make_sub(expand({
    "in order to/so as to": "to",
    "due to the fact that/owing to the fact that": "because",
    "in light of the fact that": "since",
    "despite the fact that/in spite of the fact that": "even though",
    "the fact that": "that",
    "in the event that": "if",
    "at this point in time/at the present time/at the present moment/at present": "now",
    "in the near future": "soon",
    "for the purpose of": "for",
    "with regard to/with reference to/in reference to/in relation to/regarding": "about",
    "in the course of": "during",
    "for the most part": "mostly",
    "a large number of": "many",
    "a great deal of": "a lot of",
    "a small number of": "a few",
    "a number of": "several",
    "the vast majority of": "almost all",
    "the majority of": "most",
    "a plethora of/a myriad of/a multitude of": "many",
    "in spite of": "despite",
    "in accordance with/in compliance with": "following",
    "in conjunction with/in combination with/in collaboration with/in partnership with": "with",
    "as a consequence of/as a result of/on account of": "because of",
    "as a result": "so",
    "by means of": "using",
    "for this reason/for that reason/for these reasons": "so",
    "in this regard": "here",
    "in other words": "put differently",
    "that is to say": "in other words",
    "to some extent/to a certain extent/to a certain degree": "partly",
    "to a large extent": "mostly",
    "in many cases": "often",
    "in some cases": "sometimes",
    "in most cases/in the majority of cases": "usually",
    "generally speaking": "usually",
    "broadly speaking": "roughly",
    "technically speaking": "technically",
    "such as": "like",
    "in particular": "especially",
    "in essence": "basically",
    "in summary": "to sum up",
    "in conclusion/to conclude": "to wrap up",
    "first and foremost": "first",
    "last but not least": "finally",
    "as previously mentioned/as mentioned above/as mentioned earlier/as noted above/"
    "as noted earlier/as stated above/as stated earlier": "as I said",
    "it goes without saying that": "",
    "in my opinion/in my view/from my perspective/from my point of view/"
    "it seems to me that": "I think",
    "it appears that/it seems that": "it looks like",
    "it could be argued that/one could argue that/it may be said that": "you could say",
    "there is no doubt that/there can be no doubt that": "clearly",
    "many people believe that/many people think that": "lots of people think",
    "some people believe that": "some people think",
    "most people believe that": "most people think",
    "experts believe that": "experts think",
    "researchers believe that": "researchers think",
    "what is more/what's more/on top of that": "also",
    "not to mention": "plus",
    "on the other hand": "on the flip side",
    "in contrast to": "unlike",
    "in contrast/by contrast": "on the flip side",
    "in comparison to": "compared to",
    "in comparison with": "compared with",
    "in the meantime": "meanwhile",
    "at the moment": "right now",
    "up to now/until now": "so far",
    "in the long run/in the long term": "over time",
    "in the short term": "for now",
    "on the whole/as a whole/all in all": "overall",
    "by and large": "mostly",
    "for the time being": "for now",
    "prior to": "before",
    "subsequent to": "after",
    "in addition to": "besides",
    "in addition": "also",
    "make use of/makes use of/made use of/making use of": "use/uses/used/using",
    "take into consideration/takes into consideration/took into consideration/"
    "taking into consideration/taken into consideration":
        "consider/considers/considered/considering/considered",
    "take into account/takes into account/took into account/taking into account/"
    "taken into account": "consider/considers/considered/considering/considered",
    "has a tendency to/have a tendency to": "tends to/tend to",
    "is able to/are able to": "can",
    "was able to/were able to": "could",
    "has the ability to/have the ability to/had the ability to": "can/can/could",
    "plays a crucial role in/plays a vital role in": "is key to",
    "participate in/participates in/participated in/participating in":
        "join in/joins in/joined in/joining in",
    "ensure that/ensures that/ensured that/ensuring that":
        "make sure that/makes sure that/made sure that/making sure that",
    "endeavor to/endeavors to/endeavored to/endeavoring to":
        "try to/tries to/tried to/trying to",
    "been demonstrated/was demonstrated/were demonstrated/is demonstrated/"
    "are demonstrated/be demonstrated":
        "been shown/was shown/were shown/is shown/are shown/be shown",
    "bear in mind/keep in mind": "remember",
    "pave the way for/paves the way for/paved the way for/paving the way for":
        "open the door to/opens the door to/opened the door to/opening the door to",
    "navigate the complexities of/navigates the complexities of/"
    "navigated the complexities of/navigating the complexities of":
        "deal with/deals with/dealt with/dealing with",
    "whether or not": "whether",
}), stat="phrases")

# ============================================================
# 6. SINGLE WORDS (formal -> plain)
#    Meaning- and grammar-preserving swaps only. Verbs go
#    "base/3rd/past/-ing": "new/news/newed/newing".
# ============================================================
WORDS_SUB = make_sub(expand({
    # verbs
    "utilize/utilizes/utilized/utilizing": "use/uses/used/using",
    "facilitate/facilitates/facilitated/facilitating": "help/helps/helped/helping",
    "assist/assists/assisted/assisting": "help/helps/helped/helping",
    "demonstrate/demonstrates/demonstrated/demonstrating": "show/shows/showed/showing",
    "illustrate/illustrates/illustrated/illustrating": "show/shows/showed/showing",
    "depict/depicts/depicted/depicting": "show/shows/showed/showing",
    "initiate/initiates/initiated/initiating": "start/starts/started/starting",
    "commence/commences/commenced/commencing": "start/starts/started/starting",
    "terminate/terminates/terminated/terminating": "end/ends/ended/ending",
    "ascertain/ascertains/ascertained/ascertaining":
        "find out/finds out/found out/finding out",
    "inquire/inquires/inquired/inquiring": "ask/asks/asked/asking",
    "reside/resides/resided/residing": "live/lives/lived/living",
    "obtain/obtains/obtaining": "get/gets/getting",
    "possess/possesses/possessing": "have/has/having",
    "modify/modifies/modified/modifying": "change/changes/changed/changing",
    "eliminate/eliminates/eliminated/eliminating": "remove/removes/removed/removing",
    "enhance/enhances/enhanced/enhancing": "improve/improves/improved/improving",
    "ameliorate/ameliorates/ameliorated/ameliorating": "improve/improves/improved/improving",
    "exacerbate/exacerbates/exacerbated/exacerbating": "worsen/worsens/worsened/worsening",
    "mitigate/mitigates/mitigated/mitigating": "reduce/reduces/reduced/reducing",
    "curtail/curtails/curtailed/curtailing": "cut back/cuts back/cut back/cutting back",
    "delineate/delineates/delineated/delineating": "outline/outlines/outlined/outlining",
    "proliferate/proliferates/proliferated/proliferating": "spread/spreads/spread/spreading",
    "prioritize/prioritizes/prioritizing": "focus on/focuses on/focusing on",
    "emphasize/emphasizes/emphasized/emphasizing": "stress/stresses/stressed/stressing",
    "summarize/summarizes/summarized/summarizing": "sum up/sums up/summed up/summing up",
    "categorize/categorizes/categorized/categorizing": "sort/sorts/sorted/sorting",
    "modernize/modernizes/modernized/modernizing": "update/updates/updated/updating",
    "symbolize/symbolizes/symbolized/symbolizing":
        "stand for/stands for/stood for/standing for",
    "elucidate/elucidates/elucidated/elucidating": "explain/explains/explained/explaining",
    "delve/delves/delved/delving": "dig/digs/dug/digging",
    "garner/garners/garnered/garnering": "get/gets/got/getting",
    "bolster/bolsters/bolstered/bolstering": "boost/boosts/boosted/boosting",
    "attain/attains/attained/attaining": "reach/reaches/reached/reaching",
    "necessitate/necessitates/necessitated/necessitating":
        "call for/calls for/called for/calling for",
    "leverages/leveraged/leveraging": "uses/used/using",
    "purchased/purchasing": "bought/buying",
    # nouns
    "utilization": "use", "assistance": "help",
    "modification/modifications": "change/changes",
    "terminology": "terms",
    "ramification/ramifications": "effect/effects",
    "disadvantage/disadvantages": "downside/downsides",
    "objectives": "goals", "individuals": "people", "regulations": "rules",
    # connectives and adverbs
    "furthermore/moreover/additionally": "also",
    "nevertheless/nonetheless": "still",
    "whereas/whilst": "while",
    "albeit": "though",
    "approximately": "about",
    "subsequently/subsequent": "later",
    "currently": "now",
    "predominantly/primarily/mainly/chiefly": "mostly",
    "particularly": "especially",
    "typically/generally": "usually",
    "frequently": "often",
    "occasionally": "sometimes",
    "virtually/practically": "almost",
    "merely": "just",
    "solely/exclusively": "only",
    "seamlessly": "smoothly",
    "meticulously": "carefully",
    "heretofore": "until now", "henceforth": "from now on", "thereafter": "after that",
    "aforementioned": "earlier",
    # adjectives
    "numerous/myriad": "many",
    "innumerable": "countless",
    "sufficient": "enough",
    "insufficient": "too little",
    "optimal": "ideal",
    "suboptimal": "less than ideal",
    "viable": "workable",
    "feasible": "doable",
    "probable": "likely",
    "improbable": "unlikely",
    "prevalent": "common",
    "pervasive/ubiquitous": "widespread",
    "crucial/pivotal": "key",
    "fundamental": "basic",
    "comprehensive": "full",
    "meticulous": "careful",
    "profound": "deep",
    "superficial": "shallow",
    "ambiguous": "unclear",
    "intricate/multifaceted": "complex",
    "prominent": "well known",
    "trivial": "minor",
    "negligible": "tiny",
    "detrimental/deleterious/pernicious": "harmful",
    "ephemeral": "short-lived",
    "incessant": "nonstop",
}), stat="words")

# ============================================================
# 7. INFORMAL SWAPS (each rule guarded so it can't break
#    "very much", "not quite", "quite a few", "positively charged" ...)
# ============================================================
INFORMAL_RULES = [
    (re.compile(r"(?<!the )\bvery\b(?!\s+(?:much|many|few|little|same|least|best|first|last|"
                r"end|idea|thing)\b)", re.I), "really"),
    (re.compile(r"\bextremely\b", re.I), "super"),
    (re.compile(r"\b(?:truly|genuinely)\b", re.I), "really"),
    (re.compile(r"(?<!not )\bquite\b(?!\s+(?:a|an|so)\b)", re.I), "pretty"),
]


def apply_informal(text):
    def mk(rep):
        def f(m):
            STATS["informal"] += 1
            return match_case(m.group(0), rep)
        return f
    for rx, rep in INFORMAL_RULES:
        text = rx.sub(mk(rep), text)
    return text


# ============================================================
# 8. FILLERS - only pure throat-clearing; hedges and quantity words
#    (apparently, usually, just, exactly, significantly ...) stay.
# ============================================================
OPENER_FILLERS = ["basically", "essentially", "fundamentally", "ultimately", "importantly",
                  "notably", "interestingly", "surprisingly", "obviously", "clearly",
                  "certainly", "definitely", "undoubtedly", "unquestionably"]
MID_FILLERS = ["basically", "essentially", "fundamentally", "definitely", "certainly",
               "undoubtedly", "unquestionably", "incredibly", "remarkably",
               "extraordinarily", "exceptionally", "immensely"]
_OPENER_RX = re.compile(r"^(\W*)(?:" + "|".join(OPENER_FILLERS) + r"),\s+", re.I)
_MID_RX = re.compile(r"(?<=\s)(?:" + "|".join(MID_FILLERS) + r")\s+", re.I)


def trim_fillers(text):
    t = _OPENER_RX.sub(r"\1", text)
    t2 = _MID_RX.sub("", t)
    if t2 != text:
        STATS["fillers"] += 1
    return t2


# ============================================================
# 9. PROTECTION (placeholders are private-use characters, so no
#    dictionary, regex or boundary can ever touch or half-match them)
# ============================================================
PROTECTED = [
    r"https?://\S+|www\.\S+",
    r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    r"`[^`\n]+`",
    r"\[\d+(?:\s*[,–-]\s*\d+)*\]",
    r'"[^"\n]*"',
    "“[^”\n]*”",
    r"(?<!\w)'[^'\n]{1,200}'(?!\w)",
    "(?<!\\w)‘[^’\n]{1,200}’(?!\\w)",
    r"\([^)\n]*\)",
    r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    r"\b\d{4}\b",
    r"\b[A-Z]{2,}\b",
]
_PH = re.compile(PUA_OPEN + "([-]+)" + PUA_CLOSE)


def _ph(n):
    return PUA_OPEN + "".join(chr(_DIGIT_BASE + int(d)) for d in str(n)) + PUA_CLOSE


def protect(text, extra=()):
    store = []

    def repl(m):
        store.append(m.group(0))
        return _ph(len(store) - 1)

    pats = list(PROTECTED)
    for w in extra:
        pats.insert(0, r"(?<![\w-])" + re.escape(w) + r"(?![\w-])")
    for p in pats:
        text = re.sub(p, repl, text, flags=re.I if p.startswith("(?<![\\w-])") else 0)
    return text, store


def unprotect(text, store):
    def back(m):
        return store[int("".join(str(ord(c) - _DIGIT_BASE) for c in m.group(1)))]
    for _ in range(12):                 # nested protection (a quote inside brackets)
        new = _PH.sub(back, text)
        if new == text:
            break
        text = new
    return text


# ============================================================
# 10. TEXT CLEAN-UP
# ============================================================
def tidy(text):
    text = re.sub(r",(?:\s*,)+", ",", text)
    text = re.sub(r"^[\s,;:]+", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return re.sub(r"\s{2,}", " ", text).strip()


_LEAD = "[\"'“‘(\\[]*"


def capitalize_first(s):
    return re.sub(r"^(" + _LEAD + r")([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)


# "a" vs "an" follows the NEXT word, which the swaps may have changed.
_A_SOUND = re.compile(r"^(?:uni(?![mnd])|unan|use|usu|uti|uto|eu|one|once|ubiq|ura|uri|ute|uku|ufo)")
_AN_SOUND = re.compile(r"^(?:hour|honest|honor|honour|heir)")
_ARTICLE = re.compile(r"(?<![\w'-])(an?|An?)(\s+)([A-Za-z][\w'-]*)")


def fix_articles(text):
    def repl(m):
        art, space, word = m.groups()
        if art[0] == "A" and m.start() != 0:      # "Vitamin A", "Plan A"
            return m.group(0)
        if len(word) > 1 and word.isupper():     # acronym: ambiguous, leave
            return m.group(0)
        w = word.lower()
        if _A_SOUND.match(w):
            want = "a"
        elif w[0] in "aeiou" or _AN_SOUND.match(w):
            want = "an"
        else:
            want = "a"
        return (want if art[0].islower() else want.capitalize()) + space + word
    return _ARTICLE.sub(repl, text)


# ============================================================
# 11. HEADINGS, LISTS, SENTENCES
# ============================================================
def is_heading(line):
    t = line.strip()
    if not t:
        return False
    if t.startswith("#"):
        return True
    if len(t.split()) > 12:
        return False
    if t == t.upper() and len(t) < 80 and re.search(r"[A-Z]", t):
        return True
    if re.match(r"^\d+(\.\d+)*\.?\s+\S", t) and not re.search(r"[.!?]$", t):
        return True
    if re.match(r"^(CHAPTER|Chapter|ABSTRACT|REFERENCES|DECLARATION|ACKNOWLEDGEMENT|"
                r"TABLE OF CONTENTS|Contents|Keywords)\b", t) and not re.search(r"[.!?]$", t):
        return True
    if t.endswith(":"):
        return True
    if len(t.split()) < 8 and not re.search(r"[.!?\"')]$", t):
        return True
    return False


_LIST_PREFIX = re.compile(r"^(\s*(?:[-*•]|\d+[.)])\s+)(.*)$")
_ABBREVIATIONS = {"mr", "mrs", "ms", "dr", "prof", "sr", "jr", "vs", "fig", "e.g", "i.e",
                  "cf", "al", "inc", "ltd", "approx", "etc", "no"}


def split_sentences(text):
    out = []
    for p in re.split(r"(?<=[.!?])\s+", text):
        if out:
            last = out[-1].split()[-1:] or [""]
            if last[0].endswith(".") and last[0].lower().rstrip(".") in _ABBREVIATIONS:
                out[-1] += " " + p
                continue
        out.append(p)
    return [s for s in out if s.strip()]


def split_semicolons(text):
    """'a; b' -> 'a. B' only when both halves are real clauses (not list items)."""
    parts = text.split(";")
    acc = parts[0]
    for nxt in parts[1:]:
        right = re.split(r"[.!?;]", nxt, maxsplit=1)[0]
        left = acc.rsplit(".", 1)[-1]
        if (nxt.strip() and len(left.split()) >= 5 and len(right.split()) >= 5
                and not re.match(r"\s*(?:and|or|but|nor)\b", nxt)):
            n = nxt.lstrip()
            acc = acc.rstrip() + ". " + n[0].upper() + n[1:]
            STATS["semicolons"] += 1
        else:
            acc += ";" + nxt
    return acc


_SPLIT_MARKERS = [", and ", ", but ", ", so ", ", yet "]
_SUBJECT_WORDS = {"the", "a", "an", "he", "she", "it", "they", "we", "i", "you", "this",
                  "that", "these", "those", "there", "his", "her", "their", "our", "its",
                  "my", "your", "some", "many", "most", "all", "each", "every", "both",
                  "no", "one"}


def split_long_sentence(sentence, min_words):
    """Split at ', and/but/so/yet' only when BOTH halves look like full clauses."""
    if not min_words or len(sentence.split()) < min_words or sentence.rstrip().endswith("?"):
        return [sentence]
    mid = len(sentence) / 2
    best = None
    for marker in _SPLIT_MARKERS:
        for m in re.finditer(re.escape(marker), sentence, re.IGNORECASE):
            first, rest = sentence[:m.start()], sentence[m.end():]
            if len(first.split()) < 6 or len(rest.split()) < 5:
                continue
            nxt = rest.split()[0].lower().strip("\"'(")
            if nxt not in _SUBJECT_WORDS and not nxt.startswith(PUA_OPEN):
                continue
            dist = abs(m.start() - mid)
            if best is None or dist < best[0]:
                best = (dist, first, marker.strip(", ").capitalize(), rest)
    if best is None:
        return [sentence]
    STATS["splits"] += 1
    _, first, conj, rest = best
    return [first.rstrip(",;: ") + ".", f"{conj} {rest}"]


# ============================================================
# 12. STARTER INJECTION (neutral, additive connectors only)
# ============================================================
STARTERS = ["And ", "Plus, ", "Also, "]
_CONNECTIVES = {"and", "but", "so", "or", "yet", "nor", "plus", "then", "also", "still",
                "while", "because", "though", "meanwhile", "overall", "maybe", "probably",
                "clearly", "in", "on", "to"}
_LOWERABLE = {"the", "this", "that", "these", "those", "it", "its", "they", "their", "we",
              "our", "he", "she", "his", "her", "there", "with", "by", "from", "as", "many",
              "some", "most", "all", "each", "every", "such", "one", "a", "an", "my", "your",
              "you"}


def add_starter(sentence):
    words = sentence.split()
    if len(words) < 6 or not sentence[0].isalpha():
        return sentence
    first = words[0].lower()
    if first in _CONNECTIVES or first not in _LOWERABLE:
        return sentence
    return random.choice(STARTERS) + sentence[0].lower() + sentence[1:]


# ============================================================
# 13. PIPELINE
# ============================================================
LEVELS = {
    "light":  dict(words=False, informal=False, fillers=False, split=0,  starters=0.00, max_starters=0),
    "medium": dict(words=True,  informal=True,  fillers=True,  split=18, starters=0.15, max_starters=3),
    "strong": dict(words=True,  informal=True,  fillers=True,  split=14, starters=0.25, max_starters=5),
}


def transform_sentence(s, cfg):
    m = re.match(_LEAD + "([A-Za-z])", s)
    was_cap = bool(m and m.group(1).isupper())
    s = CLICHES_SUB(s)          # first, so "it is important to note that" is dropped whole
    s = apply_openers(s)
    s = REDUNDANT_SUB(s)
    s = PHRASES_SUB(s)
    if cfg["contractions"]:
        for sub in CONTRACTION_SUBS:
            s = sub(s)
    if cfg["words"]:
        s = WORDS_SUB(s)
    if cfg["informal"]:
        s = apply_informal(s)
    if cfg["fillers"]:
        s = trim_fillers(s)
    s = tidy(s)
    s = fix_articles(s)
    if was_cap:
        s = capitalize_first(s)
    return s


def humanize_paragraph(para, cfg):
    text = para.strip().replace(PUA_OPEN, "").replace(PUA_CLOSE, "")
    if not text:
        return ""
    text, store = protect(text, cfg["keep"])

    if cfg["dashes"]:
        n = len(re.findall(r"\s*[—―]\s*", text))
        if n:
            STATS["dashes"] += n
            text = re.sub(r"\s*[—―]\s*", ", ", text)
    text = split_semicolons(text)

    pieces = []
    for sentence in split_sentences(text):
        sentence = transform_sentence(sentence, cfg)
        if sentence:
            pieces.extend(split_long_sentence(sentence, cfg["split"]))

    # "x, and y" -> "x and y" (after splitting, which needs the comma; ", so" keeps its comma)
    pieces = [re.sub(r",\s+(and|or)\b", r" \1", p) for p in pieces]

    out, used = [], 0
    for i, s in enumerate(pieces):
        if i > 0 and used < cfg["max_starters"] and random.random() < cfg["starters"]:
            new = add_starter(s)
            if new != s:
                used += 1
                STATS["starters"] += 1
                s = new
        out.append(s)

    result = re.sub(r"\s+", " ", " ".join(out)).strip()
    result = re.sub(r"\s+([.,!?])", r"\1", result)
    return unprotect(result, store)


def humanize(text, level="medium", contractions=True, dashes=True, keep=()):
    cfg = dict(LEVELS[level], contractions=contractions, dashes=dashes, keep=tuple(keep))
    output = []
    for line in text.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if not stripped:
            output.append("")
        elif is_heading(stripped):
            output.append(stripped)
        else:
            m = _LIST_PREFIX.match(line)
            if m:
                output.append(m.group(1) + humanize_paragraph(m.group(2), cfg))
            else:
                output.append(humanize_paragraph(stripped, cfg))
    return "\n".join(output)


# ============================================================
# 14. MEANING GUARD
# ============================================================
_NUM = re.compile(r"\d+(?:[.,]\d+)*")
_QUOTE = re.compile(r'"[^"\n]+"|“[^”\n]+”')
_NEG = re.compile(r"\b(?:not|no|never|neither|nor|cannot|without|none)\b|n't\b", re.I)


def check(original, result):
    warnings = []
    if Counter(_NUM.findall(original)) != Counter(_NUM.findall(result)):
        warnings.append("numbers differ")
    if Counter(_QUOTE.findall(original)) != Counter(_QUOTE.findall(result)):
        warnings.append("quoted text differs")
    a, b = len(_NEG.findall(original)), len(_NEG.findall(result))
    if a != b:
        warnings.append(f"negations changed ({a} -> {b}); read those sentences")
    if re.search("[-]|__P\\w*__", result):
        warnings.append("internal placeholder leaked (please report)")
    return warnings


# ============================================================
# 15. COMMAND LINE / INTERACTIVE MODE
# ============================================================
def read_interactive():
    print("=" * 60)
    print("  ULTIMATE HUMANIZER v4")
    print("  Offline. No API. Single file.")
    print("=" * 60)
    print()
    print("Type or paste your text below.")
    print("When done, type END on a new line and press Enter.")
    print("-" * 60)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass

    ap = argparse.ArgumentParser(description="Offline text humanizer")
    ap.add_argument("input", nargs="?", help="text file (default: paste, or stdin)")
    ap.add_argument("-o", "--output", help="output file, or - for stdout "
                                           "(default: <input>.humanized.txt)")
    ap.add_argument("--level", choices=list(LEVELS), default="medium",
                    help="light = clichés/phrases/contractions only; strong = most aggressive")
    ap.add_argument("--seed", type=int, help="repeatable random choices")
    ap.add_argument("--no-contractions", action="store_true")
    ap.add_argument("--keep-dashes", action="store_true", help="don't turn em dashes into commas")
    ap.add_argument("--keep", default="", help="comma-separated words/phrases never to touch")
    ap.add_argument("--report", action="store_true", help="show what was changed")
    ap.add_argument("--diff", action="store_true", help="show a diff instead of the text")
    ap.add_argument("--no-check", action="store_true", help="skip the meaning guard")
    ap.add_argument("--no-pause", action="store_true")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    interactive = False
    if args.input:
        text = Path(args.input).read_text(encoding="utf-8-sig", errors="replace")
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        text = read_interactive()
        interactive = True

    if not text.strip():
        print("No text given. Exiting.")
        return

    keep = [k.strip() for k in args.keep.split(",") if k.strip()]
    STATS.clear()
    result = humanize(text, args.level, not args.no_contractions, not args.keep_dashes, keep)

    if args.diff:
        print("\n".join(difflib.unified_diff(text.splitlines(), result.splitlines(),
                                             "original", "humanized", lineterm="")))
    elif interactive:
        print("-" * 60)
        print("  HUMANIZED OUTPUT")
        print("-" * 60)
        print(result)
    elif args.output == "-" or (not args.input and not args.output):
        print(result)

    if args.input or args.output not in (None, "-"):
        if args.output and args.output != "-":
            dest = Path(args.output)
        elif args.input:
            p = Path(args.input)
            dest = p.with_name(f"{p.stem}.humanized{p.suffix or '.txt'}")
        else:
            dest = None
        if dest:
            dest.write_text(result + "\n", encoding="utf-8")
            print(f"\nSaved to: {dest}", file=sys.stderr)
    elif interactive:
        try:
            Path("humanized_output.txt").write_text(result + "\n", encoding="utf-8")
            print("\nSaved to: humanized_output.txt", file=sys.stderr)
        except OSError as e:
            print(f"Could not save file: {e}", file=sys.stderr)

    if args.report:
        print(f"\nChanges ({sum(STATS.values())}):", file=sys.stderr)
        for k, n in STATS.most_common():
            print(f"  {n:>4}  {k}", file=sys.stderr)

    if not args.no_check:
        for w in check(text, result):
            print(f"WARNING: {w}", file=sys.stderr)

    if interactive and not args.no_pause and sys.stdout.isatty():
        try:
            input("\nPress Enter to close...")
        except EOFError:
            pass

# ============================================================
# WRAPPER for app.py pipeline
# ============================================================
def advanced_humanize(text, level="medium"):
    """Wrapper so app.py can import it as the advanced pass."""
    return humanize(text, level=level)
if __name__ == "__main__":
    main()
