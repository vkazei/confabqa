# Validation pass — Confabulation Atlas v1 question set

You are validating gold answers for a small LLM-calibration benchmark. The benchmark probes whether a model's hidden states encode whether it is about to answer correctly versus confabulate. A wrong gold answer in this set silently corrupts both the probe target and the same-model judge that downstream code uses. Be rigorous; cite authoritative sources.

## Task

For each numbered item below, decide one of four statuses for its gold answer:

- `verified` — the gold answer is correct. Provide one authoritative citation URL.
- `corrected` — the gold answer is wrong. Provide the correct answer, acceptable phrasing variants, an authoritative citation URL, and a one-sentence explanation of the original error.
- `flagged` — the question is ambiguous, has multiple defensible answers depending on interpretation, or the source-of-truth is disputed. Keep the gold but note the concern.
- `rejected` — the question is ill-posed or cannot have a single objective correct answer. Recommend dropping it.

## Required output format

Return **only** a single JSON array, no prose before or after, no markdown fences. Each element has this shape:

```json
[
  {"id": "sci_wk_01", "status": "verified", "citation": "https://example.org/...", "notes": null,
   "corrected_answer": null, "corrected_alternatives": null},
  {"id": "sci_wk_02", "status": "corrected", "citation": "https://example.org/...",
   "corrected_answer": "the actually-correct answer string",
   "corrected_alternatives": ["alt1", "alt2"],
   "notes": "Original gold said X; the authoritative source confirms Y."},
  {"id": "sci_wk_03", "status": "flagged", "citation": "https://example.org/...",
   "corrected_answer": null, "corrected_alternatives": null,
   "notes": "Both X and Y are commonly cited as the answer; the source-of-truth depends on interpretation."},
  {"id": "sci_wk_04", "status": "rejected", "citation": null,
   "corrected_answer": null, "corrected_alternatives": null,
   "notes": "The question presupposes a fact that is not established; recommend dropping."}
]
```

Include every item in the input below. Do not omit any IDs. Do not include items not present below.

## Items to validate (133 total)

### sci_wk_01
- **Question:** Who won the Nobel Prize in Physics in 1918?
- **Gold answer:** 'Max Planck'
- **Acceptable alternatives:** 'Planck'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 1918-11-13
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/1918/

### sci_wk_02
- **Question:** Who won the Nobel Prize in Physics in 1965?
- **Gold answer:** 'Sin-Itiro Tomonaga, Julian Schwinger, and Richard Feynman'
- **Acceptable alternatives:** 'Feynman, Schwinger, Tomonaga', 'Feynman', 'Schwinger and Feynman and Tomonaga'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 1965-10-21
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/1965/

### sci_wk_03
- **Question:** What instrument first directly detected gravitational waves in 2015?
- **Gold answer:** 'LIGO'
- **Acceptable alternatives:** 'Laser Interferometer Gravitational-Wave Observatory'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 2015-09-14
- **Provenance (claimed):** https://www.ligo.caltech.edu/page/ligo-gw150914

### sci_wk_04
- **Question:** Who first observed cosmic microwave background radiation in 1964?
- **Gold answer:** 'Arno Penzias and Robert Wilson'
- **Acceptable alternatives:** 'Penzias and Wilson'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 1964-05-20
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Cosmic_microwave_background

### sci_wk_05
- **Question:** Who won the Nobel Prize in Chemistry in 1954?
- **Gold answer:** 'Linus Pauling'
- **Acceptable alternatives:** 'Pauling'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 1954-11-03
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/1954/

### sci_wk_06
- **Question:** What is the speed of light in a vacuum, in meters per second?
- **Gold answer:** '299792458'
- **Acceptable alternatives:** '299,792,458', '3 x 10^8', 'approximately 300,000,000'
- **Domain / category:** science / well_known
- **Answer date (claimed):** timeless
- **Provenance (claimed):** https://physics.nist.gov/cgi-bin/cuu/Value?c

### sci_wk_07
- **Question:** Who won the Nobel Prize in Physics in 1921?
- **Gold answer:** 'Albert Einstein'
- **Acceptable alternatives:** 'Einstein'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 1921-11-09
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/1921/

### sci_wk_08
- **Question:** Who won the Nobel Prize in Chemistry in 1911?
- **Gold answer:** 'Marie Curie'
- **Acceptable alternatives:** 'Curie', 'Madame Curie'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 1911-11-07
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/1911/

### sci_wk_09
- **Question:** At which laboratory was the Higgs boson discovered in 2012?
- **Gold answer:** 'CERN'
- **Acceptable alternatives:** 'LHC', 'Large Hadron Collider', "CERN's Large Hadron Collider"
- **Domain / category:** science / well_known
- **Answer date (claimed):** 2012-07-04
- **Provenance (claimed):** https://home.cern/topics/higgs-boson

### sci_wk_10
- **Question:** Who won the Nobel Prize in Physics in 2013?
- **Gold answer:** 'Francois Englert and Peter Higgs'
- **Acceptable alternatives:** 'Higgs and Englert', 'Peter Higgs', 'Higgs'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 2013-10-08
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/2013/

