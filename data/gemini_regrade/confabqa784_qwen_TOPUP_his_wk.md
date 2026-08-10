# ConfabQA-784 top-up: 33 missing `his_wk` items

Your previous grading pass on the 784-item benchmark returned labels for all
categories except `his_wk` (history / well-known / pre-cutoff). This document
contains only those 33 missing items so you can complete the full 784-item
grading table.

## Grading rule (unchanged)

- **CORRECT**: the answer contains the gold answer (or an acceptable alternative).
  Extra text is fine.
- **REFUSAL**: the answer does NOT contain the gold answer AND the model declines,
  says it lacks information, says the event has not happened, or anchors to a
  knowledge cutoff. The model is NOT asserting a specific competing fact.
- **WRONG**: the answer does NOT contain the gold answer AND the model confidently
  asserts a specific competing fact (a different name, date, entity, etc.).

Decision order:
1. Contains gold? -> CORRECT.
2. Otherwise, asserts a specific competing fact? -> WRONG.
3. Otherwise (declined, hedged, said it doesn't know) -> REFUSAL.

## Expected output

A single markdown table with columns `item_id | label` for all 33 items below.
Nothing else needed — no verification table, no prose. Just the 33-row grading
table.

---

# Items

## 001. `his_wk_01` (history, well_known, pre-cutoff)

**Q:** Who was the leader of Nazi Germany from 1934 to 1945?
**Gold:** Adolf Hitler
**Acceptable alternatives:** 'Hitler'
**Model answer:**
> The leader of Nazi Germany from 1934 to 1945 was **Adolf Hitler**. He was the Chancellor of Germany and the leader of the Nazi Party (National Socialist German Workers' Party) from 1933 until his death in 1945. Hitler came to

**Label:** ___

## 002. `his_wk_02` (history, well_known, pre-cutoff)

**Q:** In what year did the Wright brothers achieve the first powered flight?
**Gold:** 1903
**Acceptable alternatives:** (none)
**Model answer:**
> The Wright brothers achieved the first powered flight on **December 17, 1903**, during a flight at Kitty Hawk, North Carolina. This historic flight was conducted with the Wright Flyer, their first successful airplane.

**Label:** ___

## 003. `his_wk_03` (history, well_known, pre-cutoff)

**Q:** Who was the President of the United States during the Civil War?
**Gold:** Abraham Lincoln
**Acceptable alternatives:** 'Lincoln'
**Model answer:**
> The President of the United States during the Civil War (1861–1865) was **Abraham Lincoln**. He was elected in 1860 and took office just as the Civil War began. Lincoln served as the 16th President of the United States and is widely regarded

**Label:** ___

## 004. `his_wk_04` (history, well_known, pre-cutoff)

**Q:** Who was the first president of post-apartheid South Africa?
**Gold:** Nelson Mandela
**Acceptable alternatives:** 'Mandela'
**Model answer:**
> The first president of post-apartheid South Africa was **Nelson Mandela**. He served as the country's president from 1994 to 1999, following the end of apartheid in 1994. Mandela was a key figure in the struggle against apartheid and played a central role

**Label:** ___

## 005. `his_wk_05` (history, well_known, pre-cutoff)

**Q:** Who was the primary author of the United States Declaration of Independence?
**Gold:** Thomas Jefferson
**Acceptable alternatives:** 'Jefferson'
**Model answer:**
> The primary author of the United States Declaration of Independence was **Thomas Jefferson**. He was the principal writer of the document, which was adopted by the Continental Congress on July 4, 1776. While other members of the Congress, such as John Adams, Benjamin Franklin, and Robert Livingston, contributed ideas

**Label:** ___

## 006. `his_wk_06` (history, well_known, pre-cutoff)

**Q:** In what year did the United States gain independence?
**Gold:** 1776
**Acceptable alternatives:** (none)
**Model answer:**
> The United States gained independence on **July 4, 1776**, when the Continental Congress adopted the Declaration of Independence. This date is celebrated as **Independence Day** in the United States.

**Label:** ___

## 007. `his_wk_07` (history, well_known, pre-cutoff)

**Q:** Who was Prime Minister of the United Kingdom during most of World War II?
**Gold:** Winston Churchill
**Acceptable alternatives:** 'Churchill'
**Model answer:**
> During most of World War II, the Prime Minister of the United Kingdom was **Winston Churchill**. He served as Prime Minister from 1940 to 1945, leading the country through the war against Nazi Germany and the Soviet Union. Churchill was the head of government and the leader of the

**Label:** ___

## 008. `his_wk_08` (history, well_known, pre-cutoff)

**Q:** In what year did the United States declare independence from Britain?
**Gold:** 1776
**Acceptable alternatives:** (none)
**Model answer:**
> The United States declared independence from Britain on **July 4, 1776**, which is celebrated as **Independence Day**. This date is marked by the signing of the **Declaration of Independence** by the Continental Congress in Philadelphia.

**Label:** ___

## 009. `his_wk_09` (history, well_known, pre-cutoff)

**Q:** In what year did the Titanic sink?
**Gold:** 1912
**Acceptable alternatives:** 'April 1912'
**Model answer:**
> The Titanic sank in the early morning of **April 15, 1912**. It was a British ocean liner operated by the White Star Line and ran into an iceberg in the North Atlantic Ocean, leading to its tragic collision with an iceberg and subsequent sinking.

**Label:** ___

## 010. `his_wk_10` (history, well_known, pre-cutoff)

**Q:** Who was the first female Prime Minister of the United Kingdom?
**Gold:** Margaret Thatcher
**Acceptable alternatives:** 'Thatcher'
**Model answer:**
> The first female Prime Minister of the United Kingdom was **Margaret Thatcher**. She served as the Prime Minister from 1979 to 1990. Thatcher was a Conservative politician and a key figure in British politics during the 20th century, known for her leadership during the Falklands War

**Label:** ___

## 011. `his_wk_11` (history, well_known, pre-cutoff)

**Q:** Who is credited with inventing the telephone, with a patent granted in 1876?
**Gold:** Alexander Graham Bell
**Acceptable alternatives:** 'Bell', 'Graham Bell'
**Model answer:**
> The telephone was invented by **Alexander Graham Bell**, with a patent granted in **1876**. Bell is widely recognized as the inventor of the telephone, and he was awarded the patent for his invention on March 7, 1876.  While **Elias Howe** is credited with inventing

**Label:** ___

## 012. `his_wk_12` (history, well_known, pre-cutoff)

**Q:** Who painted the ceiling of the Sistine Chapel?
**Gold:** Michelangelo
**Acceptable alternatives:** (none)
**Model answer:**
> The ceiling of the Sistine Chapel was painted by **Michelangelo**. He worked on the ceiling from 1508 to 1512, and the work is one of the most celebrated achievements in art history. The ceiling features a vast depiction of the **Creation of Adam**, which is a

**Label:** ___

## 013. `his_wk_13` (history, well_known, pre-cutoff)

**Q:** Who was the President of the United States from 2009 to 2017?
**Gold:** Barack Obama
**Acceptable alternatives:** 'Obama'
**Model answer:**
> The President of the United States from 2009 to 2017 was **Barack Obama**. He served as the 44th President, taking office on January 20, 2009, and was re-elected in 2012 and 201

**Label:** ___

## 014. `his_wk_14` (history, well_known, pre-cutoff)

**Q:** Which 1066 battle saw William the Conqueror defeat King Harold of England?
**Gold:** Battle of Hastings
**Acceptable alternatives:** 'Hastings'
**Model answer:**
> The 1066 battle in question is **Battle of Hastings**, where **William the Conqueror** defeated **King Harold II** of England.  ### Key Details: - **Date:** October 14, 1066 - **Location:** Hastings, East Anglia, England -

**Label:** ___

## 015. `his_wk_15` (history, well_known, pre-cutoff)

**Q:** Who was the first European to lead an expedition that circumnavigated the globe (completed after his death in 1521)?
**Gold:** Ferdinand Magellan
**Acceptable alternatives:** 'Magellan'
**Model answer:**
> The first European to lead an expedition that circumnavigated the globe and completed the journey after his death in 1521 was **Ferdinand Magellan**.  ### Key Details: - **Name:** Ferdinand Magellan - **Role:** Portuguese explorer and navigator - **Expedition:** The

**Label:** ___

## 016. `his_wk_16` (history, well_known, pre-cutoff)

**Q:** In what year did World War II end?
**Gold:** 1945
**Acceptable alternatives:** (none)
**Model answer:**
> World War II ended in 1945. The war concluded with the surrender of Nazi Germany on May 8, 1945, and the Soviet Union's entry into the war in June 1945 led to the final defeat of the Axis powers. The war is often referred to as

**Label:** ___

## 017. `his_wk_17` (history, well_known, pre-cutoff)

**Q:** What major international agreement on climate change was adopted in 2015?
**Gold:** Paris Agreement
**Acceptable alternatives:** 'Paris Climate Agreement'
**Model answer:**
> The major international agreement on climate change adopted in 2015 is the **Paris Agreement**. It was signed by 196 countries at the 21st Conference of the Parties (COP21) to the United Nations Framework Convention on Climate Change (UNFCCC) in Paris, France

**Label:** ___

## 018. `his_wk_18` (history, well_known, pre-cutoff)

**Q:** Who was the founder of the People's Republic of China, proclaimed in 1949?
**Gold:** Mao Zedong
**Acceptable alternatives:** 'Mao', 'Mao Tse-tung'
**Model answer:**
> The founder of the People's Republic of China, proclaimed in 1949, was **Mao Zedong**. He was the leader of the Chinese Communist Party and the de facto leader of the People's Republic of China after the Chinese Civil War concluded in 1949.

**Label:** ___

## 019. `his_wk_19` (history, well_known, pre-cutoff)

**Q:** In what year did the Soviet Union dissolve?
**Gold:** 1991
**Acceptable alternatives:** (none)
**Model answer:**
> The Soviet Union dissolved in **1991**. It officially ceased to exist on **December 25, 1991**, following the collapse of the Soviet Union and the dissolution of the Union of Soviet Socialist Republics (USSR).

**Label:** ___

## 020. `his_wk_20` (history, well_known, pre-cutoff)

**Q:** Which treaty signed in 1919 formally ended World War I?
**Gold:** Treaty of Versailles
**Acceptable alternatives:** (none)
**Model answer:**
> The treaty that formally ended World War I was the **Treaty of Versailles**, signed on **June 28, 1919** in the Hall of Mirrors in the Palace of Versailles, France. It was signed between the Allied Powers, including the United States, the United Kingdom,

**Label:** ___

## 021. `his_wk_21` (history, well_known, pre-cutoff)

**Q:** Who was the first person to walk on the Moon?
**Gold:** Neil Armstrong
**Acceptable alternatives:** 'Armstrong'
**Model answer:**
> The first person to walk on the Moon was **Neil Armstrong**. He was the commander of the Apollo 11 mission and became the first human to set foot on the lunar surface on **July 20, 1969**, during the Apollo 11 mission. Armstrong's famous words upon landing

**Label:** ___

## 022. `his_wk_22` (history, well_known, pre-cutoff)

**Q:** Who was the longest-reigning British monarch, who died in 2022?
**Gold:** Queen Elizabeth II
**Acceptable alternatives:** 'Elizabeth II', 'Elizabeth the Second'
**Model answer:**
> The longest-reigning British monarch who died in 2022 was **Queen Elizabeth II**. She reigned for **64 years**, from 1952 to 2022. She passed away on **21 April 2022** at the age of 9

**Label:** ___

## 023. `his_wk_23` (history, well_known, pre-cutoff)

**Q:** Who was the first president of the United States?
**Gold:** George Washington
**Acceptable alternatives:** 'Washington'
**Model answer:**
> The first president of the United States was **George Washington**, who served from 1789 to 1797. He was the first leader of the United States and is often referred to as the "Father of the Nation."

**Label:** ___

## 024. `his_wk_24` (history, well_known, pre-cutoff)

**Q:** In what year did Christopher Columbus first reach the Americas?
**Gold:** 1492
**Acceptable alternatives:** (none)
**Model answer:**
> Christopher Columbus first reached the Americas on **October 12, 1492**, when he landed on an island in the Bahamas, now known as **Cuba**. This was the first time Europeans had set foot on the American continent since the fall of the Roman Empire.

**Label:** ___

## 025. `his_wk_25` (history, well_known, pre-cutoff)

**Q:** Which 1815 battle ended the Napoleonic Wars?
**Gold:** Battle of Waterloo
**Acceptable alternatives:** 'Waterloo'
**Model answer:**
> The 1815 battle that ended the Napoleonic Wars was the **Battle of Waterloo**. It took place on June 10, 1815, near Waterloo in present-day Belgium. This battle marked the final confrontation between Napoleon I of France and the Seventh Coalition, which included major European

**Label:** ___

## 026. `his_wk_26` (history, well_known, pre-cutoff)

**Q:** Who was the President of Russia from 2000 onwards (with one term as Prime Minister)?
**Gold:** Vladimir Putin
**Acceptable alternatives:** 'Putin'
**Model answer:**
> The person who served as the President of Russia from 2000 onwards and held one term as Prime Minister is **Vladimir Putin**.  ### Key Details: - **President of Russia**: Vladimir Putin served as President from **2000 to 2008** and again from **2

**Label:** ___

## 027. `his_wk_27` (history, well_known, pre-cutoff)

**Q:** Which event in 1969 saw humans land on the Moon for the first time?
**Gold:** Apollo 11
**Acceptable alternatives:** (none)
**Model answer:**
> The event in 1969 that saw humans land on the Moon for the first time was the **Apollo 11 mission**. On **July 20, 1969**, NASA's Apollo 11 spacecraft successfully landed on the Moon, with **Neil Armstrong** and **Buzz Ald

**Label:** ___

## 028. `his_wk_28` (history, well_known, pre-cutoff)

**Q:** In what year did the French Revolution begin?
**Gold:** 1789
**Acceptable alternatives:** (none)
**Model answer:**
> The French Revolution began in **1789**. It was a period of radical political change in France that led to the rise of the French Republic and the fall of the monarchy. The revolution is often considered to have started with the storming of the Bastille on July 14, 178

**Label:** ___

## 029. `his_wk_29` (history, well_known, pre-cutoff)

**Q:** Who was the French general and President who led the Free French during WWII?
**Gold:** Charles de Gaulle
**Acceptable alternatives:** 'de Gaulle'
**Model answer:**
> The French general and President who led the Free French during World War II was **Charles de Gaulle**.  ### Key Points: - **Charles de Gaulle** was a French politician, military leader, and president of the French Republic. - He was a key figure in the **Free French Forces** (French Resistance

**Label:** ___

## 030. `his_wk_30` (history, well_known, pre-cutoff)

**Q:** Which company released the first iPhone, in 2007?
**Gold:** Apple
**Acceptable alternatives:** 'Apple Inc.'
**Model answer:**
> The first iPhone was released by **Apple Inc.** in **2007**. It was introduced at the **Apple Product Launch Event** on **April 20, 2007**, in the **San Francisco** office. The iPhone combined a mobile phone, an iPod, and an internet

**Label:** ___

## 031. `his_wk_31` (history, well_known, pre-cutoff)

**Q:** Who succeeded Stalin as leader of the Soviet Union after his death in 1953?
**Gold:** Nikita Khrushchev
**Acceptable alternatives:** 'Khrushchev'
**Model answer:**
> After Stalin's death in 1953, the Soviet Union was led by **Khrushchev** (Joseph Stalin). Khrushchev became the General Secretary of the Communist Party of the Soviet Union and took over as the leader of the Soviet Union in 1953. He is

**Label:** ___

## 032. `his_wk_32` (history, well_known, pre-cutoff)

**Q:** In what year did the Berlin Wall fall?
**Gold:** 1989
**Acceptable alternatives:** 'Nov 1989', 'November 1989'
**Model answer:**
> The Berlin Wall fell on **November 9, 1989**. This event marked the beginning of the reunification of Germany and was a pivotal moment in the Cold War.

**Label:** ___

## 033. `his_wk_33` (history, well_known, pre-cutoff)

**Q:** In what year was the World Wide Web invented by Tim Berners-Lee at CERN?
**Gold:** 1989
**Acceptable alternatives:** 'March 1989'
**Model answer:**
> The World Wide Web was invented by Tim Berners-Lee at CERN in the year **1989**.  Berners-Lee first proposed the concept of the World Wide Web in 1989 while working at CERN. He developed the foundational technologies, including the Hypertext Transfer Protocol (HTTP

**Label:** ___
