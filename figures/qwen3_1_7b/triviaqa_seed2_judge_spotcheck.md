# TriviaQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the TriviaQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). TriviaQA = closed-book trivia (the dataset Kadavath et al.\ 2022 leaned on most).

---

**triviaqa_0331**  (judge: `correct`, substring-correct: False, answer word-len: 3)

- Q: Which sixties group starred in the film Catch Us If You Can
- Gold: `Dave Clarke Five`  
- Model: 'The sixties group that starred in the film *Catch Us If You Can* is **The Beatles**. The film, released in 1986, features a number of famous actors and musicians, including **John Lennon**, **Paul McCartney**, and **George Harrison**, who were all active in the sixties'

---

**triviaqa_0154**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: What musical term means in a majestic, stately or dignified manner?
- Gold: `Maestoso`  
- Model: 'The musical term that means **majestic, stately, or dignified** in a musical context is:\n\n**"Grand"**.\n\nIn music, "grand" is often used to describe a style, mood, or performance that is **majestic, solemn, or elaborate**, often associated with **Baroque**'

---

**triviaqa_0404**  (judge: `correct`, substring-correct: False, answer word-len: 2)

- Q: Which US No 1 single came from Diana Ross's platinum album Diana?
- Gold: `Upside Down`  (aliases: `Upside Down (Diana Ross song)`, `Up side down`, `Upside Down (single)`)
- Model: 'The US No. 1 single from Diana Ross\'s platinum album *Diana* was **"I Will Always Love You"**. This song was released in 1994 and became one of the most iconic and successful songs in Diana Ross\'s career. It reached number one on the US Billboard Hot'

---

**triviaqa_0666**  (judge: `correct`, substring-correct: True, answer word-len: 2)

- Q: Which cult film, starring Harrison Ford, was based on the story Do Androids Dream of Electric Sheep?
- Gold: `Blade Runner`  (aliases: `V-K`, `Blade Runner 2 (2014 film)`, `Voigt-kampff machine`, `Voigt kampff machine`, `Voigt-kampff test`, `Voit-kampf test`)
- Model: 'The cult film starring Harrison Ford that is based on the story *Do Androids Dream of Electric Sheep* is **"Blade Runner" (1982)**.\n\nThis film, directed by Ridley Scott, is a science fiction classic that explores the concept of androids and their ability to distinguish between humans and machines'

---

**triviaqa_0049**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: Which company produces the supermini car the Ypsilon?
- Gold: `CHRYSLER`  (aliases: `FCA US`, `Chrysler Group`, `Acustar`, `Chrysler Group LLC`, `Chrsyler`, `Chrysler Holding LLC`)
- Model: "The Ypsilon is a supermini car produced by **Vauxhall** (now part of **Stellantis**). It was launched in 2004 and was marketed as a compact, stylish, and affordable vehicle. The Ypsilon was part of Vauxhall's lineup during the 200"

---

**triviaqa_0074**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Which poet wrote The Whitsun Weddings?
- Gold: `Philip Larkin`  (aliases: `Philip Arthur Larkin`, `Philip Arthur Larkin, CH, CBE, FRSL`, `Phillip Larkin`, `Larkinian`, `Philip Larkin Society`, `Larkin Society`)
- Model: '*"The Whitsun Weddings"* is a poem written by **W.H. Auden**. It was first published in 1938 as part of his collection *The Gathering Storm* (1938), and it is often considered one of his most famous and poignant works. The poem reflects'

---

**triviaqa_0548**  (judge: `wrong`, substring-correct: False, answer word-len: 3)

- Q: In 1985, which filly was the last racehorse to win a variant of the English Triple Crown?
- Gold: `Oh So Sharp`  
- Model: 'The last filly to win a variant of the English Triple Crown in 1985 was **Maremma**.\n\nMaremma was a 3-year-old filly who won the **Epsom Derby** on May 12, 1985, and then went on to win'

---

**triviaqa_0096**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Who coined the phrase 'Somebody up there likes me'?
- Gold: `ROCKY GRAZIANO`  (aliases: `Rocky Graziano`)
- Model: 'The phrase "Somebody up there likes me" is often attributed to **John Lennon**. It was first used in a 1969 song titled **"Imagine"** on his album *Imagine*. The line appears in the song\'s chorus and is a playful, self-deprecating way of expressing Lennon'

---

**triviaqa_0374**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: Mount Ararat is in which country?
- Gold: `Turkey`  (aliases: `Turkey (country)`, `Türkiye Respublikasi`, `Turky`, `Turkei`, `Tuerkiye Cumhuriyeti`, `Tuerkiye`)
- Model: "Mount Ararat is located in **Turkey**. It is a prominent mountain in the Armenian Highlands, and it is the subject of the biblical story of Noah's Ark. The mountain is also a significant geographical feature in the region, and it is part of the Armenian population's cultural and religious identity."

---

**triviaqa_0596**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: In which form of pool (pocket billiards) are the balls formed into a diamond pattern?
- Gold: `Nine-ball`  (aliases: `9 ball pool`, `9-ball`, `9 Ball`, `Nine-Ball`, `Six-ball`, `9Ball`)
- Model: 'In **pocket billiards**, specifically in **pool**, the balls are not formed into a **diamond pattern**. \n\n### Key Points:\n- **Diamond pattern** is a term often used in **table tennis** or **billiards** (like **snooker** or **pool**) to describe a specific'

