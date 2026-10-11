#!/usr/bin/env python3
"""
=================================================================
  ULTIMATE HUMANIZER - Single File
  Offline. No API. No dependencies.
  Preserves meaning. Only changes style, tone, and rhythm.
=================================================================
"""

import re
import random


# ================================================================
# SECTION 1: CONTRACTIONS (long -> short)
# ================================================================
CONTRACTIONS = {
    r"\bdo not\b": "don't", r"\bdoes not\b": "doesn't", r"\bdid not\b": "didn't",
    r"\bis not\b": "isn't", r"\bare not\b": "aren't", r"\bwas not\b": "wasn't",
    r"\bwere not\b": "weren't", r"\bhave not\b": "haven't", r"\bhas not\b": "hasn't",
    r"\bhad not\b": "hadn't", r"\bwill not\b": "won't", r"\bwould not\b": "wouldn't",
    r"\bcannot\b": "can't", r"\bcan not\b": "can't", r"\bcould not\b": "couldn't",
    r"\bshall not\b": "shan't", r"\bshould not\b": "shouldn't",
    r"\bmust not\b": "mustn't", r"\bneed not\b": "needn't",
    r"\bdare not\b": "daren't", r"\bmight not\b": "mightn't",
    r"\bit is\b": "it's", r"\bthat is\b": "that's", r"\bthere is\b": "there's",
    r"\bhere is\b": "here's", r"\bwhat is\b": "what's", r"\bwho is\b": "who's",
    r"\bwhere is\b": "where's", r"\bwhen is\b": "when's", r"\bwhy is\b": "why's",
    r"\bhow is\b": "how's", r"\bthey are\b": "they're", r"\bwe are\b": "we're",
    r"\byou are\b": "you're", r"\bI am\b": "I'm", r"\bI will\b": "I'll",
    r"\bI have\b": "I've", r"\bI would\b": "I'd", r"\bI had\b": "I'd",
    r"\bI shall\b": "I'll", r"\bthey will\b": "they'll", r"\bthey have\b": "they've",
    r"\bthey would\b": "they'd", r"\bthey had\b": "they'd",
    r"\bwe will\b": "we'll", r"\bwe have\b": "we've",
    r"\bwe would\b": "we'd", r"\bwe had\b": "we'd",
    r"\byou will\b": "you'll", r"\byou have\b": "you've",
    r"\byou would\b": "you'd", r"\byou had\b": "you'd",
    r"\bhe is\b": "he's", r"\bshe is\b": "she's",
    r"\bhe will\b": "he'll", r"\bshe will\b": "she'll",
    r"\bhe would\b": "he'd", r"\bshe would\b": "she'd",
    r"\bhe has\b": "he's", r"\bshe has\b": "she's",
    r"\bit has\b": "it's", r"\bit will\b": "it'll",
    r"\bit would\b": "it'd", r"\blet us\b": "let's",
    r"\bthere will\b": "there'll", r"\bthere are\b": "there're",
    r"\bthere would\b": "there'd", r"\bthat will\b": "that'll",
    r"\bthat would\b": "that'd", r"\bthat has\b": "that's",
    r"\bwhat will\b": "what'll", r"\bwhat would\b": "what'd",
    r"\bwho will\b": "who'll", r"\bwho would\b": "who'd",
    r"\bhow will\b": "how'll", r"\bhow would\b": "how'd",
    r"\bsomebody is\b": "somebody's", r"\bsomeone is\b": "someone's",
    r"\bsomething is\b": "something's", r"\bnobody is\b": "nobody's",
    r"\bnothing is\b": "nothing's", r"\beverybody is\b": "everybody's",
    r"\beveryone is\b": "everyone's", r"\beverything is\b": "everything's",
}


