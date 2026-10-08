#!/usr/bin/env python3
"""
ULTRA HUMANIZER v2 - WORKING VERSION
Offline. No API. No internet needed.
"""

import re
import random


# ============================================================
# CONTRACTIONS
# ============================================================
CONTRACTIONS = {
    r"\bdo not\b": "don't", r"\bdoes not\b": "doesn't", r"\bdid not\b": "didn't",
    r"\bis not\b": "isn't", r"\bare not\b": "aren't", r"\bwas not\b": "wasn't",
    r"\bwere not\b": "weren't", r"\bhave not\b": "haven't", r"\bhas not\b": "hasn't",
    r"\bhad not\b": "hadn't", r"\bwill not\b": "won't", r"\bwould not\b": "wouldn't",
    r"\bcannot\b": "can't", r"\bcan not\b": "can't", r"\bcould not\b": "couldn't",
    r"\bshould not\b": "shouldn't", r"\bmust not\b": "mustn't", r"\bneed not\b": "needn't",
    r"\bit is\b": "it's", r"\bthat is\b": "that's", r"\bthere is\b": "there's",
    r"\bhere is\b": "here's", r"\bwhat is\b": "what's", r"\bwho is\b": "who's",
    r"\bwhere is\b": "where's", r"\bwhen is\b": "when's", r"\bwhy is\b": "why's",
    r"\bhow is\b": "how's", r"\bthey are\b": "they're", r"\bwe are\b": "we're",
    r"\byou are\b": "you're", r"\bI am\b": "I'm", r"\bI will\b": "I'll",
    r"\bI have\b": "I've", r"\bI would\b": "I'd", r"\bI had\b": "I'd",
    r"\bthey will\b": "they'll", r"\bthey have\b": "they've", r"\bthey would\b": "they'd",
    r"\bwe will\b": "we'll", r"\bwe have\b": "we've", r"\bwe would\b": "we'd",
    r"\byou will\b": "you'll", r"\byou have\b": "you've", r"\byou would\b": "you'd",
    r"\bhe is\b": "he's", r"\bshe is\b": "she's", r"\bhe will\b": "he'll",
    r"\bshe will\b": "she'll", r"\bhe would\b": "he'd", r"\bshe would\b": "she'd",
    r"\bhe has\b": "he's", r"\bshe has\b": "she's", r"\blet us\b": "let's",
    r"\bthere will\b": "there'll", r"\bthere are\b": "there're",
}