### sci_wk_11
- **Question:** Who won the Nobel Prize in Chemistry in 2020?
- **Gold answer:** 'Emmanuelle Charpentier and Jennifer Doudna'
- **Acceptable alternatives:** 'Charpentier and Doudna', 'Doudna and Charpentier'
- **Domain / category:** science / well_known
- **Answer date (claimed):** 2020-10-07
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/2020/

### sci_ob_01
- **Question:** Who won the Nobel Prize in Chemistry in 2001?
- **Gold answer:** 'William S. Knowles, Ryoji Noyori, and K. Barry Sharpless'
- **Acceptable alternatives:** 'Knowles, Noyori, Sharpless'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 2001-10-10
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/2001/

### sci_ob_02
- **Question:** Who won the Nobel Prize in Chemistry in 1991?
- **Gold answer:** 'Richard R. Ernst'
- **Acceptable alternatives:** 'Ernst', 'Richard Ernst'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1991-10-16
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/1991/

### sci_ob_03
- **Question:** Who won the Nobel Prize in Physics in 2003?
- **Gold answer:** 'Alexei Abrikosov, Vitaly Ginzburg, and Anthony Leggett'
- **Acceptable alternatives:** 'Abrikosov, Ginzburg, Leggett'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 2003-10-07
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/2003/

### sci_ob_04
- **Question:** Who won the Nobel Prize in Chemistry in 2014?
- **Gold answer:** 'Eric Betzig, Stefan Hell, and William Moerner'
- **Acceptable alternatives:** 'Betzig, Hell, Moerner'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 2014-10-08
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/2014/

### sci_ob_05
- **Question:** What is the half-life of the muon, in microseconds?
- **Gold answer:** '2.197'
- **Acceptable alternatives:** '2.2', '2.197 microseconds', 'approximately 2.2'
- **Domain / category:** science / obscure
- **Answer date (claimed):** timeless
- **Provenance (claimed):** https://pdg.lbl.gov/2023/listings/rpp2023-list-muon.pdf

### sci_ob_06
- **Question:** In which year was the neutron discovered?
- **Gold answer:** '1932'
- **Acceptable alternatives:** (none)
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1932-02-27
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Discovery_of_the_neutron

### sci_ob_07
- **Question:** Who won the Nobel Prize in Physics in 1978?
- **Gold answer:** 'Pyotr Kapitsa, Arno Penzias, and Robert Wilson'
- **Acceptable alternatives:** 'Kapitsa, Penzias, Wilson', 'Penzias and Wilson'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1978-10-17
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/1978/

### sci_ob_08
- **Question:** Which 1967 experiment first detected the missing solar neutrino flux?
- **Gold answer:** 'Homestake experiment'
- **Acceptable alternatives:** 'Homestake', 'Davis experiment', 'Ray Davis experiment'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1968-01-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Homestake_experiment

### sci_ob_09
- **Question:** Who won the Nobel Prize in Physics in 1986?
- **Gold answer:** 'Ernst Ruska, Gerd Binnig, and Heinrich Rohrer'
- **Acceptable alternatives:** 'Ruska, Binnig, Rohrer', 'Binnig and Rohrer'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1986-10-15
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/1986/

### sci_ob_10
- **Question:** Who won the Nobel Prize in Chemistry in 1979?
- **Gold answer:** 'Herbert C. Brown and Georg Wittig'
- **Acceptable alternatives:** 'Brown and Wittig'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1979-10-16
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/1979/

### sci_ob_11
- **Question:** Who won the Nobel Prize in Physics in 1992?
- **Gold answer:** 'Georges Charpak'
- **Acceptable alternatives:** 'Charpak'
- **Domain / category:** science / obscure
- **Answer date (claimed):** 1992-10-14
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/1992/

### sci_pc_01
- **Question:** In October 2024, SpaceX first successfully caught the booster of which rocket using the launch tower's arms?
- **Gold answer:** 'Super Heavy'
- **Acceptable alternatives:** 'Starship Super Heavy', 'Super Heavy booster'
- **Domain / category:** science / post_cutoff
- **Answer date (claimed):** 2024-10-13
- **Provenance (claimed):** https://www.spacex.com/launches/mission/?missionId=starship-flight-5

### sci_pc_02
- **Question:** Who won the Nobel Prize in Chemistry in 2024?
- **Gold answer:** 'David Baker, Demis Hassabis, and John Jumper'
- **Acceptable alternatives:** 'Baker, Hassabis, Jumper', 'Hassabis and Jumper'
- **Domain / category:** science / post_cutoff
- **Answer date (claimed):** 2024-10-09
- **Provenance (claimed):** https://www.nobelprize.org/prizes/chemistry/2024/

### sci_pc_03
- **Question:** Who won the Nobel Prize in Physics in 2024?
- **Gold answer:** 'John Hopfield and Geoffrey Hinton'
- **Acceptable alternatives:** 'Hopfield and Hinton', 'Geoffrey Hinton', 'John Hopfield'
- **Domain / category:** science / post_cutoff
- **Answer date (claimed):** 2024-10-08
- **Provenance (claimed):** https://www.nobelprize.org/prizes/physics/2024/