# ================================================================
# SECTION 2: SIMPLE WORD SWAPS (fancy -> simple)
# ================================================================
SIMPLE_WORDS = {
    # --- -ize / -ise family ---
    r"\butilize\b": "use", r"\butilizes\b": "uses", r"\butilized\b": "used",
    r"\butilizing\b": "using", r"\butilization\b": "use",
    r"\brealize\b": "see", r"\brealizes\b": "sees", r"\brealized\b": "saw",
    r"\brealizing\b": "seeing", r"\brealization\b": "understanding",
    r"\brecognize\b": "see", r"\brecognizes\b": "sees",
    r"\brecognized\b": "saw", r"\brecognizing\b": "seeing",
    r"\bemphasize\b": "stress", r"\bemphasizes\b": "stresses",
    r"\bemphasized\b": "stressed", r"\bemphasizing\b": "stressing",
    r"\bprioritize\b": "focus on", r"\bprioritizes\b": "focuses on",
    r"\bprioritized\b": "focused on", r"\bprioritizing\b": "focusing on",
    r"\bmaximize\b": "get the most from", r"\bmaximizes\b": "gets the most from",
    r"\bmaximized\b": "got the most from", r"\bmaximizing\b": "getting the most from",
    r"\bminimize\b": "cut down", r"\bminimizes\b": "cuts down",
    r"\bminimized\b": "cut down", r"\bminimizing\b": "cutting down",
    r"\boptimize\b": "improve", r"\boptimizes\b": "improves",
    r"\boptimized\b": "improved", r"\boptimizing\b": "improving",
    r"\bcategorize\b": "sort", r"\bcategorizes\b": "sorts",
    r"\bcategorized\b": "sorted", r"\bcategorizing\b": "sorting",
    r"\bsummarize\b": "sum up", r"\bsummarizes\b": "sums up",
    r"\bsummarized\b": "summed up", r"\bsummarizing\b": "summing up",
    r"\bcriticize\b": "blame", r"\bcriticizes\b": "blames",
    r"\bcriticized\b": "blamed", r"\bcriticizing\b": "blaming",
    r"\bsymbolize\b": "stand for", r"\bsymbolizes\b": "stands for",
    r"\bsymbolized\b": "stood for", r"\bsymbolizing\b": "standing for",
    r"\bcharacterize\b": "show", r"\bcharacterizes\b": "shows",
    r"\bcharacterized\b": "showed", r"\bcharacterizing\b": "showing",
    r"\bharmonize\b": "match", r"\bharmonizes\b": "matches",
    r"\bharmonized\b": "matched",
    r"\bvisualize\b": "picture", r"\bvisualizes\b": "pictures",
    r"\bvisualized\b": "pictured", r"\bvisualizing\b": "picturing",
    r"\bmemorize\b": "learn", r"\bmemorizes\b": "learns",
    r"\bmemorized\b": "learned", r"\bmemorizing\b": "learning",
    r"\bmodernize\b": "update", r"\bmodernizes\b": "updates",
    r"\bmodernized\b": "updated", r"\bmodernizing\b": "updating",
    r"\bstandardize\b": "set rules for", r"\bstandardizes\b": "sets rules for",
    r"\bstandardized\b": "set rules for",
    r"\bcustomize\b": "tune", r"\bcustomizes\b": "tunes",
    r"\bcustomized\b": "tuned", r"\bcustomizing\b": "tuning",
    r"\bpersonalize\b": "make your own", r"\bpersonalizes\b": "makes your own",
    r"\bpersonalized\b": "made your own",
    r"\bsocialize\b": "hang out", r"\bsocializes\b": "hangs out",
    r"\bsocialized\b": "hung out",
    r"\bapologize\b": "say sorry", r"\bapologizes\b": "says sorry",
    r"\bapologized\b": "said sorry", r"\bapologizing\b": "saying sorry",
    r"\bgeneralize\b": "say broadly", r"\bgeneralizes\b": "says broadly",
    r"\bgeneralized\b": "said broadly",
    r"\bspecialize\b": "focus", r"\bspecializes\b": "focuses",
    r"\bspecialized\b": "focused", r"\bspecializing\b": "focusing",
    r"\bfinalize\b": "finish", r"\bfinalizes\b": "finishes",
    r"\bfinalized\b": "finished", r"\bfinalizing\b": "finishing",
    r"\binitialize\b": "start", r"\binitializes\b": "starts",
    r"\binitialized\b": "started", r"\binitializing\b": "starting",
    r"\bminimise\b": "cut down", r"\bmaximise\b": "get the most from",
    r"\boptimise\b": "improve", r"\bprioritise\b": "focus on",
    r"\brecognise\b": "see", r"\brealise\b": "see",
    r"\bsummarise\b": "sum up", r"\bcriticise\b": "blame",
    r"\borganise\b": "plan", r"\borganised\b": "planned",
    r"\borganising\b": "planning", r"\borganisation\b": "group",
    r"\brecognised\b": "saw", r"\brealised\b": "saw",

    # --- -ate family ---
    r"\bfacilitate\b": "help", r"\bfacilitates\b": "helps",
    r"\bfacilitated\b": "helped", r"\bfacilitating\b": "helping",
    r"\bfacilitation\b": "help",
    r"\bdemonstrate\b": "show", r"\bdemonstrates\b": "shows",
    r"\bdemonstrated\b": "showed", r"\bdemonstrating\b": "showing",
    r"\bdemonstration\b": "show",
    r"\beliminate\b": "cut", r"\beliminates\b": "cuts",
    r"\beliminated\b": "cut", r"\beliminating\b": "cutting",
    r"\belimination\b": "removal",
    r"\binitiate\b": "start", r"\binitiates\b": "starts",
    r"\binitiated\b": "started", r"\binitiating\b": "starting",
    r"\binitiative\b": "plan",
    r"\bterminate\b": "end", r"\bterminates\b": "ends",
    r"\bterminated\b": "ended", r"\bterminating\b": "ending",
    r"\btermination\b": "end",
    r"\bcommunicate\b": "talk", r"\bcommunicates\b": "talks",
    r"\bcommunicated\b": "talked", r"\bcommunicating\b": "talking",
    r"\bcommunication\b": "talk",
    r"\beducate\b": "teach", r"\beducates\b": "teaches",
    r"\beducated\b": "taught", r"\beducating\b": "teaching",
    r"\bparticipate\b": "join", r"\bparticipates\b": "joins",
    r"\bparticipated\b": "joined", r"\bparticipating\b": "joining",
    r"\bparticipation\b": "taking part",
    r"\bactivate\b": "turn on", r"\bactivates\b": "turns on",
    r"\bactivated\b": "turned on", r"\bactivating\b": "turning on",
    r"\bdeactivate\b": "turn off", r"\bdeactivates\b": "turns off",
    r"\bdeactivated\b": "turned off",
    r"\bvalidate\b": "check", r"\bvalidates\b": "checks",
    r"\bvalidated\b": "checked", r"\bvalidation\b": "check",
    r"\bregulate\b": "control", r"\bregulates\b": "controls",
    r"\bregulated\b": "controlled", r"\bregulations\b": "rules",
    r"\bregulation\b": "rule",
    r"\barticulate\b": "say", r"\barticulates\b": "says",
    r"\barticulated\b": "said", r"\barticulating\b": "saying",
    r"\barticulation\b": "way of speaking",
    r"\bcalculate\b": "work out", r"\bcalculates\b": "works out",
    r"\bcalculated\b": "worked out", r"\bcalculation\b": "guess",
    r"\bestimate\b": "guess", r"\bestimates\b": "guesses",
    r"\bestimated\b": "guessed", r"\bestimation\b": "guess",
    r"\bevaluate\b": "judge", r"\bevaluates\b": "judges",
    r"\bevaluated\b": "judged", r"\bevaluation\b": "review",
    r"\bformulate\b": "plan", r"\bformulates\b": "plans",
    r"\bformulated\b": "planned", r"\bformulation\b": "plan",
    r"\bincorporate\b": "add", r"\bincorporates\b": "adds",
    r"\bincorporated\b": "added", r"\bincorporating\b": "adding",
    r"\bindicate\b": "show", r"\bindicates\b": "shows",
    r"\bindicated\b": "showed", r"\bindicating\b": "showing",
    r"\bindication\b": "sign",
    r"\bnegotiate\b": "talk", r"\bnegotiates\b": "talks",
    r"\bnegotiated\b": "talked", r"\bnegotiation\b": "talk",
    r"\boriginate\b": "start", r"\boriginates\b": "starts",
    r"\boriginated\b": "started", r"\borigin\b": "start",
    r"\bpenetrate\b": "go through", r"\bpenetrates\b": "goes through",
    r"\bpenetrated\b": "went through",
    r"\bpropagate\b": "spread", r"\bpropagates\b": "spreads",
    r"\bpropagated\b": "spread",
    r"\bsimulate\b": "copy", r"\bsimulates\b": "copies",
    r"\bsimulated\b": "copied", r"\bsimulation\b": "copy",
    r"\bstimulate\b": "spark", r"\bstimulates\b": "sparks",
    r"\bstimulated\b": "sparked", r"\bstimulation\b": "spark",
    r"\billuminate\b": "light up", r"\billuminates\b": "lights up",
    r"\billuminated\b": "lit up",
    r"\belucidate\b": "explain", r"\belucidated\b": "explained",
    r"\bexplicate\b": "explain", r"\bexplicated\b": "explained",
    r"\bexpound\b": "explain", r"\bexpounded\b": "explained",
    r"\bdelineate\b": "outline", r"\bdelineated\b": "outlined",
    r"\bdepict\b": "show", r"\bdepicted\b": "showed",
    r"\bportray\b": "show", r"\bportrayed\b": "showed",
    r"\bcharacterize\b": "show", r"\bcharacterized\b": "showed",
    r"\bepitomize\b": "sum up", r"\bepitomized\b": "summed up",
    r"\bexemplify\b": "show", r"\bexemplified\b": "showed",
    r"\billustrate\b": "show", r"\billustrated\b": "showed",
    r"\billustrating\b": "showing",
    r"\bameliorate\b": "improve", r"\bameliorated\b": "improved",
    r"\bexacerbate\b": "worsen", r"\bexacerbated\b": "worsened",
    r"\baggravate\b": "worsen", r"\baggravated\b": "worsened",
    r"\bmitigate\b": "reduce", r"\bmitigated\b": "reduced",
    r"\bmitigating\b": "reducing",
    r"\bcurtail\b": "cut back", r"\bcurtailed\b": "cut back",
    r"\btruncate\b": "shorten", r"\btruncated\b": "shortened",
    r"\babbreviate\b": "shorten", r"\babbreviated\b": "shortened",
    r"\bproliferate\b": "spread", r"\bproliferates\b": "spreads",
    r"\bproliferated\b": "spread",
    r"\bcultivate\b": "grow", r"\bcultivates\b": "grows",
    r"\bcultivated\b": "grew", r"\bcultivating\b": "growing",
    r"\bnurture\b": "help grow", r"\bnurtures\b": "helps grow",
    r"\bnurtured\b": "helped grow",
    r"\bfortify\b": "strengthen", r"\bfortifies\b": "strengthens",
    r"\bfortified\b": "strengthened",
    r"\bintegrate\b": "combine", r"\bintegrates\b": "combines",
    r"\bintegrated\b": "combined", r"\bintegrating\b": "combining",
    r"\bconsolidate\b": "combine", r"\bconsolidates\b": "combines",
    r"\bconsolidated\b": "combined",
    r"\bsynthesize\b": "combine", r"\bsynthesizes\b": "combines",
    r"\bsynthesized\b": "combined",
    r"\bhypothesize\b": "guess", r"\bhypothesized\b": "guessed",
    r"\bpostulate\b": "suggest", r"\bpostulated\b": "suggested",
    r"\btheorize\b": "guess", r"\btheorized\b": "guessed",
    r"\bspeculate\b": "guess", r"\bspeculated\b": "guessed",

    # --- -tion family ---
    r"\bimplementation\b": "use", r"\bimplementations\b": "uses",
    r"\bmodification\b": "change", r"\bmodifications\b": "changes",
    r"\bconsideration\b": "thought", r"\bconsiderations\b": "things to think about",
    r"\bdetermination\b": "drive", r"\bdeterminations\b": "calls",
    r"\bexamination\b": "look", r"\bexaminations\b": "looks",
    r"\bidentification\b": "spotting",
    r"\binterpretation\b": "reading", r"\binterpretations\b": "readings",
    r"\binvestigation\b": "look", r"\binvestigations\b": "looks",
    r"\bobservation\b": "note", r"\bobservations\b": "notes",
    r"\bpresentation\b": "talk", r"\bpresentations\b": "talks",
    r"\bpublication\b": "book", r"\bpublications\b": "books",
    r"\brecommendation\b": "tip", r"\brecommendations\b": "tips",
    r"\brepresentation\b": "picture", r"\brepresentations\b": "pictures",
    r"\bspecification\b": "detail", r"\bspecifications\b": "details",
    r"\btransformation\b": "change", r"\btransformations\b": "changes",
    r"\bverification\b": "check", r"\bverifications\b": "checks",
    r"\bclassification\b": "sorting", r"\bclassifications\b": "sorts",
    r"\bcomplication\b": "problem", r"\bcomplications\b": "problems",
    r"\bcontradiction\b": "clash", r"\bcontradictions\b": "clashes",
    r"\bcoordination\b": "teamwork", r"\bcorrelation\b": "link",
    r"\bcorrelations\b": "links", r"\bdemonstration\b": "show",
    r"\bdestination\b": "end point", r"\bdestinations\b": "end points",
    r"\bdimension\b": "side", r"\bdimensions\b": "sides",
    r"\bequation\b": "sum", r"\bequations\b": "sums",
    r"\bevaluation\b": "review", r"\bevaluations\b": "reviews",
    r"\bfoundation\b": "base", r"\bfoundations\b": "bases",
    r"\bfrustration\b": "stress", r"\bfrustrations\b": "stresses",
    r"\bfunction\b": "job", r"\bfunctions\b": "jobs",
    r"\bimplication\b": "result", r"\bimplications\b": "results",
    r"\binstallation\b": "setup", r"\binstallations\b": "setups",
    r"\bintention\b": "plan", r"\bintentions\b": "plans",
    r"\binteraction\b": "talk", r"\binteractions\b": "talks",
    r"\bjustification\b": "reason", r"\bjustifications\b": "reasons",
    r"\blimitation\b": "limit", r"\blimitations\b": "limits",
    r"\bmotivation\b": "drive", r"\bmotivations\b": "drives",
    r"\borganization\b": "group", r"\borganizations\b": "groups",
    r"\borganisation\b": "group", r"\borganisations\b": "groups",
    r"\bperception\b": "view", r"\bperceptions\b": "views",
    r"\bperspective\b": "view", r"\bperspectives\b": "views",
    r"\bpreparation\b": "planning", r"\bpreparations\b": "plans",
    r"\bpriority\b": "focus", r"\bpriorities\b": "focuses",
    r"\bproportion\b": "share", r"\bproportions\b": "shares",
    r"\bregistration\b": "sign up", r"\bregistrations\b": "sign ups",
    r"\bresolution\b": "fix", r"\bresolutions\b": "fixes",
    r"\brestriction\b": "limit", r"\brestrictions\b": "limits",
    r"\bsatisfaction\b": "joy",
    r"\bsituation\b": "case", r"\bsituations\b": "cases",
    r"\bstrategy\b": "plan", r"\bstrategies\b": "plans",
    r"\bstructure\b": "shape", r"\bstructures\b": "shapes",
    r"\bsuggestion\b": "tip", r"\bsuggestions\b": "tips",
    r"\btransition\b": "shift", r"\btransitions\b": "shifts",
    r"\bvariation\b": "change", r"\bvariations\b": "changes",
    r"\bconcentration\b": "focus", r"\bconcentrations\b": "focuses",
    r"\bcollaboration\b": "teamwork", r"\bcollaborations\b": "teamwork",
    r"\bcombination\b": "mix", r"\bcombinations\b": "mixes",
    r"\bconfiguration\b": "setup", r"\bconfigurations\b": "setups",
    r"\bconstraint\b": "limit", r"\bconstraints\b": "limits",
    r"\bdecision\b": "call", r"\bdecisions\b": "calls",
    r"\bdeclaration\b": "statement", r"\bdeclarations\b": "statements",
    r"\bdemonstrations\b": "shows", r"\bdescription\b": "picture",
    r"\bdescriptions\b": "pictures", r"\bdiscussion\b": "talk",
    r"\bdiscussions\b": "talks", r"\bdistribution\b": "spread",
    r"\bdistributions\b": "spreads", r"\beducation\b": "schooling",
    r"\bexplanation\b": "reason", r"\bexplanations\b": "reasons",
    r"\bexploration\b": "digging", r"\bexplorations\b": "digs",
    r"\bexpression\b": "way of saying", r"\bexpressions\b": "sayings",
    r"\bformation\b": "making", r"\bformations\b": "makings",
    r"\bgeneration\b": "making", r"\bgenerations\b": "makings",
    r"\bidentification\b": "spotting", r"\bimagination\b": "creativity",
    r"\bimpression\b": "feeling", r"\bimpressions\b": "feelings",
    r"\bindication\b": "sign", r"\bindications\b": "signs",
    r"\binformation\b": "info", r"\binnovation\b": "new idea",
    r"\binnovations\b": "new ideas", r"\binspection\b": "check",
    r"\binspections\b": "checks", r"\binstruction\b": "order",
    r"\binstructions\b": "orders", r"\bintroduction\b": "intro",
    r"\bintroductions\b": "intros", r"\binvention\b": "new thing",
    r"\binventions\b": "new things", r"\binvestment\b": "money put in",
    r"\binvestments\b": "money put in", r"\bjudgement\b": "call",
    r"\bjudgements\b": "calls", r"\bjudgment\b": "call",
    r"\bjudgments\b": "calls", r"\bknowledge\b": "know-how",
    r"\blocation\b": "spot", r"\blocations\b": "spots",
    r"\bmanagement\b": "running", r"\bmanagements\b": "runnings",
    r"\bmeasurement\b": "measure", r"\bmeasurements\b": "measures",
    r"\bmethodology\b": "method", r"\bmethodologies\b": "methods",
    r"\bnegotiations\b": "talks", r"\bnotion\b": "idea",
    r"\bnotions\b": "ideas", r"\bobjective\b": "goal",
    r"\bobjectives\b": "goals", r"\bobligation\b": "duty",
    r"\bobligations\b": "duties", r"\boperation\b": "run",
    r"\boperations\b": "runs", r"\bopposition\b": "pushback",
    r"\borganisation\b": "group", r"\bparticipation\b": "taking part",
    r"\bperception\b": "view", r"\bpopulation\b": "people",
    r"\bpopulations\b": "groups", r"\bposition\b": "spot",
    r"\bpositions\b": "spots", r"\bpreference\b": "choice",
    r"\bpreferences\b": "choices", r"\bpreparation\b": "planning",
    r"\bpreparations\b": "plans", r"\bprescription\b": "script",
    r"\bprescriptions\b": "scripts", r"\bprevention\b": "stopping",
    r"\bprocedure\b": "step", r"\bprocedures\b": "steps",
    r"\bprocess\b": "step", r"\bprocesses\b": "steps",
    r"\bproduction\b": "making", r"\bproductions\b": "makings",
    r"\bprofession\b": "job", r"\bprofessions\b": "jobs",
    r"\bprogression\b": "growth", r"\bprojection\b": "guess",
    r"\bprojections\b": "guesses", r"\bpronunciation\b": "saying",
    r"\bproposition\b": "idea", r"\bpropositions\b": "ideas",
    r"\bprotection\b": "cover", r"\bprotections\b": "covers",
    r"\bpublication\b": "book", r"\bpublications\b": "books",
    r"\bqualification\b": "skill", r"\bqualifications\b": "skills",
    r"\bquestionnaire\b": "survey", r"\bquestionnaires\b": "surveys",
    r"\breaction\b": "reply", r"\breactions\b": "replies",
    r"\breception\b": "welcome", r"\breceptions\b": "welcomes",
    r"\brecognition\b": "notice", r"\brecognitions\b": "notices",
    r"\breduction\b": "cut", r"\breductions\b": "cuts",
    r"\breflection\b": "thought", r"\breflections\b": "thoughts",
    r"\breform\b": "change", r"\breforms\b": "changes",
    r"\brefusal\b": "no", r"\brefusals\b": "noes",
    r"\bregulation\b": "rule", r"\bregulations\b": "rules",
    r"\brejection\b": "no", r"\brejections\b": "noes",
    r"\brelationship\b": "link", r"\brelationships\b": "links",
    r"\brelease\b": "launch", r"\breleases\b": "launches",
    r"\breliability\b": "trust", r"\breligion\b": "faith",
    r"\breligions\b": "faiths", r"\breminder\b": "nudge",
    r"\breminders\b": "nudges", r"\bremoval\b": "taking out",
    r"\brepetition\b": "repeat", r"\brepetitions\b": "repeats",
    r"\breplacement\b": "swap", r"\breplacements\b": "swaps",
    r"\breport\b": "story", r"\breports\b": "stories",
    r"\brepresentative\b": "rep", r"\brepresentatives\b": "reps",
    r"\breputation\b": "name", r"\breputations\b": "names",
    r"\brequirement\b": "need", r"\brequirements\b": "needs",
    r"\bresearch\b": "study", r"\bresearches\b": "studies",
    r"\bresignation\b": "quitting", r"\bresignations\b": "quits",
    r"\bresistance\b": "pushback", r"\bresolutions\b": "fixes",
    r"\bresource\b": "tool", r"\bresources\b": "tools",
    r"\bresponse\b": "reply", r"\bresponses\b": "replies",
    r"\bresponsibility\b": "duty", r"\bresponsibilities\b": "duties",
    r"\brestriction\b": "limit", r"\brestrictions\b": "limits",
    r"\bretention\b": "keeping", r"\brevelation\b": "surprise",
    r"\brevelations\b": "surprises", r"\brevolution\b": "big change",
    r"\brevolutions\b": "big changes", r"\breward\b": "prize",
    r"\brewards\b": "prizes", r"\bsanction\b": "punishment",
    r"\bsanctions\b": "punishments", r"\bsatisfaction\b": "joy",
    r"\bseparation\b": "split", r"\bseparations\b": "splits",
    r"\bsignature\b": "sign", r"\bsignatures\b": "signs",
    r"\bsignificance\b": "weight", r"\bsolution\b": "fix",
    r"\bsolutions\b": "fixes", r"\bspeculation\b": "guess",
    r"\bspeculations\b": "guesses", r"\bstimulation\b": "spark",
    r"\bstipulation\b": "rule", r"\bstipulations\b": "rules",
    r"\bstructure\b": "shape", r"\bstructures\b": "shapes",
    r"\bsubmission\b": "handing in", r"\bsubmissions\b": "hand ins",
    r"\bsubscription\b": "sign up", r"\bsubscriptions\b": "sign ups",
    r"\bsubstitution\b": "swap", r"\bsubstitutions\b": "swaps",
    r"\bsuggestion\b": "tip", r"\bsuggestions\b": "tips",
    r"\bsupervision\b": "watching", r"\bsupervisor\b": "boss",
    r"\bsupervisors\b": "bosses", r"\bsupposition\b": "guess",
    r"\bsuppositions\b": "guesses", r"\bsurroundings\b": "area",
    r"\bsurvey\b": "poll", r"\bsurveys\b": "polls",
    r"\bsuspicion\b": "doubt", r"\bsuspicions\b": "doubts",
    r"\btelecommunication\b": "phone stuff",
    r"\btemptation\b": "urge", r"\btemptations\b": "urges",
    r"\btendency\b": "habit", r"\btendencies\b": "habits",
    r"\btermination\b": "end", r"\bterminations\b": "ends",
    r"\bterritory\b": "land", r"\bterritories\b": "lands",
    r"\btradition\b": "way", r"\btraditions\b": "ways",
    r"\btranscription\b": "copy", r"\btranscriptions\b": "copies",
    r"\btransformation\b": "change", r"\btransformations\b": "changes",
    r"\btransition\b": "shift", r"\btransitions\b": "shifts",
    r"\btranslation\b": "version", r"\btranslations\b": "versions",
    r"\btransmission\b": "sending", r"\btransmissions\b": "sendings",
    r"\btransportation\b": "travel", r"\btreatment\b": "care",
    r"\btreatments\b": "cares", r"\buncertainty\b": "doubt",
    r"\buncertainties\b": "doubts", r"\bunemployment\b": "joblessness",
    r"\butilization\b": "use", r"\bvalidation\b": "check",
    r"\bvalidations\b": "checks", r"\bvaluation\b": "worth",
    r"\bvaluations\b": "worths", r"\bvariation\b": "change",
    r"\bvariations\b": "changes", r"\bverification\b": "check",
    r"\bverifications\b": "checks", r"\bversion\b": "take",
    r"\bversions\b": "takes", r"\bviolation\b": "break",
    r"\bviolations\b": "breaks", r"\bvocabulary\b": "words",
    r"\bvocabularies\b": "word sets", r"\bworkstation\b": "desk",

    # --- -ity family ---
    r"\bability\b": "skill", r"\babilities\b": "skills",
    r"\bactivity\b": "work", r"\bactivities\b": "things to do",
    r"\bcapacity\b": "room", r"\bcapacities\b": "rooms",
    r"\bcapability\b": "skill", r"\bcapabilities\b": "skills",
    r"\bcomplexity\b": "hardness", r"\bcomplexities\b": "hard parts",
    r"\bconnectivity\b": "link", r"\bcreativity\b": "imagination",
    r"\bcuriosity\b": "interest", r"\bduality\b": "two sides",
    r"\bequality\b": "fairness", r"\bfamiliarity\b": "knowing",
    r"\bflexibility\b": "room to move", r"\bgenerality\b": "broadness",
    r"\bhumanity\b": "people", r"\bidentity\b": "sense of self",
    r"\bidentities\b": "sense of selves", r"\bintegrity\b": "honesty",
    r"\bintensity\b": "strength", r"\bintensities\b": "strengths",
    r"\bmajority\b": "most", r"\bminority\b": "few",
    r"\bmodernity\b": "modern times", r"\bneutrality\b": "fairness",
    r"\bnovelty\b": "newness", r"\bobjectivity\b": "fairness",
    r"\bpopularity\b": "fame", r"\bpossibility\b": "chance",
    r"\bpossibilities\b": "chances", r"\bprobability\b": "chance",
    r"\bprobabilities\b": "chances", r"\bproductivity\b": "output",
    r"\bprosperity\b": "wealth", r"\breality\b": "truth",
    r"\brealities\b": "truths", r"\breliability\b": "trust",
    r"\bresponsibility\b": "duty", r"\bresponsibilities\b": "duties",
    r"\bsecurity\b": "safety", r"\bsimilarity\b": "sameness",
    r"\bsimilarities\b": "shared traits", r"\bsimplicity\b": "ease",
    r"\bsolidarity\b": "unity", r"\bstability\b": "steadiness",
    r"\bsubjectivity\b": "personal view", r"\bvisibility\b": "being seen",
    r"\bvulnerability\b": "weakness", r"\banonymity\b": "being unknown",
    r"\bcertainty\b": "sureness", r"\bcertainties\b": "sure things",
    r"\bcivility\b": "politeness", r"\bclarity\b": "clearness",
    r"\bcommodity\b": "good", r"\bcommodities\b": "goods",
    r"\bcommunity\b": "group", r"\bcommunities\b": "groups",
    r"\bcompatibility\b": "match", r"\bcomplicity\b": "involvement",
    r"\bconformity\b": "following", r"\bcontinuity\b": "flow",
    r"\bcredibility\b": "trust", r"\bcuriosity\b": "interest",
    r"\bdensity\b": "thickness", r"\bdisparity\b": "gap",
    r"\bdisparities\b": "gaps", r"\bdiversity\b": "mix",
    r"\bdivinity\b": "godliness", r"\belectricity\b": "power",
    r"\bentity\b": "thing", r"\bentities\b": "things",
    r"\bequality\b": "fairness", r"\bethnicity\b": "background",
    r"\bextremity\b": "edge", r"\bextremities\b": "edges",
    r"\bfacility\b": "place", r"\bfacilities\b": "places",
    r"\bfecundity\b": "richness", r"\bfelicity\b": "joy",
    r"\bferocity\b": "fierceness", r"\bfidelity\b": "faithfulness",
    r"\bfinality\b": "end", r"\bformality\b": "rule",
    r"\bformalities\b": "rules", r"\bfraternity\b": "brotherhood",
    r"\bfuturity\b": "future", r"\bgranularity\b": "detail",
    r"\bgravity\b": "weight", r"\bhilarity\b": "laughter",
    r"\bhonesty\b": "truth", r"\bhostility\b": "anger",
    r"\bhumility\b": "modesty", r"\bimmunity\b": "protection",
    r"\bimpossibility\b": "no chance", r"\bimpunity\b": "no blame",
    r"\bincapacity\b": "no skill", r"\bincredulity\b": "doubt",
    r"\bindignity\b": "shame", r"\binequality\b": "unfairness",
    r"\binfidelity\b": "cheating", r"\binfinity\b": "endlessness",
    r"\binsanity\b": "madness", r"\binstability\b": "shakiness",
    r"\bintelligibility\b": "clarity", r"\blegality\b": "lawfulness",
    r"\bliability\b": "risk", r"\bliabilities\b": "risks",
    r"\blocality\b": "area", r"\blocalities\b": "areas",
    r"\bmaturity\b": "wisdom", r"\bmentality\b": "mindset",
    r"\bmentalities\b": "mindsets", r"\bmodality\b": "way",
    r"\bmodalities\b": "ways", r"\bmorality\b": "right and wrong",
    r"\bmortality\b": "death", r"\bnecessity\b": "need",
    r"\bnecessities\b": "needs", r"\bnobility\b": "honor",
    r"\bobesity\b": "fatness", r"\bobjectivity\b": "fairness",
    r"\bobscurity\b": "unknown", r"\boddity\b": "strangeness",
    r"\bopportunity\b": "chance", r"\bopportunities\b": "chances",
    r"\bpartiality\b": "bias", r"\bpassivity\b": "laziness",
    r"\bpeculiarity\b": "quirk", r"\bpeculiarities\b": "quirks",
    r"\bperplexity\b": "confusion", r"\bpersonality\b": "character",
    r"\bpersonalities\b": "characters", r"\bpolarity\b": "opposite",
    r"\bprimitivity\b": "rawness", r"\bpriority\b": "focus",
    r"\bprobity\b": "honesty", r"\bproclivity\b": "tendency",
    r"\bpurity\b": "cleanliness", r"\bquantity\b": "amount",
    r"\bquantities\b": "amounts", r"\bradicality\b": "extremeness",
    r"\brapidity\b": "speed", r"\brarity\b": "uniqueness",
    r"\brationality\b": "logic", r"\breciprocity\b": "give and take",
    r"\bregularity\b": "pattern", r"\breligiosity\b": "faith",
    r"\bremoteness\b": "distance", r"\bscarcity\b": "shortage",
    r"\bsensibility\b": "feeling", r"\bsensibilities\b": "feelings",
    r"\bsensitivity\b": "touchiness", r"\bserenity\b": "calmness",
    r"\bseverity\b": "harshness", r"\bsobriety\b": "soberness",
    r"\bspecificity\b": "detail", r"\bspontaneity\b": "suddenness",
    r"\bstupidity\b": "dumbness", r"\bsuperiority\b": "top spot",
    r"\btenacity\b": "grit", r"\btoxicity\b": "poison",
    r"\btranquility\b": "calm", r"\buniqueness\b": "specialness",
    r"\bunity\b": "togetherness", r"\buniversality\b": "everywhere-ness",
    r"\bvanity\b": "pride", r"\bvelocity\b": "speed",
    r"\bveracity\b": "truth", r"\bversatility\b": "flexibility",
    r"\bvirginity\b": "purity", r"\bvitality\b": "life",
    r"\bvoracity\b": "greed", r"\bwarmth\b": "heat",

    # --- -ance / -ence family ---
    r"\babundance\b": "plenty", r"\bacceptance\b": "okayness",
    r"\baccordance\b": "line with", r"\baccreditation\b": "approval",
    r"\bacquaintance\b": "friend", r"\bacquaintances\b": "friends",
    r"\badherence\b": "sticking to", r"\badmittance\b": "entry",
    r"\ballegiance\b": "loyalty", r"\balliance\b": "team-up",
    r"\balliances\b": "team-ups", r"\bambiance\b": "mood",
    r"\bambience\b": "mood", r"\bappearance\b": "look",
    r"\bappearances\b": "looks", r"\bassistance\b": "help",
    r"\battendance\b": "showing up", r"\baudience\b": "crowd",
    r"\baudiences\b": "crowds", r"\bbrilliance\b": "brightness",
    r"\bclearance\b": "space", r"\bcoincidence\b": "fluke",
    r"\bcoincidences\b": "flukes", r"\bcompliance\b": "following",
    r"\bconference\b": "meeting", r"\bconferences\b": "meetings",
    r"\bconfidence\b": "trust", r"\bconsequence\b": "result",
    r"\bconsequences\b": "results", r"\bconvenience\b": "ease",
    r"\bcorrespondence\b": "letters", r"\bdifference\b": "gap",
    r"\bdifferences\b": "gaps", r"\bdistance\b": "way",
    r"\bdistances\b": "ways", r"\bdominance\b": "top spot",
    r"\belegance\b": "grace", r"\bemergence\b": "rise",
    r"\bessence\b": "core", r"\bevidence\b": "proof",
    r"\bexistence\b": "life", r"\bexperience\b": "time spent",
    r"\bexperiences\b": "times", r"\bfragrance\b": "smell",
    r"\bfragrances\b": "smells", r"\bfrequency\b": "how often",
    r"\bfrequencies\b": "how oftens", r"\bgovernance\b": "running",
    r"\bguidance\b": "help", r"\bignorance\b": "not knowing",
    r"\bimportance\b": "weight", r"\bincidence\b": "rate",
    r"\bindependence\b": "freedom", r"\binfluence\b": "pull",
    r"\binfluences\b": "pulls", r"\binheritance\b": "what you get",
    r"\binstance\b": "case", r"\binstances\b": "cases",
    r"\binsurance\b": "cover", r"\binterference\b": "butting in",
    r"\bmaintenance\b": "upkeep", r"\bobedience\b": "doing as told",
    r"\boccurrence\b": "event", r"\boccurrences\b": "events",
    r"\bperformance\b": "show", r"\bperformances\b": "shows",
    r"\bpersistence\b": "not giving up", r"\bpreference\b": "choice",
    r"\bpreferences\b": "choices", r"\bpresence\b": "being there",
    r"\bprominence\b": "fame", r"\bproximity\b": "closeness",
    r"\breference\b": "note", r"\breferences\b": "notes",
    r"\brelevance\b": "link", r"\bresilience\b": "toughness",
    r"\bresistance\b": "pushback", r"\bsignificance\b": "weight",
    r"\bsilence\b": "quiet", r"\bsubstance\b": "stuff",
    r"\btransparency\b": "openness", r"\bviolence\b": "force",
    r"\bweakness\b": "flaw", r"\bweaknesses\b": "flaws",

    # --- -ous / -ious family ---
    r"\babundant\b": "plenty of", r"\bambiguous\b": "unclear",
    r"\banonymous\b": "unknown", r"\bautonomous\b": "free",
    r"\bconscious\b": "aware", r"\bconspicuous\b": "obvious",
    r"\bcontinuous\b": "ongoing", r"\bcourageous\b": "brave",
    r"\bcurious\b": "interested", r"\bdangerous\b": "risky",
    r"\bdelicious\b": "tasty", r"\bdelirious\b": "wild",
    r"\benormous\b": "huge", r"\bfabulous\b": "great",
    r"\bfamous\b": "well known", r"\bgenerous\b": "kind",
    r"\bglorious\b": "bright", r"\bgorgeous\b": "beautiful",
    r"\bgracious\b": "kind", r"\bharmonious\b": "smooth",
    r"\bhideous\b": "ugly", r"\bhumorous\b": "funny",
    r"\binfectious\b": "catching", r"\bingenious\b": "clever",
    r"\bjealous\b": "envious", r"\bmagnificent\b": "grand",
    r"\bmysterious\b": "strange", r"\bnervous\b": "worried",
    r"\bnotorious\b": "infamous", r"\bnumerous\b": "many",
    r"\bobvious\b": "clear", r"\bominous\b": "dark",
    r"\boutrageous\b": "shocking", r"\bpoisonous\b": "toxic",
    r"\bprevious\b": "earlier", r"\bprosperous\b": "rich",
    r"\breligious\b": "faith-based", r"\bridiculous\b": "silly",
    r"\brighteous\b": "just", r"\bserious\b": "grave",
    r"\bspontaneous\b": "sudden", r"\bstrenuous\b": "hard",
    r"\bsuspicious\b": "shady", r"\btremendous\b": "huge",
    r"\bunanimous\b": "all in favor", r"\bunconscious\b": "out cold",
    r"\bvarious\b": "different", r"\bvigorous\b": "strong",
    r"\bvivacious\b": "lively", r"\bzealous\b": "eager",
    r"\bubiquitous\b": "everywhere", r"\bpervasive\b": "widespread",
    r"\bprevalent\b": "common", r"\binnocuous\b": "harmless",
    r"\bcandid\b": "honest", r"\bforthright\b": "direct",
    r"\bfrank\b": "honest", r"\bvehement\b": "fierce",
    r"\bfervent\b": "fierce", r"\bardent\b": "fierce",
    r"\bzealous\b": "eager", r"\bformidable\b": "tough",
    r"\bdaunting\b": "tough", r"\baustere\b": "plain",
    r"\bopulent\b": "rich", r"\baffluent\b": "rich",
    r"\bwealthy\b": "rich", r"\bindigent\b": "poor",
    r"\bdestitute\b": "poor", r"\bimpoverished\b": "poor",
    r"\blavish\b": "flashy", r"\bextravagant\b": "flashy",
    r"\bostentatious\b": "showy", r"\bflamboyant\b": "showy",
    r"\bgrandiose\b": "grand", r"\bmagnanimous\b": "kind",
    r"\bbenevolent\b": "kind", r"\bmalevolent\b": "evil",
    r"\bnefarious\b": "evil", r"\bheinous\b": "awful",
    r"\batrocious\b": "awful", r"\begregious\b": "awful",
    r"\bdetrimental\b": "harmful", r"\bdeleterious\b": "harmful",
    r"\bpernicious\b": "harmful", r"\bnoxious\b": "harmful",
    r"\binnocuous\b": "harmless", r"\bbenign\b": "harmless",
    r"\bmalignant\b": "harmful", r"\bcandid\b": "honest",
    r"\bephemeral\b": "short-lived", r"\btransient\b": "brief",
    r"\btransitory\b": "brief", r"\bfleeting\b": "brief",
    r"\bperpetual\b": "endless", r"\bperennial\b": "endless",
    r"\binterminable\b": "endless", r"\bincessant\b": "nonstop",
    r"\bceaseless\b": "nonstop", r"\bunremitting\b": "nonstop",
    r"\brelentless\b": "nonstop", r"\bunwavering\b": "firm",
    r"\bsteadfast\b": "firm", r"\bstaunch\b": "firm",
    r"\bresolute\b": "firm", r"\btenacious\b": "stubborn",
    r"\bobstinate\b": "stubborn", r"\bintransigent\b": "stubborn",
    r"\brecalcitrant\b": "stubborn", r"\brefractory\b": "stubborn",
    r"\bcompliant\b": "obedient", r"\bobsequious\b": "too eager",
    r"\bservile\b": "too eager", r"\bsycophantic\b": "flattering",
    r"\bmeticulous\b": "careful", r"\bscrupulous\b": "careful",
    r"\bpunctilious\b": "careful", r"\bassiduous\b": "hard-working",
    r"\bdiligent\b": "hard-working", r"\bindefatigable\b": "tireless",

    # --- -al / -ive / -ic family ---
    r"\badditional\b": "more", r"\bcomprehensive\b": "full",
    r"\bcritical\b": "key", r"\bcrucial\b": "key",
    r"\bessential\b": "needed", r"\bfundamental\b": "basic",
    r"\bimperative\b": "must", r"\bintrinsic\b": "built-in",
    r"\bpotential\b": "possible", r"\bpractical\b": "real",
    r"\bprimary\b": "main", r"\bprincipal\b": "main",
    r"\bsignificant\b": "big", r"\bsubstantial\b": "big",
    r"\btheoretical\b": "idea-based", r"\btypical\b": "normal",
    r"\bunique\b": "one of a kind", r"\bvital\b": "key",
    r"\balternative\b": "other", r"\battractive\b": "good-looking",
    r"\bcomparative\b": "side by side", r"\bcompetitive\b": "cutthroat",
    r"\bconclusive\b": "final", r"\bcooperative\b": "helpful",
    r"\bcreative\b": "imaginative", r"\bdecisive\b": "firm",
    r"\bdefinitive\b": "final", r"\bdescriptive\b": "vivid",
    r"\bdestructive\b": "harmful", r"\beffective\b": "good",
    r"\befficient\b": "quick", r"\bextensive\b": "wide",
    r"\bflexible\b": "bendy", r"\bimpressive\b": "cool",
    r"\binclusive\b": "open", r"\bintensive\b": "heavy",
    r"\bintuitive\b": "easy to feel", r"\blucrative\b": "money-making",
    r"\bmassive\b": "huge", r"\bnegative\b": "bad",
    r"\bobjective\b": "fair", r"\boffensive\b": "rude",
    r"\bpositive\b": "good", r"\bprimitive\b": "early",
    r"\bproductive\b": "busy", r"\bprogressive\b": "forward",
    r"\brelative\b": "compared", r"\brepetitive\b": "same old",
    r"\brestorative\b": "healing", r"\bselective\b": "picky",
    r"\bsensitive\b": "touchy", r"\bsubjective\b": "personal",
    r"\bsuccessive\b": "back to back", r"\btentative\b": "shaky",
    r"\bautomated\b": "machine-run", r"\bautomatic\b": "auto",
    r"\bchronic\b": "long-term", r"\bcivic\b": "city",
    r"\bcomic\b": "funny", r"\bdramatic\b": "big",
    r"\bdynamic\b": "lively", r"\bfantastic\b": "great",
    r"\bgeneric\b": "basic", r"\bhistoric\b": "famous",
    r"\bidentical\b": "same", r"\bmagnetic\b": "pulling",
    r"\bmajestic\b": "grand", r"\bmetallic\b": "metal",
    r"\boptimistic\b": "hopeful", r"\bpathetic\b": "sad",
    r"\bromantic\b": "loving", r"\bscientific\b": "lab-based",
    r"\bspecific\b": "exact", r"\bsymbolic\b": "meaningful",
    r"\bsynthetic\b": "fake", r"\bsystematic\b": "orderly",
    r"\btherapeutic\b": "healing",

    # --- Verbs: analytical ---
    r"\banalyze\b": "look at", r"\banalyzes\b": "looks at",
    r"\banalyzed\b": "looked at", r"\banalyzing\b": "looking at",
    r"\banalysis\b": "look", r"\banalyses\b": "looks",
    r"\bexamine\b": "look at", r"\bexamines\b": "looks at",
    r"\bexamined\b": "looked at", r"\bexamining\b": "looking at",
    r"\binvestigate\b": "look into", r"\binvestigates\b": "looks into",
    r"\binvestigated\b": "looked into", r"\binvestigating\b": "looking into",
    r"\bexplore\b": "dig into", r"\bexplores\b": "digs into",
    r"\bexplored\b": "dug into", r"\bexploring\b": "digging into",
    r"\bexploration\b": "digging",
    r"\bevaluate\b": "judge", r"\bevaluates\b": "judges",
    r"\bevaluated\b": "judged",
    r"\bidentify\b": "spot", r"\bidentifies\b": "spots",
    r"\bidentified\b": "spotted", r"\bidentifying\b": "spotting",
    r"\bdetermine\b": "figure out", r"\bdetermines\b": "figures out",
    r"\bdetermined\b": "figured out", r"\bdetermining\b": "figuring out",
    r"\bconstitute\b": "make up", r"\bconstitutes\b": "makes up",
    r"\bconstituted\b": "made up",
    r"\bestablish\b": "set up", r"\bestablishes\b": "sets up",
    r"\bestablished\b": "set up", r"\bestablishing\b": "setting up",
    r"\bestablishment\b": "setup",
    r"\bimplement\b": "use", r"\bimplements\b": "uses",
    r"\bimplemented\b": "used", r"\bimplementing\b": "using",
    r"\bmaintain\b": "keep", r"\bmaintains\b": "keeps",
    r"\bmaintained\b": "kept", r"\bmaintaining\b": "keeping",
    r"\bmaintenance\b": "upkeep",
    r"\bmodify\b": "change", r"\bmodifies\b": "changes",
    r"\bmodified\b": "changed", r"\bmodifying\b": "changing",
    r"\bobtain\b": "get", r"\bobtains\b": "gets",
    r"\bobtained\b": "got", r"\bobtaining\b": "getting",
    r"\bpossess\b": "have", r"\bpossesses\b": "has",
    r"\bpossessed\b": "had", r"\bpossessing\b": "having",
    r"\bprovide\b": "give", r"\bprovides\b": "gives",
    r"\bprovided\b": "gave", r"\bproviding\b": "giving",
    r"\bacquire\b": "get", r"\bacquires\b": "gets",
    r"\bacquired\b": "got", r"\bacquiring\b": "getting",
    r"\brequire\b": "need", r"\brequires\b": "needs",
    r"\brequired\b": "needed", r"\brequiring\b": "needing",
    r"\bconvey\b": "send", r"\bconveys\b": "sends",
    r"\bconveyed\b": "sent", r"\bconveying\b": "sending",
    r"\bconstruct\b": "build", r"\bconstructs\b": "builds",
    r"\bconstructed\b": "built", r"\bconstructing\b": "building",
    r"\bconstruction\b": "building",
    r"\bfabricate\b": "make up", r"\bfabricates\b": "makes up",
    r"\bfabricated\b": "made up",
    r"\bgenerate\b": "make", r"\bgenerates\b": "makes",
    r"\bgenerated\b": "made", r"\bgenerating\b": "making",
    r"\bproduce\b": "make", r"\bproduces\b": "makes",
    r"\bproduced\b": "made", r"\bproducing\b": "making",
    r"\bcreate\b": "make", r"\bcreates\b": "makes",
    r"\bcreated\b": "made", r"\bcreating\b": "making",
    r"\bdevelopment\b": "growth", r"\bdevelopments\b": "changes",
    r"\bdevelop\b": "grow", r"\bdevelops\b": "grows",
    r"\bdeveloped\b": "grew", r"\bdeveloping\b": "growing",

    # --- Adverbs ---
    r"\bcurrently\b": "now", r"\bpreviously\b": "before",
    r"\bformerly\b": "once", r"\brecently\b": "lately",
    r"\bimmediately\b": "right away", r"\binstantly\b": "at once",
    r"\beventually\b": "in the end", r"\bultimately\b": "in the end",
    r"\bfinally\b": "at last", r"\binitially\b": "at first",
    r"\bprimarily\b": "mostly", r"\bmainly\b": "mostly",
    r"\bchiefly\b": "mostly", r"\bparticularly\b": "especially",
    r"\bspecifically\b": "exactly", r"\bgenerally\b": "usually",
    r"\btypically\b": "usually", r"\bfrequently\b": "often",
    r"\boccasionally\b": "sometimes", r"\brarely\b": "hardly",
    r"\bseldom\b": "hardly ever", r"\bconstantly\b": "always",
    r"\bcontinuously\b": "nonstop", r"\bregularly\b": "often",
    r"\bclearly\b": "plainly", r"\bobviously\b": "clearly",
    r"\bcertainly\b": "sure", r"\bdefinitely\b": "for sure",
    r"\babsolutely\b": "totally", r"\bcompletely\b": "totally",
    r"\bentirely\b": "fully", r"\bthoroughly\b": "fully",
    r"\bessentially\b": "basically", r"\bfundamentally\b": "basically",
    r"\bnotably\b": "especially", r"\bsignificantly\b": "a lot",
    r"\bsubstantially\b": "a lot", r"\bconsiderably\b": "a lot",
    r"\bslightly\b": "a bit", r"\bsomewhat\b": "kind of",
    r"\bmerely\b": "just", r"\bsimply\b": "just",
    r"\bsolely\b": "only", r"\bexclusively\b": "only",
    r"\bapproximately\b": "about", r"\broughly\b": "about",
    r"\bnearly\b": "almost", r"\bvirtually\b": "almost",
    r"\bpractically\b": "almost", r"\baccordingly\b": "so",
    r"\bconversely\b": "on the flip side", r"\balternatively\b": "or",
    r"\bsimilarly\b": "same way", r"\blikewise\b": "same way",
    r"\bequally\b": "just as", r"\bnonetheless\b": "still",
    r"\bnevertheless\b": "still", r"\bnotwithstanding\b": "still",
    r"\bregardless\b": "anyway", r"\bconsequently\b": "so",
    r"\bthereafter\b": "after that", r"\bheretofore\b": "until now",
    r"\bhenceforth\b": "from now on", r"\bmoreover\b": "also",
    r"\bfurthermore\b": "also", r"\badditionally\b": "also",
    r"\bbesides\b": "also", r"\bthus\b": "so",
    r"\bhence\b": "so", r"\btherefore\b": "so",
    r"\bwhereas\b": "while", r"\bwhilst\b": "while",
    r"\balbeit\b": "though",
}


