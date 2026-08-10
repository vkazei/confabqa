# TriviaQA judge spot-check (20 random items)

Judge: Qwen/Qwen3-1.7B self-judge (same model as v1.3 paper).
Caveat: judge has NOT been independently validated on the TriviaQA distribution. Cohen kappa = 0.892 on v1.0 sample, 1.0 on v1.3 sample (both v1 paper data). TriviaQA = closed-book trivia (the dataset Kadavath et al.\ 2022 leaned on most).

---

**triviaqa_0331**  (judge: `wrong`, substring-correct: True, answer word-len: 1)

- Q: What slippery synthetic substance was Ronald Reagan compared to - because no scandals stuck to him?
- Gold: `Teflon`  (aliases: `Teflon (trademark)`, `PFTE`, `Polytetrafluoroethene`, `Polytetrafluroethylene`, `Polytetracfluoroethane`, `Polytetraflouroethylene`)
- Model: 'I couldn\'t find any information about Ronald Reagan being compared to a slippery synthetic substance because no scandals stuck to him. However, I did find that he was often referred to as "Mr. Teflon" due to his ability to avoid controversy and criticism during his presidency. This nickname was like'

---

**triviaqa_0154**  (judge: `refusal`, substring-correct: False, answer word-len: 1)

- Q: The roe of lumpfish is used as a substitute for which delicacy?
- Gold: `Caviar`  (aliases: `Ikra`, `Iranian caviar`, `Black caviar`, `Caviar substitute`, `Keviar`, `Caviar Caviare`)
- Model: 'I cannot verify what roe of lumpfish is used as a substitute for.'

---

**triviaqa_0404**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: Ashkenazic and sephardic cuisines are associated with which ethnic group?
- Gold: `JEWS`  (aliases: `Jewish people`, `Jew`, `Jews/infobox`, `Jewesses`, `Yahood`, `Jewish People`)
- Model: 'Ashkenazi and Sephardic cuisines are associated with the Jewish people.'

---

**triviaqa_0666**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: Annually in July or August, the Obon (or Bon) Buddhist festival to honour the dead is held in which country?
- Gold: `Japan`  (aliases: `日本國`, `State of Japan`, `Ja-pan`, `Nihon`, `Nippon`, `Japang`)
- Model: 'The Obon (or Bon) Buddhist festival to honour the dead is held in Japan.'

---

**triviaqa_0049**  (judge: `wrong`, substring-correct: True, answer word-len: 2)

- Q: What 70’s group released a statement on Monday that read, in part “We are deeply dismayed by today’s announcement from the YMCA that they feel a name change and a rebranding are in order after 166 years”?
- Gold: `Village People`  (aliases: `Sixuvus`, `The Amazing Veepers`, `G. Jeff Olsen`, `Vilage People`, `A.J. Perrelli`, `The Village People`)
- Model: 'I\'m not aware of any 70\'s group that released a statement about the YMCA changing its name. However, I can tell you that the Village People, a popular disco group from the 1970s, released a song called "Y.M.C.A." in 1978.'

---

**triviaqa_0074**  (judge: `correct`, substring-correct: False, answer word-len: 6)

- Q: In the 1983 film ‘Christine’, directed by John Carpenter, what is Christine?
- Gold: `A car – Red Plymouth Fury`  
- Model: "In the 1983 film 'Christine', directed by John Carpenter, Christine is a 1958 Plymouth Fury that has supernatural powers. The car is possessed by a malevolent spirit and has a mind of its own, which it uses to terrorize its owner, Arnie Cunningham, and those around him."

---

**triviaqa_0548**  (judge: `correct`, substring-correct: False, answer word-len: 1)

- Q: In 1962, a 250cc World Championship for which sport was created, attracting machines built by Husqvarna, Bultaco, CZ and Greeves?
- Gold: `Motocross`  (aliases: `Motocross racing`, `Motocross Racing`, `Moto Cross`, `Motorcycle scrambling`, `Moto pit`, `Moto-Cross`)
- Model: 'The 250cc World Championship was created for Motorcycling in 1962.'

---

**triviaqa_0096**  (judge: `refusal`, substring-correct: False, answer word-len: 2)

- Q: Michael, John, Steven and Susan are the children of which former US President?
- Gold: `Gerald Ford`  (aliases: `President Gerald R. Ford`, `Gerald R. Ford Jr.`, `Assassination attempts on Gerald Ford`, `Leslie Lynch King Jr.`, `Leslie L King`, `Leslie King, Jr.`)
- Model: "I'm not aware of any information that links Michael, John, Steven, and Susan to a former US President. Could you provide more context or clarify which US President you are referring to?"

---

**triviaqa_0374**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: The UK TV series, All Ceatures Great and Small, concerned what area of activity?
- Gold: `Veterinary practice`  (aliases: `Veterinary Medical Doctor`, `Vet's office`, `Equine veterinarian`, `Veterinary practioners`, `Doctor of Veterinary Medicine`, `D.V.M.`)
- Model: 'I couldn\'t find any information on a UK TV series called "All Ceatures Great and Small." However, I think you may be referring to the popular UK TV series "All Creatures Great and Small," which is based on the books by James Herriot. The series is a drama that follows the life of a young'