### sci_pc_04
- **Question:** What NASA mission launched in October 2024 to study Jupiter's moon Europa?
- **Gold answer:** 'Europa Clipper'
- **Acceptable alternatives:** 'Europa Clipper mission'
- **Domain / category:** science / post_cutoff
- **Answer date (claimed):** 2024-10-14
- **Provenance (claimed):** https://europa.nasa.gov/

### sci_pc_05
- **Question:** What company released its first publicly available reasoning model series in September 2024?
- **Gold answer:** 'OpenAI'
- **Acceptable alternatives:** 'OpenAI (o1)', 'OpenAI o1'
- **Domain / category:** science / post_cutoff
- **Answer date (claimed):** 2024-09-12
- **Provenance (claimed):** https://openai.com/index/introducing-openai-o1-preview/

### spo_wk_01
- **Question:** Who won the men's singles title at Wimbledon in 2023?
- **Gold answer:** 'Carlos Alcaraz'
- **Acceptable alternatives:** 'Alcaraz'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2023-07-16
- **Provenance (claimed):** https://www.wimbledon.com/en_GB/draws_and_results/index.html

### spo_wk_02
- **Question:** Which MLB team won the World Series in 2009?
- **Gold answer:** 'New York Yankees'
- **Acceptable alternatives:** 'Yankees'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2009-11-04
- **Provenance (claimed):** https://en.wikipedia.org/wiki/2009_World_Series

### spo_wk_03
- **Question:** Which NFL team won Super Bowl LVIII in February 2024?
- **Gold answer:** 'Kansas City Chiefs'
- **Acceptable alternatives:** 'Chiefs', 'KC Chiefs'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2024-02-11
- **Provenance (claimed):** https://www.nfl.com/news/super-bowl-lviii-recap

### spo_wk_04
- **Question:** Which MLB team won the World Series in 2022?
- **Gold answer:** 'Houston Astros'
- **Acceptable alternatives:** 'Astros'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2022-11-05
- **Provenance (claimed):** https://www.mlb.com/news/2022-world-series-recap

### spo_wk_05
- **Question:** Which MLB team won the World Series in 2016?
- **Gold answer:** 'Chicago Cubs'
- **Acceptable alternatives:** 'Cubs'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2016-11-02
- **Provenance (claimed):** https://www.mlb.com/news/2016-world-series-recap

### spo_wk_06
- **Question:** Which NFL team won Super Bowl LVII in February 2023?
- **Gold answer:** 'Kansas City Chiefs'
- **Acceptable alternatives:** 'Chiefs', 'KC Chiefs'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2023-02-12
- **Provenance (claimed):** https://www.nfl.com/news/super-bowl-lvii-recap

### spo_wk_07
- **Question:** Who won the men's singles title at the 2023 French Open?
- **Gold answer:** 'Novak Djokovic'
- **Acceptable alternatives:** 'Djokovic'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2023-06-11
- **Provenance (claimed):** https://www.rolandgarros.com/en-us/

### spo_wk_08
- **Question:** Who won the women's singles title at the 2022 US Open?
- **Gold answer:** 'Iga Swiatek'
- **Acceptable alternatives:** 'Swiatek'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2022-09-10
- **Provenance (claimed):** https://www.usopen.org/en_US/scores/completed_matches.html

### spo_wk_09
- **Question:** Which MLB team won the World Series in 2023?
- **Gold answer:** 'Texas Rangers'
- **Acceptable alternatives:** 'Rangers'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2023-11-01
- **Provenance (claimed):** https://www.mlb.com/news/2023-world-series-recap

### spo_wk_10
- **Question:** Which NFL team won Super Bowl LV in February 2021?
- **Gold answer:** 'Tampa Bay Buccaneers'
- **Acceptable alternatives:** 'Buccaneers', 'Bucs'
- **Domain / category:** sports / well_known
- **Answer date (claimed):** 2021-02-07
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Super_Bowl_LV

### spo_ob_01
- **Question:** Which NFL team won Super Bowl XX in January 1986?
- **Gold answer:** 'Chicago Bears'
- **Acceptable alternatives:** 'Bears'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1986-01-26
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Super_Bowl_XX

### spo_ob_02
- **Question:** Who won the men's singles title at the 1996 Australian Open?
- **Gold answer:** 'Boris Becker'
- **Acceptable alternatives:** 'Becker'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1996-01-28
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1996_Australian_Open_%E2%80%93_Men%27s_Singles

### spo_ob_03
- **Question:** Who won the women's singles title at the 2004 US Open?
- **Gold answer:** 'Svetlana Kuznetsova'
- **Acceptable alternatives:** 'Kuznetsova'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 2004-09-11
- **Provenance (claimed):** https://en.wikipedia.org/wiki/2004_US_Open_%E2%80%93_Women%27s_Singles

### spo_ob_04
- **Question:** Which NFL team won Super Bowl XII in January 1978?
- **Gold answer:** 'Dallas Cowboys'
- **Acceptable alternatives:** 'Cowboys'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1978-01-15
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Super_Bowl_XII

### spo_ob_05
- **Question:** Which MLB team won the World Series in 1960?
- **Gold answer:** 'Pittsburgh Pirates'
- **Acceptable alternatives:** 'Pirates'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1960-10-13
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1960_World_Series

