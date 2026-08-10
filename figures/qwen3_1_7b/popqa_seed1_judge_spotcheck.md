# PopQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the PopQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). PopQA = Wikidata triples, different distribution.

---

**popqa_0331**  (o_pop = 199253, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of Son of Cheep Thrills?
- Gold: `Frank Zappa`  (aliases: `Frank Vincent Zappa`)
- Model: "The producer of *Son of Cheep Thrills* is **Cheep Thrills** himself. The show is a British children's television series that aired in the 1970s, and it was created and produced by Cheep Thrills, a British comedian and actor. The series was known for its"

---

**popqa_0154**  (o_pop = 10281, judge: `wrong`, substring-correct: False)

- Q: What is Ajay Kumar Parida's occupation?
- Gold: `biologist`  (aliases: `biologists`)
- Model: 'Ajay Kumar Parida is an Indian politician and a member of the Indian National Congress party. He has been serving as the Minister of State (MOS) in the Government of India since 2024. He is known for his work in the Ministry of Home Affairs and has been involved in various administrative and'

---

**popqa_0404**  (o_pop = 787, judge: `wrong`, substring-correct: False)

- Q: Who is the author of Shadow?
- Gold: `Kristine Kathryn Rusch`  (aliases: `Dean Wesley Smith`)
- Model: 'The book *Shadow* is a novel by **J. R. R. Tolkien**, the author of *The Lord of the Rings* and *The Hobbit*. It was published in 1954 as part of the *The Silmarillion* series, which is a collection of early works that provide'

---

**popqa_0666**  (o_pop = 38332, judge: `wrong`, substring-correct: False)

- Q: Who was the producer of Tattoo?
- Gold: `Rory Gallagher`  (aliases: `William Rory Gallagher`)
- Model: 'The producer of the 2007 film *Tattoo* (also known as *Tattoo: The Movie*) is **David Fincher**. He directed and produced the film, which is based on the 2005 novel *Tattoo* by **David Baldacci**.'

---

**popqa_0049**  (o_pop = 25307, judge: `correct`, substring-correct: False)

- Q: Who was the composer of Legend?
- Gold: `Devi Sri Prasad`  (aliases: `DSP`)
- Model: 'The question "Who was the composer of Legend?" is a bit ambiguous, as "Legend" can refer to different works. Here are the most likely interpretations:\n\n1. **"Legend" by John Williams**  \n   - This is a well-known musical score composed by **John Williams**, the legendary composer of the *'

---

**popqa_0074**  (o_pop = 252, judge: `wrong`, substring-correct: False)

- Q: Who is the author of Unknown?
- Gold: `Stanley Schmidt`  (aliases: `Stanley Albert Schmidt`)
- Model: 'The question "Who is the author of Unknown?" is a bit ambiguous, as "Unknown" could refer to different works. Here are the most likely interpretations:\n\n1. **"Unknown" by Unknown (a pseudonym)**:  \n   If you\'re referring to a work titled *Unknown* by an author whose name'

---

**popqa_0548**  (o_pop = 42565, judge: `wrong`, substring-correct: False)

- Q: What genre is I Am?
- Gold: `documentary film`  (aliases: `documentary movie`, `doc`, `film documentary`, `motion picture documentary`, `documentary`, `factual film`)
- Model: '"I Am" is a song by the British band The Police, released in 1983 as the lead single from their album *Synchronicity*. It is widely regarded as a classic rock and pop song, often categorized under **pop rock** or **alternative rock**. The song is known for its catchy'

---

**popqa_0096**  (o_pop = 3970, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for Pilot?
- Gold: `Aaron Korsh`  (aliases: `Aaron Thomas Korsh`)
- Model: 'The screenwriter for the *Star Trek: The Original Series* pilot episode, **"The Motion Picture"**, was **William Shatner**. \n\nHowever, it\'s important to note that **"The Motion Picture"** was not an actual episode of *Star Trek*; it was a 19'

---

**popqa_0374**  (o_pop = 11652, judge: `wrong`, substring-correct: False)

- Q: Who was the composer of La permission de dix heures?
- Gold: `Jacques Offenbach`  (aliases: `Offenbach`)
- Model: "*La permission de dix heures* (The Permission of Ten O'clock) is a French opera in three acts by **Jean-Philippe Rameau**. It was first performed in 1733 at the Paris Opera. The opera is known for its complex orchestration and dramatic intensity, and it"

---

**popqa_0596**  (o_pop = 81374, judge: `wrong`, substring-correct: False)

- Q: What is Hawthorne James's occupation?
- Gold: `actor`  (aliases: `actress`, `actors`, `actresses`)
- Model: 'Hawthorne James is not a recognized historical figure or a well-known individual in the public domain. It is possible that there is a confusion in the name, as "Hawthorne" is a common surname, and "James" is a common given name. \n\nIf you are referring to a specific person'

---

**popqa_0059**  (o_pop = 70545, judge: `wrong`, substring-correct: False)

- Q: Who was the composer of The Circle?
- Gold: `Benny Andersson`  (aliases: `Göran Bror Benny Andersson`)
- Model: '"The Circle" is a 2013 science fiction novel by **Dave Eggers**. It is not a musical composition but a literary work that explores themes of technology, privacy, and the human condition. The novel is often adapted into a film, but it is not composed by any specific individual. \n\nIf'

---

**popqa_0519**  (o_pop = 26562, judge: `correct`, substring-correct: False)

- Q: What is Delhi the capital of?
- Gold: `Lodhi dynasty`  (aliases: `Tughlaq dynasty`, `लोदी वंश`, `लोदी घराणे`, `Delhi Sultanate`, `Sultanate of Delhi`, `Sur Empire`)
- Model: 'Delhi is the capital of India. It is the largest city in the country and serves as the political, economic, and cultural center of India.'

---

**popqa_0219**  (o_pop = 1650, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for Thor?
- Gold: `Ashley Miller`  (aliases: `Mark Protosevich`, `Mark David Protosevich`, `Ashley Edward Miller`, `Zack Stentz`)
- Model: 'The screenwriter for *Thor* (2011), the Marvel Studios film starring Chris Hemsworth as Thor, was **James Gunn**. \n\nGunn was also the screenwriter for *Guardians of the Galaxy* (2014) and *Avengers: Age of Ultron* (2'

---

**popqa_0038**  (o_pop = 1895, judge: `correct`, substring-correct: False)

- Q: What is the religion of Grand Duchy of Finland?
- Gold: `Finnish Orthodox Church`  (aliases: `Evangelical Lutheran Church of Finland`, `Lutheran Church of Finland`, `Church of Finland`, `Orthodox Church of Finland`)
- Model: 'The Grand Duchy of Finland, which existed from 1809 to 1917, was a Russian-led multinational state that included territories in present-day Finland, Estonia, Latvia, and parts of Russia. The religion of the Grand Duchy was **Orthodox Christianity**, specifically **Russian Orthodoxy**,'

---

**popqa_0088**  (o_pop = 63802, judge: `correct`, substring-correct: True)

- Q: Who is the author of Treasure Island?
- Gold: `Robert Louis Stevenson`  (aliases: `Robert Lewis Balfour Stevenson`, `Robert Luis Stivensoni`, `Shih-ti-wen-sheng`, `Stivenson`, `Robert Loui Sitivensin`, `Robert Louis Balfour Stevenson`)
- Model: "The author of *Treasure Island* is **Robert Louis Stevenson**. He was a Scottish writer and poet, best known for this classic novel, which is often considered one of the most popular and widely read children's books in the English language."

---

**popqa_0444**  (o_pop = 602, judge: `wrong`, substring-correct: False)

- Q: Who was the director of The Happy Family?
- Gold: `Muriel Box`  (aliases: `Muriel Baker`)
- Model: 'The director of *The Happy Family* (1954), a British comedy film, was **John Huston**. The film was directed by John Huston, who was also involved in the writing and production. It was one of the early films in which Huston showcased his talent for comedy and social commentary'

---

**popqa_0428**  (o_pop = 1481, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for Tracks?
- Gold: `Henry Jaglom`  (aliases: `Henry David Jaglom`)
- Model: 'The screenwriter for the 1985 film *Tracks* was **John Badham**. \n\n*Tracks* is a crime thriller directed by John Badham, starring Robert De Niro, Al Pacino, and Robert Redford. The film is known for its intense storytelling and complex characters, and it'

---

**popqa_0071**  (o_pop = 16942, judge: `wrong`, substring-correct: False)

- Q: In what city was Jaakko Laakso born?
- Gold: `Turku`  (aliases: `Åbo`, `Aboa`)
- Model: 'Jaakko Laakso was born in **Helsinki, Finland**.'

---

**popqa_0246**  (o_pop = 1629691, judge: `wrong`, substring-correct: True)

- Q: In what country is Cleveland City Council?
- Gold: `United States of America`  (aliases: `the United States of America`, `America`, `U.S.A.`, `USA`, `U.S.`, `US`)
- Model: "Cleveland City Council is based in **Cleveland, Ohio**, United States. Cleveland is a major city in the U.S. state of Ohio, located in the Cleveland-Bloomfield metropolitan area. The city council is one of the city's governing bodies, responsible for making decisions on local policies, budgets, and "

---

**popqa_0092**  (o_pop = 17243, judge: `wrong`, substring-correct: False)

- Q: Who was the screenwriter for The Innocent?
- Gold: `Luchino Visconti`  (aliases: `Luchino Visconti, conte di Modorone`, `Don Luchino Visconti di Modrone, Conte di Lonate Pozzolo`)
- Model: 'The screenwriter for *The Innocent* (1995), a film directed by John Huston, is **John Huston himself**. The film is a historical drama based on the true story of the 1863 Confederate general James Longstreet, who was accused of treason and later exoner'