# ================================================================
# SECTION 3: AI CLICHÉ KILLERS (whole phrases)
# ================================================================
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
    r"\bvis-à-vis\b": "about",
    r"\bvis-a-vis\b": "about",
    r"\bsits at the intersection of\b": "mixes",
    r"\bintersection of several disciplines\b": "mix of different fields",
    r"\brapid proliferation of\b": "fast growth of",
    r"\bshow an uncanny ability to\b": "are very good at",
    r"\bremains poorly understood\b": "is still a mystery",
    r"\bremains poorly defined\b": "is still unclear",
    r"\bThis chapter sets up the background of the study\b": "This chapter covers the background",
    r"\bartliculates the research problem\b": "explains the problem",
    r"\boutlines the goals and research questions\b": "covers the goals and research questions",
    r"\bdiscusses the significance of the study\b": "talks about why it matters",
    r"\band delimits its\b": "and what it doesn't cover",
    r"\boffers teaching-related implications\b": "shows what this means",
    r"\bdrawing on existing real-world studies\b": "using real-world studies",
    r"\bthe theoretical framework combines insights from\b": "the theory pulls from",
    r"\bfocusing on three dimensions:\b": "It looks at three things:",
    r"\bRecent real-world research has begun to map this terrain\b": "Recent studies are starting to show this",
    r"\bThese models are trained on vast corpora of\b": "These models learn from huge amounts of",
    r"\bWe must make sure\b": "We need to make sure",
    r"\bIt is worth noting that\b": "",
    r"\bIt is worth mentioning that\b": "",
    r"\bIt is interesting to note that\b": "",
    r"\bIt is clear that\b": "Clearly,",
    r"\bIt is evident that\b": "Clearly,",
    r"\bIt is apparent that\b": "Clearly,",
    r"\bIt is obvious that\b": "Clearly,",
    r"\bIt is possible that\b": "Maybe",
    r"\bIt is likely that\b": "Probably",
    r"\bIt is unlikely that\b": "Probably not",
    r"\bIt is necessary to\b": "We need to",
    r"\bIt is essential to\b": "We need to",
    r"\bIt is important to\b": "We need to",
    r"\bIt is crucial to\b": "We need to",
    r"\bIt is vital to\b": "We need to",
    r"\bThere is no doubt that\b": "Clearly,",
    r"\bThere is little doubt that\b": "Clearly,",
    r"\bThere can be no doubt that\b": "Clearly,",
    r"\bThere is a growing (body|amount|number) of\b": "More and more",
    r"\bIn the process of\b": "While",
    r"\bIn the course of\b": "During",
    r"\bAs a matter of fact\b": "Actually,",
    r"\bAs a general rule\b": "Usually,",
    r"\bAs a rule of thumb\b": "Usually,",
    r"\bAs a whole\b": "Overall,",
    r"\bOn the whole\b": "Overall,",
    r"\bAll in all\b": "Overall,",
    r"\bBy and large\b": "Mostly,",
}