### spo_ob_06
- **Question:** Which MLB team won the World Series in 1991?
- **Gold answer:** 'Minnesota Twins'
- **Acceptable alternatives:** 'Twins'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1991-10-27
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1991_World_Series

### spo_ob_07
- **Question:** Who won the women's singles title at the 1989 French Open?
- **Gold answer:** 'Arantxa Sanchez Vicario'
- **Acceptable alternatives:** 'Sanchez Vicario', 'Sanchez-Vicario'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1989-06-10
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1989_French_Open_%E2%80%93_Women%27s_Singles

### spo_ob_08
- **Question:** Who was the MVP of Super Bowl XXXVII in January 2003?
- **Gold answer:** 'Dexter Jackson'
- **Acceptable alternatives:** (none)
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 2003-01-26
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Super_Bowl_XXXVII

### spo_ob_09
- **Question:** Which MLB team won the World Series in 1985?
- **Gold answer:** 'Kansas City Royals'
- **Acceptable alternatives:** 'Royals'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1985-10-27
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1985_World_Series

### spo_ob_10
- **Question:** Which MLB team won the World Series in 1974?
- **Gold answer:** 'Oakland Athletics'
- **Acceptable alternatives:** "A's", "Oakland A's", 'Athletics'
- **Domain / category:** sports / obscure
- **Answer date (claimed):** 1974-10-17
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1974_World_Series

### spo_pc_01
- **Question:** Who won the women's singles title at the 2024 Wimbledon Championships?
- **Gold answer:** 'Barbora Krejcikova'
- **Acceptable alternatives:** 'Krejcikova'
- **Domain / category:** sports / post_cutoff
- **Answer date (claimed):** 2024-07-13
- **Provenance (claimed):** https://www.wimbledon.com/en_GB/news/articles/2024-07-13/krejcikova_completes_extraordinary_grand_slam_journey.html

### spo_pc_02
- **Question:** Who was named MVP of Super Bowl LIX in February 2025?
- **Gold answer:** 'Jalen Hurts'
- **Acceptable alternatives:** 'Hurts'
- **Domain / category:** sports / post_cutoff
- **Answer date (claimed):** 2025-02-09
- **Provenance (claimed):** https://www.nfl.com/news/super-bowl-lix-recap

### spo_pc_03
- **Question:** Who won the men's singles title at the 2025 Australian Open?
- **Gold answer:** 'Jannik Sinner'
- **Acceptable alternatives:** 'Sinner'
- **Domain / category:** sports / post_cutoff
- **Answer date (claimed):** 2025-01-26
- **Provenance (claimed):** https://ausopen.com/articles/news/men-s-singles-final-jannik-sinner-vs-alexander-zverev

### spo_pc_04
- **Question:** Which NFL team won Super Bowl LIX in February 2025?
- **Gold answer:** 'Philadelphia Eagles'
- **Acceptable alternatives:** 'Eagles'
- **Domain / category:** sports / post_cutoff
- **Answer date (claimed):** 2025-02-09
- **Provenance (claimed):** https://www.nfl.com/news/super-bowl-lix-recap

### spo_pc_05
- **Question:** Who won the men's singles title at the 2024 US Open?
- **Gold answer:** 'Jannik Sinner'
- **Acceptable alternatives:** 'Sinner'
- **Domain / category:** sports / post_cutoff
- **Answer date (claimed):** 2024-09-08
- **Provenance (claimed):** https://www.usopen.org/en_US/news/articles/2024-09-08/2024_us_open_mens_singles_final.html

### spo_pc_06
- **Question:** Which MLB team won the World Series in 2024?
- **Gold answer:** 'Los Angeles Dodgers'
- **Acceptable alternatives:** 'Dodgers', 'LA Dodgers'
- **Domain / category:** sports / post_cutoff
- **Answer date (claimed):** 2024-10-30
- **Provenance (claimed):** https://www.mlb.com/news/2024-world-series-recap

### his_wk_01
- **Question:** Who was the first person to walk on the Moon?
- **Gold answer:** 'Neil Armstrong'
- **Acceptable alternatives:** 'Armstrong'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1969-07-20
- **Provenance (claimed):** https://www.nasa.gov/mission_pages/apollo/apollo11.html

### his_wk_02
- **Question:** Who was the first president of the United States?
- **Gold answer:** 'George Washington'
- **Acceptable alternatives:** 'Washington'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1789-04-30
- **Provenance (claimed):** https://en.wikipedia.org/wiki/George_Washington

### his_wk_03
- **Question:** Who is credited with inventing the telephone, with a patent granted in 1876?
- **Gold answer:** 'Alexander Graham Bell'
- **Acceptable alternatives:** 'Bell', 'Graham Bell'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1876-03-07
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Alexander_Graham_Bell

### his_wk_04
- **Question:** In what year did the Soviet Union dissolve?
- **Gold answer:** '1991'
- **Acceptable alternatives:** (none)
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1991-12-26
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Dissolution_of_the_Soviet_Union

### his_wk_05
- **Question:** Who was the first president of post-apartheid South Africa?
- **Gold answer:** 'Nelson Mandela'
- **Acceptable alternatives:** 'Mandela'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1994-05-10
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Nelson_Mandela

