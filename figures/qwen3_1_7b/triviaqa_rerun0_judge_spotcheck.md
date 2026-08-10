# TriviaQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the TriviaQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). TriviaQA = closed-book trivia (the dataset Kadavath et al.\ 2022 leaned on most).

---

**triviaqa_0331**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: What slippery synthetic substance was Ronald Reagan compared to - because no scandals stuck to him?
- Gold: `Teflon`  (aliases: `Teflon (trademark)`, `PFTE`, `Polytetrafluoroethene`, `Polytetrafluroethylene`, `Polytetracfluoroethane`, `Polytetraflouroethylene`)
- Model: 'Ronald Reagan was compared to a "slippery synthetic substance" because he was often described as having a "slippery slope" in his political career, particularly in the context of his later years. This metaphor was used to suggest that his policies and actions, while controversial, did not lead to a '

---

**triviaqa_0154**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: The roe of lumpfish is used as a substitute for which delicacy?
- Gold: `Caviar`  (aliases: `Ikra`, `Iranian caviar`, `Black caviar`, `Caviar substitute`, `Keviar`, `Caviar Caviare`)
- Model: 'The roe of lumpfish is used as a substitute for **cod liver oil** in some traditional dishes, particularly in Chinese cuisine. This practice is rooted in historical and cultural contexts where fish roe was valued for its nutritional content and was used as a substitute for cod liver oil in cooking. '

---

**triviaqa_0404**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: Ashkenazic and sephardic cuisines are associated with which ethnic group?
- Gold: `JEWS`  (aliases: `Jewish people`, `Jew`, `Jews/infobox`, `Jewesses`, `Yahood`, `Jewish People`)
- Model: 'Ashkenazic and Sephardic cuisines are associated with **Jewish ethnic groups**.\n\n- **Ashkenazic cuisine** is the traditional cuisine of the **Ashkenazi Jews**, who are primarily found in Central and Eastern Europe.\n- **Sephardic cuisine** is the traditional cuisine of the **'

---

**triviaqa_0666**  (judge: `refusal`, substring-correct: False, answer word-len: 1)

- Q: Annually in July or August, the Obon (or Bon) Buddhist festival to honour the dead is held in which country?
- Gold: `Japan`  (aliases: `日本國`, `State of Japan`, `Ja-pan`, `Nihon`, `Nippon`, `Japang`)
- Model: 'The Obon (or Bon) Buddhist festival, which is held annually in July or August, is celebrated in **Thailand**. This festival is a significant event in Thai culture, where families honor their deceased relatives by performing rituals, visiting temples, and offering food and incense to the spirits of t'

---

**triviaqa_0049**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: What 70’s group released a statement on Monday that read, in part “We are deeply dismayed by today’s announcement from the YMCA that they feel a name change and a rebranding are in order after 166 years”?
- Gold: `Village People`  (aliases: `Sixuvus`, `The Amazing Veepers`, `G. Jeff Olsen`, `Vilage People`, `A.J. Perrelli`, `The Village People`)
- Model: "The 1970s group that released the statement you're referring to is **The Rolling Stones**.\n\nThe statement was released on **April 1, 1977**, and it was part of a broader campaign by the Rolling Stones to rename the **Rolling Stones** after the **YMCA"

---

**triviaqa_0074**  (judge: `correct`, substring-correct: False, answer word-len: 6)

- Q: In the 1983 film ‘Christine’, directed by John Carpenter, what is Christine?
- Gold: `A car – Red Plymouth Fury`  
- Model: "In the 1983 film *Christine*, directed by John Carpenter, **Christine** is the protagonist. She is a young woman who is kidnapped and later murdered by her abusive father, who is also the film's antagonist. The film is a psychological horror thriller that explores themes of abuse, trauma,"

---

**triviaqa_0548**  (judge: `correct`, substring-correct: False, answer word-len: 1)

- Q: In 1962, a 250cc World Championship for which sport was created, attracting machines built by Husqvarna, Bultaco, CZ and Greeves?
- Gold: `Motocross`  (aliases: `Motocross racing`, `Motocross Racing`, `Moto Cross`, `Motorcycle scrambling`, `Moto pit`, `Moto-Cross`)
- Model: 'In 1962, a 250cc World Championship for **motorcycling** was created, attracting machines built by **Husqvarna, Bultaco, CZ (CZ is the abbreviation for **CZ Motorsport**, a Czech motorcycle manufacturer), and Greeves**. This'

---

**triviaqa_0096**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Michael, John, Steven and Susan are the children of which former US President?
- Gold: `Gerald Ford`  (aliases: `President Gerald R. Ford`, `Gerald R. Ford Jr.`, `Assassination attempts on Gerald Ford`, `Leslie Lynch King Jr.`, `Leslie L King`, `Leslie King, Jr.`)
- Model: 'Michael, John, Steven, and Susan are the children of **George H.W. Bush**, the 41st president of the United States. \n\n- **Michael Bush** (born 1946) – son of George H.W. Bush  \n- **John Bush** (born 194'

---

**triviaqa_0374**  (judge: `correct`, substring-correct: False, answer word-len: 2)

- Q: The UK TV series, All Ceatures Great and Small, concerned what area of activity?
- Gold: `Veterinary practice`  (aliases: `Veterinary Medical Doctor`, `Vet's office`, `Equine veterinarian`, `Veterinary practioners`, `Doctor of Veterinary Medicine`, `D.V.M.`)
- Model: "The UK TV series *All Features Great and Small* (often abbreviated as *All Features*) was a popular children's television show that aired in the 1970s and 1980s. It was designed to teach children about various aspects of life, including:\n\n- **School life**\n-"