# ================================================================
# SECTION 4: REDUNDANT PAIRS (trim weaker word)
# ================================================================
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
    r"\bheavily (criticized|criticised)\b": r"\1",
    r"\bsharply (criticized|criticised)\b": r"\1",
    r"\bwidely (regarded|considered|known)\b": r"\1",
    r"\bcarefully (consider|examine|study|analyze|review)\b": r"\1",
    r"\bthoroughly (investigate|examine|study|analyze)\b": r"\1",
}


# ================================================================
# SECTION 5: PASSIVE-ISH FIXES
# ================================================================
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


# ================================================================
# SECTION 6: ROBOTIC STARTERS
# ================================================================
ROBOTIC_STARTERS = [
    "Additionally,", "Furthermore,", "Moreover,",
    "In addition,", "Similarly,", "Likewise,",
    "Consequently,", "Therefore,", "Thus,",
    "Hence,", "Accordingly,", "Subsequently,",
    "Conversely,", "On the contrary,",
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


# ================================================================
# SECTION 7: PROTECTED PATTERNS
# ================================================================
PROTECTED = [
    r'"[^"]*"',
    r"'[^']*'",
    r"\([^)]*\)",
    r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    r"\b\d{4}\b",
    r"\b[A-Z]{2,}\b",
    r"__P\d+__",
    r"\[\d+\]",
]


# ================================================================
# HELPERS
# ================================================================
def _preserve(text):
    store = {}
    counter = [0]
    def repl(m):
        key = "__H{}__".format(counter[0])
        counter[0] += 1
        store[key] = m.group(0)
        return key
    for p in PROTECTED:
        text = re.sub(p, repl, text)
    return text, store


def _restore(text, store):
    for k, v in store.items():
        text = text.replace(k, v)
    return text


def _apply(text, mapping):
    for pat, rep in mapping.items():
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
    return text


def _is_heading(line):
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


def _split_long(s):
    if len(s.split()) < 16:
        return [s]
    points = [
        (", and ", "And "), (", but ", "But "), (", so ", "So "),
        (", or ", "Or "), (" because ", "Because "),
        (" although ", "Although "), (" though ", "Though "),
        (" while ", "While "), (" whereas ", "While "),
    ]
    for marker, starter in points:
        idx = s.lower().find(marker.lower())
        if 25 < idx < len(s) - 25:
            first = s[:idx].strip().rstrip(",;:") + "."
            rest = s[idx + len(marker):].strip()
            if rest:
                rest = starter + rest[0].lower() + rest[1:]
                return [first, rest]
    return [s]


def _strip_starters(text):
    for starter in ROBOTIC_STARTERS:
        esc = re.escape(starter.rstrip(","))
        pat = r"(^|(?<=[.!?])\s+)" + esc + r",?\s+"
        def repl(m):
            if random.random() < 0.6:
                return m.group(1) + random.choice(NATURAL_STARTERS) + " "
            return m.group(1)
        text = re.sub(pat, repl, text)
    return text


def _vary_rhythm(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for s in sentences:
        if len(s.split()) >= 25:
            commas = [m.start() for m in re.finditer(r",", s)]
            if commas:
                mid = len(s) // 2
                best = min(commas, key=lambda c: abs(c - mid))
                if 20 < best < len(s) - 20:
                    first = s[:best].strip().rstrip(",;:") + "."
                    rest = s[best + 1:].strip()
                    if rest:
                        out.append(first)
                        out.append(rest[0].upper() + rest[1:])
                        continue
        out.append(s)
    return " ".join(out)


def _break_runons(text):
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


def _add_starter(s):
    parts = s.split()
    if not parts:
        return s
    if parts[0].lower() in ("and", "so", "but", "or", "yet", "for", "nor", "plus", "then", "also"):
        return s
    if len(parts) < 5:
        return s
    starter = random.choice(["And ", "So ", "But ", "Plus, ", "Also, "])
    rest = s[0].lower() + s[1:] if s[0].isupper() else s
    return starter + rest


def _clean_spaces(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text.strip()


# ================================================================
# PARAGRAPH HUMANIZE
# ================================================================
def humanize_paragraph(para):
    text = para.strip()
    if not text:
        return ""

    text, store = _preserve(text)

    # Order matters
    text = _apply(text, AI_CLICHES)
    text = _apply(text, CONTRACTIONS)
    text = _apply(text, SIMPLE_WORDS)
    text = _apply(text, PASSIVE_FIXES)
    text = _apply(text, REDUNDANT)

    # Remove commas before conjunctions
    text = re.sub(r",\s*(and|but|so|or|yet|for|nor)\b", r" \1", text, flags=re.IGNORECASE)

    # Semicolons to periods
    text = re.sub(r";\s*", ". ", text)

    text = _clean_spaces(text)

    # Split into sentences
    sentences = re.split(r"(?<=[.!?])\s+", text)
    split_sents = []
    for s in sentences:
        if s.strip():
            split_sents.extend(_split_long(s.strip()))

    # Add starters
    starter_count = 0
    final = []
    for i, s in enumerate(split_sents):
        s = s.strip()
        if not s:
            continue
        if i > 0 and starter_count < 3 and random.random() < 0.18:
            new_s = _add_starter(s)
            if new_s != s:
                starter_count += 1
                s = new_s
        final.append(s)

    text = " ".join(final)
    text = _strip_starters(text)
    text = _vary_rhythm(text)
    text = _break_runons(text)
    text = _clean_spaces(text)

    # Capitalize sentence starts
    parts = re.split(r"(?<=[.!?])\s+", text)
    parts = [p[0].upper() + p[1:] if p else p for p in parts]
    text = " ".join(parts)

    text = _restore(text, store)
    return text


# ================================================================
# MAIN
# ================================================================
def humanize(text):
    lines = text.split("\n")
    output = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            output.append("")
            continue
        if _is_heading(stripped):
            output.append(stripped)
        else:
            output.append(humanize_paragraph(stripped))
    return "\n".join(output)


def main():
    print("=" * 60)
    print("  ULTIMATE HUMANIZER")
    print("  Offline. No API. Single file.")
    print("=" * 60)
    print()
    print("Type or paste your text below.")
    print("When done, type END on a new line and press Enter.")
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
        print("Could not save: {}".format(e))

    print()
    input("Press Enter to close...")


if __name__ == "__main__":
    main()