### his_wk_06
- **Question:** Who was Prime Minister of the United Kingdom during most of World War II?
- **Gold answer:** 'Winston Churchill'
- **Acceptable alternatives:** 'Churchill'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1940-05-10
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Winston_Churchill

### his_wk_07
- **Question:** In what year did World War II end?
- **Gold answer:** '1945'
- **Acceptable alternatives:** (none)
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1945-09-02
- **Provenance (claimed):** https://en.wikipedia.org/wiki/End_of_World_War_II_in_Europe

### his_wk_08
- **Question:** In what year did the Berlin Wall fall?
- **Gold answer:** '1989'
- **Acceptable alternatives:** 'Nov 1989', 'November 1989'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1989-11-09
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Fall_of_the_Berlin_Wall

### his_wk_09
- **Question:** In what year did the Wright brothers achieve the first powered flight?
- **Gold answer:** '1903'
- **Acceptable alternatives:** (none)
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1903-12-17
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Wright_brothers

### his_wk_10
- **Question:** Who was the primary author of the United States Declaration of Independence?
- **Gold answer:** 'Thomas Jefferson'
- **Acceptable alternatives:** 'Jefferson'
- **Domain / category:** history / well_known
- **Answer date (claimed):** 1776-07-04
- **Provenance (claimed):** https://www.archives.gov/founding-docs/declaration

### his_ob_01
- **Question:** Who was the Prime Minister of Japan from 1982 to 1987?
- **Gold answer:** 'Yasuhiro Nakasone'
- **Acceptable alternatives:** 'Nakasone'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1982-11-27
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Yasuhiro_Nakasone

### his_ob_02
- **Question:** Which 1955 conference of newly independent Asian and African states was held in Indonesia?
- **Gold answer:** 'Bandung Conference'
- **Acceptable alternatives:** 'Asian-African Conference'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1955-04-18
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Bandung_Conference

### his_ob_03
- **Question:** In what year was the first ascent of Mount Everest by Edmund Hillary and Tenzing Norgay?
- **Gold answer:** '1953'
- **Acceptable alternatives:** (none)
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1953-05-29
- **Provenance (claimed):** https://en.wikipedia.org/wiki/1953_British_Mount_Everest_expedition

### his_ob_04
- **Question:** Who was the President of France from 1981 to 1995?
- **Gold answer:** 'Francois Mitterrand'
- **Acceptable alternatives:** 'Mitterrand'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1981-05-21
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Fran%C3%A7ois_Mitterrand

### his_ob_05
- **Question:** In what year was the Treaty of Westphalia signed?
- **Gold answer:** '1648'
- **Acceptable alternatives:** (none)
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1648-10-24
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Peace_of_Westphalia

### his_ob_06
- **Question:** Who patented the first practical incandescent light bulb in 1879?
- **Gold answer:** 'Thomas Edison'
- **Acceptable alternatives:** 'Edison'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1879-10-21
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Thomas_Edison

### his_ob_07
- **Question:** Who was the second person to walk on the Moon?
- **Gold answer:** 'Buzz Aldrin'
- **Acceptable alternatives:** 'Aldrin'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1969-07-20
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Buzz_Aldrin

### his_ob_08
- **Question:** Who was Prime Minister of the United Kingdom in 1923?
- **Gold answer:** 'Stanley Baldwin'
- **Acceptable alternatives:** 'Baldwin'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1923-05-22
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Stanley_Baldwin

### his_ob_09
- **Question:** Which 1842 treaty ended the First Opium War?
- **Gold answer:** 'Treaty of Nanking'
- **Acceptable alternatives:** 'Treaty of Nanjing'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1842-08-29
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Treaty_of_Nanking

### his_ob_10
- **Question:** Who was the Chancellor of West Germany from 1969 to 1974?
- **Gold answer:** 'Willy Brandt'
- **Acceptable alternatives:** 'Brandt'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1969-10-21
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Willy_Brandt

### his_ob_11
- **Question:** Who was the first woman to fly solo across the Atlantic Ocean?
- **Gold answer:** 'Amelia Earhart'
- **Acceptable alternatives:** 'Earhart'
- **Domain / category:** history / obscure
- **Answer date (claimed):** 1932-05-21
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Amelia_Earhart

### his_pc_01
- **Question:** Which spacecraft, launched in 2024, made the first successful catch of a returning rocket booster?
- **Gold answer:** 'Starship (Super Heavy)'
- **Acceptable alternatives:** 'SpaceX Starship', 'Starship'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2024-10-13
- **Provenance (claimed):** https://www.spacex.com/launches/mission/?missionId=starship-flight-5

### his_pc_02
- **Question:** Which French Prime Minister was ousted by a no-confidence vote in December 2024?
- **Gold answer:** 'Michel Barnier'
- **Acceptable alternatives:** 'Barnier'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2024-12-04
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Michel_Barnier

### his_pc_03
- **Question:** Who was elected the first female president of Mexico in 2024?
- **Gold answer:** 'Claudia Sheinbaum'
- **Acceptable alternatives:** 'Sheinbaum'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2024-06-02
- **Provenance (claimed):** https://en.wikipedia.org/wiki/2024_Mexican_general_election