# ============================================================
# SIMPLE WORD SWAPS (fancy -> simple)
# ============================================================
SIMPLE_WORDS = {
    r"\butilize\b": "use", r"\butilizes\b": "uses", r"\butilized\b": "used",
    r"\butilizing\b": "using", r"\butilization\b": "use",
    r"\bfurthermore\b": "also", r"\bmoreover\b": "also", r"\badditionally\b": "also",
    r"\bconsequently\b": "so", r"\bsubsequently\b": "then", r"\btherefore\b": "so",
    r"\bthus\b": "so", r"\bhence\b": "so",
    r"\bdelve\b": "look", r"\bdelves\b": "looks", r"\bdelving\b": "looking",
    r"\bcommence\b": "start", r"\bcommences\b": "starts", r"\bcommenced\b": "started",
    r"\bterminate\b": "end", r"\bterminates\b": "ends", r"\bterminated\b": "ended",
    r"\bendeavor\b": "try", r"\bendeavors\b": "tries", r"\bendeavored\b": "tried",
    r"\bascertain\b": "find out",
    r"\bdemonstrate\b": "show", r"\bdemonstrates\b": "shows",
    r"\bdemonstrated\b": "showed", r"\bdemonstrating\b": "showing",
    r"\bfacilitate\b": "help", r"\bfacilitates\b": "helps",
    r"\bfacilitated\b": "helped", r"\bfacilitating\b": "helping",
    r"\bimplement\b": "use", r"\bimplements\b": "uses", r"\bimplemented\b": "used",
    r"\bimplementation\b": "use",
    r"\boptimal\b": "best", r"\boptimize\b": "improve", r"\boptimized\b": "improved",
    r"\bnumerous\b": "many", r"\bindividuals\b": "people", r"\bindividual\b": "person",
    r"\bprior to\b": "before", r"\bsubsequent to\b": "after",
    r"\bin order to\b": "to", r"\bdue to the fact that\b": "because",
    r"\bin the event that\b": "if", r"\bat this point in time\b": "now",
    r"\ba large number of\b": "many", r"\bthe majority of\b": "most",
    r"\bin spite of\b": "despite", r"\bwith regard to\b": "about",
    r"\bwith respect to\b": "about", r"\bin reference to\b": "about",
    r"\bconcerning\b": "about", r"\bregarding\b": "about",
    r"\bpossess\b": "have", r"\bpossesses\b": "has", r"\bpossessed\b": "had",
    r"\brequire\b": "need", r"\brequires\b": "needs", r"\brequired\b": "needed",
    r"\brequirement\b": "need", r"\brequirements\b": "needs",
    r"\bobtain\b": "get", r"\bobtains\b": "gets", r"\bobtained\b": "got",
    r"\bprovide\b": "give", r"\bprovides\b": "gives", r"\bprovided\b": "gave",
    r"\bassist\b": "help", r"\bassists\b": "helps", r"\bassisted\b": "helped",
    r"\bassistance\b": "help", r"\battempt\b": "try", r"\battempts\b": "tries",
    r"\battempted\b": "tried", r"\battempting\b": "trying",
    r"\bsufficient\b": "enough", r"\badditional\b": "more",
    r"\binitial\b": "first", r"\bfinal\b": "last",
    r"\bcomprehend\b": "understand", r"\bcomprehends\b": "understands",
    r"\bcomprehended\b": "understood",
    r"\bestablish\b": "set up", r"\bestablishes\b": "sets up",
    r"\bestablished\b": "set up", r"\bestablishing\b": "setting up",
    r"\beliminate\b": "cut", r"\beliminates\b": "cuts", r"\beliminated\b": "cut",
    r"\bmodify\b": "change", r"\bmodifies\b": "changes", r"\bmodified\b": "changed",
    r"\bmodification\b": "change",
    r"\bgenerate\b": "make", r"\bgenerates\b": "makes", r"\bgenerated\b": "made",
    r"\banalyze\b": "look at", r"\banalyzes\b": "looks at",
    r"\banalyzed\b": "looked at", r"\banalyzing\b": "looking at",
    r"\banalysis\b": "look",
    r"\binterpret\b": "read", r"\binterprets\b": "reads",
    r"\binterpreted\b": "read", r"\binterpretation\b": "reading",
    r"\bnevertheless\b": "still", r"\bnonetheless\b": "still",
    r"\bnotwithstanding\b": "still",
    r"\bwhereas\b": "while", r"\bwhilst\b": "while",
    r"\bmyriad\b": "many", r"\bplethora\b": "many", r"\bmultitude\b": "many",
    r"\bparadigm\b": "model", r"\bmethodology\b": "method",
    r"\bphenomenon\b": "thing", r"\bcognizant\b": "aware",
    r"\binitiate\b": "start", r"\binitiates\b": "starts",
    r"\binitiated\b": "started", r"\binitiating\b": "starting",
    r"\bmitigate\b": "reduce", r"\bmitigates\b": "reduces",
    r"\bmitigated\b": "reduced",
    r"\bnecessitate\b": "need", r"\bnecessitates\b": "needs",
    r"\bnotion\b": "idea", r"\bnotions\b": "ideas",
    r"\bobjective\b": "goal", r"\bobjectives\b": "goals",
    r"\bproficient\b": "good", r"\bproximity\b": "closeness",
    r"\bramifications\b": "results",
    r"\bscrutinize\b": "study", r"\bscrutinizes\b": "studies",
    r"\bscrutinized\b": "studied",
    r"\bsubstantial\b": "big", r"\btransmit\b": "send",
    r"\bviable\b": "workable",
    r"\bameliorate\b": "improve", r"\barticulate\b": "say",
    r"\bdisseminate\b": "spread", r"\bexemplify\b": "show",
    r"\bjuxtapose\b": "compare",
    r"\bcommence\b": "start", r"\bculminate\b": "end",
    r"\bexacerbate\b": "worsen", r"\bexpedite\b": "speed up",
    r"\bfabricate\b": "make up", r"\bhypothesize\b": "guess",
    r"\bpostulate\b": "suggest", r"\bpresuppose\b": "assume",
    r"\brationalize\b": "explain", r"\bsynthesize\b": "combine",
    r"\bvalidate\b": "check", r"\bcorroborate\b": "back up",
    r"\badvocate\b": "support", r"\bcondone\b": "allow",
    r"\bdenounce\b": "condemn", r"\bbolster\b": "boost",
    r"\bcurtail\b": "cut back", r"\bexacerbate\b": "worsen",
    r"\bproliferate\b": "spread", r"\bameliorate\b": "improve",
    r"\bostensibly\b": "supposedly", r"\bpurportedly\b": "supposedly",
    r"\barguably\b": "maybe", r"\bpresumably\b": "probably",
    r"\bconceivably\b": "possibly", r"\bplausibly\b": "possibly",
    r"\binevitably\b": "for sure", r"\bultimately\b": "in the end",
    r"\bfundamentally\b": "basically", r"\bessentially\b": "basically",
    r"\bparticularly\b": "especially", r"\bnotably\b": "especially",
    r"\bpredominantly\b": "mostly", r"\bprimarily\b": "mostly",
    r"\bchiefly\b": "mostly", r"\bprincipally\b": "mainly",
    r"\bexclusively\b": "only", r"\bsolely\b": "only",
    r"\bmerely\b": "just", r"\bsimply\b": "just",
    r"\bapproximately\b": "about", r"\broughly\b": "about",
    r"\bnearly\b": "almost", r"\bvirtually\b": "almost",
    r"\bpractically\b": "almost",
    r"\bregardless\b": "anyway", r"\birrespective\b": "no matter",
    r"\bin accordance with\b": "following",
    r"\bin conjunction with\b": "with",
    r"\bas a result of\b": "because of",
    r"\bas a consequence of\b": "because of",
    r"\bon account of\b": "because of",
    r"\bby means of\b": "using",
    r"\bfor this reason\b": "so",
    r"\bfor that reason\b": "so",
    r"\bin this regard\b": "here",
    r"\bin other words\b": "meaning",
    r"\bthat is to say\b": "meaning",
    r"\bto some extent\b": "sort of",
    r"\bto a large extent\b": "mostly",
    r"\bin many cases\b": "often",
    r"\bin most cases\b": "usually",
    r"\bfor instance\b": "like",
    r"\bfor example\b": "like",
    r"\bin particular\b": "especially",
    r"\bin essence\b": "basically",
    r"\bin summary\b": "to sum up",
    r"\bin conclusion\b": "to wrap up",
    r"\bin short\b": "basically",
    r"\bin brief\b": "quickly",
    r"\bto conclude\b": "so",
    r"\bas previously mentioned\b": "as I said",
    r"\bas mentioned above\b": "as I said",
    r"\bit is important to note that\b": "note that",
    r"\bit should be noted that\b": "note that",
    r"\bit is worth noting that\b": "note that",
    r"\bit goes without saying that\b": "",
    r"\bwithout a doubt\b": "for sure",
    r"\bin my opinion\b": "I think",
    r"\bin my view\b": "I think",
    r"\bit seems that\b": "it looks like",
    r"\bit appears that\b": "it looks like",
    r"\bmany people believe that\b": "lots of people think",
    r"\bsome people believe that\b": "some people think",
    r"\bthe fact that\b": "that",
    r"\bwhat is more\b": "also",
    r"\bon top of that\b": "also",
    r"\bon the other hand\b": "on the flip side",
    r"\bon the contrary\b": "actually",
    r"\bin contrast\b": "on the flip side",
    r"\bdespite the fact that\b": "even though",
    r"\bat the same time\b": "also",
    r"\bat the moment\b": "right now",
    r"\bat present\b": "now",
    r"\bas a whole\b": "overall",
    r"\bon the whole\b": "overall",
    r"\ball in all\b": "overall",
    r"\bby and large\b": "mostly",
}