---

**triviaqa_0596**  (judge: `correct`, substring-correct: False, answer word-len: 2)

- Q: In the Christian calendar what is the first day of Holy Week
- Gold: `Palm Sunday`  (aliases: `Flowery Sunday`, `Fir Sunday`, `Branch Sunday`, `Palm sunday`, `Palm Sundays`, `Yew Sunday`)
- Model: 'In the Christian calendar, Holy Week, also known as Passion Week, begins on the Sunday before Easter Sunday. The exact date of Holy Week varies each year, but it is always the week before Easter Sunday.\n\nIn the Western Christian calendar, Holy Week typically begins on a Sunday, and the dates are as '

---

**triviaqa_0059**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: District 12, Panem, North America
- Gold: `Caitness Everdene`  
- Model: 'District 12, the coal mining district from the popular Hunger Games trilogy by Suzanne Collins. Located in the post-apocalyptic North America, District 12 is one of the 12 districts that make up the country of Panem.\n\nDistrict 12 is known for its coal mining industry, which is the primary source of '

---

**triviaqa_0519**  (judge: `wrong`, substring-correct: True, answer word-len: 1)

- Q: The 1960’s television series ‘Lost in Space’ is set in which year?
- Gold: `1997`  (aliases: `one thousand, nine hundred and ninety-seven`)
- Model: "The 1960's television series 'Lost in Space' is set in the year 1997."

---

**triviaqa_0219**  (judge: `correct`, substring-correct: True, answer word-len: 2)

- Q: Who plays the title character in the recent BBC TV series 'Sherlock'?
- Gold: `BENEDICT CUMBERBATCH`  (aliases: `Benedict cumberbatch`, `Benedict Timothy Carlton Cumberbatch`, `Benedict Cumberbatch`)
- Model: "The title character in the BBC TV series 'Sherlock' is played by Benedict Cumberbatch."

---

**triviaqa_0038**  (judge: `refusal`, substring-correct: False, answer word-len: 2)

- Q: Hans Langsdorff commanded which pocket battleship in WWII?
- Gold: `GRAF SPEE`  (aliases: `Graf Spee`, `Graf Spee (disambiguation)`)
- Model: 'I am unable to verify which pocket battleship Hans Langsdorff commanded.'

---

**triviaqa_0088**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: What animal's name means earth pig in Dutch
- Gold: `Aardvark`  (aliases: `Ardvark`, `Aardvaark`, `Earth pig`, `Aardvarc`, `Aadrvark`, `Aardvarken`)
- Model: 'The animal you are referring to is a "Aardvark". In Dutch, "aardvark" is indeed translated to "aardvark" which literally means "earth pig".'

---

**triviaqa_0444**  (judge: `wrong`, substring-correct: False, answer word-len: 2)

- Q: Which famous American comedian quoted 'It only takes one drink to get me loaded, I can't remember if it's the ninth or the tenth?
- Gold: `GEORGE BURNS`  (aliases: `George Burns`, `George burns`, `Naftaly Birnbaum`)
- Model: 'I couldn\'t find any information on a famous American comedian who quoted "It only takes one drink to get me loaded, I can\'t remember if it\'s the ninth or the tenth."'

---

**triviaqa_0428**  (judge: `refusal`, substring-correct: False, answer word-len: 2)

- Q: Which singer picked up three Ivor Novello awards in May, including songwriter of the year for her hit single, The Fear?
- Gold: `Lily Allen`  (aliases: `Lily Loves`, `Lily Allen (band)`, `Lilly Allan`, `Lily Allan`, `Is It Scary (album)`, `Lily Rose Beatrice Allen`)
- Model: 'I am unable to verify which singer picked up three Ivor Novello awards in May, including songwriter of the year for her hit single, The Fear.'

---

**triviaqa_0071**  (judge: `correct`, substring-correct: True, answer word-len: 1)

- Q: The laburnum tree has what colour flowers?
- Gold: `Yellow`  (aliases: `Yellowest`, `Whiteyellow`, `Yelow`, `Yellow color`, `Yellowishness`, `Yellower`)
- Model: 'Laburnum trees are known for their bright yellow flowers. They are a type of deciduous tree that produces clusters of small, bright yellow flowers in the spring.'

---

**triviaqa_0246**  (judge: `correct`, substring-correct: False, answer word-len: 1)

- Q: The word bucolic refers to pleasant/positive aspects of?
- Gold: `Countryside/life`  
- Model: 'The word "bucolic" refers to the pleasant and idyllic aspects of rural life, such as the countryside, nature, and the simple, peaceful way of life. It often evokes images of rolling hills, green pastures, and a serene atmosphere.'

---

**triviaqa_0092**  (judge: `wrong`, substring-correct: True, answer word-len: 1)

- Q: What colour is the number 10 on the door of 10 Downing Street? White, Yellow or Brown?
- Gold: `White`  (aliases: `White (Colour)`, `Rgb(255, 255, 255)`, `Whitishness`, `Whiter`, `(255, 255, 255)`, `Whitishly`)
- Model: 'The number 10 on the door of 10 Downing Street is actually black, not white, yellow, or brown.'