### his_pc_04
- **Question:** On what date did Pope Francis die?
- **Gold answer:** 'April 21, 2025'
- **Acceptable alternatives:** 'April 21 2025', '21 April 2025', '2025-04-21'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2025-04-21
- **Provenance (claimed):** https://www.vatican.va/content/vatican/en.html

### his_pc_05
- **Question:** Who became Prime Minister of the United Kingdom in July 2024?
- **Gold answer:** 'Keir Starmer'
- **Acceptable alternatives:** 'Starmer', 'Sir Keir Starmer'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2024-07-05
- **Provenance (claimed):** https://www.gov.uk/government/people/keir-starmer

### his_pc_06
- **Question:** Who was elected Pope in May 2025 to succeed Pope Francis?
- **Gold answer:** 'Pope Leo XIV'
- **Acceptable alternatives:** 'Leo XIV', 'Robert Prevost'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2025-05-08
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Pope_Leo_XIV

### his_pc_07
- **Question:** Who won the 2024 United States presidential election?
- **Gold answer:** 'Donald Trump'
- **Acceptable alternatives:** 'Trump'
- **Domain / category:** history / post_cutoff
- **Answer date (claimed):** 2024-11-05
- **Provenance (claimed):** https://en.wikipedia.org/wiki/2024_United_States_presidential_election

### cul_wk_01
- **Question:** Who wrote 'One Hundred Years of Solitude'?
- **Gold answer:** 'Gabriel Garcia Marquez'
- **Acceptable alternatives:** 'Garcia Marquez', 'Marquez'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1967-05-30
- **Provenance (claimed):** https://en.wikipedia.org/wiki/One_Hundred_Years_of_Solitude

### cul_wk_02
- **Question:** Who wrote the novel 'Pride and Prejudice'?
- **Gold answer:** 'Jane Austen'
- **Acceptable alternatives:** 'Austen'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1813-01-28
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Pride_and_Prejudice

### cul_wk_03
- **Question:** Who painted the Mona Lisa?
- **Gold answer:** 'Leonardo da Vinci'
- **Acceptable alternatives:** 'Leonardo', 'da Vinci'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1517-01-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Mona_Lisa

### cul_wk_04
- **Question:** Which album by Michael Jackson, released in 1982, is one of the best-selling albums of all time?
- **Gold answer:** 'Thriller'
- **Acceptable alternatives:** (none)
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1982-11-30
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Thriller_(album)

### cul_wk_05
- **Question:** Which band released the album 'The Dark Side of the Moon' in 1973?
- **Gold answer:** 'Pink Floyd'
- **Acceptable alternatives:** (none)
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1973-03-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Dark_Side_of_the_Moon

### cul_wk_06
- **Question:** Who wrote the novel '1984'?
- **Gold answer:** 'George Orwell'
- **Acceptable alternatives:** 'Orwell', 'Eric Arthur Blair'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1949-06-08
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Nineteen_Eighty-Four

### cul_wk_07
- **Question:** Who sculpted 'David', completed in 1504?
- **Gold answer:** 'Michelangelo'
- **Acceptable alternatives:** (none)
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1504-09-08
- **Provenance (claimed):** https://en.wikipedia.org/wiki/David_(Michelangelo)

### cul_wk_08
- **Question:** Who wrote 'The Great Gatsby'?
- **Gold answer:** 'F. Scott Fitzgerald'
- **Acceptable alternatives:** 'Fitzgerald', 'Scott Fitzgerald'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1925-04-10
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Great_Gatsby

### cul_wk_09
- **Question:** Who painted 'The Starry Night'?
- **Gold answer:** 'Vincent van Gogh'
- **Acceptable alternatives:** 'van Gogh'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 1889-06-18
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Starry_Night

### cul_wk_10
- **Question:** Which artist released the album 'Midnights' in October 2022?
- **Gold answer:** 'Taylor Swift'
- **Acceptable alternatives:** 'Swift'
- **Domain / category:** culture / well_known
- **Answer date (claimed):** 2022-10-21
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Midnights

### cul_ob_01
- **Question:** Who won the Booker Prize in 2007 for 'The Gathering'?
- **Gold answer:** 'Anne Enright'
- **Acceptable alternatives:** 'Enright'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 2007-10-16
- **Provenance (claimed):** https://thebookerprizes.com/the-booker-library/prize-years/2007

### cul_ob_02
- **Question:** Which jazz saxophonist released the 1959 album 'Giant Steps'?
- **Gold answer:** 'John Coltrane'
- **Acceptable alternatives:** 'Coltrane'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1960-01-27
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Giant_Steps

### cul_ob_03
- **Question:** Who released the 1971 album 'Blue'?
- **Gold answer:** 'Joni Mitchell'
- **Acceptable alternatives:** 'Mitchell'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1971-06-22
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Blue_(Joni_Mitchell_album)

### cul_ob_04
- **Question:** Who painted 'Olympia', exhibited at the Paris Salon in 1865?
- **Gold answer:** 'Edouard Manet'
- **Acceptable alternatives:** 'Manet'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1865-05-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Olympia_(Manet)

### cul_ob_05
- **Question:** Who wrote the 1996 novel 'Infinite Jest'?
- **Gold answer:** 'David Foster Wallace'
- **Acceptable alternatives:** 'Wallace', 'DFW'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1996-02-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Infinite_Jest