---

**triviaqa_0596**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: In the Christian calendar what is the first day of Holy Week
- Gold: `Palm Sunday`  (aliases: `Flowery Sunday`, `Fir Sunday`, `Branch Sunday`, `Palm sunday`, `Palm Sundays`, `Yew Sunday`)
- Model: 'In the Christian calendar, **Holy Week** begins on **Passion Sunday**, which is the **first Sunday of Lent**. \n\n- **Lent** is a 40-day period of preparation for Easter, and it begins on **Shrove Tuesday (Shrove Monday)**, which is **February 2'

---

**triviaqa_0059**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: District 12, Panem, North America
- Gold: `Caitness Everdene`  
- Model: 'District 12 is a fictional district from the *Panem* series by Suzanne Collins. It is one of the 12 districts in the Capitol-ruled nation of Panem, which was established after the Great Hunger, a period of civil war and famine that left the Capitol with control over the remaining food'

---

**triviaqa_0519**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: The 1960’s television series ‘Lost in Space’ is set in which year?
- Gold: `1997`  (aliases: `one thousand, nine hundred and ninety-seven`)
- Model: 'The 1960’s television series *Lost in Space* is set in the year **1965**. The show originally aired in 1965 and continued through 1968, following the adventures of the Robinson family on the spaceship *USS Enterprise* in the distant future'

---

**triviaqa_0219**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Who plays the title character in the recent BBC TV series 'Sherlock'?
- Gold: `BENEDICT CUMBERBATCH`  (aliases: `Benedict cumberbatch`, `Benedict Timothy Carlton Cumberbatch`, `Benedict Cumberbatch`)
- Model: 'The title character in the recent BBC TV series *Sherlock* is **Arthur Conan Doyle**, the famous author of the Sherlock Holmes stories. The series is a modern adaptation of these classic tales, created by Steven Moffat and written by Martin Freeman.\n\n**Martin Freeman** plays the role of **Arthur Con'

---

**triviaqa_0038**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Hans Langsdorff commanded which pocket battleship in WWII?
- Gold: `GRAF SPEE`  (aliases: `Graf Spee`, `Graf Spee (disambiguation)`)
- Model: 'Hans Langsdorff commanded the **Scharnhorst** during World War II.\n\nThe **Scharnhorst** was a German battleship of the German Imperial Navy (Kaiserliche Marine), part of the *Grosser Kriegsmarine* (Great Navy). It was one of the largest'

---

**triviaqa_0088**  (judge: `wrong`, substring-correct: True, answer word-len: 1)

- Q: What animal's name means earth pig in Dutch
- Gold: `Aardvark`  (aliases: `Ardvark`, `Aardvaark`, `Earth pig`, `Aardvarc`, `Aadrvark`, `Aardvarken`)
- Model: 'The animal whose name means "earth pig" in Dutch is **"pigeon"** (in Dutch, it\'s **"pigeon"** or **"pigeon"** — but more commonly, the word for **"pigeon"** in Dutch is **"pigeon"'

---

**triviaqa_0444**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Which famous American comedian quoted 'It only takes one drink to get me loaded, I can't remember if it's the ninth or the tenth?
- Gold: `GEORGE BURNS`  (aliases: `George Burns`, `George burns`, `Naftaly Birnbaum`)
- Model: 'The quote you\'re referring to is from the famous American comedian **Jackie Gleason**, who was known for his work on the TV show *The Honeymooners* and his stand-up comedy. The line:\n\n> **"It only takes one drink to get me loaded, I can\'t remember if it\'s'

---

**triviaqa_0428**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Which singer picked up three Ivor Novello awards in May, including songwriter of the year for her hit single, The Fear?
- Gold: `Lily Allen`  (aliases: `Lily Loves`, `Lily Allen (band)`, `Lilly Allan`, `Lily Allan`, `Is It Scary (album)`, `Lily Rose Beatrice Allen`)
- Model: 'The singer who picked up three Ivor Novello awards in May, including the **Songwriter of the Year** for her hit single **"The Fear"**, was **Lana Del Rey**.\n\nShe won:\n- **Songwriter of the Year** for "The Fear" (2017)\n-'

---

**triviaqa_0071**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: The laburnum tree has what colour flowers?
- Gold: `Yellow`  (aliases: `Yellowest`, `Whiteyellow`, `Yelow`, `Yellow color`, `Yellowishness`, `Yellower`)
- Model: 'The laburnum tree (scientific name: *Gleditsia loba*) is known for its large, showy flowers. The flowers are typically **yellow** in color, though they can sometimes appear **orange** or **red** depending on the variety and the time of year.\n\nSo, the answer is'

---

**triviaqa_0246**  (judge: `correct`, substring-correct: False, answer word-len: 1)

- Q: The word bucolic refers to pleasant/positive aspects of?
- Gold: `Countryside/life`  
- Model: 'The word **"bucolic"** refers to **pleasant or positive aspects of rural life**.\n\nIt comes from the Greek **"boukōlos"**, meaning "country" or "rural," and it is often used to describe a peaceful, idyllic, or harmonious lifestyle in the'

---

**triviaqa_0092**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: What colour is the number 10 on the door of 10 Downing Street? White, Yellow or Brown?
- Gold: `White`  (aliases: `White (Colour)`, `Rgb(255, 255, 255)`, `Whitishness`, `Whiter`, `(255, 255, 255)`, `Whitishly`)
- Model: "The number 10 on the door of 10 Downing Street is **white**.\n\nThis is a well-known fact in the UK, where the numbers on the doors of the Downing Street building are painted in white, while the building's exterior is typically painted in a darker color, such as brown or black."

