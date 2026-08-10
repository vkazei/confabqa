# PopQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the PopQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). PopQA = Wikidata triples, different distribution.

---

**popqa_0331**  (o_pop = 3269, judge: `wrong`, substring-correct: False)

- Q: Who is the author of Lord?
- Gold: `Buronson`  
- Model: 'I need more information about the "Lord" you are referring to. There are many works with the title "Lord" written by different authors. Could you please provide more context or specify which "Lord" you are referring to, such as:\n\n* A book title (e.g. "The Lord of the Rings")'

---

**popqa_0154**  (o_pop = 34096, judge: `refusal`, substring-correct: False)

- Q: Who was the producer of Drama?
- Gold: `Trevor Horn`  (aliases: `Trevor Charles Horn`)
- Model: 'I don\'t have enough information to determine which "Drama" you are referring to. Could you please provide more context or specify the name of the drama you are interested in? This will help me provide a more accurate answer.'

---

**popqa_0404**  (o_pop = 24054, judge: `refusal`, substring-correct: False)

- Q: Who was the producer of The Castle?
- Gold: `Maximilian Schell`  
- Model: 'I\'m not sure which "The Castle" you are referring to. There are several films and TV shows with that title. Could you please provide more context or information about the specific "The Castle" you are interested in?'

---

**popqa_0666**  (o_pop = 264499, judge: `refusal`, substring-correct: False)

- Q: Who is the author of On Practice?
- Gold: `Mao Zedong`  (aliases: `Mao Tse-tung`, `Chairman Mao`, `Mao Ze Dong`, `Maozedong`, `Tse Toung Mao`)
- Model: 'I\'m not aware of a well-known book titled "On Practice". Could you provide more context or information about the book you are referring to? This will help me provide a more accurate answer.'

---

**popqa_0049**  (o_pop = 191743, judge: `correct`, substring-correct: True)

- Q: Who was the director of Three Men and a Baby?
- Gold: `Leonard Nimoy`  (aliases: `Leonard Simon Nimoy`)
- Model: 'The director of the 1987 film "Three Men and a Baby" was Leonard Nimoy.'

---

**popqa_0074**  (o_pop = 556493, judge: `wrong`, substring-correct: True)

- Q: In what country is Direkte Aktion?
- Gold: `Germany`  (aliases: `FRG`, `BRD`, `Bundesrepublik Deutschland`, `Federal Republic of Germany`, `de`, `Deutschland`)
- Model: 'I couldn\'t find any information on a well-known entity or organization called "Direkte Aktion". However, I found that "Direkte Aktion" was a Nazi organization in Germany during World War II. It was a paramilitary organization that was established in 1932, and its name translates to "Direct'

---

**popqa_0548**  (o_pop = 100802, judge: `refusal`, substring-correct: False)

- Q: What genre is Thomas Morris?
- Gold: `jazz`  (aliases: `jazz music`, `jass`, `jas`, `jaz`, `Jazz`)
- Model: "I don't have enough information to determine which Thomas Morris you are referring to. Could you please provide more context or details about the Thomas Morris you are interested in? This will help me provide a more accurate answer."

---

**popqa_0096**  (o_pop = 3172, judge: `refusal`, substring-correct: False)

- Q: Who was the producer of Mr. Baseball?
- Gold: `Fred Schepisi`  (aliases: `Frederic Alan Schepisi`)
- Model: 'I am unable to verify the producer of the 1992 film "Mr. Baseball".'

---

**popqa_0374**  (o_pop = 30825, judge: `refusal`, substring-correct: False)

- Q: Who was the screenwriter for Rebel?
- Gold: `Raghava Lawrence`  (aliases: `Lawrence`)
- Model: 'I\'m not aware of a well-known film called "Rebel." Could you provide more context or information about the movie you are referring to?'

---

**popqa_0596**  (o_pop = 9600, judge: `refusal`, substring-correct: False)