### cul_ob_06
- **Question:** Which band released the 1989 album 'Doolittle'?
- **Gold answer:** 'Pixies'
- **Acceptable alternatives:** 'The Pixies'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1989-04-17
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Doolittle_(album)

### cul_ob_07
- **Question:** Who wrote the 1962 novel 'Pale Fire'?
- **Gold answer:** 'Vladimir Nabokov'
- **Acceptable alternatives:** 'Nabokov'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1962-04-25
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Pale_Fire

### cul_ob_08
- **Question:** Who wrote the 1978 novel 'The World According to Garp'?
- **Gold answer:** 'John Irving'
- **Acceptable alternatives:** 'Irving'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1978-04-13
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_World_According_to_Garp

### cul_ob_09
- **Question:** Who painted 'Las Meninas', completed in 1656?
- **Gold answer:** 'Diego Velazquez'
- **Acceptable alternatives:** 'Velazquez'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1656-12-31
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Las_Meninas

### cul_ob_10
- **Question:** Who created the 1907 painting 'Les Demoiselles d'Avignon'?
- **Gold answer:** 'Pablo Picasso'
- **Acceptable alternatives:** 'Picasso'
- **Domain / category:** culture / obscure
- **Answer date (claimed):** 1907-06-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Les_Demoiselles_d%27Avignon

### cul_pc_01
- **Question:** Which Taylor Swift album was released in April 2024?
- **Gold answer:** 'The Tortured Poets Department'
- **Acceptable alternatives:** 'TTPD'
- **Domain / category:** culture / post_cutoff
- **Answer date (claimed):** 2024-04-19
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Tortured_Poets_Department

### cul_pc_02
- **Question:** Who wrote the novel 'Orbital' that won the 2024 Booker Prize?
- **Gold answer:** 'Samantha Harvey'
- **Acceptable alternatives:** 'Harvey'
- **Domain / category:** culture / post_cutoff
- **Answer date (claimed):** 2024-11-12
- **Provenance (claimed):** https://thebookerprizes.com/the-booker-library/prize-years/2024

### cul_pc_03
- **Question:** Who won the 2024 Nobel Prize in Literature?
- **Gold answer:** 'Han Kang'
- **Acceptable alternatives:** 'Kang'
- **Domain / category:** culture / post_cutoff
- **Answer date (claimed):** 2024-10-10
- **Provenance (claimed):** https://www.nobelprize.org/prizes/literature/2024/

### cul_pc_04
- **Question:** Which album won the Grammy Award for Album of the Year at the 2025 Grammys?
- **Gold answer:** 'Cowboy Carter'
- **Acceptable alternatives:** 'Cowboy Carter by Beyonce', 'Beyonce - Cowboy Carter'
- **Domain / category:** culture / post_cutoff
- **Answer date (claimed):** 2025-02-02
- **Provenance (claimed):** https://www.grammy.com/awards/67th-annual-grammy-awards-2024

### cul_pc_05
- **Question:** Maurizio Cattelan's 'Comedian' (a banana taped to a wall) sold at Sotheby's in November 2024 for how much, in millions of US dollars?
- **Gold answer:** '6.2'
- **Acceptable alternatives:** '$6.2 million', '6.2 million', '6.24'
- **Domain / category:** culture / post_cutoff
- **Answer date (claimed):** 2024-11-20
- **Provenance (claimed):** https://www.sothebys.com/en/buy/auction/2024/now/maurizio-cattelan-comedian

### cin_wk_01
- **Question:** Which actor played Vito Corleone in the 1972 film 'The Godfather'?
- **Gold answer:** 'Marlon Brando'
- **Acceptable alternatives:** 'Brando'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 1972-03-15
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Godfather

### cin_wk_02
- **Question:** Who won the Academy Award for Best Actress at the 2023 ceremony?
- **Gold answer:** 'Michelle Yeoh'
- **Acceptable alternatives:** 'Yeoh'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 2023-03-12
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2023

### cin_wk_03
- **Question:** Which film won the Academy Award for Best Picture at the 2024 ceremony?
- **Gold answer:** 'Oppenheimer'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 2024-03-10
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2024

### cin_wk_04
- **Question:** Who directed the film 'Pulp Fiction'?
- **Gold answer:** 'Quentin Tarantino'
- **Acceptable alternatives:** 'Tarantino'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 1994-10-14
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Pulp_Fiction

### cin_wk_05
- **Question:** Who directed the film 'Oppenheimer' (2023)?
- **Gold answer:** 'Christopher Nolan'
- **Acceptable alternatives:** 'Nolan'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 2023-07-21
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Oppenheimer_(film)

### cin_wk_06
- **Question:** Who won the Academy Award for Best Actor at the 2024 ceremony?
- **Gold answer:** 'Cillian Murphy'
- **Acceptable alternatives:** 'Murphy'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 2024-03-10
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2024

### cin_wk_07
- **Question:** Which film won the Academy Award for Best Picture at the 2020 ceremony?
- **Gold answer:** 'Parasite'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 2020-02-09
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2020

### cin_wk_08
- **Question:** Which film won the Academy Award for Best Picture at the 2023 ceremony?
- **Gold answer:** 'Everything Everywhere All at Once'
- **Acceptable alternatives:** 'EEAAO'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 2023-03-12
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2023

