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
        # ---- EXPANSION 1: More academic verbs ----
    r"\bfacilitate\b": "help", r"\bfacilitated\b": "helped",
    r"\bpromulgate\b": "spread", r"\bpromulgates\b": "spreads",
    r"\bproliferate\b": "spread", r"\bproliferates\b": "spreads",
    r"\bostracize\b": "shun", r"\bostracizes\b": "shuns",
    r"\bcultivate\b": "grow", r"\bcultivates\b": "grows",
    r"\bcultivated\b": "grew", r"\bcultivating\b": "growing",
    r"\bnurture\b": "help grow", r"\bnurtures\b": "helps grow",
    r"\bfortify\b": "strengthen", r"\bfortifies\b": "strengthens",
    r"\bfortified\b": "strengthened",
    r"\bharmonize\b": "match", r"\bharmonizes\b": "matches",
    r"\bintegrate\b": "combine", r"\bintegrates\b": "combines",
    r"\bintegrated\b": "combined", r"\bintegrating\b": "combining",
    r"\bconsolidate\b": "combine", r"\bconsolidates\b": "combines",
    r"\bconsolidated\b": "combined",
    r"\bamalgamate\b": "mix", r"\bamalgamates\b": "mixes",
    r"\bsynthesize\b": "combine", r"\bsynthesizes\b": "combines",
    r"\bsynthesized\b": "combined",
    r"\bformulate\b": "plan", r"\bformulated\b": "planned",
    r"\bhypothesize\b": "guess", r"\bhypothesized\b": "guessed",
    r"\bpostulate\b": "suggest", r"\bpostulated\b": "suggested",
    r"\btheorize\b": "guess", r"\btheorized\b": "guessed",
    r"\bspeculate\b": "guess", r"\bspeculated\b": "guessed",
    r"\bconjecture\b": "guess", r"\bconjectured\b": "guessed",
    r"\bpostulate\b": "suggest", r"\bposits\b": "says",
    r"\bposit\b": "say", r"\bproffers\b": "offers",
    r"\bproffer\b": "offer", r"\bproffered\b": "offered",
    r"\btender\b": "give", r"\btendered\b": "gave",
    r"\brender\b": "make", r"\brenders\b": "makes",
    r"\brendered\b": "made", r"\brendering\b": "making",
    r"\breconstitute\b": "rebuild", r"\breconstituted\b": "rebuilt",
    r"\breconfigure\b": "reset", r"\breconfigured\b": "reset",
    r"\brecalibrate\b": "adjust", r"\brecalibrated\b": "adjusted",
    r"\breinvigorate\b": "refresh", r"\breinvigorated\b": "refreshed",
    r"\brejuvenate\b": "refresh", r"\brejuvenated\b": "refreshed",
    r"\brevitalize\b": "refresh", r"\brevitalized\b": "refreshed",
    r"\bameliorate\b": "improve", r"\bameliorated\b": "improved",
    r"\bexacerbate\b": "worsen", r"\bexacerbated\b": "worsened",
    r"\baggravate\b": "worsen", r"\baggravated\b": "worsened",
    r"\bmitigate\b": "reduce", r"\bmitigated\b": "reduced",
    r"\bcurtail\b": "cut back", r"\bcurtailed\b": "cut back",
    r"\btruncate\b": "shorten", r"\btruncated\b": "shortened",
    r"\babbreviate\b": "shorten", r"\babbreviated\b": "shortened",
    r"\belucidate\b": "explain", r"\belucidated\b": "explained",
    r"\bexplicate\b": "explain", r"\bexplicated\b": "explained",
    r"\bexpound\b": "explain", r"\bexpounded\b": "explained",
    r"\bdelineate\b": "outline", r"\bdelineated\b": "outlined",
    r"\bdepict\b": "show", r"\bdepicted\b": "showed",
    r"\bportray\b": "show", r"\bportrayed\b": "showed",
    r"\bdepict\b": "show", r"\bdepiction\b": "image",
    r"\bcharacterize\b": "show", r"\bcharacterized\b": "showed",
    r"\bepitomize\b": "sum up", r"\bepitomized\b": "summed up",
    r"\bexemplify\b": "show", r"\bexemplified\b": "showed",
    r"\billustrate\b": "show", r"\billustrated\b": "showed",
    r"\billuminating\b": "helpful", r"\billuminates\b": "shows",
    r"\billuminate\b": "show",

    # ---- EXPANSION 2: Fancy adjectives ----
    r"\bubiquitous\b": "everywhere", r"\bomnipresent\b": "everywhere",
    r"\bpervasive\b": "widespread", r"\bprevalent\b": "common",
    r"\bpredominant\b": "main", r"\bparamount\b": "top",
    r"\bsupreme\b": "top", r"\bpreeminent\b": "top",
    r"\bforemost\b": "top", r"\bprincipal\b": "main",
    r"\bcardinal\b": "key", r"\bquintessential\b": "classic",
    r"\barchetypal\b": "classic", r"\bparadigmatic\b": "classic",
    r"\bexemplary\b": "great", r"\bexemplar\b": "example",
    r"\bcommendable\b": "good", r"\badmirable\b": "good",
    r"\bpraiseworthy\b": "good", r"\blaudable\b": "good",
    r"\bformidable\b": "tough", r"\bdaunting\b": "tough",
    r"\bintimidating\b": "scary", r"\bforbidding\b": "scary",
    r"\baustere\b": "plain", r"\bspartan\b": "plain",
    r"\bopulent\b": "rich", r"\baffluent\b": "rich",
    r"\bprosperous\b": "rich", r"\bwealthy\b": "rich",
    r"\bindigent\b": "poor", r"\bdestitute\b": "poor",
    r"\bimpoverished\b": "poor", r"\bpenurious\b": "poor",
    r"\blavish\b": "flashy", r"\bextravagant\b": "flashy",
    r"\bostentatious\b": "showy", r"\bflamboyant\b": "showy",
    r"\bgrandiose\b": "grand", r"\bmagnanimous\b": "kind",
    r"\bbenevolent\b": "kind", r"\bmalevolent\b": "evil",
    r"\bnefarious\b": "evil", r"\bheinous\b": "awful",
    r"\batrocious\b": "awful", r"\begregious\b": "awful",
    r"\bdetrimental\b": "harmful", r"\bdeleterious\b": "harmful",
    r"\bpernicious\b": "harmful", r"\bnoxious\b": "harmful",
    r"\bbaleful\b": "harmful", r"\binimical\b": "harmful",
    r"\bpropitious\b": "good", r"\bauspicious\b": "good",
    r"\bfortuitous\b": "lucky", r"\bprovidential\b": "lucky",
    r"\bserendipitous\b": "lucky", r"\bopportune\b": "timely",
    r"\binopportune\b": "bad timing", r"\buntimely\b": "bad timing",
    r"\bephemeral\b": "short-lived", r"\btransient\b": "brief",
    r"\btransitory\b": "brief", r"\bfleeting\b": "brief",
    r"\bperpetual\b": "endless", r"\bperennial\b": "endless",
    r"\binterminable\b": "endless", r"\binterminable\b": "endless",
    r"\bincessant\b": "nonstop", r"\bceaseless\b": "nonstop",
    r"\bunremitting\b": "nonstop", r"\brelentless\b": "nonstop",
    r"\bincessant\b": "nonstop", r"\bunwavering\b": "firm",
    r"\bsteadfast\b": "firm", r"\bstaunch\b": "firm",
    r"\bresolute\b": "firm", r"\btenacious\b": "stubborn",
    r"\bobstinate\b": "stubborn", r"\bintransigent\b": "stubborn",
    r"\brecalcitrant\b": "stubborn", r"\brefractory\b": "stubborn",
    r"\bcompliant\b": "obedient", r"\bobsequious\b": "too eager",
    r"\bservile\b": "too eager", r"\bsycophantic\b": "flattering",
    r"\bmeticulous\b": "careful", r"\bscrupulous\b": "careful",
    r"\bpunctilious\b": "careful", r"\bassiduous\b": "hard-working",
    r"\bdiligent\b": "hard-working", r"\bindefatigable\b": "tireless",
    r"\bubiquitous\b": "everywhere", r"\binnocuous\b": "harmless",
    r"\bbenign\b": "harmless", r"\bmalignant\b": "harmful",
    r"\bcandid\b": "honest", r"\bforthright\b": "direct",
    r"\bblunt\b": "direct", r"\bfrank\b": "honest",
    r"\bvehement\b": "fierce", r"\bfervent\b": "fierce",
    r"\bardent\b": "fierce", r"\bzealous\b": "eager",
    r"\bfervid\b": "fierce", r"\btorrid\b": "hot",
    r"\bfrigid\b": "cold", r"\bgelid\b": "cold",
    r"\bscorching\b": "hot", r"\bblistering\b": "hot",
    r"\binclement\b": "harsh", r"\bauspicious\b": "good",

    # ---- EXPANSION 3: Business jargon ----
    r"\bleverage\b": "use", r"\bleverages\b": "uses",
    r"\bleveraged\b": "used", r"\bleveraging\b": "using",
    r"\bsynergize\b": "team up", r"\bsynergies\b": "teamwork",
    r"\bsynergy\b": "teamwork", r"\bparadigm shift\b": "big change",
    r"\bparadigm shifts\b": "big changes",
    r"\bholistic\b": "whole", r"\bholistically\b": "as a whole",
    r"\bproactive\b": "ahead of things", r"\bproactively\b": "ahead of time",
    r"\breactive\b": "late", r"\bactionable\b": "usable",
    r"\bdeliverable\b": "result", r"\bdeliverables\b": "results",
    r"\bstakeholder\b": "person involved", r"\bstakeholders\b": "people involved",
    r"\bbuy-in\b": "support", r"\bideate\b": "brainstorm",
    r"\bideation\b": "brainstorming", r"\bsocialize\b": "share",
    r"\bsocialized\b": "shared", r"\bcircle back\b": "return to",
    r"\btouch base\b": "talk", r"\btouchpoint\b": "contact",
    r"\btouchpoints\b": "contacts", r"\bbandwidth\b": "time",
    r"\bbandwidth\b": "room", r"\bdeep dive\b": "close look",
    r"\bdeep dives\b": "close looks", r"\blow-hanging fruit\b": "easy wins",
    r"\bmove the needle\b": "make a difference",
    r"\bmoving the needle\b": "making a difference",
    r"\bboil the ocean\b": "overdo it",
    r"\bthink outside the box\b": "think creatively",
    r"\bpivot\b": "change course", r"\bpivoted\b": "changed course",
    r"\bdisrupt\b": "shake up", r"\bdisruptive\b": "game-changing",
    r"\bdisruption\b": "shake-up", r"\bempower\b": "give power to",
    r"\bempowers\b": "gives power to", r"\bempowered\b": "gave power to",
    r"\bempowerment\b": "freedom", r"\brightsize\b": "cut staff",
    r"\bdownsize\b": "cut staff", r"\bupskill\b": "train",
    r"\bupskilling\b": "training", r"\breskill\b": "retrain",
    r"\breskilling\b": "retraining", r"\bonboard\b": "welcome",
    r"\bonboarding\b": "welcome", r"\boffboard\b": "let go",
    r"\boffboarding\b": "letting go", r"\belevate\b": "lift",
    r"\belevates\b": "lifts", r"\belevated\b": "lifted",
    r"\belevating\b": "lifting", r"\bamplify\b": "boost",
    r"\bamplifies\b": "boosts", r"\bamplified\b": "boosted",
    r"\bamplifying\b": "boosting", r"\bscale\b": "grow",
    r"\bscales\b": "grows", r"\bscaled\b": "grew",
    r"\bscaling\b": "growing", r"\bscalable\b": "can grow",
    r"\bunicorn\b": "huge startup", r"\bunicorns\b": "huge startups",
    r"\bmoat\b": "edge", r"\bmoats\b": "edges",
    r"\bgrowth hacking\b": "fast growth tricks",
    r"\brunway\b": "money left", r"\bburn rate\b": "money spent",
    r"\bchurn\b": "customers leaving", r"\bchurn rate\b": "leaving rate",
    r"\bdrop-shipping\b": "selling on demand",
    r"\bbootstrapping\b": "self-funding",
    r"\bsweat equity\b": "work for shares",
    r"\bROI\b": "return", r"\bKPIs\b": "goals",
    r"\bKPIs\b": "targets", r"\bOKRs\b": "goals",

    # ---- EXPANSION 4: Academic nouns ----
    r"\bparadigm\b": "model", r"\bparadigms\b": "models",
    r"\bepistemology\b": "theory of knowledge",
    r"\bontology\b": "theory of being",
    r"\bhegemony\b": "control", r"\bhegemonic\b": "controlling",
    r"\bdiscourse\b": "talk", r"\bdiscourses\b": "talks",
    r"\bdiscursive\b": "talk-based", r"\bdiscursively\b": "through talk",
    r"\bideology\b": "beliefs", r"\bideologies\b": "beliefs",
    r"\bideological\b": "belief-based",
    r"\bideologically\b": "by belief",
    r"\bnexus\b": "link", r"\bnexuses\b": "links",
    r"\bpedagogy\b": "teaching", r"\bpedagogies\b": "teaching styles",
    r"\bpedagogical\b": "teaching-related",
    r"\bdidactic\b": "teaching", r"\bdidactically\b": "as a lesson",
    r"\bheuristic\b": "rule of thumb",
    r"\bheuristics\b": "rules of thumb",
    r"\baphorism\b": "saying", r"\baphorisms\b": "sayings",
    r"\baxiom\b": "rule", r"\baxioms\b": "rules",
    r"\bcorollary\b": "result", r"\bcorollaries\b": "results",
    r"\bpostulate\b": "assumption", r"\bpostulates\b": "assumptions",
    r"\bprecept\b": "rule", r"\bprecepts\b": "rules",
    r"\btenet\b": "belief", r"\btenets\b": "beliefs",
    r"\bdogma\b": "fixed belief", r"\bdogmas\b": "fixed beliefs",
    r"\brationale\b": "reason", r"\brationales\b": "reasons",
    r"\bcriterion\b": "test", r"\bcriteria\b": "tests",
    r"\bparameter\b": "limit", r"\bparameters\b": "limits",
    r"\bcorrelation\b": "link", r"\bcorrelations\b": "links",
    r"\bcausation\b": "cause", r"\bempirical\b": "real-world",
    r"\bempirically\b": "in real life", r"\ba priori\b": "by reasoning",
    r"\ba posteriori\b": "from experience",
    r"\bde facto\b": "in practice", r"\bde jure\b": "by law",
    r"\bipso facto\b": "by that fact",
    r"\bper se\b": "in itself", r"\bquid pro quo\b": "trade",
    r"\bad hominem\b": "personal attack",
    r"\bcarte blanche\b": "free rein",
    r"\bfait accompli\b": "done deal",
    r"\bstatus quo\b": "current state",
    r"\bcoup de grace\b": "final blow",
    r"\bcasus belli\b": "reason for war",
    r"\bmodus operandi\b": "way of working",
    r"\braison d'etre\b": "reason to be",
    r"\btour de force\b": "great feat",
    r"\bde rigueur\b": "required",
    r"\bavant-garde\b": "cutting-edge",
    r"\bbonafide\b": "real", r"\bbona fide\b": "real",
    r"\bprima facie\b": "at first look",
    r"\bnon sequitur\b": "doesn't follow",
    r"\bred herring\b": "distraction",
    r"\bstraw man\b": "weak argument",
    r"\bslippery slope\b": "chain reaction",

    # ---- EXPANSION 5: Formal phrases ----
    r"\bin light of\b": "given", r"\bin view of\b": "given",
    r"\bin the wake of\b": "after",
    r"\bin the aftermath of\b": "after",
    r"\bby virtue of\b": "because of",
    r"\bby dint of\b": "through",
    r"\bowing to\b": "because of",
    r"\bthanks to\b": "because of",
    r"\bin the midst of\b": "during",
    r"\bat the behest of\b": "at the request of",
    r"\bat the discretion of\b": "as decided by",
    r"\bin the absence of\b": "without",
    r"\bin the presence of\b": "with",
    r"\bin the face of\b": "facing",
    r"\bin the event of\b": "if",
    r"\bin the case of\b": "for",
    r"\bin the matter of\b": "for",
    r"\bwith a view to\b": "to",
    r"\bwith an eye to\b": "to",
    r"\bwith the aim of\b": "to",
    r"\bwith the goal of\b": "to",
    r"\bfor the sake of\b": "for",
    r"\bon behalf of\b": "for",
    r"\bin favor of\b": "for",
    r"\bin opposition to\b": "against",
    r"\bin accordance with\b": "following",
    r"\bin compliance with\b": "following",
    r"\bin keeping with\b": "matching",
    r"\bin line with\b": "matching",
    r"\bcontrary to\b": "against",
    r"\bopposite to\b": "against",
    r"\bprior to\b": "before", r"\bpost to\b": "after",
    r"\bsubsequent to\b": "after",
    r"\bantecedent to\b": "before",
    r"\bconcurrent with\b": "alongside",
    r"\bsimultaneous with\b": "alongside",
    r"\bcommensurate with\b": "matching",
    r"\bproportionate to\b": "matching",
    r"\bdisproportionate to\b": "not matching",
    r"\birrespective of\b": "no matter",
    r"\bindependent of\b": "apart from",
    r"\bregardless of\b": "no matter",
    r"\bnotwithstanding\b": "even so",
    r"\bnotwithstanding that\b": "even so",
    r"\bprovided that\b": "if",
    r"\bproviding that\b": "if",
    r"\bassuming that\b": "if",
    r"\bgiven that\b": "since",
    r"\bconsidering that\b": "since",
    r"\bseeing that\b": "since",
    r"\binsofar as\b": "as far as",
    r"\bto the extent that\b": "as much as",
    r"\bin as much as\b": "as far as",
    r"\bforasmuch as\b": "since",
    r"\bwhereby\b": "where", r"\bwherein\b": "where",
    r"\bwhereof\b": "of which", r"\bwhereupon\b": "then",
    r"\bhereby\b": "by this", r"\bherein\b": "in this",
    r"\bhereof\b": "of this", r"\bhereto\b": "to this",
    r"\bheretofore\b": "before now", r"\bhereinafter\b": "below",
    r"\bthereof\b": "of that", r"\btherein\b": "in that",
    r"\bthereto\b": "to that", r"\bthereupon\b": "then",
    r"\btherewith\b": "with that", r"\bthereafter\b": "after that",
    r"\bthereby\b": "by that", r"\bwhereas\b": "while",
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
    r"__P\d+__",
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