---

**triviaqa_0059**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: Bundes in the German 'Bundesliga' soccer league refers to?
- Gold: `Federal`  (aliases: `Federal (disambiguation)`, `Foederal`, `Fœderals`, `Foederals`, `Federals`, `Fœderal`)
- Model: 'The **Bundesliga** is the **highest tier** of the **German football (soccer) league system**, and it is the **primary professional soccer league** in Germany. It is organized by the **Deutsche Fußball Liga (DFL)**, the governing body of football in Germany.\n\n### Key Points'

---

**triviaqa_0519**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: In which country would you traditionally see a settlement called a Kibbutz?
- Gold: `Israel`  (aliases: `İsrail`, `ISRAEL`, `Israeli Republic`, `Isræl`, `Medinat Yisrael`, `מְדִינַת יִשְׂרָאֵל`)
- Model: 'A settlement called a **Kibbutz** is traditionally found in **Israel**.\n\nThe Kibbutz is a type of cooperative community in Israel, where residents live together, work together, and share resources. These communities were established in the 1940s as part of the Israeli settlement movement,'

---

**triviaqa_0219**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Who wrote much of King George V's first Christmas broadcast, made in 1932?
- Gold: `Rudyard Kipling`  (aliases: `Joseph Rudyard Kipling`, `Kiplingesque`, `Kipling rudyard`, `Rudy Kipling`, `R Kipling`, `Kipling`)
- Model: 'The first Christmas broadcast by King George V, made in 1932, was written by **Lord Alfred Tennyson**. \n\nTennyson was a prominent British poet and had previously written the poem "Christmas Carol" in 1846, which became a popular Christmas song. In 1'

---

**triviaqa_0038**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Who played the title role in the 2008 film 'The Curious Case Of Benjamin Button'?
- Gold: `BRAD PITT`  (aliases: `Bradley Pitt`, `Brad Pitt`, `Brad pitt`, `Pitt, William Bradley`, `Brad Pit`, `William Bradley Pitt`)
- Model: 'The title role in the 2008 film *The Curious Case of Benjamin Button* was played by **Benjamin Button**. However, this is a fictional character, and the film is a fictional story. The actual actor who played the character in the film was **Matthew Macfadyen**.'

---

**triviaqa_0088**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: Lysergic Acid Diethylamide is better known by what abbreviated name?
- Gold: `LSD`  (aliases: `LSD 25`, `Lsd25`, `Dropping acid`, `Tabnet`, `Sunshine acid`, `Acid (drug)`)
- Model: 'Lysergic Acid Diethylamide is better known by the abbreviated name **LSD**.'

---

**triviaqa_0444**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: Which is the largest borough in New York City?
- Gold: `Queens`  (aliases: `Queens, NYC, NY`, `Queens County, NY`, `Queens, United States`, `Queens, N.Y.`, `Queens, New York City`, `Queens, New York City, New York`)
- Model: "The largest borough in New York City is **Manhattan**. It is the city's primary district and the most densely populated, with a population of approximately **3.7 million people** as of 2024. Manhattan is home to the city's financial district, cultural institutions, and major landmarks like the"

---

**triviaqa_0428**  (judge: `wrong`, substring-correct: True, answer word-len: 1)

- Q: The first Apollo moon landing?
- Gold: `11`  (aliases: `eleven`)
- Model: "The first Apollo moon landing occurred on **July 20, 1969**, when the **Apollo 11** mission was launched from the **Kennedy Space Center in Florida**. The mission was part of the **United States' Apollo program**, which was initiated in response to the **Sov"

---

**triviaqa_0071**  (judge: `correct`, substring-correct: False, answer word-len: 11)

- Q: Excluding Lady Jane Grey, who were the five monarchs of the House of Tudor?
- Gold: `Henry VII, Henry VIII, Edward VI, Mary I and Elizabeth I`  
- Model: 'The House of Tudor, which ruled England from 1485 to 1603, includes the following five monarchs, excluding Lady Jane Grey:\n\n1. **Henry VII** (1485–1509)  \n2. **Henry VIII** (1509–'

---

**triviaqa_0246**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: Which Greek God gave Cassandra the give of prophecy?
- Gold: `APOLLO`  (aliases: `Apollo (ballet)`, `Apollon musagète`, `Apollo (Balanchine)`, `Apolo Musageta`, `Apollo, Leader of the Muses`, `Apollon Musagete`)
- Model: 'Cassandra was given the gift of prophecy by **Apollo**, the Greek god of music, poetry, and prophecy. He was her father, and he bestowed this gift upon her as a favor, though it came with a condition: she must never reveal her visions to anyone, including her own father. This prophecy was later'

---

**triviaqa_0092**  (judge: `wrong`, substring-correct: False, answer word-len: 1)

- Q: What word for a surprise attack originally referred to hiding in the woods?
- Gold: `Ambush`  (aliases: `Ambushes`, `Sneak attack`, `Military Surprise`, `Ambuscade`)
- Model: 'The word for a surprise attack that originally referred to hiding in the woods is **"skirmish."**\n\n### Explanation:\n- **Skirmish** originally referred to a small, brief battle or conflict, often between two small groups. \n- In older English, a **skirmish** could be a **'