# ============================================================
# INFORMAL SWAPS
# ============================================================
INFORMAL = {
    r"\bvery\b": "really",
    r"\bquite\b": "pretty",
    r"\brather\b": "kind of",
    r"\bsomewhat\b": "kind of",
    r"\bextremely\b": "super",
    r"\bhighly\b": "really",
    r"\btruly\b": "really",
    r"\bgenuinely\b": "really",
    r"\bindeed\b": "really",
    r"\bcompletely\b": "totally",
    r"\bentirely\b": "totally",
    r"\babsolutely\b": "totally",
    r"\bcertainly\b": "sure",
    r"\bdefinitely\b": "for sure",
    r"\bundoubtedly\b": "no doubt",
    r"\bhowever\b": "but",
}


# ============================================================
# PROTECTED PATTERNS
# ============================================================
PROTECTED = [
    r'"[^"]*"',
    r"'[^']*'",
    r"\([^)]*\)",
    r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    r"\b\d{4}\b",
    r"\b[A-Z]{2,}\b",
]


def protect(text):
    store = {}
    counter = [0]
    def repl(m):
        key = "__PROTECT_{}__".format(counter[0])
        counter[0] += 1
        store[key] = m.group(0)
        return key
    for pat in PROTECTED:
        text = re.sub(pat, repl, text)
    return text, store


def unprotect(text, store):
    for key, val in store.items():
        text = text.replace(key, val)
    return text


