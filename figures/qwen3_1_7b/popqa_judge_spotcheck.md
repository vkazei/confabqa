# PopQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the PopQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). PopQA = Wikidata triples, different distribution.

---

**popqa_0331**  (o_pop = 3269, judge: `correct`, substring-correct: False)

- Q: Who is the author of Lord?
- Gold: `Buronson`  
- Model: 'The question "Who is the author of Lord?" is a bit ambiguous, as "Lord" can refer to different works. Here are the most likely interpretations:\n\n1. **"Lord of the Flies" by William Golding**  \n   - This is the most commonly cited "Lord" in literature. It is'

---

**popqa_0154**  (o_pop = 34096, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of Drama?
- Gold: `Trevor Horn`  (aliases: `Trevor Charles Horn`)
- Model: 'To answer your question, I need a bit more context. The phrase "Drama" could refer to:\n\n1. **A specific drama** (e.g., a TV show, movie, or play).\n2. **A genre** (e.g., "Drama" as a genre in film or television).'

---

**popqa_0404**  (o_pop = 24054, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of The Castle?
- Gold: `Maximilian Schell`  
- Model: 'The producer of *The Castle* (a 2015 American psychological thriller film directed by David Fincher) is **David Fincher** himself. The film was written and directed by Fincher, and he also served as the producer.'

---

**popqa_0666**  (o_pop = 264499, judge: `wrong`, substring-correct: False)

- Q: Who is the author of On Practice?
- Gold: `Mao Zedong`  (aliases: `Mao Tse-tung`, `Chairman Mao`, `Mao Ze Dong`, `Maozedong`, `Tse Toung Mao`)
- Model: 'The author of *On Practice* (also known as *On the Practice of Life* or *On the Practice of the Art of Living*) is **Mencius** (or **Mengzi**), a Chinese philosopher from the Warring States period (475–283 BCE). This text'

---

**popqa_0049**  (o_pop = 191743, judge: `wrong`, substring-correct: False)

- Q: Who was the director of Three Men and a Baby?
- Gold: `Leonard Nimoy`  (aliases: `Leonard Simon Nimoy`)
- Model: 'The film *Three Men and a Baby* (1950), directed by **John Huston**, is a classic American drama that explores the complexities of family and human relationships. It is often regarded as one of the greatest films of the 20th century.'

---

**popqa_0074**  (o_pop = 556493, judge: `wrong`, substring-correct: False)

- Q: In what country is Direkte Aktion?
- Gold: `Germany`  (aliases: `FRG`, `BRD`, `Bundesrepublik Deutschland`, `Federal Republic of Germany`, `de`, `Deutschland`)
- Model: 'Direkte Aktion is a term that refers to a **direct action** or **direct strike** in the context of **social movements**, **political activism**, or **civil disobedience**. It is commonly associated with **direct action** as a form of protest or resistance.\n\nHowever, the term **"Direkte'

---

**popqa_0548**  (o_pop = 100802, judge: `wrong`, substring-correct: False)

- Q: What genre is Thomas Morris?
- Gold: `jazz`  (aliases: `jazz music`, `jass`, `jas`, `jaz`, `Jazz`)
- Model: 'Thomas Morris is a British author, poet, and playwright known for his work in **poetry and drama**. He is often associated with the **Modernist movement** in English literature. His writing is characterized by its **lyrical quality**, **complex structure**, and **deep philosophical reflections**.\n\nS'

---

**popqa_0096**  (o_pop = 3172, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of Mr. Baseball?
- Gold: `Fred Schepisi`  (aliases: `Frederic Alan Schepisi`)
- Model: 'The producer of *Mr. Baseball* (1988) was **John Landis**. The film, directed by John Landis and written by him, is a satirical comedy that parodies the American baseball culture of the 1980s. It features a fictionalized version of the'

---

**popqa_0374**  (o_pop = 30825, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for Rebel?
- Gold: `Raghava Lawrence`  (aliases: `Lawrence`)
- Model: 'The screenwriter for the 1984 film *Rebel* (also known as *Rebel Without a Cause*) was **Walter Hill**. \n\n*Rebel* is a classic American film directed by Walter Hill, and it is often considered one of the greatest films of the 198'

---

**popqa_0596**  (o_pop = 9600, judge: `wrong`, substring-correct: False)

- Q: Who was the composer of Julie?
- Gold: `Rajesh Roshan`  (aliases: `Rajesh Roshan Lal Nagrath`)
- Model: "The composer of *Julie* is **Ludwig van Beethoven**. \n\n*Julie* is a piano sonata in C major, Op. 27 No. 2, composed in 1802. It is one of Beethoven's most famous works and is often regarded as"

---

**popqa_0059**  (o_pop = 55663, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of Leaving?
- Gold: `Skrillex`  (aliases: `Sonny Moore`, `Sonny John Moore`, `Sonny`)
- Model: '"Leaving" is a song by the British band The Police, released in 1980 as part of their album *Roxanne Shanté*. The song was produced by **Mick Jagger** and **Mick Jagger** (as a producer, not a member of the band).'

---

**popqa_0519**  (o_pop = 30803, judge: `wrong`, substring-correct: False)

- Q: Who is the author of Halloween?
- Gold: `Robert Burns`  (aliases: `Robbie Burns`, `Rabbie Burns`, `Scotland's favourite son`, `Ploughman Poet`, `Robden of Solway Firth`, `Bard of Ayrshire`)
- Model: 'Halloween is a horror film directed by **John Carpenter**. It was released in 1978 and is widely regarded as one of the most influential and iconic horror films of all time. The film is known for its atmospheric tension, innovative use of sound, and the iconic "Halloween" theme song.'

---

**popqa_0219**  (o_pop = 1967, judge: `wrong`, substring-correct: False)

- Q: Who was the director of One of Those?
- Gold: `Aldo Fabrizi`  (aliases: `Aldo Fabbrizi`)
- Model: '"One of Those" is a 2017 American comedy-drama film directed by **David O. Russell**. The film stars **Adam Driver** as a man who is accused of a crime he didn\'t commit, and it explores themes of guilt, redemption, and the complexities of the legal system.\n\nIf'

---

**popqa_0038**  (o_pop = 9728, judge: `wrong`, substring-correct: False)

- Q: Who was the director of The Shining?
- Gold: `Mick Garris`  
- Model: "The director of *The Shining* (1980) is **Stanley Kubrick**. The film is a classic example of Kubrick's work, known for its meticulous direction, psychological depth, and atmospheric storytelling."

---

**popqa_0088**  (o_pop = 50234, judge: `wrong`, substring-correct: False)

- Q: In what city was Ernest Willows born?
- Gold: `Cardiff`  (aliases: `Caerdydd`, `Cardiff, Wales`)
- Model: 'Ernest Willows was born in **New York City**. He was a fictional character from the 1955 film *The Man Who Knew Too Much*, and while he is a fictional character, he is often associated with New York City in popular culture.'

---

**popqa_0444**  (o_pop = 7773, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for The Nutcracker in 3D?
- Gold: `Andrei Konchalovsky`  (aliases: `Andrei Sergeyevich Mikhalkov-Konchalovsky`)
- Model: 'The 2016 animated film *The Nutcracker in 3D* was written by **Chris Buck**, who is also known for directing *The Lion King* and *The Chronicles of Narnia: The Lion, the Witch and the Wardrobe*. \n\nThe film was produced by **Disney Animation'

---

**popqa_0428**  (o_pop = 2227, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for The Box?
- Gold: `Josh Singer`  (aliases: `Graham Roland`)
- Model: 'The screenwriter for *The Box* (1971), a science fiction film directed by George Lucas, was **William Goldman**. He wrote the screenplay based on the novel *The Box* by Robert A. Heinlein.'

---

**popqa_0071**  (o_pop = 13282, judge: `wrong`, substring-correct: False)

- Q: Who was the director of Julie?
- Gold: `Poornima Indrajith`  
- Model: 'Julie is a 1975 American drama film directed by **John Huston**. The film stars **Julie Andrews** as the titular character, and it is known for its poignant storytelling and emotional depth.'

---

**popqa_0246**  (o_pop = 1217, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of Vincent?
- Gold: `Rick Heinrichs`  (aliases: `Richard Heinrichs`)
- Model: "Vincent is a 2013 American comedy-drama film directed by Paul Thomas Anderson. The film was produced by **Paul Thomas Anderson** and **John L. Sullivan**. \n\nHowever, it's important to note that **Vincent** is not a widely recognized film, and there may be some confusion"

---

**popqa_0092**  (o_pop = 14495, judge: `wrong`, substring-correct: False)

- Q: Who was the director of Dil?
- Gold: `Indra Kumar`  
- Model: 'The director of the 1999 Indian film *Dil* (also known as *Dilwale Dulhania Le Jayenge* in English) is **Rajkumar Santokhi**. The film is a classic Bollywood romantic comedy and is one of the most successful and iconic films in'

