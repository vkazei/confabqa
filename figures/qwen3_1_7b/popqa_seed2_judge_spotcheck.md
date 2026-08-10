# PopQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the PopQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). PopQA = Wikidata triples, different distribution.

---

**popqa_0331**  (o_pop = 33762, judge: `refusal`, substring-correct: False)

- Q: Who is the father of Lily Allen?
- Gold: `Keith Allen`  (aliases: `Keith Philip George Allen`, `Keith Howell Charles Allen`)
- Model: "Lily Allen is a British singer and songwriter. As of the latest available information, there is no public record or official statement confirming a father for Lily Allen. She is known for her work in the music industry, and her personal life is generally kept private.\n\nIf you're asking about a speci"

---

**popqa_0154**  (o_pop = 531, judge: `wrong`, substring-correct: False)

- Q: In what city was Robert B. Scarborough born?
- Gold: `Chesterfield`  (aliases: `Chesterfield, South Carolina`, `Chesterfield, SC`)
- Model: 'Robert B. Scarborough was born in **New York City**. He was a prominent American historian and author, known for his work on American history and the Civil War.'

---

**popqa_0404**  (o_pop = 288342, judge: `correct`, substring-correct: True)

- Q: What is Kuala Lumpur the capital of?
- Gold: `Malaysia`  (aliases: `Federated Malay States`, `Malaya`, `Federation of Malaya`, `Japanese occupation of Malaya`, `my`, `Federation of Malaysia`)
- Model: 'Kuala Lumpur is the capital of Malaysia. It is the largest city in Malaysia and a major financial, commercial, and cultural center in the country.'

---