# ============================================================
# HEADING DETECTION
# ============================================================
def is_heading(line):
    t = line.strip()
    if not t:
        return False
    if t == t.upper() and len(t) < 80 and len(t.split()) < 12:
        return True
    if re.match(r"^\d+(\.\d+)*\s", t):
        return True
    if re.match(r"^(CHAPTER|Chapter|ABSTRACT|REFERENCES|DECLARATION|ACKNOWLEDGEMENT|TABLE OF CONTENTS|Contents|Keywords)\b", t):
        return True
    if t.endswith(":") and len(t.split()) < 10:
        return True
    if len(t.split()) < 8 and not re.search(r"[.!?]$", t):
        return True
    return False


# ============================================================
# SENTENCE SPLITTING
# ============================================================
def split_long_sentence(sentence):
    words = sentence.split()
    if len(words) < 16:
        return [sentence]

    split_points = [
        (", and ", "And "),
        (", but ", "But "),
        (", so ", "So "),
        (", or ", "Or "),
        (" because ", "Because "),
        (" although ", "Although "),
        (" though ", "Though "),
        (" while ", "While "),
        (" whereas ", "While "),
    ]

    for marker, starter in split_points:
        idx = sentence.lower().find(marker.lower())
        if idx > 25 and idx < len(sentence) - 25:
            first = sentence[:idx].strip().rstrip(",;:") + "."
            second_raw = sentence[idx + len(marker):].strip()
            if not second_raw:
                continue
            second = starter + second_raw[0].lower() + second_raw[1:]
            return [first, second]
    return [sentence]


# ============================================================
# STARTER INJECTION
# ============================================================
STARTERS = ["And ", "So ", "But ", "Plus, ", "Also, "]


def add_starter(sentence):
    parts = sentence.split()
    if not parts:
        return sentence
    first_word = parts[0].lower()
    if first_word in ("and", "so", "but", "or", "yet", "for", "nor", "plus", "then", "also"):
        return sentence
    if len(parts) < 5:
        return sentence
    starter = random.choice(STARTERS)
    if sentence[0].isupper():
        rest = sentence[0].lower() + sentence[1:]
    else:
        rest = sentence
    return starter + rest


# ============================================================
# MAIN HUMANIZE
# ============================================================
def apply_dict(text, mapping):
    for pat, rep in mapping.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


def humanize_paragraph(para):
    text = para.strip()
    if not text:
        return ""

    text, store = protect(text)

    # Apply swaps (order matters)
    text = apply_dict(text, CONTRACTIONS)
    text = apply_dict(text, SIMPLE_WORDS)
    text = apply_dict(text, INFORMAL)

    # Remove commas before conjunctions
    text = re.sub(r",\s*(and|but|so|or|yet|for|nor)\b", r" \1", text, flags=re.IGNORECASE)

    # Semicolons -> periods
    text = re.sub(r";\s*", ". ", text)

    # Fix spacing
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    new_sentences = []
    for s in sentences:
        if not s.strip():
            continue
        new_sentences.extend(split_long_sentence(s.strip()))

    # Add starters
    starter_count = 0
    final = []
    for i, s in enumerate(new_sentences):
        s = s.strip()
        if not s:
            continue
        if i > 0 and starter_count < 3 and random.random() < 0.20:
            new_s = add_starter(s)
            if new_s != s:
                starter_count += 1
                s = new_s
        final.append(s)

    result = " ".join(final)
    result = re.sub(r"\s+", " ", result).strip()
    result = re.sub(r"\s+([.,!?])", r"\1", result)

    result = unprotect(result, store)
    return result


def humanize(text):
    lines = text.split("\n")
    output = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            output.append("")
            continue
        if is_heading(stripped):
            output.append(stripped)
        else:
            output.append(humanize_paragraph(stripped))
    return "\n".join(output)


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("  ULTRA HUMANIZER v2")
    print("  Offline. No API. No internet.")
    print("=" * 60)
    print()
    print("HOW TO USE:")
    print("  1. Paste or type your text below.")
    print("  2. When you are done, type END on a new line")
    print("     and press Enter.")
    print("-" * 60)
    print()

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)

    while lines and lines[-1].strip() == "":
        lines.pop()

    text = "\n".join(lines)
    if not text.strip():
        print("No text given. Exiting.")
        return

    print()
    print("-" * 60)
    print("Processing...")
    print("-" * 60)

    result = humanize(text)

    print()
    print("=" * 60)
    print("  HUMANIZED OUTPUT")
    print("=" * 60)
    print()
    print(result)
    print()

    try:
        with open("humanized_output.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("-" * 60)
        print("Saved to: humanized_output.txt")
    except Exception as e:
        print("Could not save file: {}".format(e))

    print()
    input("Press Enter to close...")


if __name__ == "__main__":
    main()