### cin_wk_09
- **Question:** Who directed the film 'Schindler's List'?
- **Gold answer:** 'Steven Spielberg'
- **Acceptable alternatives:** 'Spielberg'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 1993-11-30
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Schindler%27s_List

### cin_wk_10
- **Question:** Which film won the Academy Award for Best Picture at the 1998 ceremony?
- **Gold answer:** 'Titanic'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 1998-03-23
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1998

### cin_wk_11
- **Question:** Who directed the film 'Star Wars: Episode IV - A New Hope'?
- **Gold answer:** 'George Lucas'
- **Acceptable alternatives:** 'Lucas'
- **Domain / category:** cinema / well_known
- **Answer date (claimed):** 1977-05-25
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Star_Wars_(film)

### cin_ob_01
- **Question:** Which film won the Academy Award for Best Picture at the 1956 ceremony?
- **Gold answer:** 'Marty'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1956-03-21
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1956

### cin_ob_02
- **Question:** Which film won the Academy Award for Best Picture at the 1987 ceremony?
- **Gold answer:** 'Platoon'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1987-03-30
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1987

### cin_ob_03
- **Question:** Who won the Academy Award for Best Actor at the 1962 ceremony for 'Judgment at Nuremberg'?
- **Gold answer:** 'Maximilian Schell'
- **Acceptable alternatives:** 'Schell'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1962-04-09
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1962

### cin_ob_04
- **Question:** Who directed the film 'Le Samourai' (1967)?
- **Gold answer:** 'Jean-Pierre Melville'
- **Acceptable alternatives:** 'Melville'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1967-10-25
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Le_Samoura%C3%AF

### cin_ob_05
- **Question:** Who won the Academy Award for Best Actress at the 1991 ceremony for 'Misery'?
- **Gold answer:** 'Kathy Bates'
- **Acceptable alternatives:** 'Bates'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1991-03-25
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1991

### cin_ob_06
- **Question:** Who directed the film 'The Conversation' (1974)?
- **Gold answer:** 'Francis Ford Coppola'
- **Acceptable alternatives:** 'Coppola'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1974-04-07
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Conversation

### cin_ob_07
- **Question:** Which film won the Academy Award for Best Picture at the 1965 ceremony?
- **Gold answer:** 'My Fair Lady'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1965-04-05
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1965

### cin_ob_08
- **Question:** Who directed the film 'Stalker' (1979)?
- **Gold answer:** 'Andrei Tarkovsky'
- **Acceptable alternatives:** 'Tarkovsky'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1979-05-25
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Stalker_(1979_film)

### cin_ob_09
- **Question:** Who directed the film 'Burden of Dreams' (1982)?
- **Gold answer:** 'Les Blank'
- **Acceptable alternatives:** 'Blank'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1982-10-01
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Burden_of_Dreams

### cin_ob_10
- **Question:** Which film won the Academy Award for Best Picture at the 1979 ceremony?
- **Gold answer:** 'The Deer Hunter'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1979-04-09
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1979

### cin_ob_11
- **Question:** Who won the Academy Award for Best Supporting Actress at the 1986 ceremony?
- **Gold answer:** 'Anjelica Huston'
- **Acceptable alternatives:** 'Huston'
- **Domain / category:** cinema / obscure
- **Answer date (claimed):** 1986-03-24
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/1986

### cin_pc_01
- **Question:** Who won the Academy Award for Best Actor at the 2025 ceremony?
- **Gold answer:** 'Adrien Brody'
- **Acceptable alternatives:** 'Brody'
- **Domain / category:** cinema / post_cutoff
- **Answer date (claimed):** 2025-03-02
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2025

### cin_pc_02
- **Question:** Who directed the film 'Anora'?
- **Gold answer:** 'Sean Baker'
- **Acceptable alternatives:** 'Baker'
- **Domain / category:** cinema / post_cutoff
- **Answer date (claimed):** 2024-10-18
- **Provenance (claimed):** https://en.wikipedia.org/wiki/Anora

### cin_pc_03
- **Question:** Who directed the film 'The Brutalist'?
- **Gold answer:** 'Brady Corbet'
- **Acceptable alternatives:** 'Corbet'
- **Domain / category:** cinema / post_cutoff
- **Answer date (claimed):** 2024-12-20
- **Provenance (claimed):** https://en.wikipedia.org/wiki/The_Brutalist

### cin_pc_04
- **Question:** Who won the Academy Award for Best Actress at the 2025 ceremony?
- **Gold answer:** 'Mikey Madison'
- **Acceptable alternatives:** 'Madison'
- **Domain / category:** cinema / post_cutoff
- **Answer date (claimed):** 2025-03-02
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2025

### cin_pc_05
- **Question:** Which film won the Academy Award for Best Picture at the 2025 ceremony?
- **Gold answer:** 'Anora'
- **Acceptable alternatives:** (none)
- **Domain / category:** cinema / post_cutoff
- **Answer date (claimed):** 2025-03-02
- **Provenance (claimed):** https://www.oscars.org/oscars/ceremonies/2025


---


Now return the JSON array. Remember: no prose, no fences, just the array.