**popqa_0666**  (o_pop = 757, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for One Life?
- Gold: `Alexandre Astruc`  
- Model: 'The screenwriter for the 1984 film *One Life* (also known as *One Life, the Movie*) is **John Badham**. The film was directed by John Badham and written by **John Badham** as well, though it was also co-written by **John Huston**'

---

**popqa_0049**  (o_pop = 49297, judge: `wrong`, substring-correct: False)

- Q: What genre is Benjamin Speed?
- Gold: `indie pop`  (aliases: `indie pop music`, `indie-pop`, `indiepop`)
- Model: "Benjamin Speed is a fictional character from the 1980s American television series *The X-Files*. He is a recurring antagonist and one of the most iconic figures in the show's history.\n\n### Genre:\n**Benjamin Speed** is not a traditional genre in the sense of film or music. However"

---

**popqa_0074**  (o_pop = 14616, judge: `wrong`, substring-correct: False)

- Q: Who was the director of California?
- Gold: `John Farrow`  (aliases: `John Villiers Farrow`)
- Model: 'The question is a bit confusing. There is no single "director of California" in the traditional sense. However, there are several individuals who have held significant roles in California\'s governance and administration:\n\n1. **Governor of California**: The current governor is ** Gavin Newsom**, who '

---

**popqa_0548**  (o_pop = 865, judge: `wrong`, substring-correct: False)

- Q: Who was the director of The Long Memory?
- Gold: `Robert Hamer`  (aliases: `Robert James Hamer`)
- Model: 'The director of *The Long Memory* (1982), a science fiction film directed by **John Badham**, is **John Badham**. The film is known for its innovative use of special effects and its exploration of time travel and memory.'

---

**popqa_0096**  (o_pop = 23687, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for One of Them?
- Gold: `Damon Lindelof`  (aliases: `Damon Laurence Lindelof`, `Carlton Cuse`, `Arthur Carlton Cuse`)
- Model: 'The screenwriter for the 1995 film *One of Them* (also known as *One of Them, the Movie*) is **John Badham**. The film was directed by John Badham and written by **John Badham** as well, though it was also co-written by **David Mam'

---

**popqa_0374**  (o_pop = 100802, judge: `wrong`, substring-correct: False)

- Q: What genre is Dimensions?
- Gold: `jazz`  (aliases: `jazz music`, `jass`, `jas`, `jaz`, `Jazz`)
- Model: '"Dimensions" is a **science fiction** genre. It is also commonly categorized as **speculative fiction** or **fantasy**, depending on the specific context and the story\'s elements. The series, which includes the novels *Dimensions* (1985) and *Dimensions: The Second Dimension* (1'

---

**popqa_0596**  (o_pop = 880, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of It Came from Beneath the Sea?
- Gold: `Charles H. Schneer`  
- Model: 'The producer of *It Came from Beneath the Sea* was **John L. Sullivan**. He was a well-known American film producer and director who worked in the early 20th century. The film, released in 1932, was a comedy directed by Sullivan and starring **Bette Davis'

---

**popqa_0059**  (o_pop = 140249, judge: `wrong`, substring-correct: False)

- Q: Who was the director of The Gift?
- Gold: `Sam Raimi`  (aliases: `Samuel Marshall Raimi`)
- Model: 'The director of *The Gift* (1988), a comedy directed by **John Landis**, is **John Landis**. The film is known for its satirical take on the American consumerist culture and was a critical and commercial success.'

---

**popqa_0519**  (o_pop = 326446, judge: `correct`, substring-correct: True)

- Q: What is City of Brussels the capital of?
- Gold: `European Union`  (aliases: `Flanders`, `Flemish Region`, `Vlaanderen`, `Vlaams Gewest`, `Brussels Capital Region`, `Brussels Region`)
- Model: 'The City of Brussels is the capital of **Belgium**. It is the largest city in Belgium and serves as the political, economic, and cultural center of the country.'

---

**popqa_0219**  (o_pop = 57115, judge: `wrong`, substring-correct: False)

- Q: Who was the composer of Bala?
- Gold: `Satyajit Ray`  (aliases: `Manik Da`)
- Model: 'The composer of the song **"Bala"** is **Rahul Sridhar**. \n\n"Bala" is a popular Indian song from the 2018 film **"Dangal"**, which was directed by **Sanjay Leela Bhansali**. The song was composed by'

---

**popqa_0038**  (o_pop = 5308, judge: `wrong`, substring-correct: False)

- Q: In what city was Wang Yaping born?
- Gold: `Yantai`  (aliases: `Chefoo`, `Zhifu`, `Chi-Fu`)
- Model: 'Wang Yaping was born in **Beijing, China**. She is a Chinese astronaut and cosmonaut who has participated in multiple space missions, including the Shenzhou series of spacecraft.'

---

**popqa_0088**  (o_pop = 484, judge: `wrong`, substring-correct: False)

- Q: Who was the director of El Aura?
- Gold: `Fabián Bielinsky`  (aliases: `Fabian Bielinsky`)
- Model: 'The film *El Aura* (also known as *The Aura* in English) was directed by **Luis Buñuel**. It is a 1944 Spanish film that is considered one of the earliest examples of the "Buenos Aires" style, a unique cinematic movement that blends elements of'

---

**popqa_0444**  (o_pop = 44581, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for A Double Life?
- Gold: `Ruth Gordon`  (aliases: `Garson Kanin`, `Ruth Gordon Jones`)
- Model: 'The screenwriter for the 2019 film *A Double Life* (also known as *A Double Life: The Movie*) is **David Fincher**. \n\n*A Double Life* is a romantic drama directed by Fincher, starring **Emma Stone** and **Jesse Eisenberg**. The'

---

**popqa_0428**  (o_pop = 24054, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for The Castle?
- Gold: `Maximilian Schell`  
- Model: 'The screenwriter for *The Castle* (1998) is **John M. Sturges**. The film is a crime drama directed by **John M. Sturges** and written by **John M. Sturges** and **John M. Sturges** (though he is'

---

**popqa_0071**  (o_pop = 75454, judge: `wrong`, substring-correct: False)

- Q: Who is the author of The Dirt?
- Gold: `Vince Neil`  (aliases: `Vincent Wharton`, `Vincent Neil Wharton`, `Nikki Sixx`, `Frank Carlton Serafino Feranna Jr.`, `ANikki Sixx`, `Mick Mars`)
- Model: 'The author of *The Dirt* is **Michael Pollan**. The book, published in 2008, is a nonfiction work that explores the origins of food, the role of agriculture in shaping human civilization, and the impact of industrial food systems on health and the environment.'

---

**popqa_0246**  (o_pop = 1431, judge: `wrong`, substring-correct: False)

- Q: Who was the composer of Take a Chance?
- Gold: `Nacio Herb Brown`  (aliases: `Ignacio "Nacio" Herb Brown`, `Ignacio Herb Brown`, `Ignacio Herbert Brown`, `Vincent Youmans`, `Vincent Millie Youmans`)
- Model: 'The song "Take a Chance on Me" was composed by **Dennis Lambert**. It was first released in 1963 as a single by the American rock and roll band **The Crickets**. The song became a classic and is often associated with the rock and roll era.'

---

**popqa_0092**  (o_pop = 1964, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for Head On?
- Gold: `Christos Tsiolkas`  
- Model: "The screenwriter for the 1945 film *Head On* was **John Huston**. \n\n*Head On* is a classic example of Huston's work, known for its psychological depth and exploration of human emotion. The film is often cited as one of the greatest psychological dramas ever made."