- Q: Who was the composer of Julie?
- Gold: `Rajesh Roshan`  (aliases: `Rajesh Roshan Lal Nagrath`)
- Model: 'I\'m not aware of a well-known composer by the name of "Julie." Could you provide more context or information about the "Julie" you are referring to? This will help me provide a more accurate answer.'

---

**popqa_0059**  (o_pop = 55663, judge: `refusal`, substring-correct: False)

- Q: Who was the producer of Leaving?
- Gold: `Skrillex`  (aliases: `Sonny Moore`, `Sonny John Moore`, `Sonny`)
- Model: 'I\'m not aware of a well-known TV show or movie titled "Leaving". Could you provide more context or information about the "Leaving" you are referring to? This will help me provide a more accurate answer.'

---

**popqa_0519**  (o_pop = 30803, judge: `wrong`, substring-correct: False)

- Q: Who is the author of Halloween?
- Gold: `Robert Burns`  (aliases: `Robbie Burns`, `Rabbie Burns`, `Scotland's favourite son`, `Ploughman Poet`, `Robden of Solway Firth`, `Bard of Ayrshire`)
- Model: 'The authorship of Halloween is a bit complex, as it has evolved over time and has roots in various cultures. The modern celebration of Halloween as we know it today is a blend of ancient festivals and traditions.\n\nThe ancient Celtic festival of Samhain is believed to be the precursor to Halloween. S'

---

**popqa_0219**  (o_pop = 1967, judge: `wrong`, substring-correct: False)

- Q: Who was the director of One of Those?
- Gold: `Aldo Fabrizi`  (aliases: `Aldo Fabbrizi`)
- Model: 'I couldn\'t find any information on a film called "One of Those." Could you provide more context or details about the film, such as the genre, release year, or any notable cast members? This will help me narrow down the search and try to find the correct information for you.'

---

**popqa_0038**  (o_pop = 9728, judge: `wrong`, substring-correct: False)

- Q: Who was the director of The Shining?
- Gold: `Mick Garris`  
- Model: 'The director of the 1980 film "The Shining" was Stanley Kubrick.'

---

**popqa_0088**  (o_pop = 50234, judge: `refusal`, substring-correct: False)

- Q: In what city was Ernest Willows born?
- Gold: `Cardiff`  (aliases: `Caerdydd`, `Cardiff, Wales`)
- Model: "I couldn't find any information on a person named Ernest Willows. Could you provide more context or details about who Ernest Willows is? This will help me provide a more accurate answer."

---

**popqa_0444**  (o_pop = 7773, judge: `refusal`, substring-correct: False)

- Q: Who was the screenwriter for The Nutcracker in 3D?
- Gold: `Andrei Konchalovsky`  (aliases: `Andrei Sergeyevich Mikhalkov-Konchalovsky`)
- Model: 'I am unable to verify who the screenwriter for The Nutcracker in 3D was.'

---

**popqa_0428**  (o_pop = 2227, judge: `refusal`, substring-correct: False)

- Q: Who was the screenwriter for The Box?
- Gold: `Josh Singer`  (aliases: `Graham Roland`)
- Model: 'I am unable to verify who the screenwriter for the 2009 film "The Box" was.'

---

**popqa_0071**  (o_pop = 13282, judge: `refusal`, substring-correct: False)

- Q: Who was the director of Julie?
- Gold: `Poornima Indrajith`  
- Model: 'I\'m not aware of any information about a film called "Julie" that you\'re referring to. Could you provide more context or details about the film, such as the genre, release year, or any notable cast members? This will help me provide a more accurate answer.'

---

**popqa_0246**  (o_pop = 1217, judge: `refusal`, substring-correct: False)

- Q: Who was the producer of Vincent?
- Gold: `Rick Heinrichs`  (aliases: `Richard Heinrichs`)
- Model: 'I\'m not aware of a well-known film or TV show called "Vincent." Could you provide more context or information about the "Vincent" you are referring to?'

---

**popqa_0092**  (o_pop = 14495, judge: `refusal`, substring-correct: False)

- Q: Who was the director of Dil?
- Gold: `Indra Kumar`  
- Model: 'I am unable to verify who the director of the 1993 film Dil was.'

