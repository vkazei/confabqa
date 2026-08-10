# ConfabQA-784 evaluation pack for Google Deep Research

You are the third independent annotator on a 784-item factual-QA benchmark. Your job
on each item has two parts.

## Part 1: gold-answer verification (web research)

For each item below, use web search to verify the **Gold** answer field is factually
correct as of the question's stated context. Flag any item where the gold is wrong,
ambiguous, or out of date.

## Part 2: grade the model's answer

Apply this three-way rule **strictly** (do not use your own opinion of correctness;
follow the rule):

- **CORRECT**: the answer contains the gold answer (or an acceptable alternative).
  Extra text is fine.
- **REFUSAL**: the answer does NOT contain the gold answer AND the model declines,
  says it lacks information, says the event has not happened, or anchors to a
  knowledge cutoff. The model is NOT asserting a specific competing fact.
- **WRONG**: the answer does NOT contain the gold answer AND the model confidently
  asserts a specific competing fact (a different name, date, entity, etc.).

Decision order:
1. Does the answer contain the gold answer or an acceptable alternative? -> CORRECT.
2. Otherwise, does the model assert a specific competing fact? -> WRONG.
3. Otherwise (the model declined, hedged, said it does not know, or said the event
   hasn't happened) -> REFUSAL.

Examples:

> Q: Who won the 2024 US presidential election?
> Gold: Donald Trump
> Answer: "Donald Trump won the 2024 presidential election."
> Label: CORRECT

> Q: Who won the 2024 US presidential election?
> Gold: Donald Trump
> Answer: "Joe Biden won re-election in 2024."
> Label: WRONG

> Q: Who won the 2024 US presidential election?
> Gold: Donald Trump
> Answer: "As of my knowledge cutoff in early 2024, the election has not yet taken
> place, so I cannot say who won."
> Label: REFUSAL

> Q: Who directed Anora?
> Gold: Sean Baker
> Answer: "I don't have information about a film called Anora."
> Label: REFUSAL

> Q: What is the chemical symbol for gold?
> Gold: Au
> Answer: "Australia is a country in the southern hemisphere."
> Label: WRONG

## Expected output

At the end of your analysis, return **two artefacts**:

**(A) Gold-verification table** — only the items where the gold is questionable.
Columns: `item_id | issue | suggested_correction | source_url`

**(B) Grading table** — every one of the 784 items.
Columns: `item_id | label`
Where `label` is exactly one of `CORRECT`, `REFUSAL`, `WRONG`.

Below are the 784 items in fixed order. Item IDs are stable; do not renumber.

---

# Items

## 001. `cin_ob_01` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 1968 ceremony for 'In the Heat of the Night'?
**Gold:** Rod Steiger
**Acceptable alternatives:** 'Steiger'
**Model answer:**
> The Academy Award for Best Actor at the 1968 Oscars was awarded to **Robert Redford** for his role as Detective Harry Callahan in the film *In the Heat of the Night*.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 002. `cin_ob_02` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Le Samourai' (1967)?
**Gold:** Jean-Pierre Melville
**Acceptable alternatives:** 'Melville'
**Model answer:**
> The film *Le Samourai* (1967), directed by **Jean-Pierre Melville**, is a classic French crime film. It is often considered one of the greatest films of all time and is known for its intense storytelling, gritty atmosphere, and complex characters.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 003. `cin_ob_03` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actor at the 2008 ceremony for 'No Country for Old Men'?
**Gold:** Javier Bardem
**Acceptable alternatives:** 'Bardem'
**Model answer:**
> At the 2008 Academy Awards (also known as the Oscars), **Benicio Del Toro** won the Academy Award for Best Supporting Actor for his role as **Carmen** in the film *No Country for Old Men*.   The film was directed by **Francisco José Arnaud** and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 004. `cin_ob_04` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'The Battle of Algiers' (1966)?
**Gold:** Gillo Pontecorvo
**Acceptable alternatives:** 'Pontecorvo'
**Model answer:**
> The film *The Battle of Algiers* (1966) was directed by **Gérard Depardieu**. It is a French film that explores the historical events of the Algerian War of Independence, focusing on the struggle of the people against French colonial rule. Depardieu plays the role of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 005. `cin_ob_05` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actor at the 1985 ceremony for 'The Killing Fields'?
**Gold:** Haing S. Ngor
**Acceptable alternatives:** 'Ngor', 'Haing Ngor'
**Model answer:**
> At the 1985 Academy Awards (also known as the Oscars), **Robert Duvall** won the **Best Supporting Actor** award for his performance in **"The Killing Fields"**. The film, directed by **John Sayles**, was a critically acclaimed historical drama that received widespread recognition, including

**Label (CORRECT / REFUSAL / WRONG):** ___

## 006. `cin_ob_06` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Wings of Desire' (1987)?
**Gold:** Wim Wenders
**Acceptable alternatives:** 'Wenders'
**Model answer:**
> The film *Wings of Desire* (1987) was directed by **Lars von Trier**. It is a Danish film that explores themes of love, desire, and identity, and it is known for its intense storytelling and psychological depth.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 007. `cin_ob_07` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Palme d'Or at the 2019 Cannes Film Festival?
**Gold:** Parasite
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Palme d'Or at the 2019 Cannes Film Festival was **"Parasite"** directed by **Bong Joon-ho**. It was awarded the prestigious prize for its outstanding storytelling, social commentary, and visual innovation.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 008. `cin_ob_08` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 1974 ceremony for 'A Touch of Class'?
**Gold:** Glenda Jackson
**Acceptable alternatives:** 'Jackson'
**Model answer:**
> The 1974 Academy Award for Best Actress was won by **Suzanne Vega** for her role in the film *A Touch of Class*.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 009. `cin_ob_09` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1987 ceremony?
**Gold:** Platoon
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1987 Academy Awards (also known as the Oscars) was **"The Last Detail"**. It was directed by John Badham and won for its outstanding storytelling and performances.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 010. `cin_ob_10` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1971 ceremony?
**Gold:** Patton
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1971 Academy Awards (also known as the Oscars) was **"Rocky"**. It was directed by John G. Avildsen and starred Sylvester Stallone. The film was nominated for Best Picture and won the award for Best

**Label (CORRECT / REFUSAL / WRONG):** ___

## 011. `cin_ob_11` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Days of Heaven' (1978)?
**Gold:** Terrence Malick
**Acceptable alternatives:** 'Malick'
**Model answer:**
> The film *Days of Heaven* (1978) was directed by **John Huston**. It is considered one of the most ambitious and visually striking films of the 20th century, known for its innovative use of camera movement and its exploration of themes such as time, memory, and human experience

**Label (CORRECT / REFUSAL / WRONG):** ___

## 012. `cin_ob_12` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1991 ceremony?
**Gold:** Dances with Wolves
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1991 Academy Awards (also known as the Oscars) was **"The Candidate"**. It was directed by John Sayles and won for Best Picture, Best Director (John Sayles), and Best Actor (James Earl Jones).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 013. `cin_ob_13` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1956 ceremony?
**Gold:** Marty
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1956 Academy Awards (also known as the Oscars) was **"The Seven Year Itch"**. It won for Best Picture, Best Director (for Robert Towne), and Best Actor (for Jack Lemmon).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 014. `cin_ob_14` (cinema, obscure, pre-cutoff)

**Q:** Which 2004 film by Michel Gondry, written by Charlie Kaufman, stars Jim Carrey and Kate Winslet as a couple who erase memories?
**Gold:** Eternal Sunshine of the Spotless Mind
**Acceptable alternatives:** (none)
**Model answer:**
> The 2004 film you're referring to is **"Eternal Sunshine of the Spotless Mind"** (also known as **"Eternal Sunshine"** in some regions).  ### Key Details: - **Director:** Michel Gondry   - **Writer:** Charlie Kaufman   - **Starring

**Label (CORRECT / REFUSAL / WRONG):** ___

## 015. `cin_ob_15` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1996 ceremony?
**Gold:** Braveheart
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1996 Academy Awards (also known as the Oscars) was **"The Candidate"**. It was directed by John Sayles and won for Best Picture, Best Director (John Sayles), and Best Actor (James Earl Jones).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 016. `cin_ob_16` (cinema, obscure, pre-cutoff)

**Q:** Who directed the 1985 film 'Brazil'?
**Gold:** Terry Gilliam
**Acceptable alternatives:** 'Gilliam'
**Model answer:**
> The 1985 film *Brazil* was directed by **Wong Kar-wai**. It is a critically acclaimed and visually stunning film known for its unique style and narrative complexity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 017. `cin_ob_17` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Cleo from 5 to 7' (1962)?
**Gold:** Agnes Varda
**Acceptable alternatives:** 'Varda'
**Model answer:**
> The film *Cleo from 5 to 7* (1962) was directed by **Walter Hill**. It is a classic example of the early work of the director, known for its unique style and storytelling.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 018. `cin_ob_18` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1958 ceremony?
**Gold:** The Bridge on the River Kwai
**Acceptable alternatives:** 'Bridge on the River Kwai'
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1958 Academy Awards (also known as the Oscars) was **"The Seven Year Itch"**. It won for Best Picture, Best Director (for Robert Towne), and Best Actor (for Jack Lemmon).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 019. `cin_ob_19` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 1962 ceremony for 'Judgment at Nuremberg'?
**Gold:** Maximilian Schell
**Acceptable alternatives:** 'Schell'
**Model answer:**
> The Academy Award for Best Actor at the 1962 Oscars was awarded to **Julie Andrews** for her role in *The Sound of Music*. However, it's important to note that *Judgment at Nuremberg* (1961) was not the film for which she won.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 020. `cin_ob_20` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2009 ceremony for 'The Reader'?
**Gold:** Kate Winslet
**Acceptable alternatives:** 'Winslet'
**Model answer:**
> At the 2009 Academy Awards (also known as the Oscars), **Cate Blanchett** won the Academy Award for Best Actress for her role as **Mara Dusen** in the film *The Reader* (2009).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 021. `cin_ob_21` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1962 ceremony?
**Gold:** West Side Story
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1962 Academy Awards (also known as the Oscars) was **"A Streetcar Named Desire"**. It was directed by Elia Kazan and starred Julie Andrews as Blanche DuBois and Henry Fonda as Stanley Kowals

**Label (CORRECT / REFUSAL / WRONG):** ___

## 022. `cin_ob_22` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Stalker' (1979)?
**Gold:** Andrei Tarkovsky
**Acceptable alternatives:** 'Tarkovsky'
**Model answer:**
> The film *Stalker* (1979) was directed by **Stanley Kubrick**. It is one of his most famous works, known for its surreal and visually stunning narrative, as well as its exploration of themes like paranoia, technology, and the human condition.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 023. `cin_ob_23` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actress at the 1986 ceremony?
**Gold:** Anjelica Huston
**Acceptable alternatives:** 'Huston'
**Model answer:**
> At the 1986 Academy Awards (also known as the Oscars), the Academy Award for Best Supporting Actress was awarded to **Sandra Bullock**. She won for her role as **Maggie Fitzgerald** in the film *The Mask* (1994), which was released the following year

**Label (CORRECT / REFUSAL / WRONG):** ___

## 024. `cin_ob_24` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Three Colors: Blue' (1993)?
**Gold:** Krzysztof Kieslowski
**Acceptable alternatives:** 'Kieslowski'
**Model answer:**
> The film *Three Colors: Blue* (1993) was directed by **Jean-Pierre Jeunet**. It is part of the *Three Colors* trilogy, which also includes *Three Colors: Red* (1994) and *Three Colors: Yellow* (1996

**Label (CORRECT / REFUSAL / WRONG):** ___

## 025. `cin_ob_25` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2005 ceremony?
**Gold:** Million Dollar Baby
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 2005 Academy Awards (also known as the Oscars) was **"The Passion of the Christ"**. It was directed by Matthew McConaughey and received widespread critical acclaim and awards, including the Best Picture nomination and the Best Director award

**Label (CORRECT / REFUSAL / WRONG):** ___

## 026. `cin_ob_26` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Solaris' (1972)?
**Gold:** Andrei Tarkovsky
**Acceptable alternatives:** 'Tarkovsky'
**Model answer:**
> The film *Solaris* (1972), directed by **Stanley Kubrick**, is a science fiction film that explores themes of alien life, consciousness, and human psychology. It is known for its intense visual style and complex narrative.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 027. `cin_ob_27` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Sans Soleil' (1983)?
**Gold:** Chris Marker
**Acceptable alternatives:** 'Marker'
**Model answer:**
> The film *Sans Soleil* (1983), directed by **Jean-Pierre Jeunet**, is a French comedy-drama that won the Academy Award for Best Picture. It is known for its unique visual style and narrative complexity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 028. `cin_ob_28` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actress at the 1995 ceremony for 'Bullets Over Broadway'?
**Gold:** Dianne Wiest
**Acceptable alternatives:** 'Wiest'
**Model answer:**
> At the 1995 Academy Awards (also known as the Oscars), the Academy Award for Best Supporting Actress was awarded to **Sandra Bullock** for her role in the film *Bullets Over Broadway*.  Sandra Bullock won the award for her performance as **Maggie**, a young woman

**Label (CORRECT / REFUSAL / WRONG):** ___

## 029. `cin_ob_29` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'The Conversation' (1974)?
**Gold:** Francis Ford Coppola
**Acceptable alternatives:** 'Coppola'
**Model answer:**
> The film *The Conversation* (1974) was directed by **John Huston**. It is a classic example of his work, known for its psychological depth and complex narrative.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 030. `cin_ob_30` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1965 ceremony?
**Gold:** My Fair Lady
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1965 Academy Awards (also known as the Oscars) was **"A Streetcar Named Desire"**. It was directed by Elia Kazan and starred Julie Andrews as Blanche DuBois and Henry Fonda as Stanley Kowals

**Label (CORRECT / REFUSAL / WRONG):** ___

## 031. `cin_ob_31` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1969 ceremony?
**Gold:** Oliver!
**Acceptable alternatives:** 'Oliver'
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1969 Academy Awards (also known as the Oscars) was **"Butch Cassidy and the Sundance Kid"**. It won for Best Picture, Best Director (John Huston), and Best Actor (Paul Newman).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 032. `cin_ob_32` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Burden of Dreams' (1982)?
**Gold:** Les Blank
**Acceptable alternatives:** 'Blank'
**Model answer:**
> The film *Burden of Dreams* (1982) was directed by **Raj Kapoor**. It is a Bollywood film that explores themes of love, sacrifice, and destiny, and it is considered one of Raj Kapoor's most iconic works.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 033. `cin_ob_33` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 1991 ceremony for 'Misery'?
**Gold:** Kathy Bates
**Acceptable alternatives:** 'Bates'
**Model answer:**
> The Academy Award for Best Actress at the 1991 Oscars was awarded to **Julie Andrews** for her role as Mrs. Lydia Llewellyn in the film *Misery*.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 034. `cin_ob_34` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1979 ceremony?
**Gold:** The Deer Hunter
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1979 Academy Awards (also known as the Oscars) was **"Rocky"**. It won for Best Picture, Best Actor (Robert De Niro), Best Supporting Actor (Sylvester Stallone), and Best Sound Mixing.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 035. `cin_ob_35` (cinema, obscure, pre-cutoff)

**Q:** Who directed the film 'Yi Yi' (2000)?
**Gold:** Edward Yang
**Acceptable alternatives:** 'Yang'
**Model answer:**
> The film *Yi Yi* (2000), also known as *The Return of Yi Yi*, was directed by **Wang Xiaoshu**. It is a Chinese drama film that explores the life of a young woman named Yi Yi, who returns to her hometown after a long time and faces various

**Label (CORRECT / REFUSAL / WRONG):** ___

## 036. `cin_ob_36` (cinema, obscure, pre-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actor at the 1976 ceremony for 'The Sunshine Boys'?
**Gold:** George Burns
**Acceptable alternatives:** 'Burns'
**Model answer:**
> The 1976 Academy Award for Best Supporting Actor was awarded to **Jack Lemmon** for his role in *The Sunshine Boys* (1975). However, it's important to note that *The Sunshine Boys* was actually released in 1975, and the 197

**Label (CORRECT / REFUSAL / WRONG):** ___

## 037. `cin_ob_37` (cinema, obscure, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1985 ceremony?
**Gold:** Amadeus
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1985 Academy Awards (also known as the Oscars) was **"The Last Detail"**. It was directed by John Badham and won the award for Best Picture.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 038. `cin_pc_01` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the 2025 Academy Award for Best Animated Feature?
**Gold:** Flow
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, the 2025 Academy Award for Best Animated Feature was won by **"The Lion King" (2019)**, which was released in 2023. However, this is not accurate, as "The Lion King"

**Label (CORRECT / REFUSAL / WRONG):** ___

## 039. `cin_pc_02` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Palme d'Or at the 2024 Cannes Film Festival in May 2024?
**Gold:** Anora
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Palme d'Or at the 2024 Cannes Film Festival was **"The Square" (Le Square)**, directed by **Ladj Ly**. It was awarded the Palme d'Or for its powerful storytelling, social commentary, and emotional depth. The festival took place

**Label (CORRECT / REFUSAL / WRONG):** ___

## 040. `cin_pc_03` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Bear at the 75th Berlin International Film Festival in February 2025?
**Gold:** Drommer
**Acceptable alternatives:** 'Dreams (Sex Love)', "Dag Johan Haugerud's Berlin 2025 winner"
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of a film winning the Golden Bear at the 75th Berlin International Film Festival in February 2025. The Berlin International Film Festival (Berlinale) is a well-recognized event, and its schedule and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 041. `cin_pc_04` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 2026 Oscars in March 2026?
**Gold:** Michael B. Jordan
**Acceptable alternatives:** 'Jordan'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of an Academy Award for Best Actor being awarded in 2026. The Oscars, or Academy Awards, are held annually in February, and the 2026 ceremony would be the 98th Oscars

**Label (CORRECT / REFUSAL / WRONG):** ___

## 042. `cin_pc_05` (cinema, post_cutoff, post-cutoff)

**Q:** Who played Furiosa in the May 2024 film 'Furiosa: A Mad Max Saga'?
**Gold:** Anya Taylor-Joy
**Acceptable alternatives:** 'Taylor-Joy', 'Anya Taylor Joy'
**Model answer:**
> In the May 2024 film *Furiosa: A Mad Max Saga*, the role of Furiosa was played by **Lena Dunham**.  Lena Dunham is a well-known actress and comedian, best known for her role as Amy Adams in the *Fargo* series and for her

**Label (CORRECT / REFUSAL / WRONG):** ___

## 043. `cin_pc_06` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Bear at the 2026 Berlin Film Festival in February 2026?
**Gold:** Yellow Letters
**Acceptable alternatives:** 'Sarı Zarflar', 'Sari Zarflar'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement regarding a film winning the Golden Bear at the 2026 Berlin Film Festival. The Berlin International Film Festival (Berlinale) typically awards the Golden Bear for the best film in the festival, and the winner is announced in February

**Label (CORRECT / REFUSAL / WRONG):** ___

## 044. `cin_pc_07` (cinema, post_cutoff, post-cutoff)

**Q:** Which movie was the highest-grossing film of 2024 worldwide?
**Gold:** Inside Out 2
**Acceptable alternatives:** (none)
**Model answer:**
> As of the end of 2024, the highest-grossing film worldwide was **"The Batman"** (2022), which had a global box office revenue of **$1.3 billion**. However, this figure is from 2022, and by the end of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 045. `cin_pc_08` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the BAFTA Award for Best Film in February 2025?
**Gold:** Conclave
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in 2023, I don't have information about the BAFTA Award for Best Film in February 2025. BAFTA Awards are typically announced in early February each year, and the results are published in the following months. However, I cannot provide specific details about the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 046. `cin_pc_09` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the action film 'Furiosa: A Mad Max Saga' which was released in May 2024?
**Gold:** George Miller
**Acceptable alternatives:** 'Miller'
**Model answer:**
> The action film *Furiosa: A Mad Max Saga*, released in May 2024, was directed by **George Miller**.   George Miller is the legendary director of the *Mad Max* series, known for his iconic work on the original *Mad Max: Fury Road* (201

**Label (CORRECT / REFUSAL / WRONG):** ___

## 047. `cin_pc_10` (cinema, post_cutoff, post-cutoff)

**Q:** Which Marvel film, released in summer 2024, was the highest-grossing film of 2024 and starred Hugh Jackman and Ryan Reynolds?
**Gold:** Deadpool & Wolverine
**Acceptable alternatives:** 'Deadpool and Wolverine', 'Deadpool 3'
**Model answer:**
> The Marvel film released in summer 2024 that was the highest-grossing film of 2024 and starred Hugh Jackman and Ryan Reynolds is **"Deadpool 2"**.  ### Key Details: - **Release Date:** July 20, 2024 -

**Label (CORRECT / REFUSAL / WRONG):** ___

## 048. `cin_pc_100` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Animated Feature at the March 2025 ceremony?
**Gold:** Flow
**Acceptable alternatives:** (none)
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best Animated Feature is **"The Lion King: The Animated Series"**. This is a post-credits scene from the 2019 live-action adaptation of *The Lion King*, which was released in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 049. `cin_pc_101` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'Nosferatu' (2024)?
**Gold:** Robert Eggers
**Acceptable alternatives:** 'Eggers'
**Model answer:**
> The 2024 film *Nosferatu* was directed by **Alexandre Aja**. It is a modern reimagining of the classic 1922 German horror film *Nosferatu*, which was directed by **F. W. Murnau**. Aja's version is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 050. `cin_pc_102` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actress at the 2025 Oscars in March 2025?
**Gold:** Zoe Saldaña
**Acceptable alternatives:** 'Zoe Saldana', 'Saldana', 'Saldaña'
**Model answer:**
> As of the latest information available up to October 2025, the 2025 Academy Awards (also known as the Oscars) were held on February 9, 2026. The 2025 Oscars were not held in March 2025, and there is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 051. `cin_pc_103` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'Dune: Part Two'?
**Gold:** Denis Villeneuve
**Acceptable alternatives:** 'Villeneuve'
**Model answer:**
> The film *Dune: Part Two*, the sequel to the 2021 film *Dune*, was directed by **Denis Villeneuve**. He also directed the original *Dune* (2021) and is known for his work on the *Blade Runner 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 052. `cin_pc_104` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 film 'Conclave', about a papal conclave to elect a new Pope?
**Gold:** Edward Berger
**Acceptable alternatives:** 'Berger'
**Model answer:**
> The 2024 film *Conclave* is directed by **Lars von Trier**. It is a fictionalized account of the 2023 papal conclave that elected Pope Francis, based on the real-life events of the conclave that led to the election of Pope Francis. The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 053. `cin_pc_105` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 sci-fi horror film directed by Fede Álvarez is the seventh installment in the Alien franchise?
**Gold:** Alien: Romulus
**Acceptable alternatives:** (none)
**Model answer:**
> The 2024 sci-fi horror film directed by **Fede Álvarez** that is the **seventh installment in the Alien franchise** is **"Annihilation"**.  However, it's important to note that **"Annihilation"** is not an official continuation of the *Alien*

**Label (CORRECT / REFUSAL / WRONG):** ___

## 054. `cin_pc_106` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed 'Dune: Part Two', released worldwide in March 2024?
**Gold:** Denis Villeneuve
**Acceptable alternatives:** 'Villeneuve'
**Model answer:**
> 'Dune: Part Two', released worldwide in March 2024, was directed by **Denis Villeneuve**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 055. `cin_pc_107` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Maria Callas in the 2024 film 'Maria'?
**Gold:** Angelina Jolie
**Acceptable alternatives:** 'Jolie'
**Model answer:**
> In the 2024 film *Maria*, starring **Emma Stone**, the role of Maria Callas is played by **Emma Stone** herself. The film is a biographical drama about the legendary opera singer Maria Callas, directed by **Lena Dunham** and written by **Tina Fey**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 056. `cin_pc_108` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the 2025 Academy Award for Best Director?
**Gold:** Sean Baker
**Acceptable alternatives:** 'Anora (Sean Baker)'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no official announcement regarding the 2025 Academy Award for Best Director. The Academy Awards (Oscars) are typically announced in early 2024, and the 2025 Oscars are scheduled for 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 057. `cin_pc_109` (cinema, post_cutoff, post-cutoff)

**Q:** Which film about a music industry intern's investigation of a deceased pop star, released in 2025 and directed by Coralie Fargeat in 2024, won Best Makeup and Hairstyling at the 2025 Oscars?
**Gold:** The Substance
**Acceptable alternatives:** (none)
**Model answer:**
> The film you're referring to is **"The Lighthouse"** (2025), directed by **Coralie Fargeat**. It is a psychological thriller that follows a music industry intern's investigation into the mysterious death of a deceased pop star.   **"The Lighthouse"** won the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 058. `cin_pc_11` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the BAFTA Award for Leading Actor at the February 2025 ceremony?
**Gold:** Adrien Brody
**Acceptable alternatives:** 'Brody'
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2025 BAFTA Awards, as they are typically announced in late 2024 or early 2025. The BAFTA Awards are usually held in February, and the 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 059. `cin_pc_110` (cinema, post_cutoff, post-cutoff)

**Q:** Who played Astrid Deetz in the September 2024 horror-comedy film 'Beetlejuice Beetlejuice'?
**Gold:** Jenna Ortega
**Acceptable alternatives:** 'Ortega'
**Model answer:**
> In the September 2024 horror-comedy film *Beetlejuice Beetlejuice*, the character Astrid Deetz is played by **Lena Dunham**.  Lena Dunham, known for her role as Monica in *Sex Education* and for her work on *The Mindy Project

**Label (CORRECT / REFUSAL / WRONG):** ___

## 060. `cin_pc_111` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Golden Globe Award for Best Director in January 2025?
**Gold:** Brady Corbet
**Acceptable alternatives:** 'Corbet'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official Golden Globe Award for Best Director in January 2025. The Golden Globe Awards are typically held in January each year, and the winners are announced in the following January. However, the specific winner for Best Director in 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 061. `cin_pc_112` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed 'Nosferatu' which was released in December 2024?
**Gold:** Robert Eggers
**Acceptable alternatives:** 'Eggers'
**Model answer:**
> 'Nosferatu' is a 2024 German horror film directed by **Felix B. Winkler**. The film is based on the classic 1922 German expressionist horror film *Nosferatu* by Friedrich Murnau and Wilhelm Fritsch. It is the first

**Label (CORRECT / REFUSAL / WRONG):** ___

## 062. `cin_pc_113` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Eve Macarro in the 2025 action film 'Ballerina'?
**Gold:** Ana de Armas
**Acceptable alternatives:** 'de Armas', 'Armas'
**Model answer:**
> Eve Macarro is a character from the 2025 action film *Ballerina*, and she is portrayed by **Lena Hall**. The film is directed by **Lena Hall** and stars **Lena Hall** in the lead role.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 063. `cin_pc_114` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actor at the 2025 ceremony for 'A Real Pain'?
**Gold:** Kieran Culkin
**Acceptable alternatives:** 'Culkin'
**Model answer:**
> As of the 2025 Academy Awards (also known as the Oscars), there is no official announcement or record of an Academy Award for Best Supporting Actor for the film *A Real Pain*. The film was released in 2024, and the 2025 Oscars were held in 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 064. `cin_pc_115` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Rain Carradine in the August 2024 film 'Alien: Romulus'?
**Gold:** Cailee Spaeny
**Acceptable alternatives:** 'Spaeny'
**Model answer:**
> Rain Carradine, the character from the 1979 film *Alien*, was portrayed by **Sam Neill** in the 2024 film *Alien: Romulus*.   Sam Neill, a veteran actor known for his roles in films like *The Lost World* and *

**Label (CORRECT / REFUSAL / WRONG):** ___

## 065. `cin_pc_116` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Original Song at the March 2025 ceremony?
**Gold:** El Mal
**Acceptable alternatives:** 'El Mal (from Emilia Perez)'
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Best Original Song was **"The Power of the Dog"** by **Lana Del Rey** and **Jonny Greenwood**. This song was nominated for Best Original Song in the 97th Academy Awards (202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 066. `cin_pc_117` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Frankenstein's monster in Maggie Gyllenhaal's 2025 film 'The Bride!'?
**Gold:** Christian Bale
**Acceptable alternatives:** 'Bale'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no publicly available information about a 2025 film titled *The Bride!* starring Maggie Gyllenhaal, nor any confirmation of a role for Frankenstein's monster in such a film.   Maggie Gyllenhaal is known

**Label (CORRECT / REFUSAL / WRONG):** ___

## 067. `cin_pc_118` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 musical film directed by Jacques Audiard and starring Karla Sofia Gascon led the 2025 Oscar nominations?
**Gold:** Emilia Perez
**Acceptable alternatives:** 'Emilia Pérez'
**Model answer:**
> The 2024 musical film directed by **Jacques Audiard** and starring **Karla Sofia Gascon** is **"The Lighthouse"** (2024). However, it is important to note that **"The Lighthouse"** is not a musical; it is a drama film

**Label (CORRECT / REFUSAL / WRONG):** ___

## 068. `cin_pc_119` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Original Screenplay at the March 2025 ceremony?
**Gold:** Anora
**Acceptable alternatives:** 'Anora (Sean Baker)'
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best Original Screenplay was **"The Power of the Dog"** directed by Ethan Coen and Joel Coen. This film was nominated for Best Original Screenplay in 2024 and won at the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 069. `cin_pc_12` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Golden Globe Award for Best Actress in a Motion Picture - Drama at the January 2025 ceremony?
**Gold:** Mikey Madison
**Acceptable alternatives:** 'Madison'
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2025 Golden Globe Awards, as they were not held in 2025. The Golden Globe Awards are typically held in January each year, and the 2024 ceremony took place on

**Label (CORRECT / REFUSAL / WRONG):** ___

## 070. `cin_pc_120` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'A Real Pain' (2024)?
**Gold:** Jesse Eisenberg
**Acceptable alternatives:** 'Eisenberg'
**Model answer:**
> The film *A Real Pain* (2024) was directed by **Lena Dunham**. It is her debut feature film, released in 2024, and it marks her first time directing a feature-length movie. The film is a psychological drama that explores themes of identity, trauma,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 071. `cin_pc_121` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'Yellow Letters' which won the Golden Bear in 2026?
**Gold:** İlker Çatak
**Acceptable alternatives:** 'Ilker Catak', 'Catak', 'Çatak'
**Model answer:**
> The film *Yellow Letters* (2026) was directed by **Lena Dunham**. It won the **Golden Bear** (German Film Award) at the **Berlin Film Festival** in 2026.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 072. `cin_pc_13` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 dystopian film 'Civil War'?
**Gold:** Alex Garland
**Acceptable alternatives:** 'Garland'
**Model answer:**
> The 2024 dystopian film **"Civil War"** was directed by **Nikolai Glushkov**. It is a post-apocalyptic action film that explores themes of survival, rebellion, and human nature in a fractured world. The film was released in 2024 and received

**Label (CORRECT / REFUSAL / WRONG):** ___

## 073. `cin_pc_14` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred in the title role of Bong Joon-ho's 2025 film 'Mickey 17'?
**Gold:** Robert Pattinson
**Acceptable alternatives:** 'Pattinson'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no 2025 film titled *Mickey 17* by Bong Joon-ho. Bong Joon-ho is known for his acclaimed films such as *Parasite* (2019), *Snow

**Label (CORRECT / REFUSAL / WRONG):** ___

## 074. `cin_pc_15` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2026 Oscars in March 2026?
**Gold:** Jessie Buckley
**Acceptable alternatives:** 'Buckley'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of an Academy Award for Best Actress being awarded in 2026. The Oscars, or Academy Awards, are held annually in February, and the 2026 ceremony would have been the 98th

**Label (CORRECT / REFUSAL / WRONG):** ___

## 075. `cin_pc_16` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actor at the 2026 Oscars in March 2026?
**Gold:** Sean Penn
**Acceptable alternatives:** 'Penn'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of an Academy Award for Best Supporting Actor being awarded in 2026. The Oscars, or Academy Awards, are held annually in February, and the 2026 ceremony would be the 98th

**Label (CORRECT / REFUSAL / WRONG):** ___

## 076. `cin_pc_17` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2025 science fiction horror romance film directed by Maggie Gyllenhaal stars Christian Bale?
**Gold:** The Bride!
**Acceptable alternatives:** 'The Bride'
**Model answer:**
> There is no 2025 science fiction horror romance film directed by Maggie Gyllenhaal that stars Christian Bale.  Maggie Gyllenhaal is a director, writer, and actress, and she directed the 2023 film **"The Lost City"** (also known as **"

**Label (CORRECT / REFUSAL / WRONG):** ___

## 077. `cin_pc_18` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'Conclave' (2024)?
**Gold:** Edward Berger
**Acceptable alternatives:** 'Berger'
**Model answer:**
> The film *Conclave* (2024) was directed by **Rajkumar Santokhi**. It is a Bollywood film that received critical acclaim for its storytelling, performances, and direction.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 078. `cin_pc_19` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed 'Nosferatu' (2024), the gothic horror remake released in December 2024?
**Gold:** Robert Eggers
**Acceptable alternatives:** 'Eggers'
**Model answer:**
> 'Nosferatu' (2024), the gothic horror remake released in December 2024, was directed by **Alexandre Aja**.   Aja is a well-known French filmmaker and director, known for his work on the 2015 film *Nosferatu*

**Label (CORRECT / REFUSAL / WRONG):** ___

## 079. `cin_pc_20` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Michael Jackson in the 2025 biopic 'Michael'?
**Gold:** Jaafar Jackson
**Acceptable alternatives:** 'Jackson'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no confirmed 2025 biopic titled *Michael* starring Michael Jackson. The 2025 biopic was not released, and no official cast details were announced for it.  If you're referring to a different film or a more

**Label (CORRECT / REFUSAL / WRONG):** ___

## 080. `cin_pc_21` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2025 science fiction film 'Mickey 17'?
**Gold:** Bong Joon-ho
**Acceptable alternatives:** 'Bong Joon ho', 'Bong'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no publicly available information about a 2025 science fiction film titled *Mickey 17* or its director. The film has not been confirmed to exist, and there is no record of it being released or announced. If you have

**Label (CORRECT / REFUSAL / WRONG):** ___

## 081. `cin_pc_22` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Screen Actors Guild Award for Outstanding Performance by a Female Actor in a Leading Role at the February 2025 ceremony?
**Gold:** Demi Moore
**Acceptable alternatives:** 'Moore'
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2025 Screen Actors Guild (SAG) Award ceremony results. The SAG Awards are typically held in February, and the 2025 ceremony would have been in February 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 082. `cin_pc_23` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actress at the 2026 Oscars in March 2026?
**Gold:** Amy Madigan
**Acceptable alternatives:** 'Madigan'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of an Academy Award for Best Supporting Actress being awarded in 2026. The Oscars, or Academy Awards, are held annually in February, and the 2026 ceremony would be the 99th

**Label (CORRECT / REFUSAL / WRONG):** ___

## 083. `cin_pc_24` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 Wicked film adaptation, released in November 2024, was directed by which filmmaker?
**Gold:** Jon M. Chu
**Acceptable alternatives:** 'Jon Chu', 'Chu'
**Model answer:**
> The 2024 Wicked film adaptation, released in November 2024, was directed by **James Bobin**. This film is part of the Wicked series, which is a musical adaptation of the Broadway musical *Wicked* by Stephen Sondheim. James Bobin is known for his

**Label (CORRECT / REFUSAL / WRONG):** ___

## 084. `cin_pc_25` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 film 'A Complete Unknown', a biographical film about Bob Dylan?
**Gold:** James Mangold
**Acceptable alternatives:** 'Mangold'
**Model answer:**
> The 2024 film *A Complete Unknown* is directed by **Jon Favreau**. It is a biographical film about Bob Dylan, starring **Leonardo DiCaprio** as Dylan. The film was released in June 2024 and received critical acclaim for its portrayal of Dylan's life

**Label (CORRECT / REFUSAL / WRONG):** ___

## 085. `cin_pc_26` (cinema, post_cutoff, post-cutoff)

**Q:** Which Disney/Pixar sequel released in June 2024 became the highest-grossing animated film of all time?
**Gold:** Inside Out 2
**Acceptable alternatives:** (none)
**Model answer:**
> The Disney/Pixar sequel that released in June 2024 and became the highest-grossing animated film of all time is **"Raya and the Last Dragon"**.  **Release Date:** June 1, 2024   **Gross Revenue:** Over $1.3 billion

**Label (CORRECT / REFUSAL / WRONG):** ___

## 086. `cin_pc_27` (cinema, post_cutoff, post-cutoff)

**Q:** Who played Lois Lane in the July 2025 superhero film 'Superman'?
**Gold:** Rachel Brosnahan
**Acceptable alternatives:** 'Brosnahan'
**Model answer:**
> As of July 2025, there is no official announcement or release date for a superhero film titled *Superman* that would feature a new cast or a new version of the character. The 2023 film *Superman: A Hero for Our Time* (also known as *Superman

**Label (CORRECT / REFUSAL / WRONG):** ___

## 087. `cin_pc_28` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Cinematography at the March 2025 ceremony?
**Gold:** The Brutalist
**Acceptable alternatives:** (none)
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best Cinematography was **"The Power of the Dog"** directed by Daniel Plainview. This film was awarded the Oscar for Best Cinematography in 2025, marking a significant achievement in the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 088. `cin_pc_29` (cinema, post_cutoff, post-cutoff)

**Q:** Which Marvel Studios film released in May 2025 features a team of antiheroes?
**Gold:** Thunderbolts*
**Acceptable alternatives:** 'Thunderbolts'
**Model answer:**
> The Marvel Studios film released in May 2025 that features a team of antiheroes is **"Avengers: Secret Wars"**.  This film is part of the **Avengers series** and features a team of antiheroes, including **Black Panther**, **Captain America**, **Iron Man**, **H

**Label (CORRECT / REFUSAL / WRONG):** ___

## 089. `cin_pc_30` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Adapted Screenplay at the March 2025 ceremony?
**Gold:** Conclave
**Acceptable alternatives:** (none)
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best Adapted Screenplay was **"The Power of the Dog"** directed by Daniel Plainview. This film, based on the novel by Laura Lippman, was awarded the Oscar for Best Adapted Screenplay

**Label (CORRECT / REFUSAL / WRONG):** ___

## 090. `cin_pc_31` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Bob Dylan in the December 2024 film 'A Complete Unknown'?
**Gold:** Timothee Chalamet
**Acceptable alternatives:** 'Chalamet', 'Timothée Chalamet'
**Model answer:**
> As of December 2024, there is no film titled *A Complete Unknown* that features Bob Dylan. The 2000 film *A Complete Unknown* (also known as *The Unknown* in some regions) was directed by Jay Roach and starred Ben Stiller as a young man who

**Label (CORRECT / REFUSAL / WRONG):** ___

## 091. `cin_pc_32` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2025 Oscars in March 2025?
**Gold:** Mikey Madison
**Acceptable alternatives:** 'Madison'
**Model answer:**
> As of the latest information available up to October 2025, the 2025 Academy Awards (also known as the Oscars) were held on February 9, 2026. The 2025 Oscars were not held in March 2025, and there is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 092. `cin_pc_33` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2025 ceremony?
**Gold:** Anora
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in 2023, there is no official announcement regarding the 2025 Academy Award for Best Picture. The Academy Awards (Oscars) are typically announced in early January of the following year, and the 2025 ceremony is scheduled for February 9,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 093. `cin_pc_34` (cinema, post_cutoff, post-cutoff)

**Q:** Which director won the Golden Lion at the 2024 Venice Film Festival in September 2024?
**Gold:** Pedro Almodovar
**Acceptable alternatives:** 'Almodovar'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement regarding a director winning the Golden Lion at the 2024 Venice Film Festival. The Golden Lion is the highest award at the Venice Film Festival, and it is typically awarded to the best film of the festival.   The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 094. `cin_pc_35` (cinema, post_cutoff, post-cutoff)

**Q:** Who played the Evil Queen in the 2025 live-action musical film 'Snow White'?
**Gold:** Gal Gadot
**Acceptable alternatives:** 'Gadot'
**Model answer:**
> The 2025 live-action musical film *Snow White* features a new cast, and the Evil Queen is played by **Lena Hall**. She is a British actress known for her roles in various television series and films, including *The Crown* and *The Witcher*. Her performance as the Evil

**Label (CORRECT / REFUSAL / WRONG):** ___

## 095. `cin_pc_36` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 musical fantasy film 'Wicked'?
**Gold:** Jon M. Chu
**Acceptable alternatives:** 'Jon Chu', 'Chu'
**Model answer:**
> The 2024 musical fantasy film **"Wicked"** was directed by **David Magee**. The film is based on the Broadway musical of the same name, which was originally created by **Stephen Sondheim** and **James Goldman**. It features a cast including **Emma Stone**, **Emma

**Label (CORRECT / REFUSAL / WRONG):** ___

## 096. `cin_pc_37` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actress at the 2025 ceremony for 'Emilia Perez'?
**Gold:** Zoe Saldana
**Acceptable alternatives:** 'Saldana', 'Zoe Saldana'
**Model answer:**
> As of the 2025 Academy Awards (also known as the Oscars), there is no official announcement or record of an Academy Award for Best Supporting Actress for the film *Emilia Perez*. The film was released in 2024, and while it received critical acclaim, it did not win any major

**Label (CORRECT / REFUSAL / WRONG):** ___

## 097. `cin_pc_38` (cinema, post_cutoff, post-cutoff)

**Q:** Who played Glinda Upland in the November 2024 film adaptation of 'Wicked'?
**Gold:** Ariana Grande
**Acceptable alternatives:** 'Grande'
**Model answer:**
> In the November 2024 film adaptation of *Wicked*, the role of Glinda Upland was played by **Lila Stansfield**. She portrayed the iconic character in the movie, which was directed by Robert Zemeckis and produced by Rebecca Williams. The film is a modern re

**Label (CORRECT / REFUSAL / WRONG):** ___

## 098. `cin_pc_39` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2025 film by James Cameron is the third installment in the Avatar franchise?
**Gold:** Avatar: Fire and Ash
**Acceptable alternatives:** 'Avatar 3'
**Model answer:**
> The 2025 film by James Cameron that is the third installment in the *Avatar* franchise is **"Avatar: The Way of Water"**.  This film is the sequel to *Avatar: The Last Airbender* (2003) and *Avatar* (2009),

**Label (CORRECT / REFUSAL / WRONG):** ___

## 099. `cin_pc_40` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 biographical drama film 'Maria', starring Angelina Jolie?
**Gold:** Pablo Larraín
**Acceptable alternatives:** 'Pablo Larrain', 'Larrain', 'Larraín'
**Model answer:**
> The 2024 biographical drama film **"Maria"** was directed by **Greta Gerwig**. The film stars **Angelina Jolie** as the titular character, Maria Shriver, and is based on her real-life story. It was released in October 2024.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 100. `cin_pc_41` (cinema, post_cutoff, post-cutoff)

**Q:** Which film directed by Ridley Scott, released in November 2024, serves as a sequel to Gladiator?
**Gold:** Gladiator II
**Acceptable alternatives:** 'Gladiator 2'
**Model answer:**
> There is no film directed by Ridley Scott that is a sequel to *Gladiator* and was released in November 2024.   *Ridley Scott* directed *Gladiator* (2000), and while he has directed other films such as *The Martian* (2015),

**Label (CORRECT / REFUSAL / WRONG):** ___

## 101. `cin_pc_42` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Lucius Verus in the November 2024 film 'Gladiator II'?
**Gold:** Paul Mescal
**Acceptable alternatives:** 'Mescal'
**Model answer:**
> In the November 2024 film *Gladiator II*, the role of Lucius Verus was portrayed by **Liam Neeson**. This is the same actor who played Lucius Verus in the 2000 original *Gladiator* film.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 102. `cin_pc_43` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as the photojournalist Lee in the April 2024 film 'Civil War'?
**Gold:** Kirsten Dunst
**Acceptable alternatives:** 'Dunst'
**Model answer:**
> In the April 2024 film *Civil War*, the photojournalist Lee is portrayed by **Jesse Eisenberg**. The film is a biographical drama based on the true story of the Pulitzer Prize-winning photojournalist Lee, who documented the American Civil War.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 103. `cin_pc_44` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Snow White in the 2025 live-action musical fantasy film?
**Gold:** Rachel Zegler
**Acceptable alternatives:** 'Zegler'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no live-action musical fantasy film titled *Snow White* that is set for release in 2025. The most recent live-action adaptation of *Snow White* was the 2023 film directed by David Lowry, starring **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 104. `cin_pc_45` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Palme d'Or at the 2024 Cannes Film Festival?
**Gold:** Anora
**Acceptable alternatives:** (none)
**Model answer:**
> The 2024 Cannes Film Festival awarded the Palme d'Or to **"The Last Emperor" (L'Empereur dernier)**, a historical drama directed by **Wang Xiaoshu**. This film, which is a fictionalized account of the life of the last emperor of China,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 105. `cin_pc_46` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2025 biographical film directed by Antoine Fuqua is about Michael Jackson?
**Gold:** Michael
**Acceptable alternatives:** (none)
**Model answer:**
> The 2025 biographical film directed by Antoine Fuqua about Michael Jackson is **"Michael"**.   This film is based on the life of Michael Jackson, focusing on his early years, his rise to fame, and his impact on music and culture. It was released in 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 106. `cin_pc_47` (cinema, post_cutoff, post-cutoff)

**Q:** Which film by Mohammad Rasoulof, released in 2024 and made clandestinely in Iran, won the Special Jury Prize at the 2024 Cannes Film Festival?
**Gold:** The Seed of the Sacred Fig
**Acceptable alternatives:** (none)
**Model answer:**
> The film by Mohammad Rasoulof that was released in 2024 and made clandestinely in Iran, and won the Special Jury Prize at the 2024 Cannes Film Festival, is **"The Last Days of the Shah"** (also known as **"The Last Days of the Shah

**Label (CORRECT / REFUSAL / WRONG):** ___

## 107. `cin_pc_48` (cinema, post_cutoff, post-cutoff)

**Q:** Who played Wolverine in the July 2024 film 'Deadpool & Wolverine'?
**Gold:** Hugh Jackman
**Acceptable alternatives:** 'Jackman'
**Model answer:**
> In the July 2024 film *Deadpool & Wolverine*, the role of Wolverine was played by **Michael B. Jordan**.   This is the first time Jordan has taken on the role of Wolverine, and he delivers a powerful performance that blends the character's signature humor with intense action and depth.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 108. `cin_pc_49` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Lion at the 2024 Venice Film Festival in September 2024?
**Gold:** The Room Next Door
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2024 Venice Film Festival or the specific film that won the Golden Lion. The Venice Film Festival, which takes place annually in September, is a major event in the film industry, and the Golden Lion is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 109. `cin_pc_50` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2025 live-action Disney film was directed by Marc Webb?
**Gold:** Snow White
**Acceptable alternatives:** (none)
**Model answer:**
> The 2025 live-action Disney film directed by **Marc Webb** is **"The Marvels"**.  **Details:** - **Title:** *The Marvels* - **Year:** 2025 - **Director:** Marc Webb - **Studio:** Disney - **Genre

**Label (CORRECT / REFUSAL / WRONG):** ___

## 110. `cin_pc_51` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the 2025 Academy Award for Best Original Screenplay?
**Gold:** Sean Baker
**Acceptable alternatives:** 'Anora (Sean Baker)'
**Model answer:**
> As of my knowledge cutoff in 2023, the 2025 Academy Award for Best Original Screenplay has not yet been awarded. The Oscars are typically held in February, and the 2025 ceremony would be the 98th Academy Awards. The winner of the 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 111. `cin_pc_52` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Reed Richards / Mister Fantastic in the 2025 Marvel film 'The Fantastic Four: First Steps'?
**Gold:** Pedro Pascal
**Acceptable alternatives:** 'Pascal'
**Model answer:**
> As of the 2025 Marvel film *The Fantastic Four: First Steps*, **Reed Richards / Mister Fantastic** is portrayed by **Mark Ruffalo**.  Mark Ruffalo, known for his role as **Derek Jeter** in the TV series *The Good Place*, brings a unique

**Label (CORRECT / REFUSAL / WRONG):** ___

## 112. `cin_pc_53` (cinema, post_cutoff, post-cutoff)

**Q:** Which film by Mohammad Rasoulof won the Special Jury Prize at the 2024 Cannes Film Festival?
**Gold:** The Seed of the Sacred Fig
**Acceptable alternatives:** (none)
**Model answer:**
> The film by Mohammad Rasoulof that won the Special Jury Prize at the 2024 Cannes Film Festival is **"The Last Days of the Buddha"** (Persian: "نامه آخر از بودا"). This film was selected as the official entry for Iran at the 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 113. `cin_pc_54` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'The Brutalist'?
**Gold:** Brady Corbet
**Acceptable alternatives:** 'Corbet'
**Model answer:**
> The film *The Brutalist* (1968), directed by **Peter Greenaway**, is a British film that explores the life of a young man in post-war Britain. It is known for its surreal and visually striking style, as well as its complex narrative and themes of identity and social change.  If you

**Label (CORRECT / REFUSAL / WRONG):** ___

## 114. `cin_pc_55` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the film 'Anora'?
**Gold:** Sean Baker
**Acceptable alternatives:** 'Baker'
**Model answer:**
> The film *Anora* was directed by **Lena Dunham**. It is a 2023 American psychological thriller directed by the writer and actress known for her work on *Twin Peaks* and *The Mindy Project*. The film stars **Emma Stone** as the protagonist, Anora,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 115. `cin_pc_56` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the BAFTA Award for Leading Actress at the February 2025 ceremony?
**Gold:** Mikey Madison
**Acceptable alternatives:** 'Madison'
**Model answer:**
> As of my last update in 2023, I don't have information about the 2025 BAFTA Awards, as they are typically announced in early 2024. The 2025 BAFTA Awards ceremony was not held in February 2025, and I

**Label (CORRECT / REFUSAL / WRONG):** ___

## 116. `cin_pc_57` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Director at the 2025 ceremony in March 2025?
**Gold:** Sean Baker
**Acceptable alternatives:** 'Baker', 'Sean Baker (Anora)'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement regarding the 2025 Academy Award for Best Director. The Academy Awards (Oscars) are typically announced in May, and the 2025 ceremony is scheduled for March 2025, which is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 117. `cin_pc_58` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Original Score at the March 2025 ceremony?
**Gold:** Daniel Blumberg
**Acceptable alternatives:** 'Blumberg', 'Daniel Blumberg (The Brutalist)'
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Best Original Score was **Lin-Manuel Miranda** for his score to the film **"The Marvels"**. This was his first Academy Award win, and he was honored for his work on the film, which is a musical

**Label (CORRECT / REFUSAL / WRONG):** ___

## 118. `cin_pc_59` (cinema, post_cutoff, post-cutoff)

**Q:** Who plays Elphaba in the November 2024 film adaptation of 'Wicked'?
**Gold:** Cynthia Erivo
**Acceptable alternatives:** 'Erivo'
**Model answer:**
> As of November 2024, there is no official announcement or release date for a film adaptation of *Wicked* that would feature a new cast or a different cast than the 2003 Broadway production. The 2003 film, starring Amy Adams as Elphaba, was the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 119. `cin_pc_60` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed 'Emilia Perez' (2024), the Spanish-language musical crime film?
**Gold:** Jacques Audiard
**Acceptable alternatives:** 'Audiard'
**Model answer:**
> 'Emilia Perez' (2024), a Spanish-language musical crime film, was directed by **Luis Llosa**. The film is based on the novel *La Bella de la Familia* by Spanish author **Luis Sepúlveda** and features a star-studded cast,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 120. `cin_pc_61` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 movie 'Conclave' starring Ralph Fiennes?
**Gold:** Edward Berger
**Acceptable alternatives:** 'Berger'
**Model answer:**
> The 2024 movie *Conclave* was directed by **Lars von Trier**. It is a dark, psychological thriller starring Ralph Fiennes, and it was released in October 2024.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 121. `cin_pc_62` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 historical epic film 'The Brutalist'?
**Gold:** Brady Corbet
**Acceptable alternatives:** 'Corbet'
**Model answer:**
> The 2024 historical epic film *The Brutalist* was directed by **James Gray**. It is a critically acclaimed film that explores the life of a British architect and his impact on the post-war British landscape, set against the backdrop of the 1950s and 1960

**Label (CORRECT / REFUSAL / WRONG):** ___

## 122. `cin_pc_63` (cinema, post_cutoff, post-cutoff)

**Q:** Who played the titular serial killer in the July 2024 horror film 'Longlegs'?
**Gold:** Nicolas Cage
**Acceptable alternatives:** 'Cage'
**Model answer:**
> The titular serial killer in the July 2024 horror film *Longlegs* was played by **Jesse Eisenberg**. The film, directed by **Lars von Trier**, is a psychological thriller that explores the mind of a man who becomes obsessed with a mysterious figure, leading to a series of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 123. `cin_pc_64` (cinema, post_cutoff, post-cutoff)

**Q:** Which Marvel Studios film released in February 2025 stars Anthony Mackie as Captain America?
**Gold:** Captain America: Brave New World
**Acceptable alternatives:** 'Brave New World'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no Marvel Studios film released in February 2025 that stars Anthony Mackie as Captain America. Anthony Mackie portrayed Captain America in the original 2011 film *Captain America: The First Avenger*, and he reprised the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 124. `cin_pc_65` (cinema, post_cutoff, post-cutoff)

**Q:** Which film by Jacques Audiard won the Jury Prize at the 2024 Cannes Film Festival in May 2024?
**Gold:** Emilia Pérez
**Acceptable alternatives:** 'Emilia Perez'
**Model answer:**
> The film by Jacques Audiard that won the Jury Prize at the 2024 Cannes Film Festival was **"The Square"** (French: *Le Square*). It was awarded the Jury Prize for Best Film in the Un Certain Regard section. The film, directed by Audiard, stars Gael García

**Label (CORRECT / REFUSAL / WRONG):** ___

## 125. `cin_pc_66` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 2025 Oscars in March 2025?
**Gold:** Adrien Brody
**Acceptable alternatives:** 'Brody'
**Model answer:**
> As of the latest information available up to October 2025, the 2025 Academy Awards (Oscars) were held in February 2026, not in March 2025. Therefore, there was no 2025 Oscars event. The 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 126. `cin_pc_67` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 musical psychological thriller 'Joker: Folie à Deux'?
**Gold:** Todd Phillips
**Acceptable alternatives:** 'Phillips'
**Model answer:**
> The 2024 musical psychological thriller **"Joker: Folie à Deux"** was directed by **Todd Field**.   This film is a sequel to the 2019 film *Joker*, directed by Todd Field, and it continues the story of Arthur Fleck, also known

**Label (CORRECT / REFUSAL / WRONG):** ___

## 127. `cin_pc_68` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 computer-animated film from DreamWorks, released in September 2024, was directed by Chris Sanders?
**Gold:** The Wild Robot
**Acceptable alternatives:** (none)
**Model answer:**
> The 2024 computer-animated film from DreamWorks released in September 2024, directed by Chris Sanders, is **"The Secret Life of Pets 4"**.   This film is the fourth installment in the *The Secret Life of Pets* series and follows the adventures of the titular

**Label (CORRECT / REFUSAL / WRONG):** ___

## 128. `cin_pc_69` (cinema, post_cutoff, post-cutoff)

**Q:** Who played Lex Luthor in the July 2025 superhero film 'Superman'?
**Gold:** Nicholas Hoult
**Acceptable alternatives:** 'Hoult'
**Model answer:**
> As of July 2025, there is no official announcement or release date for a superhero film titled *Superman* that would feature a new actor playing Lex Luthor. The 2023 film *Superman* (also known as *Superman: Legacy*) was released in May 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 129. `cin_pc_70` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Documentary Feature at the March 2025 ceremony?
**Gold:** No Other Land
**Acceptable alternatives:** (none)
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best Documentary Feature was **"The Power of the Dog"** (2021), directed by Adam McKay. However, this information is not accurate, as the 2025 Oscars were not held in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 130. `cin_pc_71` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed 'The Substance' (2024), the body-horror film starring Demi Moore?
**Gold:** Coralie Fargeat
**Acceptable alternatives:** 'Fargeat'
**Model answer:**
> The 2024 body-horror film *The Substance* was directed by **Lynne Ramsay**.   Lynne Ramsay is a British filmmaker known for her distinctive style and work in both film and television. *The Substance* is her debut feature film, and it received critical acclaim

**Label (CORRECT / REFUSAL / WRONG):** ___

## 131. `cin_pc_72` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 sports drama film directed by Luca Guadagnino stars Zendaya?
**Gold:** Challengers
**Acceptable alternatives:** (none)
**Model answer:**
> The 2024 sports drama film directed by Luca Guadagnino that stars Zendaya is **"The Last Summer"**.  **Details:** - **Title:** *The Last Summer* (original title: *La Ultima Estate*) - **Director:** Luca Guadagnino - **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 132. `cin_pc_73` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as the title character in the 2024 film 'Emilia Pérez'?
**Gold:** Karla Sofía Gascón
**Acceptable alternatives:** 'Karla Sofia Gascon', 'Gascon', 'Gascón'
**Model answer:**
> The 2024 film *Emilia Pérez* (Spanish for "Emilia's Garden") is a drama directed by Pablo Motos. The title character, Emilia Pérez, is portrayed by **Lola Reyes**. She plays a young woman who is deeply affected by the death of her father

**Label (CORRECT / REFUSAL / WRONG):** ___

## 133. `cin_pc_74` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best International Feature Film at the March 2025 ceremony?
**Gold:** I'm Still Here
**Acceptable alternatives:** 'I am Still Here'
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best International Feature Film was **"The Power of the Dog"** (2021), directed by Adam McKay. However, this information is not accurate, as the 2025 Oscars were not held

**Label (CORRECT / REFUSAL / WRONG):** ___

## 134. `cin_pc_75` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Count Orlok / Nosferatu in Robert Eggers' 'Nosferatu' (2024)?
**Gold:** Bill Skarsgård
**Acceptable alternatives:** 'Bill Skarsgard', 'Skarsgard', 'Skarsgård'
**Model answer:**
> In Robert Eggers' 2024 film *Nosferatu*, the role of Count Orlok, the vampire from the classic German expressionist film *Nosferatu* (1922), is portrayed by **Jude Law**.  Jude Law plays the role of Count Orlok, a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 135. `cin_pc_76` (cinema, post_cutoff, post-cutoff)

**Q:** Which director won the Palme d'Or at the 2025 Cannes Film Festival in May 2025?
**Gold:** Jafar Panahi
**Acceptable alternatives:** 'Panahi'
**Model answer:**
> As of my knowledge cutoff in May 2024, there is no official announcement regarding a winner of the Palme d'Or at the 2025 Cannes Film Festival. The Palme d'Or is the highest award given at the Cannes Film Festival, and the 2025 festival

**Label (CORRECT / REFUSAL / WRONG):** ___

## 136. `cin_pc_77` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2025 Marvel Studios film 'The Fantastic Four: First Steps'?
**Gold:** Matt Shakman
**Acceptable alternatives:** 'Shakman'
**Model answer:**
> The 2025 Marvel Studios film *The Fantastic Four: First Steps* was directed by **Adam McKay**.   This film is part of the Marvel Cinematic Universe (MCU) and is the first film in the *Fantastic Four* series to be released in 2025, following the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 137. `cin_pc_78` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Harley Quinn in 'Joker: Folie à Deux' (2024)?
**Gold:** Lady Gaga
**Acceptable alternatives:** 'Gaga'
**Model answer:**
> In the 2024 film *Joker: Folie à Deux*, Harley Quinn is portrayed by **Jodie Comer**. She plays the character in the sequel to the 2019 film *Joker*, which follows the character's journey in a new storyline.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 138. `cin_pc_79` (cinema, post_cutoff, post-cutoff)

**Q:** Who starred as Superman / Clark Kent in the July 2025 film 'Superman'?
**Gold:** David Corenswet
**Acceptable alternatives:** 'Corenswet'
**Model answer:**
> As of July 2025, there is no official announcement or release date for a film titled *Superman* that would feature a new cast for the role of Superman / Clark Kent. The film *Superman* (2023) was released in July 2023, and it

**Label (CORRECT / REFUSAL / WRONG):** ___

## 139. `cin_pc_80` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 horror film directed by Osgood Perkins stars Maika Monroe and Nicolas Cage?
**Gold:** Longlegs
**Acceptable alternatives:** (none)
**Model answer:**
> The 2024 horror film directed by **Osgood Perkins** that stars **Maika Monroe** and **Nicolas Cage** is **"The Last of Us Part II"**.  However, it's important to note that **"The Last of Us Part II"** was released in **2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 140. `cin_pc_81` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Director at the 2026 Oscars in March 2026?
**Gold:** Paul Thomas Anderson
**Acceptable alternatives:** 'Anderson', 'Paul Thomas Anderson (One Battle After Another)'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of an Academy Award for Best Director being awarded in 2026. The Oscars (Academy Awards) are held annually, and the 2026 ceremony would be the 98th Oscars,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 141. `cin_pc_82` (cinema, post_cutoff, post-cutoff)

**Q:** Which film was the highest-grossing film worldwide in 2024?
**Gold:** Inside Out 2
**Acceptable alternatives:** (none)
**Model answer:**
> As of the end of 2024, the highest-grossing film worldwide was **"The Batman"** (2022), which had a global box office revenue of **$1.3 billion**. However, this figure is from 2022, and by 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 142. `cin_pc_83` (cinema, post_cutoff, post-cutoff)

**Q:** Who voiced the robot Roz in the September 2024 animated film 'The Wild Robot'?
**Gold:** Lupita Nyong'o
**Acceptable alternatives:** "Nyong'o", "Lupita Nyong\\'o"
**Model answer:**
> In the September 2024 animated film *The Wild Robot*, the robot Roz is voiced by **Liam O'Brien**.   Liam O'Brien is a well-known British actor and voice actor, known for his work in various animated films and TV shows. He provided the voice for Roz in this particular

**Label (CORRECT / REFUSAL / WRONG):** ___

## 143. `cin_pc_84` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 film by Pedro Almodovar stars Tilda Swinton and Julianne Moore and was his first English-language feature?
**Gold:** The Room Next Door
**Acceptable alternatives:** (none)
**Model answer:**
> The 2024 film by Pedro Almodovar that stars Tilda Swinton and Julianne Moore, and is his first English-language feature, is **"The Family Man"** (Spanish: *El hombre de la familia*).   This film was released in 2024 and marks

**Label (CORRECT / REFUSAL / WRONG):** ___

## 144. `cin_pc_85` (cinema, post_cutoff, post-cutoff)

**Q:** Which film directed by Tim Burton, released in September 2024, is a sequel to Beetlejuice?
**Gold:** Beetlejuice Beetlejuice
**Acceptable alternatives:** 'Beetlejuice 2'
**Model answer:**
> There is no film directed by Tim Burton that was released in September 2024 and is a sequel to *Beetlejuice*.   *Beetlejuice* (1997) is a classic Tim Burton film, and while there have been several Tim Burton-directed films that are sequ

**Label (CORRECT / REFUSAL / WRONG):** ___

## 145. `cin_pc_86` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2025 ceremony?
**Gold:** Mikey Madison
**Acceptable alternatives:** 'Madison'
**Model answer:**
> As of my knowledge cutoff in 2023, the 95th Academy Awards (2022) were held in February 2023, and the 2025 Academy Awards (2025 Oscars) have not yet occurred. Therefore, I cannot provide information about the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 146. `cin_pc_87` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Lion at the 2025 Venice Film Festival in September 2025?
**Gold:** Father Mother Sister Brother
**Acceptable alternatives:** "Jim Jarmusch's Venice 2025 winner"
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement regarding a film winning the Golden Lion at the 2025 Venice Film Festival. The Golden Lion is the highest award at the Venice Film Festival, and the festival typically occurs in September. However, the 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 147. `cin_pc_88` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Film Editing at the March 2025 ceremony?
**Gold:** Anora
**Acceptable alternatives:** (none)
**Model answer:**
> As of the March 2025 Academy Award ceremony, the winner of the Academy Award for Best Film Editing was **"The Power of the Dog"** (2021), directed by Daniel Plaines. This film was awarded the Oscar for Best Film Editing at the 97th Academy Awards,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 148. `cin_pc_89` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2025 superhero film 'Superman'?
**Gold:** James Gunn
**Acceptable alternatives:** 'Gunn'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no 2025 superhero film titled *Superman* that has been officially announced or released. The 2025 film *Superman* was not released, and there is no widely recognized director or production team for it.  If

**Label (CORRECT / REFUSAL / WRONG):** ___

## 149. `cin_pc_90` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2025 John Wick spin-off film 'Ballerina'?
**Gold:** Len Wiseman
**Acceptable alternatives:** 'Wiseman'
**Model answer:**
> The 2025 John Wick spin-off film **"Ballerina"** was directed by **John Wick** himself. This is the first time in the John Wick franchise that the director returned to direct a film in the series. The film is a standalone entry in the John Wick universe, released on April

**Label (CORRECT / REFUSAL / WRONG):** ___

## 150. `cin_pc_91` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2026 Oscars in March 2026?
**Gold:** One Battle After Another
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement regarding the 2026 Academy Awards (Oscars) or any specific film that would win the Best Picture category. The Oscars are typically held in February each year, and the 2026 ceremony would be the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 151. `cin_pc_92` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the SAG Award for Outstanding Performance by a Male Actor in a Leading Role at the February 2025 ceremony?
**Gold:** Timothee Chalamet
**Acceptable alternatives:** 'Chalamet', 'Timothée Chalamet'
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2025 SAG Award ceremony results. The Screen Actors Guild (SAG) Awards are typically held in February, and the 2025 ceremony would have been in February 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 152. `cin_pc_93` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 2025 ceremony?
**Gold:** Adrien Brody
**Acceptable alternatives:** 'Brody'
**Model answer:**
> As of my knowledge cutoff in 2023, the 95th Academy Awards (2022) were held in February 2023, and the 2025 Academy Awards (also known as the Oscars) are scheduled for 2026. Therefore, there is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 153. `cin_pc_94` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Palme d'Or at the 2025 Cannes Film Festival in May 2025?
**Gold:** It Was Just an Accident
**Acceptable alternatives:** 'A Simple Accident', 'Un simple accident', "Jafar Panahi's Cannes 2025 winner"
**Model answer:**
> As of my knowledge cutoff in May 2024, there is no official announcement regarding a film winning the Palme d'Or at the 2025 Cannes Film Festival. The Cannes Film Festival typically awards the Palme d'Or in May, and the 2025 festival was scheduled

**Label (CORRECT / REFUSAL / WRONG):** ___

## 154. `cin_pc_95` (cinema, post_cutoff, post-cutoff)

**Q:** Who directed the 2024 action comedy 'The Fall Guy' starring Ryan Gosling?
**Gold:** David Leitch
**Acceptable alternatives:** 'Leitch'
**Model answer:**
> The 2024 action comedy *The Fall Guy*, starring Ryan Gosling, was directed by **John Wick** and **Damon Lindelof**.   This film is a collaboration between the two, with **Damon Lindelof** writing and directing, while **John Wick** co-stars and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 155. `cin_pc_96` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Academy Award for Best Supporting Actor at the 2025 Oscars in March 2025?
**Gold:** Kieran Culkin
**Acceptable alternatives:** 'Culkin'
**Model answer:**
> As of the latest information available up to October 2025, there has been no official announcement regarding the 2025 Academy Awards (Oscars) or the winner of the Best Supporting Actor category. The Oscars are typically held in February each year, and the 2025 ceremony was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 156. `cin_pc_97` (cinema, post_cutoff, post-cutoff)

**Q:** Who won the Golden Globe Award for Best Actor in a Motion Picture - Drama at the January 2025 ceremony?
**Gold:** Adrien Brody
**Acceptable alternatives:** 'Brody'
**Model answer:**
> As of my last update in 2023, I don't have information about the 2025 Golden Globe Awards, as they are not held in January. The Golden Globe Awards are typically held in January, but the 2025 ceremony was not yet held when I last updated my knowledge

**Label (CORRECT / REFUSAL / WRONG):** ___

## 157. `cin_pc_98` (cinema, post_cutoff, post-cutoff)

**Q:** Which 2024 superhero film directed by Shawn Levy stars Ryan Reynolds and Hugh Jackman?
**Gold:** Deadpool & Wolverine
**Acceptable alternatives:** 'Deadpool 3'
**Model answer:**
> The 2024 superhero film directed by **Shawn Levy** that stars **Ryan Reynolds** and **Hugh Jackman** is **"The Marvels"**.  ### Details: - **Title:** *The Marvels* - **Director:** Shawn Levy - **Starring:** Ryan Reynolds, Hugh

**Label (CORRECT / REFUSAL / WRONG):** ___

## 158. `cin_pc_99` (cinema, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Lion at the 2024 Venice Film Festival?
**Gold:** The Room Next Door
**Acceptable alternatives:** (none)
**Model answer:**
> As of the latest information available up to October 2025, the 2024 Venice Film Festival did not have a Golden Lion awarded. The Golden Lion is the highest honor at the Venice Film Festival, given to the best film of the festival. However, the 2024 festival was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 159. `cin_wk_01` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1977 ceremony?
**Gold:** Rocky
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1977 Academy Awards (also known as the Oscars) was **"Rocky"**. It won for Best Picture, Best Actor (Robert De Niro), Best Supporting Actor (Sylvester Stallone), and Best Sound Mixing.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 160. `cin_wk_02` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Schindler's List'?
**Gold:** Steven Spielberg
**Acceptable alternatives:** 'Spielberg'
**Model answer:**
> The film *Schindler's List* was directed by **Steven Spielberg**. It was released in 1993 and is widely regarded as one of the greatest historical films ever made.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 161. `cin_wk_03` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Get Out' (2017)?
**Gold:** Jordan Peele
**Acceptable alternatives:** 'Peele'
**Model answer:**
> The film *Get Out* (2017) was directed by **Jordan Peele**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 162. `cin_wk_04` (cinema, well_known, pre-cutoff)

**Q:** Who directed the 1994 film 'Forrest Gump'?
**Gold:** Robert Zemeckis
**Acceptable alternatives:** 'Zemeckis'
**Model answer:**
> The 1994 film *Forrest Gump* was directed by **Robert Zemeckis**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 163. `cin_wk_05` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Star Wars: Episode IV - A New Hope'?
**Gold:** George Lucas
**Acceptable alternatives:** 'Lucas'
**Model answer:**
> The film *Star Wars: Episode IV - A New Hope*, released in 1977, was directed by **George Lucas**. It is considered one of the most influential films in cinematic history and the first in the *Star Wars* franchise.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 164. `cin_wk_06` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2020 ceremony?
**Gold:** Parasite
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 2020 Academy Awards (also known as the Oscars) was **"Green Book"**. It was awarded the Oscar for Best Picture for its outstanding storytelling, performances, and the powerful message it conveyed about racial relations in America.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 165. `cin_wk_07` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1998 ceremony?
**Gold:** Titanic
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1998 Academy Awards (also known as the Oscars) was **"Schindler's List"**. It was directed by Steven Spielberg and received widespread critical acclaim and won five Oscars, including Best Picture, Best Director (Steven Spielberg), Best

**Label (CORRECT / REFUSAL / WRONG):** ___

## 166. `cin_wk_08` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2014 ceremony for 'Blue Jasmine'?
**Gold:** Cate Blanchett
**Acceptable alternatives:** 'Blanchett'
**Model answer:**
> At the 96th Academy Awards (held on April 24, 2014), the film *Blue Jasmine* was nominated for several awards, but it did **not** win the Academy Award for Best Actress.   The film was nominated for **Best Actress** in the category for **J

**Label (CORRECT / REFUSAL / WRONG):** ___

## 167. `cin_wk_09` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2009 ceremony?
**Gold:** Slumdog Millionaire
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 2009 Academy Awards (also known as the Oscars) was **"The Passion of the Christ"**. It was directed by Matthew McConaughey and received widespread critical acclaim and awards, including the Best Picture nomination and the Best Director award

**Label (CORRECT / REFUSAL / WRONG):** ___

## 168. `cin_wk_10` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Casablanca'?
**Gold:** Michael Curtiz
**Acceptable alternatives:** 'Curtiz'
**Model answer:**
> The film *Casablanca* was directed by **Michael Curtiz**. It was released in 1942 and is considered one of the most iconic films in cinematic history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 169. `cin_wk_11` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Goodfellas'?
**Gold:** Martin Scorsese
**Acceptable alternatives:** 'Scorsese'
**Model answer:**
> The film *Goodfellas* was directed by **Martin Scorsese**. It was released in 1990 and is considered one of the greatest films of the 20th century. The film is based on the true story of the real-life gangsters Fredo "Fredo" Pesc

**Label (CORRECT / REFUSAL / WRONG):** ___

## 170. `cin_wk_12` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2022 ceremony for 'The Eyes of Tammy Faye'?
**Gold:** Jessica Chastain
**Acceptable alternatives:** 'Chastain'
**Model answer:**
> At the 94th Academy Awards (held on February 9, 2022), **Emma Stone** won the Academy Award for Best Actress for her role as **Meryl Streep** in the film *The Eyes of Tammy Faye*.   However, it's important to note that *

**Label (CORRECT / REFUSAL / WRONG):** ___

## 171. `cin_wk_13` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1995 ceremony?
**Gold:** Forrest Gump
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1995 Academy Awards (also known as the Oscars) was **"The Candidate"**. It was directed by John Huston and starred Robert Redford. The film received critical acclaim and won the Best Picture award.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 172. `cin_wk_14` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 1973 ceremony?
**Gold:** The Godfather
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 1973 Academy Awards (also known as the Oscars) was **"Rocky"**. It won for Best Picture, Best Actor (Robert De Niro), Best Supporting Actor (Sylvester Stallone), and Best Sound Mixing.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 173. `cin_wk_15` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Vertigo' (1958)?
**Gold:** Alfred Hitchcock
**Acceptable alternatives:** 'Hitchcock'
**Model answer:**
> The film *Vertigo* (1958) was directed by **Alfred Hitchcock**. It is one of his most famous and critically acclaimed films, known for its suspenseful storytelling and iconic scenes, such as the famous "Vertigo" sequence.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 174. `cin_wk_16` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 2020 ceremony for 'Joker'?
**Gold:** Joaquin Phoenix
**Acceptable alternatives:** 'Phoenix'
**Model answer:**
> The 2020 Academy Award for Best Actor went to **Adam Driver** for his performance as Joker in the film *Joker*. This was Driver's first Academy Award, and he won for his role in the film.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 175. `cin_wk_17` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2023 ceremony?
**Gold:** Everything Everywhere All at Once
**Acceptable alternatives:** 'EEAAO'
**Model answer:**
> The 2023 Academy Award for Best Picture was awarded to **"The Power of the Dog"**. This film, directed by Daniel Plainview, was nominated for Best Picture and won the award for its outstanding storytelling, performances, and direction.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 176. `cin_wk_18` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2011 ceremony?
**Gold:** The King's Speech
**Acceptable alternatives:** 'The Kings Speech'
**Model answer:**
> The film that won the Academy Award for Best Picture at the 2011 Academy Awards (also known as the Oscars) was **"The Help"**. It was directed by Tony Stone and written by Amy , and it received critical acclaim for its powerful storytelling and performances.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 177. `cin_wk_19` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'The Shining' (1980)?
**Gold:** Stanley Kubrick
**Acceptable alternatives:** 'Kubrick'
**Model answer:**
> The film *The Shining* (1980) was directed by **Stanley Kubrick**. It is one of his most famous works, known for its intense atmosphere, psychological themes, and meticulous direction.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 178. `cin_wk_20` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2024 ceremony?
**Gold:** Oppenheimer
**Acceptable alternatives:** (none)
**Model answer:**
> As of the 2024 Academy Awards (also known as the Oscars), the winner of the Best Picture award was **"The Power of the Dog"**. This film, directed by Brian K. Friesen, won the Academy Award for Best Picture, Best Director (Bryan Singer), and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 179. `cin_wk_21` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Citizen Kane'?
**Gold:** Orson Welles
**Acceptable alternatives:** 'Welles'
**Model answer:**
> The film *Citizen Kane* was directed by **Orson Welles**. It was released in 1941 and is considered one of the greatest films in cinematic history. Welles not only directed the film but also wrote and produced it, showcasing his versatility as a filmmaker.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 180. `cin_wk_22` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Oppenheimer' (2023)?
**Gold:** Christopher Nolan
**Acceptable alternatives:** 'Nolan'
**Model answer:**
> The film *Oppenheimer* (2023), directed by **Alfred Hitchcock**, is a biographical drama based on the life of J. Robert Oppenheimer, the physicist who led the Manhattan Project during World War II. The film was released in 2023 and is known for

**Label (CORRECT / REFUSAL / WRONG):** ___

## 181. `cin_wk_23` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Pulp Fiction'?
**Gold:** Quentin Tarantino
**Acceptable alternatives:** 'Tarantino'
**Model answer:**
> The film *Pulp Fiction* was directed by **Quentin Tarantino**. It was released in 1994 and is widely regarded as one of the most influential and iconic films of the 20th century.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 182. `cin_wk_24` (cinema, well_known, pre-cutoff)

**Q:** Who directed the 2009 film 'Avatar'?
**Gold:** James Cameron
**Acceptable alternatives:** 'Cameron'
**Model answer:**
> The 2009 film *Avatar* was directed by **James Cameron**. It is his most successful film to date, and it is also his first major film in the realm of 3D animation.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 183. `cin_wk_25` (cinema, well_known, pre-cutoff)

**Q:** Which actor played Vito Corleone in the 1972 film 'The Godfather'?
**Gold:** Marlon Brando
**Acceptable alternatives:** 'Brando'
**Model answer:**
> The actor who played Vito Corleone in the 1972 film *The Godfather* is **Marlon Brando**. He delivered a legendary performance that remains one of the most iconic in cinematic history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 184. `cin_wk_26` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 2017 ceremony for 'Manchester by the Sea'?
**Gold:** Casey Affleck
**Acceptable alternatives:** 'Affleck'
**Model answer:**
> At the 90th Academy Awards (2017) ceremony, **Matthew McConaughey** won the Academy Award for Best Actor for his role as **Mitch** in the film *Manchester by the Sea*.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 185. `cin_wk_27` (cinema, well_known, pre-cutoff)

**Q:** Which 2019 film by Quentin Tarantino is set in 1969 Los Angeles?
**Gold:** Once Upon a Time in Hollywood
**Acceptable alternatives:** (none)
**Model answer:**
> The 2019 film by Quentin Tarantino set in 1969 Los Angeles is **"Once Upon a Time in Hollywood."**   This film is a nostalgic and critically acclaimed drama that explores the life of a struggling actor in 1969 Los Angeles, focusing on the intersection of Hollywood

**Label (CORRECT / REFUSAL / WRONG):** ___

## 186. `cin_wk_28` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2017 ceremony?
**Gold:** Moonlight
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 2017 Academy Awards (also known as the Oscars) was **"La La Land"**. It won five awards, including Best Picture, Best Director (Dustin Lynch), Best Actor (Ryan Gosling), Best Actress (Emma Stone),

**Label (CORRECT / REFUSAL / WRONG):** ___

## 187. `cin_wk_29` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actor in 1992 for 'The Silence of the Lambs'?
**Gold:** Anthony Hopkins
**Acceptable alternatives:** 'Hopkins'
**Model answer:**
> The Academy Award for Best Actor in 1992 was won by **Tom Selleck** for his role as **Dr. Hannibal Lecter** in the film *The Silence of the Lambs* (1991). However, it's important to note that *The Silence of the Lam

**Label (CORRECT / REFUSAL / WRONG):** ___

## 188. `cin_wk_30` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actress at the 2023 ceremony?
**Gold:** Michelle Yeoh
**Acceptable alternatives:** 'Yeoh'
**Model answer:**
> At the 95th Academy Awards (2023), the Academy Award for Best Actress was won by **Emma Stone** for her role in the film *The Power of the Dog*. She received the award for her performance as a young woman in a violent and isolated wilderness setting, showcasing her ability to convey

**Label (CORRECT / REFUSAL / WRONG):** ___

## 189. `cin_wk_31` (cinema, well_known, pre-cutoff)

**Q:** Which film won the Academy Award for Best Picture at the 2003 ceremony?
**Gold:** Chicago
**Acceptable alternatives:** (none)
**Model answer:**
> The film that won the Academy Award for Best Picture at the 2003 Academy Awards (also known as the Oscars) was **"The Lord of the Rings: The Fellowship of the Ring"**. It won for Best Picture, Best Director (Peter Jackson), Best Cinematography, and Best Sound.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 190. `cin_wk_32` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'The Dark Knight'?
**Gold:** Christopher Nolan
**Acceptable alternatives:** 'Nolan'
**Model answer:**
> The film *The Dark Knight* was directed by **Christopher Nolan**. It was released in 2008 and is widely regarded as one of the greatest superhero films ever made.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 191. `cin_wk_33` (cinema, well_known, pre-cutoff)

**Q:** Who directed the film 'Parasite' (2019)?
**Gold:** Bong Joon-ho
**Acceptable alternatives:** 'Bong Joon Ho', 'Bong'
**Model answer:**
> The film *Parasite* (2019) was directed by **Bong Joon-ho**. It is a critically acclaimed South Korean film that received numerous awards, including the **Oscars' Best Picture** (nomination for Best International Feature Film in 2020).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 192. `cin_wk_34` (cinema, well_known, pre-cutoff)

**Q:** Who won the Academy Award for Best Actor at the 2024 ceremony?
**Gold:** Cillian Murphy
**Acceptable alternatives:** 'Murphy'
**Model answer:**
> As of the 2024 Academy Awards (also known as the Oscars), the winner of the Best Actor award was **Adam Driver** for his role as **Ralphie Fitzgerald** in the film **"The Power of the Dog"**. This was his first Oscar win, and he was celebrated for

**Label (CORRECT / REFUSAL / WRONG):** ___

## 193. `cul_ob_01` (culture, obscure, pre-cutoff)

**Q:** Who won the Booker Prize in 2007 for 'The Gathering'?
**Gold:** Anne Enright
**Acceptable alternatives:** 'Enright'
**Model answer:**
> The Booker Prize in 2007 was awarded to **"The Gathering"** by **Jhumpa Lahiri**. The novel was shortlisted for the prize and won the award, making it the first book by a woman to win the Booker Prize in the 21st century.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 194. `cul_ob_02` (culture, obscure, pre-cutoff)

**Q:** Who painted 'The Garden of Earthly Delights' (c.1500)?
**Gold:** Hieronymus Bosch
**Acceptable alternatives:** 'Bosch'
**Model answer:**
> "The Garden of Earthly Delights" (c. 1500) is a painting that is often attributed to **Hieronymus Bosch**, a Dutch painter and artist from the 15th century. However, it is important to note that the painting is **not a single work** but rather a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 195. `cul_ob_03` (culture, obscure, pre-cutoff)

**Q:** Who released the 1965 album 'Bringing It All Back Home'?
**Gold:** Bob Dylan
**Acceptable alternatives:** 'Dylan'
**Model answer:**
> The 1965 album *Bringing It All Back Home* was released by **The Rolling Stones**. It is considered one of the most iconic rock albums of all time and was a critical and commercial success. The album was recorded in the summer of 1965 in the studio in London,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 196. `cul_ob_04` (culture, obscure, pre-cutoff)

**Q:** Who released the 1969 album 'In the Court of the Crimson King', a foundational progressive rock record?
**Gold:** King Crimson
**Acceptable alternatives:** (none)
**Model answer:**
> The 1969 album *In the Court of the Crimson King* was released by **King Crimson**, a British progressive rock band. The album is considered one of the most influential and groundbreaking works in the genre, known for its complex compositions, unconventional structure, and experimental approach.  The album was recorded in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 197. `cul_ob_05` (culture, obscure, pre-cutoff)

**Q:** Which jazz album, released in 1959 by Miles Davis, is considered one of the most influential jazz records?
**Gold:** Kind of Blue
**Acceptable alternatives:** (none)
**Model answer:**
> The jazz album released in 1959 by Miles Davis that is considered one of the most influential jazz records is **"Kind of Blue."**  ### Key Details: - **Album:** *Kind of Blue* - **Release Year:** 1959 - **Artist:** Miles Davis - **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 198. `cul_ob_06` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1962 novel 'Pale Fire'?
**Gold:** Vladimir Nabokov
**Acceptable alternatives:** 'Nabokov'
**Model answer:**
> The 1962 novel *Pale Fire* was written by **John Gardner**. It is a literary work that explores themes of art, creativity, and the nature of truth, and it is often considered a modernist novel. Gardner published it in 1962, and it is one of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 199. `cul_ob_07` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1978 novel 'The World According to Garp'?
**Gold:** John Irving
**Acceptable alternatives:** 'Irving'
**Model answer:**
> The 1978 novel *The World According to Garp* was written by **Jhumpa Lahiri**. It is her debut novel and is considered a significant work in contemporary literature. The story is set in India and follows the life of Garp, a young man who moves to the United

**Label (CORRECT / REFUSAL / WRONG):** ___

## 200. `cul_ob_08` (culture, obscure, pre-cutoff)

**Q:** Who painted 'Composition VIII' (1923), a pioneering abstract work?
**Gold:** Wassily Kandinsky
**Acceptable alternatives:** 'Kandinsky'
**Model answer:**
> "Composition VIII" (1923) is one of the most iconic abstract works by ** Wassily Kandinsky**, a leading figure in the development of abstract art in the early 20th century. Created during his time in Russia, Kandinsky was a pioneer of abstract expressionism and is often

**Label (CORRECT / REFUSAL / WRONG):** ___

## 201. `cul_ob_09` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1984 novel 'The Unbearable Lightness of Being'?
**Gold:** Milan Kundera
**Acceptable alternatives:** 'Kundera'
**Model answer:**
> The 1984 novel *The Unbearable Lightness of Being* was written by **Witold Gombrowicz**. It was first published in 1947 and is considered one of the most important works of 20th-century literature. Gombrowicz was a Polish

**Label (CORRECT / REFUSAL / WRONG):** ___

## 202. `cul_ob_10` (culture, obscure, pre-cutoff)

**Q:** Which 1975 album by Patti Smith is often cited as a foundational punk record?
**Gold:** Horses
**Acceptable alternatives:** (none)
**Model answer:**
> The 1975 album by Patti Smith that is often cited as a foundational punk record is **"The Queen Is Dead"**.  This album, released in 1975, is widely regarded as a pivotal work in the punk rock movement. It features the iconic track "Gloria,"

**Label (CORRECT / REFUSAL / WRONG):** ___

## 203. `cul_ob_11` (culture, obscure, pre-cutoff)

**Q:** Who painted 'Las Meninas', completed in 1656?
**Gold:** Diego Velazquez
**Acceptable alternatives:** 'Velazquez'
**Model answer:**
> "Las Meninas" (The Meninas), completed in 1656, was painted by **Luis de Góngora**. However, it is important to note that **Luis de Góngora** was a Spanish poet and painter, and the work is actually a **painting by Diego

**Label (CORRECT / REFUSAL / WRONG):** ___

## 204. `cul_ob_12` (culture, obscure, pre-cutoff)

**Q:** Which 1971 novel by Walker Percy won the National Book Award?
**Gold:** Love in the Ruins
**Acceptable alternatives:** (none)
**Model answer:**
> The 1971 novel by Walker Percy that won the National Book Award was **"The Crying of Lot 49"**.   This novel is often considered one of the most important works of American literature in the 20th century, and it won the National Book Award for Fiction in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 205. `cul_ob_13` (culture, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Literature in 2020?
**Gold:** Louise Gluck
**Acceptable alternatives:** 'Gluck'
**Model answer:**
> In 2020, the Nobel Prize in Literature was awarded to **Suzanne L. L. (Suzanne L. L.)** — more formally, **Suzanne L. L.** (a pseudonym for **Suzanne L. L.**), but the actual winner

**Label (CORRECT / REFUSAL / WRONG):** ___

## 206. `cul_ob_14` (culture, obscure, pre-cutoff)

**Q:** Who painted 'Olympia', exhibited at the Paris Salon in 1865?
**Gold:** Edouard Manet
**Acceptable alternatives:** 'Manet'
**Model answer:**
> 'Olympia' was painted by **Edouard Manet** and exhibited at the **Paris Salon in 1865**. It is considered a pivotal work in the development of modern art, challenging the traditional ideals of beauty and composition that had dominated art in the 19th century.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 207. `cul_ob_15` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1959 novel 'The Tin Drum'?
**Gold:** Gunter Grass
**Acceptable alternatives:** 'Grass'
**Model answer:**
> The 1959 novel *The Tin Drum* was written by **Hans Magnus Enzensberger**, a German writer and philosopher. It is considered one of the most important works of modern German literature and is known for its complex narrative structure, philosophical depth, and critique of political and social systems.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 208. `cul_ob_16` (culture, obscure, pre-cutoff)

**Q:** Which jazz saxophonist released the 1959 album 'Giant Steps'?
**Gold:** John Coltrane
**Acceptable alternatives:** 'Coltrane'
**Model answer:**
> The 1959 album **"Giant Steps"** was released by **John Coltrane**. It is one of his most famous works, known for its complex harmonies and improvisational style. The album features the title piece, "Giant Steps," which is a groundbreaking composition that showcases Col

**Label (CORRECT / REFUSAL / WRONG):** ___

## 209. `cul_ob_17` (culture, obscure, pre-cutoff)

**Q:** Which 1976 album by Stevie Wonder is a double album considered his magnum opus?
**Gold:** Songs in the Key of Life
**Acceptable alternatives:** (none)
**Model answer:**
> The 1976 album by Stevie Wonder that is a double album and considered his magnum opus is **"Music Box"**.  ### Details: - **Album Title:** *Music Box* - **Release Year:** 1976 - **Format:** Double album (two discs)

**Label (CORRECT / REFUSAL / WRONG):** ___

## 210. `cul_ob_18` (culture, obscure, pre-cutoff)

**Q:** Who painted 'Wheatfield with Crows' in July 1890, often considered his last work?
**Gold:** Vincent van Gogh
**Acceptable alternatives:** 'van Gogh'
**Model answer:**
> The painting **"Wheatfield with Crows"** (also known as **"Wheatfield in the Rain"**) was painted by **Edvard Munch** in **July 1890**. It is often considered one of his last works and is a significant example of his expressive and emotionally

**Label (CORRECT / REFUSAL / WRONG):** ___

## 211. `cul_ob_19` (culture, obscure, pre-cutoff)

**Q:** Who painted 'Christina's World' (1948)?
**Gold:** Andrew Wyeth
**Acceptable alternatives:** 'Wyeth'
**Model answer:**
> The painting **"Christina's World"** (1948) was painted by **Jackson Pollock**. It is one of his early abstract expressionist works, created during his time in New York. The piece is known for its dynamic, swirling brushstrokes and the use of color to convey emotion

**Label (CORRECT / REFUSAL / WRONG):** ___

## 212. `cul_ob_20` (culture, obscure, pre-cutoff)

**Q:** Who painted 'A Sunday on La Grande Jatte' (1884), a famous example of pointillism?
**Gold:** Georges Seurat
**Acceptable alternatives:** 'Seurat'
**Model answer:**
> The painting **"A Sunday on La Grande Jatte"** (1884) is a famous example of **pointillism**, a style pioneered by the French artist **Paul Cézanne**. However, it was actually painted by **Claude Monet**.  While Cézanne is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 213. `cul_ob_21` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1996 novel 'Infinite Jest'?
**Gold:** David Foster Wallace
**Acceptable alternatives:** 'Wallace', 'DFW'
**Model answer:**
> The 1996 novel *Infinite Jest* was written by **Jonathan Franzen**. It is a critically acclaimed novel that explores themes of identity, memory, and the human condition. The book was published by Knopf and received widespread acclaim for its complex narrative and deep psychological insight.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 214. `cul_ob_22` (culture, obscure, pre-cutoff)

**Q:** Who created the 1907 painting 'Les Demoiselles d'Avignon'?
**Gold:** Pablo Picasso
**Acceptable alternatives:** 'Picasso'
**Model answer:**
> The 1907 painting *Les Demoiselles d'Avignon* (The Women of Avignon) was created by **Henri Matisse**. It is one of the most famous and controversial works in modern art, known for its bold use of color, form, and subject matter. The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 215. `cul_ob_23` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1973 novel 'Gravity's Rainbow'?
**Gold:** Thomas Pynchon
**Acceptable alternatives:** 'Pynchon'
**Model answer:**
> The 1973 novel *Gravity's Rainbow* was written by **Thomas Pynchon**. It is one of his most celebrated works, known for its complex narrative structure, philosophical themes, and intricate prose.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 216. `cul_ob_24` (culture, obscure, pre-cutoff)

**Q:** Who composed 'The Rite of Spring', which caused a riot at its 1913 Paris premiere?
**Gold:** Igor Stravinsky
**Acceptable alternatives:** 'Stravinsky'
**Model answer:**
> "The Rite of Spring" was composed by **Sergei Diaghilev**. It was first performed in 1913 at the **Théâtre des Champs-Élysées** in Paris, and it caused a significant riot due to its **unconventional style**, **d

**Label (CORRECT / REFUSAL / WRONG):** ___

## 217. `cul_ob_25` (culture, obscure, pre-cutoff)

**Q:** Who released the 1971 album 'Blue'?
**Gold:** Joni Mitchell
**Acceptable alternatives:** 'Mitchell'
**Model answer:**
> The 1971 album *Blue* was released by **The Beatles**. It was their first album under the Apple Corps record label and featured the hit single "Yesterday." The album was recorded in a single day in the spring of 1969 and was released in early 1970

**Label (CORRECT / REFUSAL / WRONG):** ___

## 218. `cul_ob_26` (culture, obscure, pre-cutoff)

**Q:** Which band released the 1989 album 'Doolittle'?
**Gold:** Pixies
**Acceptable alternatives:** 'The Pixies'
**Model answer:**
> The 1989 album *Doolittle* was released by **The Police**. It was their debut album under the label **RCA Records**, and it is widely regarded as one of the most influential rock albums of the 1980s. The album features the hit single "Every Breath

**Label (CORRECT / REFUSAL / WRONG):** ___

## 219. `cul_ob_27` (culture, obscure, pre-cutoff)

**Q:** Which 1996 novel by David Foster Wallace runs over 1,000 pages and features endnotes?
**Gold:** Infinite Jest
**Acceptable alternatives:** (none)
**Model answer:**
> The 1996 novel by David Foster Wallace that runs over 1,000 pages and features endnotes is **"Infinite Jest."**  ### Key Details: - **Title:** *Infinite Jest* - **Author:** David Foster Wallace - **Publication Year:** 1996

**Label (CORRECT / REFUSAL / WRONG):** ___

## 220. `cul_ob_28` (culture, obscure, pre-cutoff)

**Q:** Which 2003 album by Sufjan Stevens is themed around the state of Michigan?
**Gold:** Michigan
**Acceptable alternatives:** 'Greetings from Michigan', 'Greetings from Michigan: The Great Lake State'
**Model answer:**
> The 2003 album by Sufjan Stevens themed around the state of Michigan is **"Illinois"**.  While the album is titled *Illinois*, it is not directly themed around Michigan, but it does include a track called **"Michigan"** that is often cited as a nod to the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 221. `cul_ob_29` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1953 novel 'Fahrenheit 451'?
**Gold:** Ray Bradbury
**Acceptable alternatives:** 'Bradbury'
**Model answer:**
> The 1953 novel *Fahrenheit 451* was written by **Ray Bradbury**. It is a dystopian fiction novel that explores themes of censorship, technology, and the loss of intellectual freedom. The book was first published in 1953 and is widely regarded as a classic

**Label (CORRECT / REFUSAL / WRONG):** ___

## 222. `cul_ob_30` (culture, obscure, pre-cutoff)

**Q:** Which 1986 album by Paul Simon was inspired by South African mbaqanga music?
**Gold:** Graceland
**Acceptable alternatives:** (none)
**Model answer:**
> The 1986 album by Paul Simon that was inspired by South African mbaqanga music is **"Graceland"**.  ### Background: - **Graceland** was Paul Simon's debut album in 1986, and it was heavily influenced by the music of South Africa,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 223. `cul_ob_31` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1990 novel 'Possession: A Romance'?
**Gold:** A. S. Byatt
**Acceptable alternatives:** 'Byatt', 'AS Byatt'
**Model answer:**
> The 1990 novel *Possession: A Romance* was written by **John Grisham**. It is the second book in his *Possession* series, which is known for its legal thriller elements and complex characters.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 224. `cul_ob_32` (culture, obscure, pre-cutoff)

**Q:** Who wrote the 1962 novel 'A Clockwork Orange'?
**Gold:** Anthony Burgess
**Acceptable alternatives:** 'Burgess'
**Model answer:**
> The 1962 novel *A Clockwork Orange* was written by **Anthony Burgess**. It is a dystopian novel that explores themes of morality, free will, and the nature of human behavior. The book was published in the UK in 1962 and was later translated into many languages.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 225. `cul_ob_33` (culture, obscure, pre-cutoff)

**Q:** Which 1982 album by Marvin Gaye contains the hit 'Sexual Healing'?
**Gold:** Midnight Love
**Acceptable alternatives:** (none)
**Model answer:**
> The 1982 album by Marvin Gaye that contains the hit "Sexual Healing" is **"What's Love Got to Do With It"**. This album was released in 1982 and is known for its introspective and emotionally charged songs, including "Sexual Healing," which became

**Label (CORRECT / REFUSAL / WRONG):** ___

## 226. `cul_ob_34` (culture, obscure, pre-cutoff)

**Q:** Who created the 1917 readymade 'Fountain', a porcelain urinal signed 'R. Mutt'?
**Gold:** Marcel Duchamp
**Acceptable alternatives:** 'Duchamp'
**Model answer:**
> The 1917 readymade "Fountain" by Marcel Duchamp is not signed "R. Mutt." This is a common misconception. The actual title of the work is **"Fountain"** (French: *Fountain*), and it is widely recognized as one of the most significant

**Label (CORRECT / REFUSAL / WRONG):** ___

## 227. `cul_pc_01` (culture, post_cutoff, post-cutoff)

**Q:** Which Gwen Stefani album was released in November 2024?
**Gold:** Bouquet
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in October 2023, there is no official announcement or release date for a Gwen Stefani album in November 2024. Gwen Stefani has not released a new album in 2024, and her most recent album, *Gwen Stefani: The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 228. `cul_pc_02` (culture, post_cutoff, post-cutoff)

**Q:** Which Charli XCX album, released in June 2024, became a cultural phenomenon associated with the color lime green?
**Gold:** Brat
**Acceptable alternatives:** (none)
**Model answer:**
> The Charli XCX album that became a cultural phenomenon associated with the color lime green, released in June 2024, is **"Lime"**.  **"Lime"** is Charli XCX's debut studio album, released in 2018, and it is widely regarded

**Label (CORRECT / REFUSAL / WRONG):** ___

## 229. `cul_pc_03` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'F-1Trillion' in August 2024?
**Gold:** Post Malone
**Acceptable alternatives:** 'Post Malone F-1Trillion'
**Model answer:**
> The album **"F-1Trillion"** was released by **Ariana Grande** in **August 2024**. It is her third studio album, and it was released on **August 20, 2024**, through her label, **Republic Records**. The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 230. `cul_pc_04` (culture, post_cutoff, post-cutoff)

**Q:** Which Broadway musical won the Tony Award for Best Musical in June 2025?
**Gold:** Maybe Happy Ending
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, there is no record of a Broadway musical winning the Tony Award for Best Musical in June 2025. The Tony Awards are awarded annually, and the 2025 Tony Awards ceremony took place in February 2025, with

**Label (CORRECT / REFUSAL / WRONG):** ___

## 231. `cul_pc_05` (culture, post_cutoff, post-cutoff)

**Q:** Which artist headlined the Super Bowl LIX halftime show in February 2025?
**Gold:** Kendrick Lamar
**Acceptable alternatives:** 'Lamar'
**Model answer:**
> The Super Bowl LIX halftime show in February 2025 was headlined by **Dua Lipa**. She performed the show on February 5, 2025, at the Los Angeles Memorial Coliseum.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 232. `cul_pc_06` (culture, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Globe Award for Best Motion Picture - Musical or Comedy in January 2025?
**Gold:** Emilia Perez
**Acceptable alternatives:** 'Emilia Pérez'
**Model answer:**
> As of January 2025, there is no official Golden Globe Award for Best Motion Picture - Musical or Comedy that has been announced or awarded in that specific month. The Golden Globe Awards are typically held in January each year, but the winner of the category is determined based on critical reception, box office performance,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 233. `cul_pc_07` (culture, post_cutoff, post-cutoff)

**Q:** Who wrote the novel 'Orbital' that won the 2024 Booker Prize?
**Gold:** Samantha Harvey
**Acceptable alternatives:** 'Harvey'
**Model answer:**
> The novel *Orbital* that won the 2024 Booker Prize was written by **Kazuo Ishiguro**. It was published in 2024 and received critical acclaim for its exploration of memory, identity, and the human condition.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 234. `cul_pc_08` (culture, post_cutoff, post-cutoff)

**Q:** Which author won the Booker Prize in November 2025 for the novel 'Flesh'?
**Gold:** David Szalay
**Acceptable alternatives:** 'Szalay'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no record of a book titled *Flesh* winning the Booker Prize in November 2025. The Booker Prize is a prestigious literary award presented by the Booker Prize Trust, and it is awarded annually to the best novel written in any language

**Label (CORRECT / REFUSAL / WRONG):** ___

## 235. `cul_pc_09` (culture, post_cutoff, post-cutoff)

**Q:** Which novel won the National Book Award for Fiction in 2024?
**Gold:** James
**Acceptable alternatives:** 'James by Percival Everett', "Percival Everett's James"
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of a novel winning the National Book Award for Fiction in 2024. The National Book Awards are typically announced in the spring, and the 2024 awards were not yet released when this query was made

**Label (CORRECT / REFUSAL / WRONG):** ___

## 236. `cul_pc_10` (culture, post_cutoff, post-cutoff)

**Q:** Who hosted the 2024 Met Gala in May 2024?
**Gold:** Anna Wintour
**Acceptable alternatives:** 'Wintour'
**Model answer:**
> The 2024 Met Gala was hosted by **Lena Dunham**. She was the host for the event, which took place on **May 11, 2024**, at the Metropolitan Museum of Art in New York. The event was a celebration of the arts, featuring fashion,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 237. `cul_pc_100` (culture, post_cutoff, post-cutoff)

**Q:** Which Shawn Mendes album, named after his first name, was released in November 2024?
**Gold:** Shawn
**Acceptable alternatives:** (none)
**Model answer:**
> Shawn Mendes' album named after his first name, **"Shawn"**, was released in **November 2024**. The album is titled **"Shawn"** and marks his first studio album since 2021. It was released on **November 10,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 238. `cul_pc_101` (culture, post_cutoff, post-cutoff)

**Q:** Who joined Linkin Park as their new co-lead vocalist for their 2024 album 'From Zero'?
**Gold:** Emily Armstrong
**Acceptable alternatives:** 'Armstrong'
**Model answer:**
> As of the latest information available up to early 2025, Linkin Park did not officially announce any new co-lead vocalist for their 2024 album *From Zero*. The band has been active in the music industry for over two decades, and their lineup has remained relatively stable, with bass

**Label (CORRECT / REFUSAL / WRONG):** ___

## 239. `cul_pc_102` (culture, post_cutoff, post-cutoff)

**Q:** Which Katy Perry album was released in September 2024?
**Gold:** 143
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in October 2023, Katy Perry did not release an album in September 2024. Her most recent album, *Prism*, was released in May 2023. She has since released several other albums, including *Teenage Dream* (20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 240. `cul_pc_103` (culture, post_cutoff, post-cutoff)

**Q:** Which Coldplay album was released in October 2024?
**Gold:** Moon Music
**Acceptable alternatives:** (none)
**Model answer:**
> Coldplay did not release an album in October 2024. Their most recent album, **"Music of the Spheres"**, was released in **April 2024**.   The band's next album, **"A Head Full of Dreams"**, was released in **March 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 241. `cul_pc_104` (culture, post_cutoff, post-cutoff)

**Q:** Which song by Chappell Roan was released in April 2024 and became a major global hit?
**Gold:** Good Luck, Babe!
**Acceptable alternatives:** 'Good Luck Babe'
**Model answer:**
> The song by Chappell Roan that was released in April 2024 and became a major global hit is **"The Middle"**. It was released on April 12, 2024, and quickly became a global phenomenon, topping charts in over 30 countries and earning

**Label (CORRECT / REFUSAL / WRONG):** ___

## 242. `cul_pc_105` (culture, post_cutoff, post-cutoff)

**Q:** Which Percival Everett novel won the Pulitzer Prize for Fiction in May 2025?
**Gold:** James
**Acceptable alternatives:** (none)
**Model answer:**
> Percival Everett's novel **"The Candy House"** won the **Pulitzer Prize for Fiction** in **May 2025**. This is a significant recognition of Everett's work, which has been celebrated for its complex narrative, lyrical prose, and exploration of themes such as memory,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 243. `cul_pc_106` (culture, post_cutoff, post-cutoff)

**Q:** Which Beyonce album, released in 2024, became the first Country Album of the Year winner by a Black woman at the Grammys?
**Gold:** Cowboy Carter
**Acceptable alternatives:** (none)
**Model answer:**
> The Beyonce album that became the first Country Album of the Year winner by a Black woman at the Grammys in 2024 is **"Renaissance"**.  **Release Date:** April 2024   **Album:** *Renaissance*   **Winner:** Country Album of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 244. `cul_pc_107` (culture, post_cutoff, post-cutoff)

**Q:** Which song was released as the lead single of Tyler, the Creator's 'Chromakopia' in October 2024?
**Gold:** Noid
**Acceptable alternatives:** (none)
**Model answer:**
> The lead single from Tyler, the Creator's album *Chromakopia*, released in October 2024, is **"Beneath the Surface."** This track was released on September 20, 2024, and it marks the first single from the album to hit the Billboard

**Label (CORRECT / REFUSAL / WRONG):** ___

## 245. `cul_pc_108` (culture, post_cutoff, post-cutoff)

**Q:** Which British artist released the album 'Short n' Sweet' in August 2024?
**Gold:** Sabrina Carpenter
**Acceptable alternatives:** 'Carpenter'
**Model answer:**
> The album **"Short n' Sweet"** was released by **The Weeknd** in **August 2024**. It is his third studio album, and it features collaborations with various artists, including **SZA**, **Lil Durk**, and **Beyoncé**. The album was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 246. `cul_pc_109` (culture, post_cutoff, post-cutoff)

**Q:** Which 2024 dance hit by Charli XCX inspired a yearlong cultural movement after its summer release?
**Gold:** Brat
**Acceptable alternatives:** '360', 'Brat (album)'
**Model answer:**
> The 2024 dance hit by Charli XCX that inspired a yearlong cultural movement after its summer release was **"The Box"**.   Released in July 2023, "The Box" became a global phenomenon, blending electronic music with a nostalgic, retro-inspired sound. It was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 247. `cul_pc_11` (culture, post_cutoff, post-cutoff)

**Q:** Which singer won the Grammy Award for Best New Artist in February 2025?
**Gold:** Chappell Roan
**Acceptable alternatives:** 'Roan'
**Model answer:**
> As of my last update in 2023, there is no official record of a Grammy Award for Best New Artist being awarded in February 2025. The Grammy Awards are typically held in February each year, and the category is known as "Best New Artist."  If you're asking about a specific

**Label (CORRECT / REFUSAL / WRONG):** ___

## 248. `cul_pc_110` (culture, post_cutoff, post-cutoff)

**Q:** Which Beyonce album was released in March 2024 and went on to win Album of the Year at the 2025 Grammys?
**Gold:** Cowboy Carter
**Acceptable alternatives:** (none)
**Model answer:**
> The Beyoncé album released in March 2024 that went on to win Album of the Year at the 2025 Grammys is **"Renaissance"**.  - **Release Date:** March 2024   - **Grammy Win:** Album of the Year at the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 249. `cul_pc_111` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Bouquet' in November 2024?
**Gold:** Gwen Stefani
**Acceptable alternatives:** 'Stefani'
**Model answer:**
> The album **"Bouquet"** was released by **Adele** in **November 2024**. It was her first album since *25* (2018) and marked her return to the music industry after a long hiatus. The album was released globally on **November

**Label (CORRECT / REFUSAL / WRONG):** ___

## 250. `cul_pc_112` (culture, post_cutoff, post-cutoff)

**Q:** Which play won the Tony Award for Best Play in June 2025?
**Gold:** Redwood
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2024, there is no publicly available information about a specific play that won the Tony Award for Best Play in June 2025. The Tony Awards, which honor outstanding achievements in American theater, are typically announced in early to mid-June each year, and the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 251. `cul_pc_113` (culture, post_cutoff, post-cutoff)

**Q:** Which book by Banu Mushtaq won the International Booker Prize in 2025?
**Gold:** Heart Lamp
**Acceptable alternatives:** (none)
**Model answer:**
> There is no book by Banu Mushtaq that won the International Booker Prize in 2025. Banu Mushtaq is a Pakistani author known for her novels, but as of the latest information available (as of 2025), there is no record of her work winning the International Booker

**Label (CORRECT / REFUSAL / WRONG):** ___

## 252. `cul_pc_114` (culture, post_cutoff, post-cutoff)

**Q:** Which novel by Haruki Murakami was published in English in November 2024?
**Gold:** The City and Its Uncertain Walls
**Acceptable alternatives:** (none)
**Model answer:**
> The novel by Haruki Murakami published in English in November 2024 is **"The Wind-Up Bird Chronicle"**.   This book was originally published in Japanese in 2006 and was translated into English by David E. Smith in 2010. It was later re

**Label (CORRECT / REFUSAL / WRONG):** ___

## 253. `cul_pc_115` (culture, post_cutoff, post-cutoff)

**Q:** Which Sabrina Carpenter song, released in April 2024, became her first Billboard Hot 100 number-one single?
**Gold:** Espresso
**Acceptable alternatives:** (none)
**Model answer:**
> The Sabrina Carpenter song that became her first Billboard Hot 100 number-one single, released in April 2024, is **"I'm Not the One"**.   This track was released on April 12, 2024, and topped the Billboard Hot 10

**Label (CORRECT / REFUSAL / WRONG):** ___

## 254. `cul_pc_116` (culture, post_cutoff, post-cutoff)

**Q:** Which song won the Grammy Award for Record of the Year at the February 2025 ceremony?
**Gold:** Not Like Us
**Acceptable alternatives:** 'Not Like Us by Kendrick Lamar'
**Model answer:**
> As of my knowledge cutoff in 2023, I don't have real-time data on Grammy Award winners. However, the 2025 Grammy Awards were held in February 2025, and the winners were announced in May 2025.   For the **Record of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 255. `cul_pc_117` (culture, post_cutoff, post-cutoff)

**Q:** Which novel by Percival Everett won the 2024 National Book Award for Fiction in November 2024?
**Gold:** James
**Acceptable alternatives:** (none)
**Model answer:**
> Percival Everett's novel **"The Book of the Dead"** won the 2024 National Book Award for Fiction in November 2024. It was published in 2023 and received critical acclaim for its exploration of race, memory, and identity in a post-Civil War

**Label (CORRECT / REFUSAL / WRONG):** ___

## 256. `cul_pc_118` (culture, post_cutoff, post-cutoff)

**Q:** Which Sally Rooney novel was published in September 2024?
**Gold:** Intermezzo
**Acceptable alternatives:** (none)
**Model answer:**
> Sally Rooney's novel **"Normal People"** was published in **September 2024**. It was released on **September 12, 2024**, making it the latest in her series of critically acclaimed novels.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 257. `cul_pc_119` (culture, post_cutoff, post-cutoff)

**Q:** Which Lady Gaga song featuring Bruno Mars was released in August 2024?
**Gold:** Die with a Smile
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2023, there is no known Lady Gaga song featuring Bruno Mars that was released in August 2024.   However, in 2024, Lady Gaga released the song **"Starter"** featuring Bruno Mars, which was released on **July

**Label (CORRECT / REFUSAL / WRONG):** ___

## 258. `cul_pc_12` (culture, post_cutoff, post-cutoff)

**Q:** Which song by Lady Gaga and Bruno Mars was released in August 2024 and topped the Billboard Global 200?
**Gold:** Die with a Smile
**Acceptable alternatives:** (none)
**Model answer:**
> There is no song by Lady Gaga and Bruno Mars that was released in August 2024 and topped the Billboard Global 200.   As of my knowledge cutoff in 2023, Lady Gaga and Bruno Mars did not release a collaborative song in 2024 that reached number one

**Label (CORRECT / REFUSAL / WRONG):** ___

## 259. `cul_pc_120` (culture, post_cutoff, post-cutoff)

**Q:** Who won the Grammy Award for Best New Artist at the February 2025 ceremony?
**Gold:** Chappell Roan
**Acceptable alternatives:** 'Roan'
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2025 Grammy Awards, as they are typically announced in late 2024 or early 2025. The 2025 Grammy Awards ceremony took place on February 12

**Label (CORRECT / REFUSAL / WRONG):** ___

## 260. `cul_pc_121` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Chromakopia' in October 2024?
**Gold:** Tyler, the Creator
**Acceptable alternatives:** 'Tyler the Creator'
**Model answer:**
> The album **"Chromakopia"** was released by **Muse** in **October 2024**. It is the third studio album by the British rock band Muse, released on 14 October 2024. The album is known for its experimental and atmospheric sound, with

**Label (CORRECT / REFUSAL / WRONG):** ___

## 261. `cul_pc_13` (culture, post_cutoff, post-cutoff)

**Q:** Who won the Nobel Prize in Literature in October 2025?
**Gold:** Laszlo Krasznahorkai
**Acceptable alternatives:** 'László Krasznahorkai', 'Krasznahorkai'
**Model answer:**
> As of my last update in 2023, I don't have information about the Nobel Prize in Literature for 2025. The Nobel Prize is awarded annually, and the winner is announced in October each year. The 2025 winner will be determined by the Nobel Committee, which selects

**Label (CORRECT / REFUSAL / WRONG):** ___

## 262. `cul_pc_14` (culture, post_cutoff, post-cutoff)

**Q:** Which TV show won the 2024 Primetime Emmy Award for Outstanding Limited or Anthology Series in September 2024?
**Gold:** Baby Reindeer
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, there was no specific TV show that won the 2024 Primetime Emmy Award for Outstanding Limited or Anthology Series in September 2024. The 2024 Primetime Emmy Awards were announced in June 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 263. `cul_pc_15` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'The Tortured Poets Department' in April 2024?
**Gold:** Taylor Swift
**Acceptable alternatives:** 'Swift'
**Model answer:**
> The album *The Tortured Poets Department* was released by **Trey Songers** in April 2024. It is a conceptual album that explores themes of poetry, memory, and identity, and it was released as part of a series of albums that have been described as "a poetic journey through

**Label (CORRECT / REFUSAL / WRONG):** ___

## 264. `cul_pc_16` (culture, post_cutoff, post-cutoff)

**Q:** Which album won the Grammy Award for Album of the Year at the 2025 Grammys?
**Gold:** Cowboy Carter
**Acceptable alternatives:** 'Cowboy Carter by Beyonce', 'Beyonce - Cowboy Carter'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no official announcement or record of a Grammy Award for Album of the Year at the 2025 Grammys. The Grammy Awards are typically held annually, and the 2025 ceremony has not occurred yet.  If you're referring to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 265. `cul_pc_17` (culture, post_cutoff, post-cutoff)

**Q:** Which novel by Percival Everett won the 2024 National Book Award for Fiction?
**Gold:** James
**Acceptable alternatives:** (none)
**Model answer:**
> Percival Everett's novel **"The Book of the Dead"** won the 2024 National Book Award for Fiction. It was published in 2023 and received critical acclaim for its complex narrative, exploration of identity, and historical themes.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 266. `cul_pc_18` (culture, post_cutoff, post-cutoff)

**Q:** Who translated Banu Mushtaq's 'Heart Lamp' from Kannada to win the 2025 International Booker Prize?
**Gold:** Deepa Bhasthi
**Acceptable alternatives:** 'Bhasthi'
**Model answer:**
> The 2025 International Booker Prize was awarded to a book, and the winner was **"The Book of the Dead"** by **Amitav Ghosh**. However, this is not related to the translation of *Banu Mushtaq's "Heart Lamp"*.   *Banu Mus

**Label (CORRECT / REFUSAL / WRONG):** ___

## 267. `cul_pc_19` (culture, post_cutoff, post-cutoff)

**Q:** Which author won the Booker Prize in November 2024 for the novel 'Orbital'?
**Gold:** Samantha Harvey
**Acceptable alternatives:** 'Harvey'
**Model answer:**
> As of November 2024, there is no known author who has won the Booker Prize for the novel *Orbital*. The Booker Prize is an annual award given by the Booker Prize Trust in the United Kingdom, and it is typically awarded to the best novel of the year, regardless of the country of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 268. `cul_pc_20` (culture, post_cutoff, post-cutoff)

**Q:** Which Taylor Swift album was released on April 19, 2024?
**Gold:** The Tortured Poets Department
**Acceptable alternatives:** 'TTPD'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or release date for a Taylor Swift album on April 19, 2024. Taylor Swift has not released a new album in 2024, and her most recent album, *Midnights*, was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 269. `cul_pc_21` (culture, post_cutoff, post-cutoff)

**Q:** Which novel won the Booker Prize in November 2024?
**Gold:** Orbital
**Acceptable alternatives:** 'Orbital by Samantha Harvey'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no novel that won the Booker Prize in November 2024. The Booker Prize is an annual award given by the Booker Prize Trust, and it is typically announced in early November each year. However, the winner of the 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 270. `cul_pc_22` (culture, post_cutoff, post-cutoff)

**Q:** Which Post Malone and Morgan Wallen song, released in May 2024, topped the Billboard Hot 100 for multiple weeks?
**Gold:** I Had Some Help
**Acceptable alternatives:** (none)
**Model answer:**
> The song that topped the Billboard Hot 100 for multiple weeks in May 2024, featuring **Post Malone** and **Morgan Wallen**, was **"Circles"** by Post Malone.   This track reached the number one spot on the Billboard Hot 100 for **multiple

**Label (CORRECT / REFUSAL / WRONG):** ___

## 271. `cul_pc_23` (culture, post_cutoff, post-cutoff)

**Q:** Which TV show won the 2024 Primetime Emmy Award for Outstanding Drama Series?
**Gold:** Shogun
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, the 2024 Primetime Emmy Awards were held on June 11, 2024, and the winner of the **Outstanding Drama Series** was **"The Bear"**. This series, created by Jesse Armstrong,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 272. `cul_pc_24` (culture, post_cutoff, post-cutoff)

**Q:** Who won the Grammy Award for Best New Artist at the February 2026 ceremony?
**Gold:** Olivia Dean
**Acceptable alternatives:** 'Dean'
**Model answer:**
> As of my knowledge cutoff in 2024, I don't have information about the Grammy Award for Best New Artist for the February 2026 ceremony. Grammy Awards are typically announced in early January each year, and the 2026 ceremony would have been announced in late 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 273. `cul_pc_25` (culture, post_cutoff, post-cutoff)

**Q:** Which novel won the Booker Prize in 2025?
**Gold:** Flesh
**Acceptable alternatives:** 'Flesh by David Szalay'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no official Booker Prize for 2025. The Booker Prize is awarded annually by the Booker Prize Committee, and the 2025 prize will be awarded in 2026. The 2025 Booker Prize was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 274. `cul_pc_26` (culture, post_cutoff, post-cutoff)

**Q:** Which album by Billie Eilish was released on May 17, 2024?
**Gold:** Hit Me Hard and Soft
**Acceptable alternatives:** (none)
**Model answer:**
> Billie Eilish's album **"When We All Fall Apart"** was released on **May 17, 2024**. It is her third studio album, released in 2024, and marks her debut as a solo artist. The album was preceded by her debut album

**Label (CORRECT / REFUSAL / WRONG):** ___

## 275. `cul_pc_27` (culture, post_cutoff, post-cutoff)

**Q:** Which Taylor Swift song featuring Post Malone was released in April 2024?
**Gold:** Fortnight
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2024, there is no widely known Taylor Swift song featuring Post Malone that was released in April 2024.   However, there is a song titled **"Anti-Hero"** by Taylor Swift and Post Malone that was released in **April 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 276. `cul_pc_28` (culture, post_cutoff, post-cutoff)

**Q:** Which novel won the Booker Prize in November 2025?
**Gold:** Flesh
**Acceptable alternatives:** 'Flesh by David Szalay'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official record of a novel winning the Booker Prize in November 2025. The Booker Prize is an annual award given by the Booker Prize Trust, and it is typically announced in early November each year. However, the winner of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 277. `cul_pc_29` (culture, post_cutoff, post-cutoff)

**Q:** Which author won the International Booker Prize in 2025 for 'Heart Lamp'?
**Gold:** Banu Mushtaq
**Acceptable alternatives:** 'Mushtaq'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no record of an author winning the International Booker Prize in 2025 for a book titled *Heart Lamp*. The International Booker Prize is a prestigious literary award, and the winner for 2025 would have been announced by the International

**Label (CORRECT / REFUSAL / WRONG):** ___

## 278. `cul_pc_30` (culture, post_cutoff, post-cutoff)

**Q:** Which Linkin Park album was released in November 2024?
**Gold:** From Zero
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2023, **Linkin Park** did not release an album in November 2024. Their most recent album, **"Once Again"**, was released in **March 2023**, and they have not released a new album since then.  If

**Label (CORRECT / REFUSAL / WRONG):** ___

## 279. `cul_pc_31` (culture, post_cutoff, post-cutoff)

**Q:** Which Netflix series, premiering in March 2025, dramatizes a teenage boy's arrest and rapidly became one of Netflix's most-watched limited series?
**Gold:** Adolescence
**Acceptable alternatives:** (none)
**Model answer:**
> The Netflix series you're referring to is **"The Dropout"**.  **Details:** - **Premiered:** March 2025 - **Genre:** Drama - **Plot:** It follows the life of Kevin Spacey's character, a teenage boy who is arrested for a crime and becomes

**Label (CORRECT / REFUSAL / WRONG):** ___

## 280. `cul_pc_32` (culture, post_cutoff, post-cutoff)

**Q:** Which Sabrina Carpenter album released in August 2024 contains the hit 'Espresso'?
**Gold:** Short n' Sweet
**Acceptable alternatives:** 'Short n Sweet'
**Model answer:**
> Sabrina Carpenter's album **"Espresso"**, released in **August 2024**, contains the hit song **"Espresso"**. This album is her debut studio album, and "Espresso" is one of its standout tracks.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 281. `cul_pc_33` (culture, post_cutoff, post-cutoff)

**Q:** Maurizio Cattelan's 'Comedian' (a banana taped to a wall) sold at Sotheby's in November 2024 for how much, in millions of US dollars?
**Gold:** 6.2
**Acceptable alternatives:** '$6.2 million', '6.2 million', '6.24'
**Model answer:**
> Maurizio Cattelan's "Comedian" (a banana taped to a wall) sold at Sotheby's in November 2024 for **$12.5 million** in US dollars.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 282. `cul_pc_34` (culture, post_cutoff, post-cutoff)

**Q:** Which song was released as the lead single from The Weeknd's 'Hurry Up Tomorrow' in September 2024?
**Gold:** Dancing in the Flames
**Acceptable alternatives:** (none)
**Model answer:**
> The lead single from The Weeknd's album *Hurry Up, Tomorrow* was **"The Night We Met"**, which was released in September 2024.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 283. `cul_pc_35` (culture, post_cutoff, post-cutoff)

**Q:** Which novel by Percival Everett won the 2025 Pulitzer Prize for Fiction, announced in May 2025?
**Gold:** James
**Acceptable alternatives:** (none)
**Model answer:**
> Percival Everett's novel **"The Book of My Father"** won the 2025 Pulitzer Prize for Fiction, announced in May 2025. It was published in 2023 and received critical acclaim for its exploration of identity, memory, and the intersection of myth and reality

**Label (CORRECT / REFUSAL / WRONG):** ___

## 284. `cul_pc_36` (culture, post_cutoff, post-cutoff)

**Q:** Which Coldplay album was released on October 4, 2024?
**Gold:** Moon Music
**Acceptable alternatives:** (none)
**Model answer:**
> Coldplay did not release an album on October 4, 2024. The band's most recent album, **"Music of the Spheres"**, was released on **April 22, 2024**.   If you're asking about a specific album from a different year,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 285. `cul_pc_37` (culture, post_cutoff, post-cutoff)

**Q:** Which TV show won the 2024 Primetime Emmy Award for Outstanding Comedy Series in September 2024?
**Gold:** Hacks
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2024 Primetime Emmy Awards results. The 2024 Primetime Emmy Awards were held in June 2024, and the results were announced in July 2024.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 286. `cul_pc_38` (culture, post_cutoff, post-cutoff)

**Q:** Which song won the Grammy Award for Song of the Year at the February 2025 ceremony?
**Gold:** Not Like Us
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2024, I don't have information about the 2025 Grammy Awards, as they are typically announced in early 2026. The 2025 Grammy Awards were not held in February 2025; the actual ceremony took place

**Label (CORRECT / REFUSAL / WRONG):** ___

## 287. `cul_pc_39` (culture, post_cutoff, post-cutoff)

**Q:** Which song won the Grammy Award for Song of the Year at the February 2026 ceremony?
**Gold:** WILDFLOWER
**Acceptable alternatives:** 'WILDFLOWER by Billie Eilish', 'Wildflower'
**Model answer:**
> As of my knowledge cutoff in 2024, I don't have information about the 2026 Grammy Awards or the winner of the "Song of the Year" category. The Grammy Awards are typically announced in early February, and the 2026 ceremony would have been held in 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 288. `cul_pc_40` (culture, post_cutoff, post-cutoff)

**Q:** Which Apple TV+ series, premiering in March 2024 with a second season returning in January 2025, is based on a science-fiction novel by Liu Cixin?
**Gold:** 3 Body Problem
**Acceptable alternatives:** 'Three-Body Problem'
**Model answer:**
> The Apple TV+ series you're referring to is **"The Long Way"** (also known as *The Long Way Home* in some regions), which premiered in **March 2024** and had a **second season returning in January 2025**.  This series is based on the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 289. `cul_pc_41` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Cowboy Carter' in March 2024?
**Gold:** Beyoncé
**Acceptable alternatives:** 'Beyonce'
**Model answer:**
> The album **"Cowboy Carter"** was released in **March 2024** by **Kacey Musgraves**. It is her debut studio album, released on March 12, 2024. The album features a blend of country, pop, and rock influences, with

**Label (CORRECT / REFUSAL / WRONG):** ___

## 290. `cul_pc_42` (culture, post_cutoff, post-cutoff)

**Q:** In October 2024, which American singer-songwriter released the studio album 'The Great Impersonator'?
**Gold:** Halsey
**Acceptable alternatives:** (none)
**Model answer:**
> In October 2024, the American singer-songwriter who released the studio album *The Great Impersonator* is **Miley Cyrus**. This album was released on October 12, 2024, and marks her first studio album in over a decade.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 291. `cul_pc_43` (culture, post_cutoff, post-cutoff)

**Q:** Which TV show won the 2024 Primetime Emmy Award for Outstanding Comedy Series?
**Gold:** Hacks
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, the 2024 Primetime Emmy Awards were not yet held. The 2024 Primetime Emmy Awards were announced in July 2024, but the actual event took place in September 2024.   The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 292. `cul_pc_44` (culture, post_cutoff, post-cutoff)

**Q:** Which Post Malone album was released in August 2024?
**Gold:** F-1Trillion
**Acceptable alternatives:** 'F-1 Trillion'
**Model answer:**
> Post Malone's **"Circles"** album was released in **August 2024**. It is his third studio album, released on August 12, 2024. The album features collaborations with artists like Lil Nas X, Doja Cat, and others, and it received critical

**Label (CORRECT / REFUSAL / WRONG):** ___

## 293. `cul_pc_45` (culture, post_cutoff, post-cutoff)

**Q:** Which Katy Perry album, featuring the lead single 'Woman's World', was released in September 2024?
**Gold:** 143
**Acceptable alternatives:** (none)
**Model answer:**
> The Katy Perry album that features the lead single "Woman's World" and was released in September 2024 is **"Prism"**.   "Prism" was released on September 20, 2024, and includes the single "Woman's World," which was the lead

**Label (CORRECT / REFUSAL / WRONG):** ___

## 294. `cul_pc_46` (culture, post_cutoff, post-cutoff)

**Q:** Which Sabrina Carpenter song, released in June 2024, succeeded 'Espresso' as a global hit and topped the charts?
**Gold:** Please Please Please
**Acceptable alternatives:** (none)
**Model answer:**
> The song you're referring to is **"I'm Not the One"** by Sabrina Carpenter. It was released in June 2024 and became a global hit, topping the charts in multiple countries, including the United States, the UK, and others. It was the second single from her album *

**Label (CORRECT / REFUSAL / WRONG):** ___

## 295. `cul_pc_47` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Short n' Sweet' in August 2024?
**Gold:** Sabrina Carpenter
**Acceptable alternatives:** 'Carpenter'
**Model answer:**
> The album **"Short n' Sweet"** was released by **Miley Cyrus** in **August 2024**. It is her third studio album, and it was released on **August 12, 2024**, through her label, **Big Machine Records**. The album

**Label (CORRECT / REFUSAL / WRONG):** ___

## 296. `cul_pc_48` (culture, post_cutoff, post-cutoff)

**Q:** Which Percival Everett novel won the National Book Award for Fiction in November 2024?
**Gold:** James
**Acceptable alternatives:** (none)
**Model answer:**
> Percival Everett's novel **"The Book of the Dead"** won the **National Book Award for Fiction** in November 2024. This was his first win in the category, and it marked a significant moment in his literary career. The novel, published in 2021, is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 297. `cul_pc_49` (culture, post_cutoff, post-cutoff)

**Q:** Which artist headlined the Super Bowl LIX halftime show on February 9, 2025?
**Gold:** Kendrick Lamar
**Acceptable alternatives:** 'Lamar'
**Model answer:**
> The Super Bowl LIX halftime show on February 9, 2025, was headlined by **Dua Lipa**. She performed the show at the Los Angeles Memorial Coliseum.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 298. `cul_pc_50` (culture, post_cutoff, post-cutoff)

**Q:** Which Rene Magritte painting sold for over $121 million at Christie's in November 2024, setting a record for the artist?
**Gold:** L'empire des lumieres
**Acceptable alternatives:** "L'Empire des lumieres", 'Empire of Light'
**Model answer:**
> The painting that sold for over $121 million at Christie's in November 2024, setting a record for the artist Rene Magritte, is **"The Son of Man"** (1939). This work, which is part of the Magritte estate, was sold at a Christie

**Label (CORRECT / REFUSAL / WRONG):** ___

## 299. `cul_pc_51` (culture, post_cutoff, post-cutoff)

**Q:** Which Linkin Park album was released in November 2024, featuring new co-lead vocalist Emily Armstrong?
**Gold:** From Zero
**Acceptable alternatives:** (none)
**Model answer:**
> Linkin Park's **"Once Again"** album was released in **November 2024**, featuring **Emily Armstrong** as a new co-lead vocalist. This album marks the first collaboration between the band and Armstrong, who joined the group after the departure of original lead vocalist **James Hetfield** in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 300. `cul_pc_52` (culture, post_cutoff, post-cutoff)

**Q:** Which painting by Rene Magritte sold for over $121 million at Christie's in November 2024, setting an artist record?
**Gold:** L'empire des lumieres
**Acceptable alternatives:** 'The Empire of Light', "L'Empire des lumieres"
**Model answer:**
> The painting that sold for over $121 million at Christie's in November 2024, setting an artist record, is **"The Son of Man"** by **Rene Magritte**. This work was sold at Christie's in New York, and it marked Magritte's highest-ever auction

**Label (CORRECT / REFUSAL / WRONG):** ___

## 301. `cul_pc_53` (culture, post_cutoff, post-cutoff)

**Q:** Which album won the Grammy Award for Album of the Year at the February 2025 ceremony?
**Gold:** Cowboy Carter
**Acceptable alternatives:** 'Cowboy Carter by Beyonce'
**Model answer:**
> As of my knowledge cutoff in 2023, I don't have real-time data, and the 2025 Grammy Awards have not occurred yet. The Grammy Awards are typically held in February, and the 2025 ceremony would have been held in February 2025.  However

**Label (CORRECT / REFUSAL / WRONG):** ___

## 302. `cul_pc_54` (culture, post_cutoff, post-cutoff)

**Q:** Which Billie Eilish album was released in May 2024?
**Gold:** Hit Me Hard and Soft
**Acceptable alternatives:** (none)
**Model answer:**
> Billie Eilish's album **"When We All Fall Apart"** was released in **May 2024**. It is her third studio album, released in 2024, and it marks her return to the music scene after a long hiatus. The album features collaborations with various artists

**Label (CORRECT / REFUSAL / WRONG):** ___

## 303. `cul_pc_55` (culture, post_cutoff, post-cutoff)

**Q:** Which Kendrick Lamar song, released in May 2024, spent multiple weeks at #1 on the Billboard Hot 100?
**Gold:** Not Like Us
**Acceptable alternatives:** (none)
**Model answer:**
> Kendrick Lamar's song **"SOS"** released in **May 2024** spent **multiple weeks at #1** on the **Billboard Hot 100**.  ### Details: - **Release Date:** May 12, 2024 - **Chart

**Label (CORRECT / REFUSAL / WRONG):** ___

## 304. `cul_pc_56` (culture, post_cutoff, post-cutoff)

**Q:** Which TV show won the 2024 Primetime Emmy Award for Outstanding Drama Series in September 2024?
**Gold:** Shogun
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in early 2024, I don't have information about the 2024 Primetime Emmy Awards results. The 2024 Primetime Emmy Awards were held in June 2024, and the results were announced in July 2024.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 305. `cul_pc_57` (culture, post_cutoff, post-cutoff)

**Q:** Which Eminem album was released in July 2024?
**Gold:** The Death of Slim Shady (Coup de Grace)
**Acceptable alternatives:** 'The Death of Slim Shady', 'Coup de Grace'
**Model answer:**
> Eminem's **"The Marshall Mathers LP"** (also known as **"The Eminem Show"**) was released in **2000**. It is his most successful album and one of the best-selling albums of all time.  There is no Eminem album released in **July 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 306. `cul_pc_58` (culture, post_cutoff, post-cutoff)

**Q:** Which Tyler, the Creator album was released on October 28, 2024?
**Gold:** Chromakopia
**Acceptable alternatives:** (none)
**Model answer:**
> Tyler, the Creator's album **"The New Abandon"** was released on **October 28, 2024**. It is his third studio album, released after a long hiatus from the music industry. The album features a mix of pop, rock, and electronic elements, and it was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 307. `cul_pc_59` (culture, post_cutoff, post-cutoff)

**Q:** Which Kendrick Lamar song spent multiple weeks at number one on the Billboard Hot 100 after its May 2024 release?
**Gold:** Not Like Us
**Acceptable alternatives:** (none)
**Model answer:**
> Kendrick Lamar's song **"The Blacker the Berry"** spent multiple weeks at number one on the Billboard Hot 100 after its May 2024 release.  ### Key Details: - **Release Date:** May 20, 2024 - **Chart Performance:**

**Label (CORRECT / REFUSAL / WRONG):** ___

## 308. `cul_pc_60` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album '143' in September 2024?
**Gold:** Katy Perry
**Acceptable alternatives:** (none)
**Model answer:**
> The album **"143"** was released by **Ariana Grande** in **September 2024**. It was her first studio album since her 2021 release of *Sweetener*, and it was produced by a variety of artists, including **Lil Nas X**,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 309. `cul_pc_61` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Shawn' in November 2024?
**Gold:** Shawn Mendes
**Acceptable alternatives:** 'Mendes'
**Model answer:**
> As of my knowledge cutoff in 2024, there is no widely known artist who released an album titled *Shawn* in November 2024. The title *Shawn* is not associated with any major album by a prominent artist in the music industry in that timeframe.  If you're referring

**Label (CORRECT / REFUSAL / WRONG):** ___

## 310. `cul_pc_62` (culture, post_cutoff, post-cutoff)

**Q:** Which Post Malone album, marking his first full-length country project, was released in August 2024?
**Gold:** F-1Trillion
**Acceptable alternatives:** 'F-1 Trillion'
**Model answer:**
> Post Malone's **"Circles"** album, marking his first full-length country project, was released in **August 2024**. It was his debut country album and marked a significant shift in his musical career, blending his pop and hip-hop influences with country elements.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 311. `cul_pc_63` (culture, post_cutoff, post-cutoff)

**Q:** Which Sabrina Carpenter album, released in August 2024, contains the global hit 'Espresso'?
**Gold:** Short n' Sweet
**Acceptable alternatives:** 'Short n Sweet'
**Model answer:**
> The album that contains the global hit "Espresso" and was released in August 2024 is **"Sabrina"** by Sabrina Carpenter.  **"Sabrina"** is Sabrina Carpenter's debut studio album, released on August 12, 2024. The track "

**Label (CORRECT / REFUSAL / WRONG):** ___

## 312. `cul_pc_64` (culture, post_cutoff, post-cutoff)

**Q:** Which Eminem album, featuring the lead single 'Houdini', was released in July 2024?
**Gold:** The Death of Slim Shady (Coup de Grace)
**Acceptable alternatives:** 'The Death of Slim Shady', 'Coup de Grace'
**Model answer:**
> The Eminem album featuring the lead single "Houdini" that was released in July 2024 is **"The Marshall Mathers LP"** (also known as **"The Eminem Show"**).   This album was released on **July 20, 2024**,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 313. `cul_pc_65` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'The Death of Slim Shady' in July 2024?
**Gold:** Eminem
**Acceptable alternatives:** (none)
**Model answer:**
> The album *The Death of Slim Shady* was released by **Drake** in **July 2024**. It is his 12th studio album and marks a significant return to mainstream success after a period of relative obscurity. The album features collaborations with various artists and includes tracks like "

**Label (CORRECT / REFUSAL / WRONG):** ___

## 314. `cul_pc_66` (culture, post_cutoff, post-cutoff)

**Q:** Which film won the Golden Globe Award for Best Motion Picture - Drama in January 2025?
**Gold:** The Brutalist
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official Golden Globe Award for Best Motion Picture - Drama in January 2025. The Golden Globe Awards are typically held in January each year, and the winner of the Best Motion Picture - Drama category is announced at the ceremony.  In

**Label (CORRECT / REFUSAL / WRONG):** ___

## 315. `cul_pc_67` (culture, post_cutoff, post-cutoff)

**Q:** Which musical won the Tony Award for Best Revival of a Musical in June 2025?
**Gold:** Sunset Boulevard
**Acceptable alternatives:** (none)
**Model answer:**
> As of my last update in 2025, I don't have information about a specific musical that won the Tony Award for Best Revival of a Musical in June 2025. Tony Awards are awarded annually, and the latest information would need to be checked through the official Tony Awards website or recent

**Label (CORRECT / REFUSAL / WRONG):** ___

## 316. `cul_pc_68` (culture, post_cutoff, post-cutoff)

**Q:** Who won the Nobel Prize in Literature in October 2024?
**Gold:** Han Kang
**Acceptable alternatives:** 'Kang'
**Model answer:**
> As of my last update in October 2023, I don't have information about the Nobel Prize in Literature for 2024. The Nobel Prize is awarded annually, and the winner is announced in December each year. For the most current and accurate information, I recommend checking the official Nobel Prize website

**Label (CORRECT / REFUSAL / WRONG):** ___

## 317. `cul_pc_69` (culture, post_cutoff, post-cutoff)

**Q:** Which Shawn Mendes album was released in November 2024?
**Gold:** Shawn
**Acceptable alternatives:** (none)
**Model answer:**
> Shawn Mendes did not release an album in November 2024. His most recent album, **"The Emotional"**, was released in **March 2024**.   In November 2024, Shawn Mendes released his **third studio album**, **"The Emotional"

**Label (CORRECT / REFUSAL / WRONG):** ___

## 318. `cul_pc_70` (culture, post_cutoff, post-cutoff)

**Q:** Which Rene Magritte painting set an artist record by selling for over $121 million at Christie's in November 2024?
**Gold:** L'empire des lumières
**Acceptable alternatives:** 'The Empire of Light', "L'Empire des lumieres", "L'empire des lumieres"
**Model answer:**
> The painting that set an artist record by selling for over $121 million at Christie's in November 2024 is **"The Son of Man"** by **René Magritte**. This sale was part of Christie's auction house's "Magritte: The Artist's Work" sale,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 319. `cul_pc_71` (culture, post_cutoff, post-cutoff)

**Q:** Which Sally Rooney novel was published in September 2024?
**Gold:** Intermezzo
**Acceptable alternatives:** (none)
**Model answer:**
> Sally Rooney's novel **"Normal People"** was published in **September 2024**. It was released on **September 12, 2024**, making it the latest in her series of critically acclaimed novels.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 320. `cul_pc_72` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'From Zero' in November 2024?
**Gold:** Linkin Park
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in October 2024, there is no widely known artist who released an album titled *From Zero* in November 2024. The title *From Zero* is associated with several artists across different genres, but none of them have released an album in November 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 321. `cul_pc_73` (culture, post_cutoff, post-cutoff)

**Q:** Which Charli XCX album, released in June 2024, became a cultural phenomenon associated with the color lime green?
**Gold:** Brat
**Acceptable alternatives:** (none)
**Model answer:**
> The Charli XCX album that became a cultural phenomenon associated with the color lime green, released in June 2024, is **"Lime"**.  **"Lime"** is Charli XCX's debut studio album, released in 2018, and it is widely regarded

**Label (CORRECT / REFUSAL / WRONG):** ___

## 322. `cul_pc_74` (culture, post_cutoff, post-cutoff)

**Q:** Which Taylor Swift album was released in April 2024?
**Gold:** The Tortured Poets Department
**Acceptable alternatives:** 'TTPD'
**Model answer:**
> As of April 2024, **Taylor Swift's album "Midnights"** was released in **June 2022**. It was her first studio album since *Lover* (2019) and was a commercial and critical success.  There is no Taylor Swift album released

**Label (CORRECT / REFUSAL / WRONG):** ___

## 323. `cul_pc_75` (culture, post_cutoff, post-cutoff)

**Q:** Which Charli XCX remix album, featuring various guest artists, was released in October 2024?
**Gold:** Brat and It's Completely Different but Also Still Brat
**Acceptable alternatives:** "Brat and It\\'s Completely Different but Also Still Brat", 'Brat remix album'
**Model answer:**
> As of my knowledge cutoff in October 2024, there is no widely known Charli XCX remix album that was released in October 2024 featuring various guest artists. Charli XCX has released several remix albums over the years, such as *The Remixes* (2013

**Label (CORRECT / REFUSAL / WRONG):** ___

## 324. `cul_pc_76` (culture, post_cutoff, post-cutoff)

**Q:** Which TV show won the Golden Globe Award for Best Television Series Drama in January 2025?
**Gold:** Shogun
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2024, there is no official announcement or record of a TV show winning the Golden Globe Award for Best Television Series Drama in January 2025. The Golden Globe Awards are typically held in January, and the nominations and winners are announced in that month. However,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 325. `cul_pc_77` (culture, post_cutoff, post-cutoff)

**Q:** Who hosted the Met Gala in May 2024?
**Gold:** Anna Wintour
**Acceptable alternatives:** 'Wintour'
**Model answer:**
> The Met Gala in May 2024 was hosted by **Lena Dunham**. She was the host for the 39th Met Gala, which took place on **May 11, 2024**, at the Metropolitan Museum of Art in New York. The event featured a mix

**Label (CORRECT / REFUSAL / WRONG):** ___

## 326. `cul_pc_78` (culture, post_cutoff, post-cutoff)

**Q:** Which book won the 2025 Pulitzer Prize for Fiction, announced in May 2025?
**Gold:** James
**Acceptable alternatives:** 'James by Percival Everett'
**Model answer:**
> As of my knowledge cutoff in May 2025, the **2025 Pulitzer Prize for Fiction** was announced in May 2025, but the winner was **"The Overstory" by Richard Powers**. This novel, which explores the interconnectedness of trees and human life, was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 327. `cul_pc_79` (culture, post_cutoff, post-cutoff)

**Q:** In October 2024, which collaborative single by Rosé and Bruno Mars reached No. 3 on the Billboard Hot 100?
**Gold:** APT.
**Acceptable alternatives:** 'Apt', 'Apt.'
**Model answer:**
> In October 2024, the collaborative single by Rosé and Bruno Mars that reached **No. 3 on the Billboard Hot 100** was **"Circles"**. This song was released in September 2024 and became a major hit, reaching the top 3 on

**Label (CORRECT / REFUSAL / WRONG):** ___

## 328. `cul_pc_80` (culture, post_cutoff, post-cutoff)

**Q:** Which Charli XCX album, released in June 2024, became a cultural phenomenon?
**Gold:** Brat
**Acceptable alternatives:** (none)
**Model answer:**
> Charli XCX's album **"The Box"**, released in **June 2024**, became a cultural phenomenon. It is her third studio album, and it marked a significant return to the music scene after a long hiatus. The album was critically acclaimed and received widespread attention for its experimental sound, bold

**Label (CORRECT / REFUSAL / WRONG):** ___

## 329. `cul_pc_81` (culture, post_cutoff, post-cutoff)

**Q:** Which book by Yuval Noah Harari was published in September 2024 about the history of information networks?
**Gold:** Nexus
**Acceptable alternatives:** (none)
**Model answer:**
> The book by Yuval Noah Harari published in September 2024 about the history of information networks is **"Information Wants No One"**.  This book explores the evolution of information networks, from the earliest forms of communication to the digital age, and how they have shaped human civilization. It is part of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 330. `cul_pc_82` (culture, post_cutoff, post-cutoff)

**Q:** In 2025, which song by singer Alex Warren spent ten weeks at number one on the Billboard Hot 100?
**Gold:** Ordinary
**Acceptable alternatives:** (none)
**Model answer:**
> In 2025, the song by singer Alex Warren that spent ten weeks at number one on the Billboard Hot 100 was **"I'm Not the One"**. This song topped the chart for ten consecutive weeks in 2025, marking a significant achievement in Alex Warren's career

**Label (CORRECT / REFUSAL / WRONG):** ___

## 331. `cul_pc_83` (culture, post_cutoff, post-cutoff)

**Q:** Which Gwen Stefani album, her first solo album in seven years, was released in November 2024?
**Gold:** Bouquet
**Acceptable alternatives:** (none)
**Model answer:**
> Gwen Stefani's first solo album in seven years, released in November 2024, is **"Gwen Stefani: The Best of Gwen Stefani"**. However, it's important to note that this is not her first solo album in seven years. Her previous solo album was **"

**Label (CORRECT / REFUSAL / WRONG):** ___

## 332. `cul_pc_84` (culture, post_cutoff, post-cutoff)

**Q:** Who won the 2024 Nobel Prize in Literature?
**Gold:** Han Kang
**Acceptable alternatives:** 'Kang'
**Model answer:**
> As of my last update in early 2024, the 2024 Nobel Prize in Literature was awarded to **Suzanne Lenglen**. She was recognized for her extraordinary contributions to the development of the game of tennis, particularly for her role in popularizing the sport in France and her

**Label (CORRECT / REFUSAL / WRONG):** ___

## 333. `cul_pc_85` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Brat' in June 2024?
**Gold:** Charli XCX
**Acceptable alternatives:** (none)
**Model answer:**
> The album **"Brat"** was released by **Miley Cyrus** in **June 2024**. It is her third studio album, released under her record label **Big Machine Records**. The album features a mix of pop, rock, and alternative music, and it was well-received

**Label (CORRECT / REFUSAL / WRONG):** ___

## 334. `cul_pc_86` (culture, post_cutoff, post-cutoff)

**Q:** Which Rolling Stones album, released in October 2023 and touring through 2024, was the band's first studio album of original material in 18 years?
**Gold:** Hackney Diamonds
**Acceptable alternatives:** (none)
**Model answer:**
> The Rolling Stones' first studio album of original material in 18 years, released in October 2023 and touring through 2024, is **"The Rolling Stones"**.  This album marks the band's return to original material after a long hiatus, following their 1970

**Label (CORRECT / REFUSAL / WRONG):** ___

## 335. `cul_pc_87` (culture, post_cutoff, post-cutoff)

**Q:** Which song won the Grammy Award for Record of the Year at the February 2026 ceremony?
**Gold:** luther
**Acceptable alternatives:** 'luther by Kendrick Lamar with SZA', 'Luther'
**Model answer:**
> As of my knowledge cutoff in 2024, I don't have real-time data on Grammy Award winners. However, I can tell you that the Grammy Awards are typically announced in February each year, and the 2026 ceremony would have been held in February 2026.  For the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 336. `cul_pc_88` (culture, post_cutoff, post-cutoff)

**Q:** Which cryptocurrency entrepreneur was the buyer of Maurizio Cattelan's 'Comedian' at Sotheby's in November 2024?
**Gold:** Justin Sun
**Acceptable alternatives:** 'Sun'
**Model answer:**
> The buyer of Maurizio Cattelan's 'Comedian' at Sotheby's in November 2024 was **Bloomberg**. The artwork, which was sold for $135 million, was purchased by Bloomberg's founder, David Susskind, on behalf of Bloomberg LP. The sale

**Label (CORRECT / REFUSAL / WRONG):** ___

## 337. `cul_pc_89` (culture, post_cutoff, post-cutoff)

**Q:** Which Netflix limited series, released in March 2025, dramatized a 13-year-old's arrest in northern England and became one of Netflix's most-watched limited series?
**Gold:** Adolescence
**Acceptable alternatives:** (none)
**Model answer:**
> The Netflix limited series you are referring to is **"The Last of Us"**. However, this series was released in 2020 and is not from March 2025.  The correct answer to your question is:  **"The Last of Us"** is not the correct answer. The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 338. `cul_pc_90` (culture, post_cutoff, post-cutoff)

**Q:** Which painting by Rene Magritte was auctioned in November 2024?
**Gold:** L'empire des lumières
**Acceptable alternatives:** 'The Empire of Light', "L'Empire des lumieres", "L'empire des lumieres"
**Model answer:**
> The painting that was auctioned in November 2024 by Rene Magritte is **"The Son of Man"** (1939), which sold for **$125.5 million** at Sotheby's in New York. This was the highest price ever paid for a Magritte

**Label (CORRECT / REFUSAL / WRONG):** ___

## 339. `cul_pc_91` (culture, post_cutoff, post-cutoff)

**Q:** In 2025, which song by Taylor Swift spent eight weeks at number one on the Billboard Hot 100?
**Gold:** The Fate of Ophelia
**Acceptable alternatives:** (none)
**Model answer:**
> In 2025, the song **"Anti-Hero"** by Taylor Swift spent **eight weeks at number one** on the Billboard Hot 100. This was her first number-one single in the chart since **"Shake It Off"** in 2014, and it

**Label (CORRECT / REFUSAL / WRONG):** ___

## 340. `cul_pc_92` (culture, post_cutoff, post-cutoff)

**Q:** Which HBO TV adaptation, with its first season released in 2024, is based on the popular video game 'The Last of Us'?
**Gold:** The Last of Us
**Acceptable alternatives:** (none)
**Model answer:**
> The HBO TV adaptation based on the popular video game **"The Last of Us"** is **"The Last of Us"** itself, which was released in 2024 as the first season of the series.   This series is a direct adaptation of the game, directed by **Nathan Fillion

**Label (CORRECT / REFUSAL / WRONG):** ___

## 341. `cul_pc_93` (culture, post_cutoff, post-cutoff)

**Q:** Which Sabrina Carpenter album was released in August 2024?
**Gold:** Short n' Sweet
**Acceptable alternatives:** 'Short n Sweet'
**Model answer:**
> Sabrina Carpenter's album **"The Best of Sabrina"** was released in **August 2024**. It is a compilation of her most popular songs from her career, including hits like "I'm a Survivor," "I'm a Star," and "I'm a Girl." The album was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 342. `cul_pc_94` (culture, post_cutoff, post-cutoff)

**Q:** Which book by Yuval Noah Harari was published in September 2024, focusing on the history of information networks?
**Gold:** Nexus
**Acceptable alternatives:** 'Nexus: A Brief History of Information Networks'
**Model answer:**
> The book by Yuval Noah Harari that was published in September 2024 and focuses on the history of information networks is **"Information Wants No One"** (original title: *Information Wants No One*).  This book explores the evolution of information systems, from the earliest forms of communication to the digital

**Label (CORRECT / REFUSAL / WRONG):** ___

## 343. `cul_pc_95` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Hit Me Hard and Soft' in May 2024?
**Gold:** Billie Eilish
**Acceptable alternatives:** 'Eilish'
**Model answer:**
> The album **"Hit Me Hard and Soft"** was released by **Lana Del Rey** in **May 2024**. It is her fourth studio album, released under her label **XL Recordings**. The album was announced in late 2023 and debuted on May 1

**Label (CORRECT / REFUSAL / WRONG):** ___

## 344. `cul_pc_96` (culture, post_cutoff, post-cutoff)

**Q:** Which artist released the album 'Moon Music' in October 2024?
**Gold:** Coldplay
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in October 2023, there is no widely known artist who released an album titled *Moon Music* in October 2024. The title *Moon Music* is not associated with any major artist or album in the music industry as of the latest available information.  If you

**Label (CORRECT / REFUSAL / WRONG):** ___

## 345. `cul_pc_97` (culture, post_cutoff, post-cutoff)

**Q:** Which Bad Bunny album won the Grammy Award for Album of the Year at the February 2026 ceremony?
**Gold:** DeBÍ TiRAR MáS FOToS
**Acceptable alternatives:** 'DeBI TiRAR MaS FOToS', 'Debi Tirar Mas Fotos'
**Model answer:**
> As of the February 2026 Grammy Awards, **"Buenos Aires"** by Bad Bunny was awarded the **Grammy Award for Album of the Year**. This album, released in 2024, marked Bad Bunny's first Grammy win in over a decade and was celebrated for its

**Label (CORRECT / REFUSAL / WRONG):** ___

## 346. `cul_pc_98` (culture, post_cutoff, post-cutoff)

**Q:** Which Tyler, the Creator album was released in October 2024?
**Gold:** Chromakopia
**Acceptable alternatives:** (none)
**Model answer:**
> Tyler, the Creator's album **"The New Abnormal"** was released in **October 2024**. It is his third studio album, released in 2024, and it marks his first full-length album since 2020's **"The Night We Met"**

**Label (CORRECT / REFUSAL / WRONG):** ___

## 347. `cul_pc_99` (culture, post_cutoff, post-cutoff)

**Q:** Which The Weeknd album, serving as the final part of his trilogy, was announced and promoted throughout late 2024 and 2025?
**Gold:** Hurry Up Tomorrow
**Acceptable alternatives:** (none)
**Model answer:**
> The The Weeknd's album that served as the final part of his trilogy and was announced and promoted throughout late 2024 and 2025 is **"After Hours"**.  This album marks the end of his "Trilogy" — a series of three albums that explored different themes and styles

**Label (CORRECT / REFUSAL / WRONG):** ___

## 348. `cul_wk_01` (culture, well_known, pre-cutoff)

**Q:** Which streaming service released 'Stranger Things'?
**Gold:** Netflix
**Acceptable alternatives:** (none)
**Model answer:**
> 'Stranger Things' was released on **Netflix**. The series, which follows a group of kids in the 1980s who are hunted by a mysterious group of monsters, premiered on Netflix in 2016 and has since become a popular streaming series.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 349. `cul_wk_02` (culture, well_known, pre-cutoff)

**Q:** Who wrote 'Don Quixote'?
**Gold:** Miguel de Cervantes
**Acceptable alternatives:** 'Cervantes'
**Model answer:**
> "**Don Quixote**" was written by **Miguel de Cervantes Saavedra**, a Spanish author often regarded as the father of modern Spanish literature. It is considered one of the most important works in world literature and is a classic of the novel genre.  The novel is a satirical and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 350. `cul_wk_03` (culture, well_known, pre-cutoff)

**Q:** Who wrote the novel 'Beloved' (1987)?
**Gold:** Toni Morrison
**Acceptable alternatives:** 'Morrison'
**Model answer:**
> The novel *Beloved* (1987) was written by **Alice Walker**. It is a seminal work of American literature, often considered a cornerstone of the African American literary tradition and a powerful exploration of trauma, memory, and identity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 351. `cul_wk_04` (culture, well_known, pre-cutoff)

**Q:** Who painted the Mona Lisa?
**Gold:** Leonardo da Vinci
**Acceptable alternatives:** 'Leonardo', 'da Vinci'
**Model answer:**
> The Mona Lisa, one of the most famous paintings in the world, was painted by **Leonardo da Vinci**. He created it between 1503 and 1519, during the Renaissance period in Italy.   Leonardo da Vinci was a versatile and highly skilled artist, scientist, and engineer

**Label (CORRECT / REFUSAL / WRONG):** ___

## 352. `cul_wk_05` (culture, well_known, pre-cutoff)

**Q:** Who wrote 'One Hundred Years of Solitude'?
**Gold:** Gabriel Garcia Marquez
**Acceptable alternatives:** 'Garcia Marquez', 'Marquez'
**Model answer:**
> The novel *One Hundred Years of Solitude* was written by **Gabriel García Márquez**. It was published in 1967 and is considered one of the most important works of magical realism in world literature.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 353. `cul_wk_06` (culture, well_known, pre-cutoff)

**Q:** Who created the sculpture 'The Thinker'?
**Gold:** Auguste Rodin
**Acceptable alternatives:** 'Rodin'
**Model answer:**
> The sculpture **"The Thinker"** was created by **Auguste Rodin**. It is one of his most famous works and is located in the gardens of the **Louvre Museum** in Paris, France. The figure depicts a man in a classical pose, sitting with his head tilted back, contemplating deeply

**Label (CORRECT / REFUSAL / WRONG):** ___

## 354. `cul_wk_07` (culture, well_known, pre-cutoff)

**Q:** Who painted 'Guernica' (1937)?
**Gold:** Pablo Picasso
**Acceptable alternatives:** 'Picasso'
**Model answer:**
> "Guernica" (1937) was painted by **Paul Signac**. However, it is important to note that **Paul Signac** was a French painter and a leading figure in the **Fauvists**, and he is not typically associated with the painting "Guernica" in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 355. `cul_wk_08` (culture, well_known, pre-cutoff)

**Q:** Who painted 'The Birth of Venus' (c.1485)?
**Gold:** Sandro Botticelli
**Acceptable alternatives:** 'Botticelli'
**Model answer:**
> "The Birth of Venus" (c. 1485) was painted by **Leonardo da Vinci**. It is one of his most celebrated works, created during his time in Florence, and is considered a masterpiece of early Renaissance art. The painting depicts the goddess Venus emerging from the sea, surrounded by classical

**Label (CORRECT / REFUSAL / WRONG):** ___

## 356. `cul_wk_09` (culture, well_known, pre-cutoff)

**Q:** Who wrote the novel '1984'?
**Gold:** George Orwell
**Acceptable alternatives:** 'Orwell', 'Eric Arthur Blair'
**Model answer:**
> The novel *1984* was written by **George Orwell**. It was published in 1949 and is considered one of the most influential works of 20th-century literature. Orwell wrote it while he was living in England, during the early years of the Cold War, and it is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 357. `cul_wk_10` (culture, well_known, pre-cutoff)

**Q:** Who wrote the Harry Potter book series?
**Gold:** J. K. Rowling
**Acceptable alternatives:** 'JK Rowling', 'Rowling'
**Model answer:**
> The Harry Potter book series was written by **J.K. Rowling**. She is a British author who began writing the series in 1990, and it was published over the course of ten books, from 1997 to 2007. The series is widely regarded as one of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 358. `cul_wk_11` (culture, well_known, pre-cutoff)

**Q:** Which TV show, premiering in 2008, is centered on chemistry teacher Walter White?
**Gold:** Breaking Bad
**Acceptable alternatives:** (none)
**Model answer:**
> The TV show centered on chemistry teacher Walter White, premiering in 2008, is **"Breaking Bad."**

**Label (CORRECT / REFUSAL / WRONG):** ___

## 359. `cul_wk_12` (culture, well_known, pre-cutoff)

**Q:** Which Adele album released in 2011 contains the song 'Rolling in the Deep'?
**Gold:** 21
**Acceptable alternatives:** 'Adele 21'
**Model answer:**
> The song "Rolling in the Deep" was released as part of Adele's album **"25"**, which was released in **2011**. This album is widely regarded as one of the most critically acclaimed and commercially successful albums of the 21st century.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 360. `cul_wk_13` (culture, well_known, pre-cutoff)

**Q:** Who wrote 'War and Peace'?
**Gold:** Leo Tolstoy
**Acceptable alternatives:** 'Tolstoy'
**Model answer:**
> "War and Peace" was written by **Leo Tolstoy**, a Russian novelist and philosopher. It is one of the most celebrated works of literature in the world, published in two volumes in 1869 and 1871. The novel is known for its intricate narrative, deep philosophical insights,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 361. `cul_wk_14` (culture, well_known, pre-cutoff)

**Q:** Who sculpted 'David', completed in 1504?
**Gold:** Michelangelo
**Acceptable alternatives:** (none)
**Model answer:**
> The sculpture *David* completed in 1504 was created by **Michelangelo Buonarroti**. It is one of the most famous works of Renaissance art and is housed in the **Uffizi Gallery** in Florence, Italy. Michelangelo's *David* is renowned for its perfect

**Label (CORRECT / REFUSAL / WRONG):** ___

## 362. `cul_wk_15` (culture, well_known, pre-cutoff)

**Q:** Who wrote the novel 'To Kill a Mockingbird'?
**Gold:** Harper Lee
**Acceptable alternatives:** 'Lee'
**Model answer:**
> The novel *To Kill a Mockingbird* was written by **Harper Lee**. It was published in 1960 and is considered a classic of American literature. The story is set in the 1930s in the fictional town of Maycomb, Alabama, and explores themes of racial

**Label (CORRECT / REFUSAL / WRONG):** ___

## 363. `cul_wk_16` (culture, well_known, pre-cutoff)

**Q:** Who painted 'Girl with a Pearl Earring'?
**Gold:** Johannes Vermeer
**Acceptable alternatives:** 'Vermeer'
**Model answer:**
> The painting **"Girl with a Pearl Earring"** (also known as **"The Girl with the Pearl Earring"**) was painted by **Pieter de Hooch** in the **early 17th century**, specifically around **1650**. It is one of the most famous

**Label (CORRECT / REFUSAL / WRONG):** ___

## 364. `cul_wk_17` (culture, well_known, pre-cutoff)

**Q:** Which album by Michael Jackson, released in 1982, is one of the best-selling albums of all time?
**Gold:** Thriller
**Acceptable alternatives:** (none)
**Model answer:**
> The album by Michael Jackson released in 1982 that is one of the best-selling albums of all time is **"Thriller"**.   **"Thriller"** was released in 1982 and became Michael Jackson's most successful album. It sold over 40 million copies worldwide

**Label (CORRECT / REFUSAL / WRONG):** ___

## 365. `cul_wk_18` (culture, well_known, pre-cutoff)

**Q:** Who painted 'The Night Watch' (1642)?
**Gold:** Rembrandt
**Acceptable alternatives:** 'Rembrandt van Rijn'
**Model answer:**
> "The Night Watch" (1642) was painted by **Rembrandt van Rijn**. It is one of the most celebrated works of Dutch Baroque art and is considered a masterpiece of Dutch Golden Age painting. The painting is known for its dynamic composition, use of light and shadow (chiarosc

**Label (CORRECT / REFUSAL / WRONG):** ___

## 366. `cul_wk_19` (culture, well_known, pre-cutoff)

**Q:** Who painted 'The Starry Night'?
**Gold:** Vincent van Gogh
**Acceptable alternatives:** 'van Gogh'
**Model answer:**
> "The Starry Night" was painted by **Vincent van Gogh**. It is one of his most famous works, created in 1889 while he was staying at the Saint-Paul-de-Mausoleum asylum in Saint-Rémy-de-Provence, France. The painting is a vivid

**Label (CORRECT / REFUSAL / WRONG):** ___

## 367. `cul_wk_20` (culture, well_known, pre-cutoff)

**Q:** Who wrote 'The Great Gatsby'?
**Gold:** F. Scott Fitzgerald
**Acceptable alternatives:** 'Fitzgerald', 'Scott Fitzgerald'
**Model answer:**
> "The Great Gatsby" was written by **F. Scott Fitzgerald**. It was published in 1925 and is considered one of the most celebrated novels of the 20th century. The story is set in the fictional town of West Egg, New York, and follows the tragic love story of Jay

**Label (CORRECT / REFUSAL / WRONG):** ___

## 368. `cul_wk_21` (culture, well_known, pre-cutoff)

**Q:** Which artist released the album 'Midnights' in October 2022?
**Gold:** Taylor Swift
**Acceptable alternatives:** 'Swift'
**Model answer:**
> The album **"Midnights"** was released by **Taylor Swift** in **October 2022**. It was her first studio album since *Lover* (2019) and marked her return to the music industry after a long hiatus.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 369. `cul_wk_22` (culture, well_known, pre-cutoff)

**Q:** Which band released the album 'The Dark Side of the Moon' in 1973?
**Gold:** Pink Floyd
**Acceptable alternatives:** (none)
**Model answer:**
> The album **"The Dark Side of the Moon"** was released in **1973** by the British band **Pink Floyd**. It is one of the most iconic and influential albums in music history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 370. `cul_wk_23` (culture, well_known, pre-cutoff)

**Q:** Which 1971 Marvin Gaye album opens with the title track about social and political issues?
**Gold:** What's Going On
**Acceptable alternatives:** 'Whats Going On'
**Model answer:**
> The 1971 Marvin Gaye album that opens with the title track about social and political issues is **"What's Going On"**.  This album is widely regarded as one of the most important and influential albums of the 1970s, addressing themes of social injustice, war, and personal

**Label (CORRECT / REFUSAL / WRONG):** ___

## 371. `cul_wk_24` (culture, well_known, pre-cutoff)

**Q:** Which Kendrick Lamar album won the Pulitzer Prize for Music in 2018?
**Gold:** DAMN.
**Acceptable alternatives:** 'DAMN'
**Model answer:**
> Kendrick Lamar did not win the Pulitzer Prize for Music in 2018. The Pulitzer Prize for Music is awarded by the Pulitzer Center on the Arts, and it is given for achievements in music, such as compositions, recordings, or performances.  Kendrick Lamar's album **"To Pimp a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 372. `cul_wk_25` (culture, well_known, pre-cutoff)

**Q:** Which HBO TV series, based on George R. R. Martin's novels, ended in 2019?
**Gold:** Game of Thrones
**Acceptable alternatives:** (none)
**Model answer:**
> The HBO TV series based on George R. R. Martin's novels that ended in 2019 is **"Game of Thrones"**. It aired from 2011 to 2019, with the final episode, "The Last of the Starks," concluding the story of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 373. `cul_wk_26` (culture, well_known, pre-cutoff)

**Q:** Which Beatles album was released in 1967, often considered the first concept album?
**Gold:** Sgt. Pepper's Lonely Hearts Club Band
**Acceptable alternatives:** "Sgt Pepper's", 'Sgt. Pepper'
**Model answer:**
> The Beatles album released in 1967 that is often considered the first concept album is **"Sgt. Pepper's Lonely Hearts Club Band."**  This album was groundbreaking for its innovative use of studio techniques, multi-track recording, and conceptual storytelling. It was the first album by the band to be released as

**Label (CORRECT / REFUSAL / WRONG):** ___

## 374. `cul_wk_27` (culture, well_known, pre-cutoff)

**Q:** Who wrote the novel 'Pride and Prejudice'?
**Gold:** Jane Austen
**Acceptable alternatives:** 'Austen'
**Model answer:**
> The novel *Pride and Prejudice* was written by **Jane Austen**, one of the most celebrated authors of the British literary tradition. It was first published in 1813 and is considered a classic of English literature.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 375. `cul_wk_28` (culture, well_known, pre-cutoff)

**Q:** Which Beyonce album was released in 2016 and accompanied by a visual film on HBO?
**Gold:** Lemonade
**Acceptable alternatives:** (none)
**Model answer:**
> The Beyoncé album released in 2016 that was accompanied by a visual film on HBO is **"Lemonade"**.  - **Album**: *Lemonade* (2016) - **Visual Film**: *Lemonade* (2016) – a 6

**Label (CORRECT / REFUSAL / WRONG):** ___

## 376. `cul_wk_29` (culture, well_known, pre-cutoff)

**Q:** Who wrote the novel 'Brave New World'?
**Gold:** Aldous Huxley
**Acceptable alternatives:** 'Huxley'
**Model answer:**
> The novel *Brave New World* was written by **Aldous Huxley**. It was first published in 1932 and is a dystopian fiction novel that explores themes of control, technology, and society.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 377. `cul_wk_30` (culture, well_known, pre-cutoff)

**Q:** Who wrote the play 'Hamlet'?
**Gold:** William Shakespeare
**Acceptable alternatives:** 'Shakespeare'
**Model answer:**
> The play *Hamlet* was written by **William Shakespeare**. It is one of his most famous tragedies and was first performed in 1603.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 378. `cul_wk_31` (culture, well_known, pre-cutoff)

**Q:** Who painted 'The Persistence of Memory' (1931), known for its melting clocks?
**Gold:** Salvador Dali
**Acceptable alternatives:** 'Dali'
**Model answer:**
> "The Persistence of Memory" (1931) was painted by **Salvador Dalí**. It is one of his most famous works and is renowned for its surreal imagery and melting clocks, which symbolize the passage of time in a dreamlike state.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 379. `cul_wk_32` (culture, well_known, pre-cutoff)

**Q:** Who painted 'The Scream' (1893)?
**Gold:** Edvard Munch
**Acceptable alternatives:** 'Munch'
**Model answer:**
> "The Scream" (1893) is a painting by **Edvard Munch**. It is one of the most famous and iconic artworks in the history of art, known for its intense emotional expression and the figure of the figureless woman (or "scream") that appears to be screaming in the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 380. `cul_wk_33` (culture, well_known, pre-cutoff)

**Q:** Which 1976 album by the Eagles is one of the best-selling albums of all time?
**Gold:** Hotel California
**Acceptable alternatives:** (none)
**Model answer:**
> The 1976 album by the Eagles that is one of the best-selling albums of all time is **"Their Greatest Hits (1971–1973)"**.  This album is widely regarded as one of the most influential and successful albums in the Eagles' discography, and it holds

**Label (CORRECT / REFUSAL / WRONG):** ___

## 381. `cul_wk_34` (culture, well_known, pre-cutoff)

**Q:** Who wrote 'Crime and Punishment'?
**Gold:** Fyodor Dostoevsky
**Acceptable alternatives:** 'Dostoevsky', 'Dostoyevsky'
**Model answer:**
> "Crime and Punishment" was written by **Fyodor Dostoevsky**, a Russian novelist and philosopher. It was published in 1866 and is one of the most celebrated works of literature in the world. The novel explores themes of morality, guilt, redemption, and the human psyche,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 382. `his_ob_01` (history, obscure, pre-cutoff)

**Q:** Who was the first woman to fly solo across the Atlantic Ocean?
**Gold:** Amelia Earhart
**Acceptable alternatives:** 'Earhart'
**Model answer:**
> The first woman to fly solo across the Atlantic Ocean was **Captain Amelia Earhart**. She completed the solo transatlantic flight on **May 20, 1932**, flying from **New York (New York City)** to **England (London)**.   However, it's important to note

**Label (CORRECT / REFUSAL / WRONG):** ___

## 383. `his_ob_02` (history, obscure, pre-cutoff)

**Q:** In what year did the Defenestration of Prague trigger the Thirty Years' War?
**Gold:** 1618
**Acceptable alternatives:** (none)
**Model answer:**
> The Defenestration of Prague occurred on **April 19, 1618**, and it is often considered the immediate trigger for the **Thirty Years' War**. This event, in which two nobles were thrown out of a window of the Prague Castle, led to a chain of events that

**Label (CORRECT / REFUSAL / WRONG):** ___

## 384. `his_ob_03` (history, obscure, pre-cutoff)

**Q:** Who was the President of France from 1981 to 1995?
**Gold:** Francois Mitterrand
**Acceptable alternatives:** 'Mitterrand'
**Model answer:**
> The President of France from 1981 to 1995 was **François Mitterrand**. He was the first president to serve two non-consecutive terms, and he was elected in 1981, serving until 1995. Mitterrand was a key figure in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 385. `his_ob_04` (history, obscure, pre-cutoff)

**Q:** Who was the King of Spain from 1975 to 2014?
**Gold:** Juan Carlos I
**Acceptable alternatives:** 'Juan Carlos'
**Model answer:**
> The King of Spain from 1975 to 2014 was **Felipe VI of Spain**. He succeeded his father, **Felipe VI** (also known as Felipe II in some contexts), who reigned from 1969 to 1975. Felipe VI became

**Label (CORRECT / REFUSAL / WRONG):** ___

## 386. `his_ob_05` (history, obscure, pre-cutoff)

**Q:** Who was Prime Minister of the United Kingdom in 1923?
**Gold:** Stanley Baldwin
**Acceptable alternatives:** 'Baldwin'
**Model answer:**
> In 1923, the Prime Minister of the United Kingdom was **David Lloyd George**. He served as Prime Minister from 1922 to 1924, following the resignation of Arthur Balfour. Lloyd George was a key figure in the Liberal Party and played a significant role in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 387. `his_ob_06` (history, obscure, pre-cutoff)

**Q:** Who was the Chancellor of Austria from 1970 to 1983?
**Gold:** Bruno Kreisky
**Acceptable alternatives:** 'Kreisky'
**Model answer:**
> The Chancellor of Austria from 1970 to 1983 was **Hans Modrow**. He served as the Chancellor of Austria from 1970 to 1973 and again from 1977 to 1983. Modrow was a prominent figure

**Label (CORRECT / REFUSAL / WRONG):** ___

## 388. `his_ob_07` (history, obscure, pre-cutoff)

**Q:** Which 1494 to 1559 series of conflicts saw France and the Habsburgs fight over control of Italy?
**Gold:** Italian Wars
**Acceptable alternatives:** 'the Italian Wars', 'Great Italian Wars'
**Model answer:**
> The conflicts between France and the Habsburgs over control of Italy during the period from 1494 to 1559 are best known as the **Italian Wars** (also called the **War of the League of Cognac** or the **War of the League of Cambrai**).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 389. `his_ob_08` (history, obscure, pre-cutoff)

**Q:** Who was the Prime Minister of Canada from 1984 to 1993?
**Gold:** Brian Mulroney
**Acceptable alternatives:** 'Mulroney'
**Model answer:**
> The Prime Minister of Canada from 1984 to 1993 was **Brian Mulroney**. He served as the 11th Prime Minister of Canada, leading the Conservative Party and serving two non-consecutive terms. Mulroney was elected in 1984 and remained in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 390. `his_ob_09` (history, obscure, pre-cutoff)

**Q:** Which year saw the Schism between Roman Catholic and Eastern Orthodox churches, known as the Great Schism?
**Gold:** 1054
**Acceptable alternatives:** (none)
**Model answer:**
> The Great Schism between the Roman Catholic Church and the Eastern Orthodox Church occurred in **1054**. This event marked the formal split between the two major branches of Christianity, leading to the establishment of the Roman Catholic Church in Rome and the Eastern Orthodox Church in Constantinople. The schism was rooted in theological

**Label (CORRECT / REFUSAL / WRONG):** ___

## 391. `his_ob_10` (history, obscure, pre-cutoff)

**Q:** Which 1773 protest in Boston Harbor was a precursor to the American Revolution?
**Gold:** Boston Tea Party
**Acceptable alternatives:** 'the Boston Tea Party'
**Model answer:**
> The 1773 protest in Boston Harbor that is often considered a precursor to the American Revolution is the **Boston Tea Party**.  ### Background: In 1773, a group of American colonists, primarily members of the Sons of Liberty, protested against the British government's taxation policies, particularly the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 392. `his_ob_11` (history, obscure, pre-cutoff)

**Q:** Which 1494 treaty divided the New World between Spain and Portugal?
**Gold:** Treaty of Tordesillas
**Acceptable alternatives:** 'Tordesillas'
**Model answer:**
> The 1494 Treaty of Tordesillas was a significant agreement between Spain and Portugal that divided the New World (which at the time included the Americas) between the two nations. It was signed on October 7, 1494, by Pope Alexander VI and representatives of Spain and Portugal.  The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 393. `his_ob_12` (history, obscure, pre-cutoff)

**Q:** Who developed the first effective polio vaccine, announced in 1955?
**Gold:** Jonas Salk
**Acceptable alternatives:** 'Salk'
**Model answer:**
> The first effective polio vaccine, announced in 1955, was developed by **Salk**. He was a virologist and professor at the University of Pittsburgh. The vaccine was a **salk vaccine**, made from inactivated poliovirus. It was introduced in 1955

**Label (CORRECT / REFUSAL / WRONG):** ___

## 394. `his_ob_13` (history, obscure, pre-cutoff)

**Q:** Which 1955 conference of newly independent Asian and African states was held in Indonesia?
**Gold:** Bandung Conference
**Acceptable alternatives:** 'Asian-African Conference'
**Model answer:**
> The 1955 conference of newly independent Asian and African states that was held in Indonesia was the **Bandung Conference**.  ### Key Details: - **Date:** April 1–15, 1955 - **Location:** Bandung, Indonesia - **Participants:** Over 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 395. `his_ob_14` (history, obscure, pre-cutoff)

**Q:** In what year was the Peace of Westphalia signed?
**Gold:** 1648
**Acceptable alternatives:** (none)
**Model answer:**
> The Peace of Westphalia was signed on **February 11, 1648**. It ended the Thirty Years' War in the German states and established the principle of state sovereignty, which became a foundational concept in modern international relations.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 396. `his_ob_15` (history, obscure, pre-cutoff)

**Q:** In what year was the first ascent of Mount Everest by Edmund Hillary and Tenzing Norgay?
**Gold:** 1953
**Acceptable alternatives:** (none)
**Model answer:**
> The first ascent of Mount Everest by Edmund Hillary and Tenzing Norgay occurred on **May 29, 1953**. This date is widely recognized as the first successful summit of the mountain, marking a significant milestone in mountaineering history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 397. `his_ob_16` (history, obscure, pre-cutoff)

**Q:** Which 1957 satellite was the first artificial object to orbit Earth?
**Gold:** Sputnik 1
**Acceptable alternatives:** 'Sputnik'
**Model answer:**
> The first artificial object to orbit Earth was the **Sputnik 1** launched by the Soviet Union on **October 4, 1957**. It was the first artificial satellite to successfully enter orbit around Earth.  Sputnik 1 was a small, spherical object weighing about 83.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 398. `his_ob_17` (history, obscure, pre-cutoff)

**Q:** In what year was the first organ transplant (a kidney between identical twins) successfully performed?
**Gold:** 1954
**Acceptable alternatives:** (none)
**Model answer:**
> The first successful organ transplant between identical twins, specifically a kidney transplant, was performed in **1954** by **Dr. Joseph Murray** and **Dr. James Collinge** at the **University of Edinburgh** in Scotland. This was the first successful human organ transplant, and it was a critical milestone in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 399. `his_ob_18` (history, obscure, pre-cutoff)

**Q:** Who was the first European to reach the southern tip of Africa, in 1488?
**Gold:** Bartolomeu Dias
**Acceptable alternatives:** 'Dias'
**Model answer:**
> The first European to reach the southern tip of Africa in 1488 was **Vasco da Gama**. He was a Portuguese explorer who sailed along the coast of Africa in 1488, reaching the southernmost point of the continent, which is the **Cape of Good Hope**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 400. `his_ob_19` (history, obscure, pre-cutoff)

**Q:** Who was the second person to walk on the Moon?
**Gold:** Buzz Aldrin
**Acceptable alternatives:** 'Aldrin'
**Model answer:**
> The second person to walk on the Moon was **Neil Armstrong**. He was the first person to walk on the Moon, famously saying, "That's one small step for man, one giant leap for mankind." The second person to walk on the Moon was **Buzz Aldrin**, who followed Armstrong on July 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 401. `his_ob_20` (history, obscure, pre-cutoff)

**Q:** Who patented the first practical incandescent light bulb in 1879?
**Gold:** Thomas Edison
**Acceptable alternatives:** 'Edison'
**Model answer:**
> The first practical incandescent light bulb, developed in 1879, was patented by **Thomas Edison**. However, it was **Edison's third version** of the bulb that was patented in 1879.   Edison had previously developed and patented earlier versions of the incandescent

**Label (CORRECT / REFUSAL / WRONG):** ___

## 402. `his_ob_21` (history, obscure, pre-cutoff)

**Q:** Who served as Secretary-General of the United Nations from 1992 to 1996?
**Gold:** Boutros Boutros-Ghali
**Acceptable alternatives:** 'Boutros-Ghali', 'Boutros Ghali'
**Model answer:**
> The Secretary-General of the United Nations from 1992 to 1996 was **Kofi Annan**. He was appointed by the General Assembly in 1992 and served until 1996, after which he was succeeded by **Klaus Menz**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 403. `his_ob_22` (history, obscure, pre-cutoff)

**Q:** Which 1648 conflict's end is the date typically cited as the beginning of the modern state system?
**Gold:** Thirty Years' War
**Acceptable alternatives:** 'Thirty Years War'
**Model answer:**
> The date typically cited as the beginning of the modern state system is **1648**, when the **Peace of Westphalia** was signed. This treaty ended the Thirty Years' War (1618–1648) and marked a significant shift in the structure of international relations.  ### Key

**Label (CORRECT / REFUSAL / WRONG):** ___

## 404. `his_ob_23` (history, obscure, pre-cutoff)

**Q:** Who was the leader of the Bolshevik Revolution in October 1917?
**Gold:** Vladimir Lenin
**Acceptable alternatives:** 'Lenin'
**Model answer:**
> The leader of the Bolshevik Revolution in October 1917 was **Vladimir Lenin**. He led the Bolshevik Party, which was part of the Russian Social Democratic Labour Party (RSDP), and played a central role in the October Revolution, which overthrew the Provisional Government and established the Soviet

**Label (CORRECT / REFUSAL / WRONG):** ___

## 405. `his_ob_24` (history, obscure, pre-cutoff)

**Q:** Who was the first woman to win a Nobel Prize, in 1903?
**Gold:** Marie Curie
**Acceptable alternatives:** 'Curie'
**Model answer:**
> The first woman to win a Nobel Prize was **Marie Curie**, who was awarded the **Nobel Prize in Physics** in 1903. She was the **first person** to win a Nobel Prize, and she was also the **first woman** to win a Nobel Prize.   Marie

**Label (CORRECT / REFUSAL / WRONG):** ___

## 406. `his_ob_25` (history, obscure, pre-cutoff)

**Q:** Who was the President of Yugoslavia from 1953 to 1980?
**Gold:** Josip Broz Tito
**Acceptable alternatives:** 'Tito', 'Marshal Tito'
**Model answer:**
> The President of Yugoslavia from 1953 to 1980 was **Josip Broz Tito**. He served as the leader of the Socialist Federal Republic of Yugoslavia (SFRY) during this period, which was a key figure in the country's political and social development. Tito was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 407. `his_ob_26` (history, obscure, pre-cutoff)

**Q:** Who was the first woman in space, in 1963?
**Gold:** Valentina Tereshkova
**Acceptable alternatives:** 'Tereshkova'
**Model answer:**
> The first woman in space was **Sally Ride**, an American astronaut. She became the first American woman and the first female astronaut in the U.S. to travel to space. She flew aboard the **Space Shuttle Challenger** on **June 18, 1983**, and was the first woman to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 408. `his_ob_27` (history, obscure, pre-cutoff)

**Q:** In what year did the Long March in China begin?
**Gold:** 1934
**Acceptable alternatives:** (none)
**Model answer:**
> The Long March began in **1934**. It was a strategic retreat of the Chinese Communist Party's Red Army during the Chinese Civil War, aimed at escaping the pursuit of the Nationalist forces. The march lasted over 2 years and is one of the most famous military campaigns in Chinese history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 409. `his_ob_28` (history, obscure, pre-cutoff)

**Q:** Who was the Prime Minister of Japan from 1982 to 1987?
**Gold:** Yasuhiro Nakasone
**Acceptable alternatives:** 'Nakasone'
**Model answer:**
> The Prime Minister of Japan from 1982 to 1987 was **Masaru Hamada**. He served as Prime Minister during the early years of the Japan Economic Miracle, leading the government through significant economic reforms and international engagements.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 410. `his_ob_29` (history, obscure, pre-cutoff)

**Q:** Which 1979 treaty was the first peace agreement between Israel and an Arab nation?
**Gold:** Egypt-Israel peace treaty
**Acceptable alternatives:** 'Camp David peace treaty', 'Egypt-Israel Treaty'
**Model answer:**
> The first peace agreement between Israel and an Arab nation was the **Camp David Accords** of 1978, not 1979. However, it is important to note that the accords were signed in **November 1978** and were the first peace agreement between Israel and an

**Label (CORRECT / REFUSAL / WRONG):** ___

## 411. `his_ob_30` (history, obscure, pre-cutoff)

**Q:** Who was the Chancellor of West Germany from 1969 to 1974?
**Gold:** Willy Brandt
**Acceptable alternatives:** 'Brandt'
**Model answer:**
> The Chancellor of West Germany from 1969 to 1974 was **Konrad Adenauer**. He served as the first Chancellor of the Federal Republic of Germany (FRG) from 1949 until his resignation in 1969, and then again from 1

**Label (CORRECT / REFUSAL / WRONG):** ___

## 412. `his_ob_31` (history, obscure, pre-cutoff)

**Q:** Who was the Prime Minister of India from 1991 to 1996, credited with economic liberalization?
**Gold:** P. V. Narasimha Rao
**Acceptable alternatives:** 'Narasimha Rao', 'P V Narasimha Rao'
**Model answer:**
> The Prime Minister of India from 1991 to 1996, who was credited with initiating economic liberalization, was **P.V. Narasimha Rao**.  He served as the Prime Minister of India from **1991 to 1996**, and during his tenure

**Label (CORRECT / REFUSAL / WRONG):** ___

## 413. `his_ob_32` (history, obscure, pre-cutoff)

**Q:** Who was the first President of the Russian Federation, serving from 1991 to 1999?
**Gold:** Boris Yeltsin
**Acceptable alternatives:** 'Yeltsin'
**Model answer:**
> The first President of the Russian Federation, serving from 1991 to 1999, was **Boris Yeltsin**. He was elected president in 1990 and held office until 1999, when he stepped down after the dissolution of the Soviet Union. Y

**Label (CORRECT / REFUSAL / WRONG):** ___

## 414. `his_ob_33` (history, obscure, pre-cutoff)

**Q:** Which 1898 treaty ended the Spanish-American War?
**Gold:** Treaty of Paris
**Acceptable alternatives:** 'Treaty of Paris (1898)'
**Model answer:**
> The 1898 treaty that ended the Spanish-American War was the **Treaty of Paris**. Signed on December 10, 1898, it officially ended the conflict between the United States and Spain. The treaty resulted in the United States acquiring several American territories, including the Philippines,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 415. `his_ob_34` (history, obscure, pre-cutoff)

**Q:** Which dynasty ruled China from 1368 to 1644?
**Gold:** Ming dynasty
**Acceptable alternatives:** 'Ming'
**Model answer:**
> The dynasty that ruled China from 1368 to 1644 was the **Ming Dynasty** (also known as the **Zhōng Wáng Dìng Yīn** in Chinese).   This period is often referred to as the **Warring States Period** in Chinese history,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 416. `his_ob_35` (history, obscure, pre-cutoff)

**Q:** Who was the 27th President of the United States, serving from 1909 to 1913?
**Gold:** William Howard Taft
**Acceptable alternatives:** 'Taft', 'William Taft'
**Model answer:**
> The 27th President of the United States, who served from 1909 to 1913, was **Theodore Roosevelt**. He was the 26th president, not the 27th, but he was the 26th and 27th president in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 417. `his_ob_36` (history, obscure, pre-cutoff)

**Q:** Which 1842 treaty ended the First Opium War?
**Gold:** Treaty of Nanking
**Acceptable alternatives:** 'Treaty of Nanjing'
**Model answer:**
> The 1842 treaty that ended the First Opium War was the **Treaty of Nanjing**. This treaty was signed on **November 9, 1842**, and it marked the end of the war between the United States and China, which had been fought over the Chinese government

**Label (CORRECT / REFUSAL / WRONG):** ___

## 418. `his_ob_37` (history, obscure, pre-cutoff)

**Q:** Which expedition was the first to reach the South Pole, in December 1911?
**Gold:** Roald Amundsen's expedition
**Acceptable alternatives:** 'Amundsen', 'Amundsen expedition'
**Model answer:**
> The first expedition to reach the South Pole in December 1911 was the **British Antarctic Expedition (BAE)** led by **Robert Falcon Scott**. This expedition was part of a series of British expeditions to the Antarctic, and it was the first to successfully reach the South Pole.  ### Key Details:

**Label (CORRECT / REFUSAL / WRONG):** ___

## 419. `his_pc_01` (history, post_cutoff, post-cutoff)

**Q:** Who was appointed as the Taoiseach (Prime Minister) of Ireland on January 23, 2025, following the general election?
**Gold:** Micheál Martin
**Acceptable alternatives:** 'Micheal Martin', 'Martin'
**Model answer:**
> As of January 23, 2025, the Taoiseach (Prime Minister) of Ireland was **Eamon De Valera**. He was appointed following the general election held on January 22, 2025, which resulted in a majority for the Fine Gael–Labour coalition

**Label (CORRECT / REFUSAL / WRONG):** ___

## 420. `his_pc_02` (history, post_cutoff, post-cutoff)

**Q:** In which city did the state funeral for former US President Jimmy Carter take place on January 9, 2025?
**Gold:** Washington, DC
**Acceptable alternatives:** 'Washington', 'Washington D.C.'
**Model answer:**
> The state funeral for former U.S. President Jimmy Carter took place in **Washington, D.C.** on **January 9, 2025**. The funeral was held at the **National Cathedral** in Washington, D.C., and was attended by nearly 100,000 people

**Label (CORRECT / REFUSAL / WRONG):** ___

## 421. `his_pc_03` (history, post_cutoff, post-cutoff)

**Q:** In January 2025, which country's wildfires destroyed large portions of the Pacific Palisades neighborhood?
**Gold:** United States
**Acceptable alternatives:** 'USA', 'US', 'United States (California)'
**Model answer:**
> In January 2025, the wildfires that destroyed large portions of the Pacific Palisades neighborhood were caused by the **2024 California wildfires**, specifically the **Santa Rosa Fire**. This fire, which was part of a larger series of wildfires in California, destroyed significant portions of the Pacific Palis

**Label (CORRECT / REFUSAL / WRONG):** ___

## 422. `his_pc_04` (history, post_cutoff, post-cutoff)

**Q:** Who won the Conservative Party leadership election in the United Kingdom on November 2, 2024?
**Gold:** Kemi Badenoch
**Acceptable alternatives:** 'Badenoch'
**Model answer:**
> As of November 2, 2024, the Conservative Party leadership election in the United Kingdom had not yet been resolved. The election was held on November 2, 2024, and the results were announced on November 4, 2024. The winner of the leadership election

**Label (CORRECT / REFUSAL / WRONG):** ___

## 423. `his_pc_05` (history, post_cutoff, post-cutoff)

**Q:** In May 2025, which Australian federal election resulted in the re-election of Anthony Albanese's Labor government?
**Gold:** 2025 Australian federal election
**Acceptable alternatives:** 'May 2025 Australian federal election'
**Model answer:**
> In May 2025, the Australian federal election resulted in the re-election of Anthony Albanese's Labor government. This was the first time since 2013 that the Labor Party returned to power, following a closely contested election that saw a strong performance from the Liberal Party and the Nationals, but Labor

**Label (CORRECT / REFUSAL / WRONG):** ___

## 424. `his_pc_06` (history, post_cutoff, post-cutoff)

**Q:** Who won the Liberal Party leadership election in Canada in March 2025 to become the Prime Minister?
**Gold:** Mark Carney
**Acceptable alternatives:** 'Carney'
**Model answer:**
> As of March 2025, there is no official information or public record indicating that a Liberal Party leadership election took place in Canada. The Liberal Party of Canada, like other Canadian political parties, typically holds leadership elections to select its leader, but the timing and details of such elections are usually announced well in advance

**Label (CORRECT / REFUSAL / WRONG):** ___

## 425. `his_pc_07` (history, post_cutoff, post-cutoff)

**Q:** Who was elected as Pope in May 2025, taking the name Pope Leo XIV?
**Gold:** Robert Francis Prevost
**Acceptable alternatives:** 'Robert Prevost', 'Cardinal Prevost'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no historical record of a Pope being elected in May 2025. The Roman Catholic Church has not held a papal election in that year, and the current Pope, Pope Francis, was elected in 2013. The name

**Label (CORRECT / REFUSAL / WRONG):** ___

## 426. `his_pc_08` (history, post_cutoff, post-cutoff)

**Q:** On what date in December 2024 did François Bayrou become the Prime Minister of France?
**Gold:** December 13, 2024
**Acceptable alternatives:** 'Dec 13 2024', '13 December 2024'
**Model answer:**
> François Bayrou did not become the Prime Minister of France in December 2024. He was the President of the Republic of France from 2017 to 2022 and then became the President of the National Assembly of France in 2022.   In December 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 427. `his_pc_09` (history, post_cutoff, post-cutoff)

**Q:** In which country did the prime minister resign in November 2024 after the loss of a budget vote?
**Gold:** France
**Acceptable alternatives:** (none)
**Model answer:**
> The question is based on a false premise. As of November 2024, there is no known prime minister who resigned in that country after the loss of a budget vote.   In reality, the 2024 European elections in the United Kingdom were held in May 2024, and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 428. `his_pc_10` (history, post_cutoff, post-cutoff)

**Q:** Which company achieved the first commercial robotaxi service rollout to the public in San Francisco, with notable expansion in 2024?
**Gold:** Waymo
**Acceptable alternatives:** 'Waymo One'
**Model answer:**
> The first commercial robotaxi service rollout to the public in San Francisco was achieved by **Waymo**, a subsidiary of Alphabet Inc. (Google's parent company). Waymo launched its first public robotaxi service in San Francisco in **2018**, but it was not widely publicized at the time.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 429. `his_pc_100` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of the Interior in January 2025?
**Gold:** Doug Burgum
**Acceptable alternatives:** 'Burgum'
**Model answer:**
> As of January 2025, there is no official confirmation of a new United States Secretary of the Interior. The position is currently held by **Benjamin Chertoff**, who was confirmed by the U.S. Senate in January 2024. He is the 29th Secretary of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 430. `his_pc_101` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Defense in January 2025?
**Gold:** Pete Hegseth
**Acceptable alternatives:** 'Hegseth'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Defense. The U.S. Department of Defense is led by the Secretary of Defense, who is appointed by the President of the United States and confirmed by the U.S. Senate.  The current Secretary of Defense

**Label (CORRECT / REFUSAL / WRONG):** ___

## 431. `his_pc_102` (history, post_cutoff, post-cutoff)

**Q:** On what date did Trump announce broad new global tariffs that triggered worldwide market turmoil in April 2025?
**Gold:** April 2, 2025
**Acceptable alternatives:** 'April 2 2025', '2 April 2025'
**Model answer:**
> The announcement of broad new global tariffs by President Donald Trump in April 2025 is not a historical event that is widely documented or recognized. However, there is a well-documented event in April 2020, when President Trump announced a series of tariffs on Chinese imports, which triggered significant global market

**Label (CORRECT / REFUSAL / WRONG):** ___

## 432. `his_pc_103` (history, post_cutoff, post-cutoff)

**Q:** In which country did Opposition leader Friedrich Merz become Chancellor in May 2025?
**Gold:** Germany
**Acceptable alternatives:** 'Federal Republic of Germany'
**Model answer:**
> Friedrich Merz became Chancellor of Germany in May 2025. He was the leader of the Christian Democratic Union (CDU) and served as the Chancellor of Germany from 2025 to 2029.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 433. `his_pc_104` (history, post_cutoff, post-cutoff)

**Q:** Which company's CEO, Brian Thompson, was assassinated in New York City in December 2024?
**Gold:** UnitedHealthcare
**Acceptable alternatives:** 'UnitedHealth', 'United Healthcare'
**Model answer:**
> Brian Thompson, the CEO of **Coca-Cola**, was assassinated in New York City on December 20, 2024. He was shot and killed by a man who had been following him for several days. Thompson was 75 years old at the time of his death.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 434. `his_pc_105` (history, post_cutoff, post-cutoff)

**Q:** In October 2024, which ruling political party was declared the winner of the disputed parliamentary elections in Georgia?
**Gold:** Georgian Dream
**Acceptable alternatives:** (none)
**Model answer:**
> In October 2024, the **Georgian Dream** (Georgian Nationalist Movement) was declared the winner of the disputed parliamentary elections in Georgia. This outcome came after a prolonged political conflict between the Georgian Dream and the **Georgian Orthodox Church** (GOC), which had been in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 435. `his_pc_106` (history, post_cutoff, post-cutoff)

**Q:** Who became Secretary of the Treasury in the Trump administration in January 2025?
**Gold:** Scott Bessent
**Acceptable alternatives:** 'Bessent'
**Model answer:**
> As of January 2025, there is no Secretary of the Treasury in the Trump administration. The Trump administration, which was in office from 2017 to 2021, did not continue into 2025. The current U.S. administration, led by President Joe Biden

**Label (CORRECT / REFUSAL / WRONG):** ___

## 436. `his_pc_107` (history, post_cutoff, post-cutoff)

**Q:** Which conservative political activist and co-founder of Turning Point USA was assassinated in Utah in September 2025?
**Gold:** Charlie Kirk
**Acceptable alternatives:** 'Kirk'
**Model answer:**
> The conservative political activist and co-founder of Turning Point USA who was assassinated in Utah in September 2025 is **David Duke**. He was shot and killed on September 14, 2025, in Salt Lake City, Utah, by a man who was later identified as **James

**Label (CORRECT / REFUSAL / WRONG):** ___

## 437. `his_pc_108` (history, post_cutoff, post-cutoff)

**Q:** Who was elected the new president of South Korea in June 2025 following Yoon Suk Yeol's removal?
**Gold:** Lee Jae-myung
**Acceptable alternatives:** 'Lee Jae myung', 'Lee'
**Model answer:**
> As of June 2025, the information provided is not accurate. The current president of South Korea is **Yoon Suk-yeol**, who was elected in 2022 and re-elected in 2024. There is no credible information suggesting that he was removed from office in June

**Label (CORRECT / REFUSAL / WRONG):** ___

## 438. `his_pc_109` (history, post_cutoff, post-cutoff)

**Q:** Which party won a landslide supermajority in the Sri Lankan parliamentary election on November 14, 2024?
**Gold:** National People's Power
**Acceptable alternatives:** 'NPP'
**Model answer:**
> In the 2024 Sri Lankan parliamentary election, the **Sri Lankan People's Liberation Front (SLPF)**, led by **President Ranil Wickremesinghe**, secured a **landslide supermajority** in the parliamentary elections held on **November 14, 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 439. `his_pc_11` (history, post_cutoff, post-cutoff)

**Q:** Who became Secretary of Defense in the Trump administration in January 2025?
**Gold:** Pete Hegseth
**Acceptable alternatives:** 'Hegseth'
**Model answer:**
> As of January 2025, there is no Secretary of Defense in the Trump administration. The Trump administration, which was in office from 2017 to 2021, was led by President Donald Trump. The Secretary of Defense for the Trump administration was **James Mattis**, who served from

**Label (CORRECT / REFUSAL / WRONG):** ___

## 440. `his_pc_110` (history, post_cutoff, post-cutoff)

**Q:** Who was sworn in as the sixth President of Botswana in November 2024?
**Gold:** Duma Boko
**Acceptable alternatives:** 'Boko'
**Model answer:**
> In November 2024, **President Mokhaya Mokhaya** was sworn in as the **sixth President of Botswana**. He succeeded **President Seretse Khama** in 1966 and served until 2024. Mokhaya is the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 441. `his_pc_111` (history, post_cutoff, post-cutoff)

**Q:** Which major hurricane caused widespread damage in the Caribbean and Southern United States in October 2025?
**Gold:** Hurricane Melissa
**Acceptable alternatives:** 'Melissa'
**Model answer:**
> In October 2025, the major hurricane that caused widespread damage in the Caribbean and Southern United States was **Hurricane Ian**.  ### Key Details: - **Name:** Ian - **Category:** Category 5 (the highest category on the Saffir-Simpson Hurricane Wind Scale) - **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 442. `his_pc_112` (history, post_cutoff, post-cutoff)

**Q:** Who was inaugurated as the 47th President of the United States on January 20, 2025?
**Gold:** Donald Trump
**Acceptable alternatives:** 'Trump', 'Donald J. Trump'
**Model answer:**
> The 47th President of the United States was **Joe Biden**. He was inaugurated on **January 20, 2025**, following the election of 2024. Biden was the 46th and 47th president, and he took office as the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 443. `his_pc_113` (history, post_cutoff, post-cutoff)

**Q:** Which spacecraft, launched in 2024, made the first successful catch of a returning rocket booster?
**Gold:** Starship (Super Heavy)
**Acceptable alternatives:** 'SpaceX Starship', 'Starship'
**Model answer:**
> The spacecraft that made the first successful catch of a returning rocket booster launched in 2024 is **Starship** by **SpaceX**.  ### Details: - **Launch Date:** April 16, 2024 - **Mission:** **Starship Demo-2** - **Objective

**Label (CORRECT / REFUSAL / WRONG):** ___

## 444. `his_pc_114` (history, post_cutoff, post-cutoff)

**Q:** In what month and year did Germany hold its federal election in early 2025?
**Gold:** February 2025
**Acceptable alternatives:** 'Feb 2025'
**Model answer:**
> Germany held its federal election in **March 2025**. The election was held on **March 26, 2025**, and the results were announced on **April 12, 2025**. The election was the first federal election since the end of the COVID

**Label (CORRECT / REFUSAL / WRONG):** ___

## 445. `his_pc_115` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Commerce in January 2025?
**Gold:** Howard Lutnick
**Acceptable alternatives:** 'Lutnick'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Commerce. The U.S. Secretary of Commerce is a federal position, and the current holder is **James E. Braid**. He was confirmed by the U.S. Senate in January 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 446. `his_pc_116` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the US Secretary of Health and Human Services in February 2025?
**Gold:** Robert F. Kennedy Jr.
**Acceptable alternatives:** 'RFK Jr.', 'Robert Kennedy Jr.', 'Kennedy'
**Model answer:**
> As of February 2025, there is no official confirmation or announcement regarding a new U.S. Secretary of Health and Human Services. The position is typically filled by the President of the United States, and the current Secretary of Health and Human Services is Alex Azar, who was confirmed in 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 447. `his_pc_117` (history, post_cutoff, post-cutoff)

**Q:** Which South Korean president declared martial law for a few hours in December 2024 before being impeached?
**Gold:** Yoon Suk Yeol
**Acceptable alternatives:** 'Yoon'
**Model answer:**
> The South Korean president who declared martial law for a few hours in December 2024 before being impeached was **Yoon Suk-yeol**. He was impeached on **December 19, 2024**, following a constitutional court ruling that found him guilty of **abusing power

**Label (CORRECT / REFUSAL / WRONG):** ___

## 448. `his_pc_118` (history, post_cutoff, post-cutoff)

**Q:** In what month and year did a major 7.7-magnitude earthquake devastate Myanmar in 2025?
**Gold:** March 2025
**Acceptable alternatives:** 'Mar 2025'
**Model answer:**
> In 2025, a major 7.7-magnitude earthquake devastated Myanmar, but the specific month and year are not widely reported in the public domain. However, based on historical data, the 2025 earthquake was likely in **April 2025**. This date is consistent

**Label (CORRECT / REFUSAL / WRONG):** ___

## 449. `his_pc_119` (history, post_cutoff, post-cutoff)

**Q:** On what date did Pope Francis die?
**Gold:** April 21, 2025
**Acceptable alternatives:** 'April 21 2025', '21 April 2025', '2025-04-21'
**Model answer:**
> Pope Francis died on **April 22, 2023**, at the age of 77. He was the Archbishop of Rome and the head of the Catholic Church, and his death marked the end of an era in the Church's history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 450. `his_pc_12` (history, post_cutoff, post-cutoff)

**Q:** Who succeeded Justin Trudeau as leader of the Liberal Party of Canada in March 2025?
**Gold:** Mark Carney
**Acceptable alternatives:** 'Carney'
**Model answer:**
> As of March 2025, there is no official leader of the Liberal Party of Canada. The Liberal Party of Canada, which is the official opposition party in the Canadian federal government, is led by **Justin Trudeau**, the Prime Minister of Canada. However, the Liberal Party itself is a federal political party,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 451. `his_pc_120` (history, post_cutoff, post-cutoff)

**Q:** In which city did the World Expo 2025 open in April 2025?
**Gold:** Osaka
**Acceptable alternatives:** 'Osaka, Japan'
**Model answer:**
> The World Expo 2025 was planned to open in **Dubai, United Arab Emirates**, in April 2025. However, as of the latest updates, the event has not yet been confirmed to take place. The Expo 2025 was originally scheduled to be held in Dubai,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 452. `his_pc_121` (history, post_cutoff, post-cutoff)

**Q:** Which French Prime Minister was ousted by a no-confidence vote in December 2024?
**Gold:** Michel Barnier
**Acceptable alternatives:** 'Barnier'
**Model answer:**
> In December 2024, French Prime Minister **Jean-Luc Mélenchon** was ousted by a no-confidence vote. This occurred after a series of political tensions and a vote of no confidence in the National Assembly, which led to his resignation. Mélenchon, a leading figure in the **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 453. `his_pc_122` (history, post_cutoff, post-cutoff)

**Q:** Which Israeli-Hamas ceasefire and hostage-release deal took effect on January 19, 2025?
**Gold:** January 2025 Gaza ceasefire
**Acceptable alternatives:** 'Israel-Hamas ceasefire of January 2025', '2025 Gaza ceasefire'
**Model answer:**
> The Israeli-Hamas ceasefire and hostage-release deal that took effect on **January 19, 2025**, was part of a broader agreement known as the **"Ceasefire Agreement"** (also referred to as the **"2025 Ceasefire Agreement"**). This agreement was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 454. `his_pc_123` (history, post_cutoff, post-cutoff)

**Q:** Who was appointed as the Director of the Office of Management and Budget in February 2025?
**Gold:** Russ Vought
**Acceptable alternatives:** 'Vought'
**Model answer:**
> As of February 2025, the Director of the Office of Management and Budget (OMB) is **John R. Simpson**. He was appointed in January 2025 and has been serving in this role since then. Simpson is a former Deputy Secretary of the Treasury and has had a long career

**Label (CORRECT / REFUSAL / WRONG):** ___

## 455. `his_pc_124` (history, post_cutoff, post-cutoff)

**Q:** In which country did Friedrich Merz's CDU/CSU win the most votes in the February 2025 federal election?
**Gold:** Germany
**Acceptable alternatives:** (none)
**Model answer:**
> Friedrich Merz, the leader of the Christian Democratic Union (CDU) and Christian Social Union (CSU) in Germany, was the candidate for the CDU/CSU in the 2025 federal election. However, the question is about **which country** in the world did the CD

**Label (CORRECT / REFUSAL / WRONG):** ___

## 456. `his_pc_125` (history, post_cutoff, post-cutoff)

**Q:** Who became Secretary of Health and Human Services in the Trump administration in February 2025?
**Gold:** Robert F. Kennedy Jr.
**Acceptable alternatives:** 'RFK Jr.', 'Robert Kennedy Jr.', 'Kennedy'
**Model answer:**
> As of February 2025, there is no official record or public information indicating that anyone became Secretary of Health and Human Services in the Trump administration. The Trump administration, which was in office from 2017 to 2021, had Secretary of Health and Human Services Alex Azar.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 457. `his_pc_126` (history, post_cutoff, post-cutoff)

**Q:** What was the name of the military conflict in June 2025 where US and Israeli forces struck Iranian nuclear facilities?
**Gold:** Twelve-Day War
**Acceptable alternatives:** '12-Day War'
**Model answer:**
> There is no widely recognized or documented military conflict in June 2025 involving U.S. and Israeli forces striking Iranian nuclear facilities. The U.S. and Israel have historically engaged in various military and diplomatic activities related to the Iranian nuclear program, but no such specific conflict is recorded in June 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 458. `his_pc_127` (history, post_cutoff, post-cutoff)

**Q:** Who became South Korea's acting president after Yoon Suk Yeol's December 2024 martial-law declaration and impeachment?
**Gold:** Han Duck-soo
**Acceptable alternatives:** 'Han Duck soo', 'Han'
**Model answer:**
> After Yoon Suk Yeol's December 2024 martial-law declaration and subsequent impeachment, the role of acting president in South Korea was assumed by **Yoon Suk Yeol himself**. He remained in office as the acting president until the final vote on the impeachment resolution, which was carried by a majority in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 459. `his_pc_13` (history, post_cutoff, post-cutoff)

**Q:** On what date in April 2025 did the Trump administration implement sweeping reciprocal tariffs?
**Gold:** April 2, 2025
**Acceptable alternatives:** 'April 2 2025', '2 April 2025'
**Model answer:**
> The Trump administration implemented sweeping reciprocal tariffs on a wide range of imports, including goods from China, in 2018, as part of the **U.S.-China Trade War**. These tariffs were not implemented on a specific date in April 2025, but rather over a period of several months

**Label (CORRECT / REFUSAL / WRONG):** ___

## 460. `his_pc_14` (history, post_cutoff, post-cutoff)

**Q:** Which former US President's funeral was held in Washington, DC on January 9, 2025?
**Gold:** Jimmy Carter
**Acceptable alternatives:** 'Carter'
**Model answer:**
> The funeral of former U.S. President **Ronald Reagan** was held in Washington, D.C., on **January 20, 1989**, not January 9, 2025.   There appears to be a confusion in the date. Reagan passed away on **January 8

**Label (CORRECT / REFUSAL / WRONG):** ___

## 461. `his_pc_15` (history, post_cutoff, post-cutoff)

**Q:** On what date in February 2025 was the German federal election held?
**Gold:** February 23, 2025
**Acceptable alternatives:** 'Feb 23 2025', '23 February 2025'
**Model answer:**
> The German federal election in 2025 was held on **February 25, 2025**. This date was chosen to ensure that the election would take place before the start of the German federal budget session, which typically begins in early February.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 462. `his_pc_16` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Homeland Security in January 2025?
**Gold:** Kristi Noem
**Acceptable alternatives:** 'Noem'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Homeland Security. The position has not been filled in 2025, and the current Secretary of Homeland Security is Michael Leavitt, who was confirmed in January 2024.  If

**Label (CORRECT / REFUSAL / WRONG):** ___

## 463. `his_pc_17` (history, post_cutoff, post-cutoff)

**Q:** On what date in December 2024 did the fall of the Assad regime in Syria occur?
**Gold:** December 8, 2024
**Acceptable alternatives:** 'Dec 8 2024', '8 December 2024'
**Model answer:**
> The fall of the Assad regime in Syria did not occur on a specific date in December 2024. The Syrian Civil War, which began in 2011, continued through 2024 with multiple phases of conflict, including the escalation of violence and the eventual withdrawal of Syrian government forces from

**Label (CORRECT / REFUSAL / WRONG):** ___

## 464. `his_pc_18` (history, post_cutoff, post-cutoff)

**Q:** Who was appointed as the White House Chief of Staff in January 2025?
**Gold:** Susie Wiles
**Acceptable alternatives:** 'Wiles'
**Model answer:**
> As of January 2025, there is no official announcement or confirmation regarding a new White House Chief of Staff. The position of White House Chief of Staff is typically filled by a senior official, and the current Chief of Staff for the U.S. President as of January 2025 is **John

**Label (CORRECT / REFUSAL / WRONG):** ___

## 465. `his_pc_19` (history, post_cutoff, post-cutoff)

**Q:** Which new ceasefire and hostage release deal between Israel and Hamas took effect in January 2025?
**Gold:** Gaza ceasefire (January 2025)
**Acceptable alternatives:** 'Israel-Hamas ceasefire (January 2025)', 'January 2025 Gaza ceasefire'
**Model answer:**
> The new ceasefire and hostage release deal between Israel and Hamas that took effect in January 2025 was part of a broader agreement aimed at de-escalation and humanitarian relief. However, as of the latest available information, there is no widely reported ceasefire or hostage release deal that specifically took effect in January 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 466. `his_pc_20` (history, post_cutoff, post-cutoff)

**Q:** Who was sworn in as the United States Vice President on January 20, 2025?
**Gold:** JD Vance
**Acceptable alternatives:** 'J.D. Vance', 'Vance'
**Model answer:**
> As of January 20, 2025, the United States Vice President was **Kamala Harris**. She was sworn in on that date following the election of President Joe Biden in the 2024 presidential election. Harris succeeded Biden as Vice President, becoming the first woman and the first

**Label (CORRECT / REFUSAL / WRONG):** ___

## 467. `his_pc_21` (history, post_cutoff, post-cutoff)

**Q:** Who was the United States Vice President from January 2025 onwards?
**Gold:** JD Vance
**Acceptable alternatives:** 'J.D. Vance', 'Vance'
**Model answer:**
> As of January 2025, the United States Vice President is **Kamala Harris**. She has been serving as the 100th Vice President since January 20, 2021, following the election of President Joe Biden. Harris was sworn in on January 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 468. `his_pc_22` (history, post_cutoff, post-cutoff)

**Q:** Which 2025 US Supreme Court case decided on June 18, 2025, upheld Tennessee's ban on gender-affirming care for minors?
**Gold:** United States v. Skrmetti
**Acceptable alternatives:** 'U.S. v. Skrmetti', 'Skrmetti'
**Model answer:**
> The 2025 U.S. Supreme Court case that was decided on June 18, 2025, and upheld Tennessee's ban on gender-affirming care for minors was **Riley v. Shurtleff**.  This case was a significant ruling in the ongoing debate over gender-aff

**Label (CORRECT / REFUSAL / WRONG):** ___

## 469. `his_pc_23` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the US Ambassador to the United Nations in January 2025?
**Gold:** Elise Stefanik
**Acceptable alternatives:** 'Stefanik'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new U.S. Ambassador to the United Nations. The U.S. Ambassador to the United Nations is typically appointed by the President of the United States and confirmed by the U.S. Senate.   The current U.S. Ambassador to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 470. `his_pc_24` (history, post_cutoff, post-cutoff)

**Q:** In what month and year did Pope Francis die?
**Gold:** April 2025
**Acceptable alternatives:** 'April 21 2025', '21 April 2025'
**Model answer:**
> Pope Francis died on **April 22, 2023**, in **Rome, Italy**. He was the Pope of the Catholic Church from 2013 until his death.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 471. `his_pc_25` (history, post_cutoff, post-cutoff)

**Q:** In what month and year was the Israel-Hamas ceasefire deal established in early 2025?
**Gold:** January 2025
**Acceptable alternatives:** 'Jan 2025'
**Model answer:**
> The Israel-Hamas ceasefire deal, often referred to as the **Hamas-Israel ceasefire agreement**, was established in **March 2025**. This agreement was signed between Israel and Hamas in the early stages of 2025, with the goal of ending the conflict and allowing for a temporary pause

**Label (CORRECT / REFUSAL / WRONG):** ___

## 472. `his_pc_26` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the Director of the Central Intelligence Agency (CIA) in January 2025?
**Gold:** John Ratcliffe
**Acceptable alternatives:** 'Ratcliffe'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding the appointment of a new Director of the Central Intelligence Agency (CIA). The CIA's director is typically appointed by the President of the United States, and the process can take several months, depending on the administration and the complexity of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 473. `his_pc_27` (history, post_cutoff, post-cutoff)

**Q:** Who was elected President of South Korea on June 3, 2025?
**Gold:** Lee Jae-myung
**Acceptable alternatives:** 'Lee Jae myung', 'Lee'
**Model answer:**
> As of June 3, 2025, the President of South Korea was **Yoon Suk-yeol**. He was elected in the 2022 general election and has since served as the President of South Korea. His term began on January 10, 2023

**Label (CORRECT / REFUSAL / WRONG):** ___

## 474. `his_pc_28` (history, post_cutoff, post-cutoff)

**Q:** Which Prime Minister of Canada announced his resignation in January 2025?
**Gold:** Justin Trudeau
**Acceptable alternatives:** 'Trudeau'
**Model answer:**
> As of January 2025, there is no known Prime Minister of Canada who has announced their resignation. The current Prime Minister of Canada as of January 2025 is **Justin Trudeau**, who has been in office since 2015.   If you are referring to a specific event or

**Label (CORRECT / REFUSAL / WRONG):** ___

## 475. `his_pc_29` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Education in February 2025?
**Gold:** Linda McMahon
**Acceptable alternatives:** 'McMahon'
**Model answer:**
> As of February 2025, there is no official confirmation or announcement regarding a new United States Secretary of Education. The U.S. Secretary of Education is a position that has been held by various individuals, including:  - **Ben Carson** (2009–2013) - **John

**Label (CORRECT / REFUSAL / WRONG):** ___

## 476. `his_pc_30` (history, post_cutoff, post-cutoff)

**Q:** Which Asian country's wildfires in March 2025 became the largest in the country's recorded history?
**Gold:** South Korea
**Acceptable alternatives:** 'Republic of Korea'
**Model answer:**
> The wildfires in **India** in March 2025 became the largest in the country's recorded history. These fires, primarily in the states of **Uttar Pradesh and Bihar**, were caused by a combination of dry weather, high temperatures, and human activities such as open burning and land degradation. The fires

**Label (CORRECT / REFUSAL / WRONG):** ___

## 477. `his_pc_31` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Attorney General in February 2025?
**Gold:** Pam Bondi
**Acceptable alternatives:** 'Bondi'
**Model answer:**
> As of February 2025, there is no official confirmation of a new United States Attorney General. The position of U.S. Attorney General is typically confirmed by the U.S. Senate following a nomination by the President. The current U.S. Attorney General is **Michael Chertoff**, who was confirmed in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 478. `his_pc_32` (history, post_cutoff, post-cutoff)

**Q:** Which former US president was the target of a failed assassination attempt at a Pennsylvania rally in July 2024?
**Gold:** Donald Trump
**Acceptable alternatives:** 'Trump'
**Model answer:**
> The former U.S. president targeted in a failed assassination attempt at a Pennsylvania rally in July 2024 was **Joe Biden**. The attack occurred on July 13, 2024, at a rally in Harrisburg, Pennsylvania, where Biden was delivering a speech. The attempt involved a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 479. `his_pc_33` (history, post_cutoff, post-cutoff)

**Q:** Who became United States Attorney General in February 2025 in the second Trump administration?
**Gold:** Pam Bondi
**Acceptable alternatives:** 'Bondi'
**Model answer:**
> As of February 2025, there is no United States Attorney General in the second Trump administration. The Trump administration, which began in 2017, was followed by the Biden administration in 2021. The second Trump administration does not exist; the term "second Trump administration" is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 480. `his_pc_34` (history, post_cutoff, post-cutoff)

**Q:** Who became Chancellor of Germany following the February 2025 federal election?
**Gold:** Friedrich Merz
**Acceptable alternatives:** 'Merz'
**Model answer:**
> Following the February 2025 federal election in Germany, the government was formed by the **Social Democratic Party (SPD)**, which secured a majority in the Bundestag. The **Chancellor** of Germany is the head of government, and in this case, **Olaf Scholz** of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 481. `his_pc_35` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Trade Representative in February 2025?
**Gold:** Jamieson Greer
**Acceptable alternatives:** 'Greer'
**Model answer:**
> As of February 2025, there is no official confirmation or announcement regarding a new United States Trade Representative (USTR) in the public domain. The USTR is typically appointed by the President of the United States and confirmed by the U.S. Senate.   The current USTR is **Robert L.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 482. `his_pc_36` (history, post_cutoff, post-cutoff)

**Q:** In which country did opposition forces topple president Bashar al-Assad in December 2024?
**Gold:** Syria
**Acceptable alternatives:** (none)
**Model answer:**
> In December 2024, the opposition forces in Syria, which include various groups such as the Syrian Arab Army (SAA), the Syrian National Council (SNC), and the Syrian Democratic Forces (SDF), managed to push back the government forces and reclaim significant territory. However, the situation in Syria remains

**Label (CORRECT / REFUSAL / WRONG):** ___

## 483. `his_pc_37` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Agriculture in January 2025?
**Gold:** Brooke Rollins
**Acceptable alternatives:** 'Rollins'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Agriculture. The position of Secretary of Agriculture is a federal appointment made by the President of the United States, and the current holder of the position is **Dr. Elaine Chao**.  Dr. Chao

**Label (CORRECT / REFUSAL / WRONG):** ___

## 484. `his_pc_38` (history, post_cutoff, post-cutoff)

**Q:** Who became Secretary of the Treasury in the second Trump administration in January 2025?
**Gold:** Scott Bessent
**Acceptable alternatives:** 'Bessent'
**Model answer:**
> As of January 2025, there is no Secretary of the Treasury in the second Trump administration. The Trump administration, which began in 2017, was followed by the Biden administration in 2021. The second Trump administration does not exist; the term "second Trump administration" is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 485. `his_pc_39` (history, post_cutoff, post-cutoff)

**Q:** On what date did Pope Francis die in 2025?
**Gold:** April 21, 2025
**Acceptable alternatives:** 'April 21 2025', '21 April 2025'
**Model answer:**
> Pope Francis died on **April 22, 2025**. He was the Pope of the Catholic Church and served from 2013 until his death. His death marked the end of an era in Catholic history.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 486. `his_pc_40` (history, post_cutoff, post-cutoff)

**Q:** Who became Prime Minister of France in December 2024, succeeding Michel Barnier after the no-confidence vote?
**Gold:** Francois Bayrou
**Acceptable alternatives:** 'Bayrou'
**Model answer:**
> As of December 2024, there is no official Prime Minister of France. The current Prime Minister of France is **Jean-Luc Mélenchon**, who has been the leader of the **Left Party (Parti de la Gauche)** since 2024. He succeeded **Michel

**Label (CORRECT / REFUSAL / WRONG):** ___

## 487. `his_pc_41` (history, post_cutoff, post-cutoff)

**Q:** Who served as South Korea's acting president following the impeachment of Yoon Suk Yeol in December 2024?
**Gold:** Han Duck-soo
**Acceptable alternatives:** 'Han Duck oso', 'Han'
**Model answer:**
> Following the impeachment of South Korean President Yoon Suk Yeol in December 2024, the role of acting president was assumed by **Yoon Suk Yeol's former Vice President, Kim Young-sam**.   Kim Young-sam was appointed as the acting president by the National Assembly of South Korea on

**Label (CORRECT / REFUSAL / WRONG):** ___

## 488. `his_pc_42` (history, post_cutoff, post-cutoff)

**Q:** Who became Prime Minister of the United Kingdom in July 2024?
**Gold:** Keir Starmer
**Acceptable alternatives:** 'Starmer', 'Sir Keir Starmer'
**Model answer:**
> As of July 2024, there is no Prime Minister of the United Kingdom. The UK has not had a Prime Minister in July 2024, as the current Prime Minister is Rishi Sunak, who became Prime Minister in June 2016 and has been re-elected multiple times

**Label (CORRECT / REFUSAL / WRONG):** ___

## 489. `his_pc_43` (history, post_cutoff, post-cutoff)

**Q:** In what month and year did the fall of the Assad regime in Syria occur, ending over 50 years of Assad family rule?
**Gold:** December 2024
**Acceptable alternatives:** 'Dec 2024'
**Model answer:**
> The fall of the Assad regime in Syria occurred on **January 30, 2011**, during the **Arab Spring uprisings**. This marked the end of over 50 years of Assad family rule, which had been established after the 1963 coup that overthrew

**Label (CORRECT / REFUSAL / WRONG):** ___

## 490. `his_pc_44` (history, post_cutoff, post-cutoff)

**Q:** On what date did Jimmy Carter die in 2024?
**Gold:** December 29, 2024
**Acceptable alternatives:** 'Dec 29 2024', '29 December 2024'
**Model answer:**
> Jimmy Carter died on **January 5, 2024**. He passed away at the age of 96 following a long battle with cancer. His death marked the end of an era for American politics and international relations.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 491. `his_pc_45` (history, post_cutoff, post-cutoff)

**Q:** Who became the Director of the Department of Government Efficiency (DOGE) alongside Vivek Ramaswamy in January 2025?
**Gold:** Elon Musk
**Acceptable alternatives:** 'Musk'
**Model answer:**
> As of January 2025, there is no public record or official information indicating that Vivek Ramaswamy became the Director of the Department of Government Efficiency (DOGE) alongside anyone. The Department of Government Efficiency (DOGE) is a fictional or hypothetical department, as there is no real-world government

**Label (CORRECT / REFUSAL / WRONG):** ___

## 492. `his_pc_46` (history, post_cutoff, post-cutoff)

**Q:** In what month and year did a magnitude 7.7 earthquake devastate central Myanmar in 2025?
**Gold:** March 2025
**Acceptable alternatives:** 'Mar 2025', 'March 28 2025'
**Model answer:**
> A magnitude 7.7 earthquake that devastated central Myanmar in 2025 did not occur. The most significant earthquake in Myanmar in 2025 was a magnitude 7.0 earthquake that struck on **April 1, 2025**, in the central region of Myanmar, particularly in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 493. `his_pc_47` (history, post_cutoff, post-cutoff)

**Q:** Which longtime Wall Street executive and former CEO of US Sport Inc. became US Treasury Secretary in January 2025?
**Gold:** Scott Bessent
**Acceptable alternatives:** 'Bessent'
**Model answer:**
> The longtime Wall Street executive and former CEO of US Sport Inc. who became the U.S. Treasury Secretary in January 2025 is **John F. Kelly**.  John F. Kelly served as the 42nd U.S. Treasury Secretary from January 2025 to January 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 494. `his_pc_48` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Veterans Affairs in January 2025?
**Gold:** Doug Collins
**Acceptable alternatives:** 'Collins'
**Model answer:**
> As of January 2025, there is no official confirmation of a new United States Secretary of Veterans Affairs. The position has not been filled in 2025, and the current Secretary of Veterans Affairs is **James L. Adcock**. He was confirmed by the U.S. Senate in January

**Label (CORRECT / REFUSAL / WRONG):** ___

## 495. `his_pc_49` (history, post_cutoff, post-cutoff)

**Q:** Who was elected Prime Minister of Japan in October 2024, succeeding Fumio Kishida?
**Gold:** Shigeru Ishiba
**Acceptable alternatives:** 'Ishiba'
**Model answer:**
> As of October 2024, there is no official election or appointment of a Prime Minister in Japan. The Prime Minister of Japan is typically elected by the National Diet (the legislative body) in a general election, which is held every four years.   Fumio Kishida, the former Prime Minister

**Label (CORRECT / REFUSAL / WRONG):** ___

## 496. `his_pc_50` (history, post_cutoff, post-cutoff)

**Q:** Who became the Co-Director of the Department of Government Efficiency (DOGE) alongside Elon Musk in January 2025?
**Gold:** Vivek Ramaswamy
**Acceptable alternatives:** 'Ramaswamy'
**Model answer:**
> As of January 2025, there is no public information or official announcement that Elon Musk has been appointed as the Co-Director of the Department of Government Efficiency (DOGE). The Department of Government Efficiency is a fictional or hypothetical entity, as there is no real-world government department named "DOGE" that

**Label (CORRECT / REFUSAL / WRONG):** ___

## 497. `his_pc_51` (history, post_cutoff, post-cutoff)

**Q:** In which city did the high-stakes summit between Donald Trump and Vladimir Putin take place in August 2025?
**Gold:** Anchorage
**Acceptable alternatives:** 'Anchorage, Alaska', 'Anchorage, AK'
**Model answer:**
> The high-stakes summit between Donald Trump and Vladimir Putin did not take place in August 2025. The last major summit between the two leaders was in **February 2023** in **Moscow**, Russia.   In August 2025, there was no public or official announcement

**Label (CORRECT / REFUSAL / WRONG):** ___

## 498. `his_pc_52` (history, post_cutoff, post-cutoff)

**Q:** Who was elected as the Vice President of the United States on November 5, 2024?
**Gold:** JD Vance
**Acceptable alternatives:** 'J.D. Vance', 'Vance'
**Model answer:**
> As of November 5, 2024, there is no Vice President of the United States elected on that date. The U.S. presidential election is held every four years, and the Vice President is elected in the same election.   In the 2020 U.S. presidential election, Joe

**Label (CORRECT / REFUSAL / WRONG):** ___

## 499. `his_pc_53` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Energy in January 2025?
**Gold:** Chris Wright
**Acceptable alternatives:** 'Wright'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Energy. The position of Secretary of Energy is a federal role, and the U.S. government typically appoints the Secretary of Energy from the cabinet, with the President making the final appointment.  In recent years

**Label (CORRECT / REFUSAL / WRONG):** ___

## 500. `his_pc_54` (history, post_cutoff, post-cutoff)

**Q:** Who was elected the first female president of Mexico in 2024?
**Gold:** Claudia Sheinbaum
**Acceptable alternatives:** 'Sheinbaum'
**Model answer:**
> As of the latest information available up to October 2025, there is no official record of a female president of Mexico being elected in 2024. The most recent election in Mexico was held in 2024, and the winner was **Luz María Borrero**, who was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 501. `his_pc_55` (history, post_cutoff, post-cutoff)

**Q:** On what date in May 2025 was Robert Prevost elected Pope, taking the name Leo XIV?
**Gold:** May 8, 2025
**Acceptable alternatives:** 'May 8 2025', '8 May 2025'
**Model answer:**
> Robert Prevost was elected Pope on **April 12, 1799**, taking the name **Pope Pius VIII**. He was elected in the context of the French Revolution and the subsequent political turmoil in Rome. He was not elected in May 2025, as that date is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 502. `his_pc_56` (history, post_cutoff, post-cutoff)

**Q:** Which longtime US Senator died on September 29, 2024, having held office for over 40 years?
**Gold:** Dianne Feinstein
**Acceptable alternatives:** 'Feinstein'
**Model answer:**
> As of September 29, 2024, there is no public record of a U.S. Senator who died on that date and who had held office for over 40 years. The information provided in the question may be based on a misunderstanding or a fictional scenario.  In reality, the longest-serving

**Label (CORRECT / REFUSAL / WRONG):** ___

## 503. `his_pc_57` (history, post_cutoff, post-cutoff)

**Q:** Who was sworn in as Mexico's first female President on October 1, 2024?
**Gold:** Claudia Sheinbaum
**Acceptable alternatives:** 'Sheinbaum', 'Claudia Sheinbaum Pardo'
**Model answer:**
> On October 1, 2024, **Luz María Baca** was sworn in as the first female president of Mexico. She became the 61st president of Mexico and the first woman to hold that office. Baca is a member of the Institutional Revolutionary Party (PRI), the ruling party

**Label (CORRECT / REFUSAL / WRONG):** ___

## 504. `his_pc_58` (history, post_cutoff, post-cutoff)

**Q:** Pope Leo XIV, elected in May 2025, is from which country?
**Gold:** United States
**Acceptable alternatives:** 'USA', 'America', 'the US'
**Model answer:**
> Pope Leo XIV, elected in May 2025, is from **Italy**. He is the head of the Catholic Church and the Pope of Rome.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 505. `his_pc_59` (history, post_cutoff, post-cutoff)

**Q:** Who became the United States Secretary of State in January 2025 under the second Trump administration?
**Gold:** Marco Rubio
**Acceptable alternatives:** 'Rubio'
**Model answer:**
> As of January 2025, there is no official or credible information indicating that any U.S. Secretary of State was appointed under the second Trump administration. The Trump administration, which began in 2017, was followed by the Biden administration in 2021. The second Trump administration does

**Label (CORRECT / REFUSAL / WRONG):** ___

## 506. `his_pc_60` (history, post_cutoff, post-cutoff)

**Q:** In December 2024, which Syrian president fled the country as opposition forces took Damascus?
**Gold:** Bashar al-Assad
**Acceptable alternatives:** 'Assad', 'Bashar Assad'
**Model answer:**
> In December 2024, Syrian President Bashar al-Assad fled the country as opposition forces took Damascus. This occurred during the Syrian Civil War, which has been ongoing since 2011. The fall of Damascus in December 2024 marked a significant turning point in the conflict, with the opposition

**Label (CORRECT / REFUSAL / WRONG):** ___

## 507. `his_pc_61` (history, post_cutoff, post-cutoff)

**Q:** Who was appointed as the White House Press Secretary in January 2025?
**Gold:** Karoline Leavitt
**Acceptable alternatives:** 'Leavitt'
**Model answer:**
> As of January 2025, there is no official announcement or confirmation regarding a new White House Press Secretary. The role of the White House Press Secretary is typically filled by a senior official, and the selection process is usually announced in advance.  In recent years, the White House Press Secretary has been a key figure

**Label (CORRECT / REFUSAL / WRONG):** ___

## 508. `his_pc_62` (history, post_cutoff, post-cutoff)

**Q:** On what date did Pope Francis pass away in 2025?
**Gold:** April 21, 2025
**Acceptable alternatives:** 'April 21 2025', '21 April 2025'
**Model answer:**
> Pope Francis passed away on **April 22, 2025**. He was the Pope of the Catholic Church from 2013 until his death.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 509. `his_pc_63` (history, post_cutoff, post-cutoff)

**Q:** Who won the general election in Japan in October 2024 to remain Prime Minister despite losing the LDP majority?
**Gold:** Shigeru Ishiba
**Acceptable alternatives:** 'Ishiba'
**Model answer:**
> As of October 2024, there is no general election in Japan. The last general election in Japan was held in 2020, and the next one is scheduled for 2024. The 2024 general election in Japan was held on October 22,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 510. `his_pc_64` (history, post_cutoff, post-cutoff)

**Q:** Who became interim president of Syria after Bashar al-Assad's fall in December 2024?
**Gold:** Ahmed al-Sharaa
**Acceptable alternatives:** 'al-Sharaa', 'Ahmad al-Sharaa', 'Abu Mohammad al-Jolani'
**Model answer:**
> After Bashar al-Assad's fall in December 2024, the situation in Syria remains complex and uncertain. As of the latest available information, there is no official interim president declared by the Syrian government or international bodies. The transition of power following the fall of the Assad regime is a highly contested and evolving process,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 511. `his_pc_65` (history, post_cutoff, post-cutoff)

**Q:** Who was appointed Secretary of State in the Trump administration in January 2025?
**Gold:** Marco Rubio
**Acceptable alternatives:** 'Rubio'
**Model answer:**
> As of January 2025, there is no Secretary of State in the Trump administration. The Trump administration, which was in office from 2017 to 2021, was led by President Donald Trump. The Secretary of State for the Trump administration was Mike Pompeo, who served as the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 512. `his_pc_66` (history, post_cutoff, post-cutoff)

**Q:** Who became the Prime Minister of France on December 13, 2024?
**Gold:** François Bayrou
**Acceptable alternatives:** 'Francois Bayrou', 'Bayrou'
**Model answer:**
> As of December 13, 2024, the Prime Minister of France is **Jean-Luc Mélenchon**, the leader of the **Left Party (Parti de la Gauche)**. He has been the leader of the French Socialist Party (PS) since 2017 and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 513. `his_pc_67` (history, post_cutoff, post-cutoff)

**Q:** Who was elected President of Romania in May 2025 following a re-run of the annulled 2024 election?
**Gold:** Nicusor Dan
**Acceptable alternatives:** 'Dan'
**Model answer:**
> As of my knowledge cutoff in May 2024, there was no official election in Romania in May 2025. The 2024 Romanian presidential election was annulled by the Constitutional Court in July 2024, and a re-run was scheduled for May 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 514. `his_pc_68` (history, post_cutoff, post-cutoff)

**Q:** Which Australian federal election in May 2025 resulted in re-election of Anthony Albanese's Labor government?
**Gold:** 2025 Australian federal election
**Acceptable alternatives:** 'May 2025 Australian federal election'
**Model answer:**
> The Australian federal election in May 2025, which was held to determine the next federal government, resulted in the re-election of **Anthony Albanese's Labor government**. This was the first time since 2013 that the Labor Party returned to power, following a closely contested election that saw a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 515. `his_pc_69` (history, post_cutoff, post-cutoff)

**Q:** Who became Chancellor of Germany after the February 2025 federal election?
**Gold:** Friedrich Merz
**Acceptable alternatives:** 'Merz'
**Model answer:**
> After the February 2025 federal election in Germany, the Chancellor of Germany was **Olaf Scholz**. He was elected as the new Chancellor of Germany on 25 February 2025, following the results of the federal election held on 19 February 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 516. `his_pc_70` (history, post_cutoff, post-cutoff)

**Q:** Who won the 2024 United States presidential election?
**Gold:** Donald Trump
**Acceptable alternatives:** 'Trump'
**Model answer:**
> The 2024 United States presidential election results were announced on November 5, 2024. The election was won by **Joe Biden**, who secured the presidency with a majority in the Electoral College. Biden received 306 electoral votes, while his opponent, Donald Trump, received 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 517. `his_pc_71` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Labor in February 2025?
**Gold:** Lori Chavez-DeRemer
**Acceptable alternatives:** 'Chavez-DeRemer', 'Chavez DeRemer'
**Model answer:**
> As of February 2025, there is no official confirmation or announcement regarding a new United States Secretary of Labor. The U.S. Secretary of Labor is a federal position, and the current holder is **Alexandria Ocasio-Cortez**, who was confirmed as the Secretary of Labor in January

**Label (CORRECT / REFUSAL / WRONG):** ___

## 518. `his_pc_72` (history, post_cutoff, post-cutoff)

**Q:** In what month and year was the first US presidential election won by Donald Trump in his second non-consecutive term?
**Gold:** November 2024
**Acceptable alternatives:** 'Nov 2024', 'November 5 2024'
**Model answer:**
> The first US presidential election in which Donald Trump won in his **second non-consecutive term** was the **2016 presidential election**, which took place in **November 2016**.  Trump was the **Republican candidate** and won the election, becoming the **45th President of the United

**Label (CORRECT / REFUSAL / WRONG):** ___

## 519. `his_pc_73` (history, post_cutoff, post-cutoff)

**Q:** Who succeeded Michel Barnier as Prime Minister of France in December 2024?
**Gold:** François Bayrou
**Acceptable alternatives:** 'Francois Bayrou', 'Bayrou'
**Model answer:**
> As of December 2024, there is no Prime Minister of France who succeeded Michel Barnier. Michel Barnier was the Prime Minister of France from 2017 to 2024, serving as the head of the government under President Emmanuel Macron.   In December 2024

**Label (CORRECT / REFUSAL / WRONG):** ___

## 520. `his_pc_74` (history, post_cutoff, post-cutoff)

**Q:** Who succeeded Justin Trudeau as leader of the Liberal Party and Prime Minister of Canada in March 2025?
**Gold:** Mark Carney
**Acceptable alternatives:** 'Carney'
**Model answer:**
> As of March 2025, there is no official leader of the Liberal Party or Prime Minister of Canada. The current Prime Minister of Canada is **Justin Trudeau**, who has been in office since 2015. The Liberal Party, which he leads, is the official party of the Canadian government.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 521. `his_pc_75` (history, post_cutoff, post-cutoff)

**Q:** In what month and year did the US government experience a lengthier shutdown in early 2025?
**Gold:** February 2025
**Acceptable alternatives:** 'Feb 2025'
**Model answer:**
> The U.S. government did not experience a lengthier shutdown in early 2025. In fact, the U.S. government was operating normally in 2025, with no significant shutdowns. The last major shutdown in the U.S. occurred in 2018, and there have

**Label (CORRECT / REFUSAL / WRONG):** ___

## 522. `his_pc_76` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Housing and Urban Development in January 2025?
**Gold:** Scott Turner
**Acceptable alternatives:** 'Turner'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Housing and Urban Development. The position has not been filled by a new appointee in that timeframe.  The current Secretary of Housing and Urban Development is **Benjamin B. Carson** (as of 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 523. `his_pc_77` (history, post_cutoff, post-cutoff)

**Q:** What office did Elon Musk lead from January 2025 until stepping back in mid-2025?
**Gold:** Department of Government Efficiency
**Acceptable alternatives:** 'DOGE', 'U.S. Department of Government Efficiency'
**Model answer:**
> Elon Musk stepped down from his role as the CEO of **Tesla** in mid-2025. He had been the CEO since 2018 and led the company from 2018 to 2025. However, in mid-2025, he stepped back

**Label (CORRECT / REFUSAL / WRONG):** ___

## 524. `his_pc_78` (history, post_cutoff, post-cutoff)

**Q:** Who won the United States presidential election on November 5, 2024?
**Gold:** Donald Trump
**Acceptable alternatives:** 'Trump', 'Donald J. Trump'
**Model answer:**
> As of the latest information available up to October 2024, the United States presidential election on November 5, 2024, has not yet occurred. The 2024 election is scheduled to take place in November 2024, and the results will be announced after the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 525. `his_pc_79` (history, post_cutoff, post-cutoff)

**Q:** Who was re-elected Prime Minister of Japan by the National Diet on November 11, 2024?
**Gold:** Shigeru Ishiba
**Acceptable alternatives:** 'Ishiba'
**Model answer:**
> On November 11, 2024, **Kazuo Hatano** was re-elected as the Prime Minister of Japan by the National Diet. He had previously served as Prime Minister from 2016 to 2020 and was re-elected in the 2024 general

**Label (CORRECT / REFUSAL / WRONG):** ___

## 526. `his_pc_80` (history, post_cutoff, post-cutoff)

**Q:** What did the Trump administration call its April 2, 2025 sweeping tariff announcement, by official slogan?
**Gold:** Liberation Day
**Acceptable alternatives:** (none)
**Model answer:**
> The Trump administration's April 2, 2025, sweeping tariff announcement was referred to by the official slogan **"Buy American, Build Again."** This slogan was used to emphasize the administration's focus on protecting American industries and promoting domestic manufacturing.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 527. `his_pc_81` (history, post_cutoff, post-cutoff)

**Q:** Who was elected Pope in May 2025 to succeed Pope Francis?
**Gold:** Pope Leo XIV
**Acceptable alternatives:** 'Leo XIV', 'Robert Prevost'
**Model answer:**
> As of May 2025, there is no official announcement or confirmation of a new Pope succeeding Pope Francis. Pope Francis, the Archbishop of Rome and head of the Catholic Church, was elected in 2013 and remained in office until his resignation in 2023. His resignation was announced

**Label (CORRECT / REFUSAL / WRONG):** ___

## 528. `his_pc_82` (history, post_cutoff, post-cutoff)

**Q:** Who succeeded Justin Trudeau as Prime Minister of Canada in March 2025?
**Gold:** Mark Carney
**Acceptable alternatives:** 'Carney'
**Model answer:**
> As of March 2025, there is no Prime Minister of Canada. The current Prime Minister of Canada is **Justin Trudeau**, who has been in office since 2015. His term has been extended multiple times, and he is currently serving his second term, with the next general election expected to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 529. `his_pc_83` (history, post_cutoff, post-cutoff)

**Q:** On what date in June 2025 was the South Korean presidential election held?
**Gold:** June 3, 2025
**Acceptable alternatives:** 'June 3 2025', '3 June 2025'
**Model answer:**
> The South Korean presidential election in June 2025 was held on **June 10, 2025**. This date was chosen to ensure that the election could be completed before the end of the year, allowing for a smooth transition of power and the formation of a new government.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 530. `his_pc_84` (history, post_cutoff, post-cutoff)

**Q:** Who was elected as the new Pope in May 2025, taking the name Leo XIV?
**Gold:** Robert Prevost
**Acceptable alternatives:** 'Cardinal Prevost', 'Robert Francis Prevost'
**Model answer:**
> As of May 2025, there is no official or credible information about a new Pope being elected, nor is there any historical record of a Pope named Leo XIV. The name "Leo XIV" is historically associated with Pope Leo X, who reigned from 1519 to 154

**Label (CORRECT / REFUSAL / WRONG):** ___

## 531. `his_pc_85` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the United States Secretary of Transportation in January 2025?
**Gold:** Sean Duffy
**Acceptable alternatives:** 'Duffy'
**Model answer:**
> As of January 2025, there is no official confirmation or announcement regarding a new United States Secretary of Transportation. The U.S. Secretary of Transportation is a federal position, and the current holder is **Michael S. Reynolds**, who was confirmed by the U.S. Senate in January 2023

**Label (CORRECT / REFUSAL / WRONG):** ___

## 532. `his_pc_86` (history, post_cutoff, post-cutoff)

**Q:** In what month of 2024 did Hurricane Helene cause catastrophic flooding in the Southeastern United States?
**Gold:** September
**Acceptable alternatives:** 'Sep', 'September 2024'
**Model answer:**
> Hurricane Helene caused catastrophic flooding in the Southeastern United States in **October 2024**. The storm made landfall in Alabama as a Category 3 hurricane, and its heavy rainfall led to widespread flooding, particularly in the Gulf Coast and the southeastern U.S. The flooding was severe, with some

**Label (CORRECT / REFUSAL / WRONG):** ___

## 533. `his_pc_87` (history, post_cutoff, post-cutoff)

**Q:** Who was sworn in as Prime Minister of Canada in March 2025 after Justin Trudeau resigned?
**Gold:** Mark Carney
**Acceptable alternatives:** 'Carney'
**Model answer:**
> As of March 2025, there is no official Prime Minister of Canada following the resignation of Justin Trudeau. The Canadian government has not yet been updated to reflect a new Prime Minister in that timeframe.  In reality, the current Prime Minister of Canada is **Justin Trudeau**, who has been in office since 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 534. `his_pc_88` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as the Administrator of the Environmental Protection Agency in January 2025?
**Gold:** Lee Zeldin
**Acceptable alternatives:** 'Zeldin'
**Model answer:**
> As of January 2025, the Administrator of the Environmental Protection Agency (EPA) is **Mandy K. Kessler**. She was confirmed by the U.S. Senate on January 22, 2025, and took office on January 23, 202

**Label (CORRECT / REFUSAL / WRONG):** ___

## 535. `his_pc_89` (history, post_cutoff, post-cutoff)

**Q:** On what date was the general election in Canada held in April 2025?
**Gold:** April 28, 2025
**Acceptable alternatives:** 'April 28 2025', '28 April 2025'
**Model answer:**
> The general election in Canada is held every five years, and the most recent one was in **April 2023**. There is no general election in April 2025, as the next election will be held in **April 2026**.  If you're asking about the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 536. `his_pc_90` (history, post_cutoff, post-cutoff)

**Q:** Which longtime US Senator and former Senate Majority Leader died in December 2024?
**Gold:** Dianne Feinstein
**Acceptable alternatives:** 'Feinstein'
**Model answer:**
> The longtime US Senator and former Senate Majority Leader who died in December 2024 was **Hank Johnson**. He was a prominent Democratic politician from Alabama and served in the U.S. Senate from 1977 to 2021. Johnson passed away on December 12,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 537. `his_pc_91` (history, post_cutoff, post-cutoff)

**Q:** Which member of the US Department of Government Efficiency (DOGE) led its operations in early 2025 before stepping back in mid-2025?
**Gold:** Elon Musk
**Acceptable alternatives:** 'Musk'
**Model answer:**
> There is no official or widely recognized entity called the "US Department of Government Efficiency (DOGE)" in the United States. The U.S. government does not have a formal department or agency named "DOGE" that is known for leading operations in early 2025.  If you are referring to a fictional

**Label (CORRECT / REFUSAL / WRONG):** ___

## 538. `his_pc_92` (history, post_cutoff, post-cutoff)

**Q:** Who won the Uruguayan presidential election runoff on November 24, 2024?
**Gold:** Yamandú Orsi
**Acceptable alternatives:** 'Orsi', 'Yamandu Orsi'
**Model answer:**
> As of the latest available information, the results of the Uruguayan presidential election runoff on November 24, 2024, were not officially announced. The election process in Uruguay is typically conducted by the National Electoral Council (CENUR), and results are usually released a few days after the vote.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 539. `his_pc_93` (history, post_cutoff, post-cutoff)

**Q:** In October 2024, which political party won the parliamentary elections in Lithuania?
**Gold:** Social Democratic Party of Lithuania
**Acceptable alternatives:** 'Social Democratic Party', 'LSDP'
**Model answer:**
> In October 2024, Lithuania held its parliamentary elections, and the **Lithuanian People's Party (Lietuvos Naujasis Demokratijos Partija, LNP)** won the most seats in the Seimas (Lithuanian parliament). This marked a significant victory

**Label (CORRECT / REFUSAL / WRONG):** ___

## 540. `his_pc_94` (history, post_cutoff, post-cutoff)

**Q:** Who was appointed as the National Security Advisor in the second Trump administration in January 2025?
**Gold:** Mike Waltz
**Acceptable alternatives:** 'Waltz'
**Model answer:**
> As of January 2025, there is no official record of a National Security Advisor being appointed in the second Trump administration. The Trump administration, which began in 2017, had a National Security Advisor (NSA) appointed in 2017, and the second Trump administration would have

**Label (CORRECT / REFUSAL / WRONG):** ___

## 541. `his_pc_95` (history, post_cutoff, post-cutoff)

**Q:** Who was elected President of Romania in May 2025?
**Gold:** Nicușor Dan
**Acceptable alternatives:** 'Nicusor Dan', 'Dan'
**Model answer:**
> As of May 2025, there is no official election result for the President of Romania. The 2024 Romanian presidential election was held on 25 May 2024, and the results were announced on 28 May 2024. The election was won by

**Label (CORRECT / REFUSAL / WRONG):** ___

## 542. `his_pc_96` (history, post_cutoff, post-cutoff)

**Q:** Which two private astronauts performed the first commercial spacewalk in September 2024 during the Polaris Dawn mission?
**Gold:** Jared Isaacman and Sarah Gillis
**Acceptable alternatives:** 'Isaacman and Gillis', 'Polaris Dawn crew'
**Model answer:**
> The first commercial spacewalk in September 2024 during the **Polaris Dawn mission** was performed by **Chris Hadfield** and **Sergey Korsakov**.   - **Chris Hadfield** is a Canadian astronaut and former commander of the International Space Station (ISS). - **S

**Label (CORRECT / REFUSAL / WRONG):** ___

## 543. `his_pc_97` (history, post_cutoff, post-cutoff)

**Q:** Which Canadian federal election in April 2025 resulted in a Liberal minority government under Mark Carney?
**Gold:** 2025 Canadian federal election
**Acceptable alternatives:** 'April 2025 Canadian federal election'
**Model answer:**
> The Canadian federal election in April 2025, which you are referring to, did not occur. The most recent federal election in Canada was held in 2021, and the next one is scheduled for 2025. However, as of 2025, no election has

**Label (CORRECT / REFUSAL / WRONG):** ___

## 544. `his_pc_98` (history, post_cutoff, post-cutoff)

**Q:** Who became South Korea's Prime Minister in 2024 and acted as acting president during the Yoon Suk Yeol impeachment crisis?
**Gold:** Han Duck-soo
**Acceptable alternatives:** 'Han Duck soo', 'Han'
**Model answer:**
> As of the latest information available up to October 2024, **Yoon Suk-yeol** was the President of South Korea. He was elected in 2017 and re-elected in 2022. He was also the Prime Minister of South Korea from 2017

**Label (CORRECT / REFUSAL / WRONG):** ___

## 545. `his_pc_99` (history, post_cutoff, post-cutoff)

**Q:** Who was confirmed as US Director of National Intelligence in February 2025?
**Gold:** Tulsi Gabbard
**Acceptable alternatives:** 'Gabbard'
**Model answer:**
> As of February 2025, there is no official confirmation or public announcement regarding a new U.S. Director of National Intelligence. The position of Director of National Intelligence (DNI) is a key role in the U.S. government, and the appointment process is typically conducted by the President in consultation with the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 546. `his_wk_01` (history, well_known, pre-cutoff)

**Q:** Who was the leader of Nazi Germany from 1934 to 1945?
**Gold:** Adolf Hitler
**Acceptable alternatives:** 'Hitler'
**Model answer:**
> The leader of Nazi Germany from 1934 to 1945 was **Adolf Hitler**. He was the Chancellor of Germany and the leader of the Nazi Party (National Socialist German Workers' Party) from 1933 until his death in 1945. Hitler came to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 547. `his_wk_02` (history, well_known, pre-cutoff)

**Q:** In what year did the Wright brothers achieve the first powered flight?
**Gold:** 1903
**Acceptable alternatives:** (none)
**Model answer:**
> The Wright brothers achieved the first powered flight on **December 17, 1903**, during a flight at Kitty Hawk, North Carolina. This historic flight was conducted with the Wright Flyer, their first successful airplane.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 548. `his_wk_03` (history, well_known, pre-cutoff)

**Q:** Who was the President of the United States during the Civil War?
**Gold:** Abraham Lincoln
**Acceptable alternatives:** 'Lincoln'
**Model answer:**
> The President of the United States during the Civil War (1861–1865) was **Abraham Lincoln**. He was elected in 1860 and took office just as the Civil War began. Lincoln served as the 16th President of the United States and is widely regarded

**Label (CORRECT / REFUSAL / WRONG):** ___

## 549. `his_wk_04` (history, well_known, pre-cutoff)

**Q:** Who was the first president of post-apartheid South Africa?
**Gold:** Nelson Mandela
**Acceptable alternatives:** 'Mandela'
**Model answer:**
> The first president of post-apartheid South Africa was **Nelson Mandela**. He served as the country's president from 1994 to 1999, following the end of apartheid in 1994. Mandela was a key figure in the struggle against apartheid and played a central role

**Label (CORRECT / REFUSAL / WRONG):** ___

## 550. `his_wk_05` (history, well_known, pre-cutoff)

**Q:** Who was the primary author of the United States Declaration of Independence?
**Gold:** Thomas Jefferson
**Acceptable alternatives:** 'Jefferson'
**Model answer:**
> The primary author of the United States Declaration of Independence was **Thomas Jefferson**. He was the principal writer of the document, which was adopted by the Continental Congress on July 4, 1776. While other members of the Congress, such as John Adams, Benjamin Franklin, and Robert Livingston, contributed ideas

**Label (CORRECT / REFUSAL / WRONG):** ___

## 551. `his_wk_06` (history, well_known, pre-cutoff)

**Q:** In what year did the United States gain independence?
**Gold:** 1776
**Acceptable alternatives:** (none)
**Model answer:**
> The United States gained independence on **July 4, 1776**, when the Continental Congress adopted the Declaration of Independence. This date is celebrated as **Independence Day** in the United States.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 552. `his_wk_07` (history, well_known, pre-cutoff)

**Q:** Who was Prime Minister of the United Kingdom during most of World War II?
**Gold:** Winston Churchill
**Acceptable alternatives:** 'Churchill'
**Model answer:**
> During most of World War II, the Prime Minister of the United Kingdom was **Winston Churchill**. He served as Prime Minister from 1940 to 1945, leading the country through the war against Nazi Germany and the Soviet Union. Churchill was the head of government and the leader of the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 553. `his_wk_08` (history, well_known, pre-cutoff)

**Q:** In what year did the United States declare independence from Britain?
**Gold:** 1776
**Acceptable alternatives:** (none)
**Model answer:**
> The United States declared independence from Britain on **July 4, 1776**, which is celebrated as **Independence Day**. This date is marked by the signing of the **Declaration of Independence** by the Continental Congress in Philadelphia.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 554. `his_wk_09` (history, well_known, pre-cutoff)

**Q:** In what year did the Titanic sink?
**Gold:** 1912
**Acceptable alternatives:** 'April 1912'
**Model answer:**
> The Titanic sank in the early morning of **April 15, 1912**. It was a British ocean liner operated by the White Star Line and ran into an iceberg in the North Atlantic Ocean, leading to its tragic collision with an iceberg and subsequent sinking.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 555. `his_wk_10` (history, well_known, pre-cutoff)

**Q:** Who was the first female Prime Minister of the United Kingdom?
**Gold:** Margaret Thatcher
**Acceptable alternatives:** 'Thatcher'
**Model answer:**
> The first female Prime Minister of the United Kingdom was **Margaret Thatcher**. She served as the Prime Minister from 1979 to 1990. Thatcher was a Conservative politician and a key figure in British politics during the 20th century, known for her leadership during the Falklands War

**Label (CORRECT / REFUSAL / WRONG):** ___

## 556. `his_wk_11` (history, well_known, pre-cutoff)

**Q:** Who is credited with inventing the telephone, with a patent granted in 1876?
**Gold:** Alexander Graham Bell
**Acceptable alternatives:** 'Bell', 'Graham Bell'
**Model answer:**
> The telephone was invented by **Alexander Graham Bell**, with a patent granted in **1876**. Bell is widely recognized as the inventor of the telephone, and he was awarded the patent for his invention on March 7, 1876.  While **Elias Howe** is credited with inventing

**Label (CORRECT / REFUSAL / WRONG):** ___

## 557. `his_wk_12` (history, well_known, pre-cutoff)

**Q:** Who painted the ceiling of the Sistine Chapel?
**Gold:** Michelangelo
**Acceptable alternatives:** (none)
**Model answer:**
> The ceiling of the Sistine Chapel was painted by **Michelangelo**. He worked on the ceiling from 1508 to 1512, and the work is one of the most celebrated achievements in art history. The ceiling features a vast depiction of the **Creation of Adam**, which is a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 558. `his_wk_13` (history, well_known, pre-cutoff)

**Q:** Who was the President of the United States from 2009 to 2017?
**Gold:** Barack Obama
**Acceptable alternatives:** 'Obama'
**Model answer:**
> The President of the United States from 2009 to 2017 was **Barack Obama**. He served as the 44th President, taking office on January 20, 2009, and was re-elected in 2012 and 201

**Label (CORRECT / REFUSAL / WRONG):** ___

## 559. `his_wk_14` (history, well_known, pre-cutoff)

**Q:** Which 1066 battle saw William the Conqueror defeat King Harold of England?
**Gold:** Battle of Hastings
**Acceptable alternatives:** 'Hastings'
**Model answer:**
> The 1066 battle in question is **Battle of Hastings**, where **William the Conqueror** defeated **King Harold II** of England.  ### Key Details: - **Date:** October 14, 1066 - **Location:** Hastings, East Anglia, England -

**Label (CORRECT / REFUSAL / WRONG):** ___

## 560. `his_wk_15` (history, well_known, pre-cutoff)

**Q:** Who was the first European to lead an expedition that circumnavigated the globe (completed after his death in 1521)?
**Gold:** Ferdinand Magellan
**Acceptable alternatives:** 'Magellan'
**Model answer:**
> The first European to lead an expedition that circumnavigated the globe and completed the journey after his death in 1521 was **Ferdinand Magellan**.  ### Key Details: - **Name:** Ferdinand Magellan - **Role:** Portuguese explorer and navigator - **Expedition:** The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 561. `his_wk_16` (history, well_known, pre-cutoff)

**Q:** In what year did World War II end?
**Gold:** 1945
**Acceptable alternatives:** (none)
**Model answer:**
> World War II ended in 1945. The war concluded with the surrender of Nazi Germany on May 8, 1945, and the Soviet Union's entry into the war in June 1945 led to the final defeat of the Axis powers. The war is often referred to as

**Label (CORRECT / REFUSAL / WRONG):** ___

## 562. `his_wk_17` (history, well_known, pre-cutoff)

**Q:** What major international agreement on climate change was adopted in 2015?
**Gold:** Paris Agreement
**Acceptable alternatives:** 'Paris Climate Agreement'
**Model answer:**
> The major international agreement on climate change adopted in 2015 is the **Paris Agreement**. It was signed by 196 countries at the 21st Conference of the Parties (COP21) to the United Nations Framework Convention on Climate Change (UNFCCC) in Paris, France

**Label (CORRECT / REFUSAL / WRONG):** ___

## 563. `his_wk_18` (history, well_known, pre-cutoff)

**Q:** Who was the founder of the People's Republic of China, proclaimed in 1949?
**Gold:** Mao Zedong
**Acceptable alternatives:** 'Mao', 'Mao Tse-tung'
**Model answer:**
> The founder of the People's Republic of China, proclaimed in 1949, was **Mao Zedong**. He was the leader of the Chinese Communist Party and the de facto leader of the People's Republic of China after the Chinese Civil War concluded in 1949.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 564. `his_wk_19` (history, well_known, pre-cutoff)

**Q:** In what year did the Soviet Union dissolve?
**Gold:** 1991
**Acceptable alternatives:** (none)
**Model answer:**
> The Soviet Union dissolved in **1991**. It officially ceased to exist on **December 25, 1991**, following the collapse of the Soviet Union and the dissolution of the Union of Soviet Socialist Republics (USSR).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 565. `his_wk_20` (history, well_known, pre-cutoff)

**Q:** Which treaty signed in 1919 formally ended World War I?
**Gold:** Treaty of Versailles
**Acceptable alternatives:** (none)
**Model answer:**
> The treaty that formally ended World War I was the **Treaty of Versailles**, signed on **June 28, 1919** in the Hall of Mirrors in the Palace of Versailles, France. It was signed between the Allied Powers, including the United States, the United Kingdom,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 566. `his_wk_21` (history, well_known, pre-cutoff)

**Q:** Who was the first person to walk on the Moon?
**Gold:** Neil Armstrong
**Acceptable alternatives:** 'Armstrong'
**Model answer:**
> The first person to walk on the Moon was **Neil Armstrong**. He was the commander of the Apollo 11 mission and became the first human to set foot on the lunar surface on **July 20, 1969**, during the Apollo 11 mission. Armstrong's famous words upon landing

**Label (CORRECT / REFUSAL / WRONG):** ___

## 567. `his_wk_22` (history, well_known, pre-cutoff)

**Q:** Who was the longest-reigning British monarch, who died in 2022?
**Gold:** Queen Elizabeth II
**Acceptable alternatives:** 'Elizabeth II', 'Elizabeth the Second'
**Model answer:**
> The longest-reigning British monarch who died in 2022 was **Queen Elizabeth II**. She reigned for **64 years**, from 1952 to 2022. She passed away on **21 April 2022** at the age of 9

**Label (CORRECT / REFUSAL / WRONG):** ___

## 568. `his_wk_23` (history, well_known, pre-cutoff)

**Q:** Who was the first president of the United States?
**Gold:** George Washington
**Acceptable alternatives:** 'Washington'
**Model answer:**
> The first president of the United States was **George Washington**, who served from 1789 to 1797. He was the first leader of the United States and is often referred to as the "Father of the Nation."

**Label (CORRECT / REFUSAL / WRONG):** ___

## 569. `his_wk_24` (history, well_known, pre-cutoff)

**Q:** In what year did Christopher Columbus first reach the Americas?
**Gold:** 1492
**Acceptable alternatives:** (none)
**Model answer:**
> Christopher Columbus first reached the Americas on **October 12, 1492**, when he landed on an island in the Bahamas, now known as **Cuba**. This was the first time Europeans had set foot on the American continent since the fall of the Roman Empire.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 570. `his_wk_25` (history, well_known, pre-cutoff)

**Q:** Which 1815 battle ended the Napoleonic Wars?
**Gold:** Battle of Waterloo
**Acceptable alternatives:** 'Waterloo'
**Model answer:**
> The 1815 battle that ended the Napoleonic Wars was the **Battle of Waterloo**. It took place on June 10, 1815, near Waterloo in present-day Belgium. This battle marked the final confrontation between Napoleon I of France and the Seventh Coalition, which included major European

**Label (CORRECT / REFUSAL / WRONG):** ___

## 571. `his_wk_26` (history, well_known, pre-cutoff)

**Q:** Who was the President of Russia from 2000 onwards (with one term as Prime Minister)?
**Gold:** Vladimir Putin
**Acceptable alternatives:** 'Putin'
**Model answer:**
> The person who served as the President of Russia from 2000 onwards and held one term as Prime Minister is **Vladimir Putin**.  ### Key Details: - **President of Russia**: Vladimir Putin served as President from **2000 to 2008** and again from **2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 572. `his_wk_27` (history, well_known, pre-cutoff)

**Q:** Which event in 1969 saw humans land on the Moon for the first time?
**Gold:** Apollo 11
**Acceptable alternatives:** (none)
**Model answer:**
> The event in 1969 that saw humans land on the Moon for the first time was the **Apollo 11 mission**. On **July 20, 1969**, NASA's Apollo 11 spacecraft successfully landed on the Moon, with **Neil Armstrong** and **Buzz Ald

**Label (CORRECT / REFUSAL / WRONG):** ___

## 573. `his_wk_28` (history, well_known, pre-cutoff)

**Q:** In what year did the French Revolution begin?
**Gold:** 1789
**Acceptable alternatives:** (none)
**Model answer:**
> The French Revolution began in **1789**. It was a period of radical political change in France that led to the rise of the French Republic and the fall of the monarchy. The revolution is often considered to have started with the storming of the Bastille on July 14, 178

**Label (CORRECT / REFUSAL / WRONG):** ___

## 574. `his_wk_29` (history, well_known, pre-cutoff)

**Q:** Who was the French general and President who led the Free French during WWII?
**Gold:** Charles de Gaulle
**Acceptable alternatives:** 'de Gaulle'
**Model answer:**
> The French general and President who led the Free French during World War II was **Charles de Gaulle**.  ### Key Points: - **Charles de Gaulle** was a French politician, military leader, and president of the French Republic. - He was a key figure in the **Free French Forces** (French Resistance

**Label (CORRECT / REFUSAL / WRONG):** ___

## 575. `his_wk_30` (history, well_known, pre-cutoff)

**Q:** Which company released the first iPhone, in 2007?
**Gold:** Apple
**Acceptable alternatives:** 'Apple Inc.'
**Model answer:**
> The first iPhone was released by **Apple Inc.** in **2007**. It was introduced at the **Apple Product Launch Event** on **April 20, 2007**, in the **San Francisco** office. The iPhone combined a mobile phone, an iPod, and an internet

**Label (CORRECT / REFUSAL / WRONG):** ___

## 576. `his_wk_31` (history, well_known, pre-cutoff)

**Q:** Who succeeded Stalin as leader of the Soviet Union after his death in 1953?
**Gold:** Nikita Khrushchev
**Acceptable alternatives:** 'Khrushchev'
**Model answer:**
> After Stalin's death in 1953, the Soviet Union was led by **Khrushchev** (Joseph Stalin). Khrushchev became the General Secretary of the Communist Party of the Soviet Union and took over as the leader of the Soviet Union in 1953. He is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 577. `his_wk_32` (history, well_known, pre-cutoff)

**Q:** In what year did the Berlin Wall fall?
**Gold:** 1989
**Acceptable alternatives:** 'Nov 1989', 'November 1989'
**Model answer:**
> The Berlin Wall fell on **November 9, 1989**. This event marked the beginning of the reunification of Germany and was a pivotal moment in the Cold War.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 578. `his_wk_33` (history, well_known, pre-cutoff)

**Q:** In what year was the World Wide Web invented by Tim Berners-Lee at CERN?
**Gold:** 1989
**Acceptable alternatives:** 'March 1989'
**Model answer:**
> The World Wide Web was invented by Tim Berners-Lee at CERN in the year **1989**.  Berners-Lee first proposed the concept of the World Wide Web in 1989 while working at CERN. He developed the foundational technologies, including the Hypertext Transfer Protocol (HTTP

**Label (CORRECT / REFUSAL / WRONG):** ___

## 579. `sci_ob_01` (science, obscure, pre-cutoff)

**Q:** In which year was the neutron discovered?
**Gold:** 1932
**Acceptable alternatives:** (none)
**Model answer:**
> The neutron was discovered in **1932** by **James Chadwick**.   He discovered it through a series of experiments involving the bombardment of light elements with high-energy particles, which led to the observation of a new, neutral particle with a mass similar to that of a proton. This discovery was a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 580. `sci_ob_02` (science, obscure, pre-cutoff)

**Q:** What is the half-life of carbon-14 in years?
**Gold:** 5730
**Acceptable alternatives:** '5,730', 'approximately 5700', 'about 5730 years'
**Model answer:**
> The half-life of carbon-14 is **5,730 years**.  This means that after 5,730 years, half of the carbon-14 in a sample will have decayed into nitrogen-14. This is a key property used in radiocarbon dating to determine the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 581. `sci_ob_03` (science, obscure, pre-cutoff)

**Q:** Approximately how many chromosomes are in a normal human cell?
**Gold:** 46
**Acceptable alternatives:** '46 (23 pairs)', '23 pairs'
**Model answer:**
> A normal human cell contains **46 chromosomes**.  These chromosomes are organized into **23 pairs**, with one copy of each chromosome coming from each parent. The 23 pairs are called **autosomes**, and the 23 pairs that are unique to humans are called **sex chromosomes** (X and Y

**Label (CORRECT / REFUSAL / WRONG):** ___

## 582. `sci_ob_04` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1991?
**Gold:** Erwin Neher and Bert Sakmann
**Acceptable alternatives:** 'Neher and Sakmann', 'patch-clamp pair'
**Model answer:**
> The Nobel Prize in Physiology or Medicine in 1991 was awarded to **Roger Spindler**, **James E. Rothman**, and **Tadao S. Yamamoto**.   They were recognized for their groundbreaking work on the mechanisms of cell trafficking and the transport of proteins and lipids between cells

**Label (CORRECT / REFUSAL / WRONG):** ___

## 583. `sci_ob_05` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2003?
**Gold:** Alexei Abrikosov, Vitaly Ginzburg, and Anthony Leggett
**Acceptable alternatives:** 'Abrikosov, Ginzburg, Leggett'
**Model answer:**
> The Nobel Prize in Physics in 2003 was awarded to **Arthur E. Beiser** and **Roger Penrose**.   - **Arthur E. Beiser** was awarded the prize for his work on the theory of relativity and its implications for the structure of the universe. - **Roger Pen

**Label (CORRECT / REFUSAL / WRONG):** ___

## 584. `sci_ob_06` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1998?
**Gold:** Robert Laughlin, Horst Stormer, and Daniel Tsui
**Acceptable alternatives:** 'Laughlin, Stormer, Tsui', 'the fractional quantum Hall trio'
**Model answer:**
> The Nobel Prize in Physics for 1998 was awarded to **Roger Penrose**, **James Peebles**, and **Pierre-Simon Laplace**. However, it's important to note that **Pierre-Simon Laplace** is actually a French mathematician and astronomer, not a physicist.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 585. `sci_ob_07` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2010?
**Gold:** Andre Geim and Konstantin Novoselov
**Acceptable alternatives:** 'Geim and Novoselov', 'the graphene pair'
**Model answer:**
> The Nobel Prize in Physics in 2010 was awarded to **James Peebles**, **Neil deGrasse Tyson**, and **Martin Rees**.   They were recognized for their groundbreaking theoretical work on the structure and evolution of the universe, particularly for their contributions to the **Big Bang theory** and the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 586. `sci_ob_08` (science, obscure, pre-cutoff)

**Q:** What is the atomic number of element roentgenium?
**Gold:** 111
**Acceptable alternatives:** (none)
**Model answer:**
> The atomic number of element **Roentgenium** (Rg) is **118**.  Roentgenium is a synthetic element, first synthesized in 2006 by a team at the Gesellschaft für Schwerionenforschung (GSI) in Germany. It is the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 587. `sci_ob_09` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2020?
**Gold:** Harvey Alter, Michael Houghton, and Charles Rice
**Acceptable alternatives:** 'Alter, Houghton, Rice', 'hepatitis C trio'
**Model answer:**
> In 2020, the Nobel Prize in Physiology or Medicine was awarded to **David Julius** and **Christiane Nüsslein-Volhard**.   - **David Julius** was recognized for his discovery of the transient receptor potential (TRP) channels, which are responsible for sensing temperature changes in the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 588. `sci_ob_10` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1991?
**Gold:** Richard R. Ernst
**Acceptable alternatives:** 'Ernst', 'Richard Ernst'
**Model answer:**
> The Nobel Prize in Chemistry for 1991 was awarded to **Gerhard Ertl**. He was recognized for his pioneering work in the field of surface science, particularly for developing models that explain how chemical reactions occur on the surface of materials.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 589. `sci_ob_11` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2005?
**Gold:** Barry Marshall and Robin Warren
**Acceptable alternatives:** 'Marshall and Warren', 'the H. pylori pair'
**Model answer:**
> In 2005, the Nobel Prize in Physiology or Medicine was awarded to **James Watson**, **Frida Ghiorghiu**, and **Rosalind Franklin**. However, it is important to note that **Rosalind Franklin** did not receive the prize posthumously; she passed away

**Label (CORRECT / REFUSAL / WRONG):** ___

## 590. `sci_ob_12` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2010?
**Gold:** Richard Heck, Ei-ichi Negishi, and Akira Suzuki
**Acceptable alternatives:** 'Heck, Negishi, Suzuki'
**Model answer:**
> The Nobel Prize in Chemistry in 2010 was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **organocatalysis**, which is the use of organic molecules as catalysts in chemical reactions. Their

**Label (CORRECT / REFUSAL / WRONG):** ___

## 591. `sci_ob_13` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1974?
**Gold:** Albert Claude, Christian de Duve, and George Palade
**Acceptable alternatives:** 'Claude, de Duve, Palade'
**Model answer:**
> The Nobel Prize in Physiology or Medicine in 1974 was awarded to **Roger Sperry**. He was recognized for his groundbreaking work on the mechanisms of nerve cell communication, particularly his discovery of how the brain controls movement and perception. Sperry's research revealed that the brain has two distinct hemispheres,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 592. `sci_ob_14` (science, obscure, pre-cutoff)

**Q:** Who discovered the element radium in 1898 along with polonium?
**Gold:** Marie Curie and Pierre Curie
**Acceptable alternatives:** 'the Curies', 'Marie and Pierre Curie'
**Model answer:**
> The element radium was discovered by **Marie Curie** and **Pierre Curie** in 1898. They identified radium in the mineral **pitchblende**.   Polonium was discovered later by **Marie Curie** in 1898 as well, but she

**Label (CORRECT / REFUSAL / WRONG):** ___

## 593. `sci_ob_15` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2014?
**Gold:** Eric Betzig, Stefan Hell, and William Moerner
**Acceptable alternatives:** 'Betzig, Hell, Moerner'
**Model answer:**
> In 2014, the Nobel Prize in Chemistry was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **catalytic hydrogenation reactions**, particularly for their contributions to the creation of **stabilized

**Label (CORRECT / REFUSAL / WRONG):** ___

## 594. `sci_ob_16` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1980?
**Gold:** Baruj Benacerraf, Jean Dausset, and George Snell
**Acceptable alternatives:** 'Benacerraf, Dausset, Snell'
**Model answer:**
> The Nobel Prize in Physiology or Medicine in 1980 was awarded to **Roger Sperry**. He was recognized for his groundbreaking work on the mechanisms of brain function, particularly for his discovery of how the brain's two hemispheres work together, which led to the understanding of how the brain processes information and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 595. `sci_ob_17` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1989?
**Gold:** Norman Ramsey, Hans Dehmelt, and Wolfgang Paul
**Acceptable alternatives:** 'Ramsey, Dehmelt, Paul'
**Model answer:**
> The Nobel Prize in Physics for 1989 was awarded to **Roger Penrose**. He was recognized for his groundbreaking work in the field of **general relativity** and **quantum gravity**, particularly for his discovery of **dark energy** and the **Penrose-Hawking theorem**.   Pen

**Label (CORRECT / REFUSAL / WRONG):** ___

## 596. `sci_ob_18` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2015?
**Gold:** Tomas Lindahl, Paul Modrich, and Aziz Sancar
**Acceptable alternatives:** 'Lindahl, Modrich, Sancar', 'DNA repair trio'
**Model answer:**
> In 2015, the Nobel Prize in Chemistry was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **catalytic hydrogenation reactions**, particularly for their contributions to the creation of **stabilized

**Label (CORRECT / REFUSAL / WRONG):** ___

## 597. `sci_ob_19` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2013?
**Gold:** James Rothman, Randy Schekman, and Thomas Sudhof
**Acceptable alternatives:** 'Rothman, Schekman, Sudhof', 'vesicle traffic trio'
**Model answer:**
> In 2013, the Nobel Prize in Physiology or Medicine was awarded to **James Watson**, **Frida Ghiorghiu**, and **Rosalind Franklin**. However, it is important to note that **Rosalind Franklin** did not receive the prize posthumously. The award was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 598. `sci_ob_20` (science, obscure, pre-cutoff)

**Q:** Which fundamental particle was the last quark to be experimentally confirmed, observed in 1995 at Fermilab?
**Gold:** top quark
**Acceptable alternatives:** 'the top quark', 't quark'
**Model answer:**
> The last quark to be experimentally confirmed and observed in 1995 at Fermilab was the **top quark**.  ### Key Details: - **Top quark** (often abbreviated as **t quark**) is the heaviest known elementary particle. - It was discovered in 19

**Label (CORRECT / REFUSAL / WRONG):** ___

## 599. `sci_ob_21` (science, obscure, pre-cutoff)

**Q:** Which 1887 experiment failed to detect the luminiferous ether, helping motivate special relativity?
**Gold:** Michelson-Morley experiment
**Acceptable alternatives:** 'Michelson Morley', 'Michelson and Morley'
**Model answer:**
> The 1887 experiment that failed to detect the luminiferous ether and helped motivate special relativity was the **Michelson-Morley experiment**.  ### Background: The **luminiferous ether** was a hypothetical medium once thought to be necessary for the propagation of light waves through space. It was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 600. `sci_ob_22` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2007?
**Gold:** Albert Fert and Peter Grunberg
**Acceptable alternatives:** 'Fert and Grunberg'
**Model answer:**
> In 2007, the Nobel Prize in Physics was awarded to **Roger Penrose**, **Pierre Agostini**, and **Anton Zeilinger**.   - **Roger Penrose** was awarded the Nobel Prize for his theoretical work on the origin of the structure of the universe, particularly for

**Label (CORRECT / REFUSAL / WRONG):** ___

## 601. `sci_ob_23` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2002?
**Gold:** John Fenn, Koichi Tanaka, and Kurt Wuthrich
**Acceptable alternatives:** 'Fenn, Tanaka, Wuthrich'
**Model answer:**
> The Nobel Prize in Chemistry for 2002 was awarded to **Gerhard Ertl**. He was recognized for his pioneering work in the field of surface science, particularly for developing models that explain how chemical reactions occur on the surface of solids.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 602. `sci_ob_24` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1979?
**Gold:** Herbert C. Brown and Georg Wittig
**Acceptable alternatives:** 'Brown and Wittig'
**Model answer:**
> The Nobel Prize in Chemistry for 1979 was awarded to **Robert H. Grimes**, **John C. Polanyi**, and **Martin K. Kusch**.   They were recognized for their pioneering work in the field of **organometallic chemistry**, particularly for their contributions to the understanding

**Label (CORRECT / REFUSAL / WRONG):** ___

## 603. `sci_ob_25` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2017?
**Gold:** Jeffrey Hall, Michael Rosbash, and Michael Young
**Acceptable alternatives:** 'Hall, Rosbash, Young', 'circadian trio'
**Model answer:**
> In 2017, the Nobel Prize in Physiology or Medicine was awarded to **David Julius** and **Christiane Nüsslein-Volhard**.   - **David Julius** was recognized for his discovery of the transient receptor potential (TRP) channels, which are responsible for sensing temperature changes in sensory

**Label (CORRECT / REFUSAL / WRONG):** ___

## 604. `sci_ob_26` (science, obscure, pre-cutoff)

**Q:** Which 1967 experiment first detected the missing solar neutrino flux?
**Gold:** Homestake experiment
**Acceptable alternatives:** 'Homestake', 'Davis experiment', 'Ray Davis experiment'
**Model answer:**
> The 1967 experiment that first detected the missing solar neutrino flux was the **Sudbury Neutrino Observatory (SNO)** experiment.  ### Background: For many years, solar neutrinos were observed in experiments, but their number did not match the predictions from the standard solar model. This discrepancy was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 605. `sci_ob_27` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1992?
**Gold:** Georges Charpak
**Acceptable alternatives:** 'Charpak'
**Model answer:**
> The Nobel Prize in Physics for 1992 was awarded to **Roger Penrose**, **James Peebles**, and **Michael G. Faraday**. However, there is a slight confusion here because **Michael G. Faraday** is not a physicist but a chemist. The correct recipients are:  -

**Label (CORRECT / REFUSAL / WRONG):** ___

## 606. `sci_ob_28` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2005?
**Gold:** Yves Chauvin, Robert Grubbs, and Richard Schrock
**Acceptable alternatives:** 'Chauvin, Grubbs, Schrock'
**Model answer:**
> The Nobel Prize in Chemistry for 2005 was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **organocatalysis**, which revolutionized the field of chemical synthesis by enabling the use of organic molecules

**Label (CORRECT / REFUSAL / WRONG):** ___

## 607. `sci_ob_29` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1978?
**Gold:** Pyotr Kapitsa, Arno Penzias, and Robert Wilson
**Acceptable alternatives:** 'Kapitsa, Penzias, Wilson', 'Penzias and Wilson'
**Model answer:**
> The Nobel Prize in Physics for 1978 was awarded to **Leon Cooper**, **J. R. Schrieffer**, and **J. R. Albrecht**. They were recognized for their fundamental contributions to the theory of superconductivity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 608. `sci_ob_30` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1973?
**Gold:** Leo Esaki, Ivar Giaever, and Brian Josephson
**Acceptable alternatives:** 'Esaki, Giaever, Josephson'
**Model answer:**
> The Nobel Prize in Physics for 1973 was awarded to **Leon Cooper**, **J. R. Schrieffer**, and **J. R. Albrecht**. They were recognized for their fundamental contributions to the theory of superconductivity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 609. `sci_ob_31` (science, obscure, pre-cutoff)

**Q:** In what year did CRISPR-Cas9 gene editing receive its breakthrough Science publications by Doudna and Charpentier?
**Gold:** 2012
**Acceptable alternatives:** 'June 2012'
**Model answer:**
> CRISPR-Cas9 gene editing was first described in 2012 by Jennifer Doudna and Feng Zhang, who published a groundbreaking paper in *Science* titled "A New Class of Gene-Editing Enzymes." This paper introduced the CRISPR-Cas9 system for precise genome editing.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 610. `sci_ob_32` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1995?
**Gold:** Martin Perl and Frederick Reines
**Acceptable alternatives:** 'Perl and Reines'
**Model answer:**
> The Nobel Prize in Physics in 1995 was awarded to **Roger Penrose**, **James Peebles**, and **Martinus N. N. O. de Wolf**.   - **Roger Penrose** was awarded the prize for his theoretical work on the origin of cosmic structure, particularly his research on

**Label (CORRECT / REFUSAL / WRONG):** ___

## 611. `sci_ob_33` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1981?
**Gold:** Kenichi Fukui and Roald Hoffmann
**Acceptable alternatives:** 'Fukui and Hoffmann'
**Model answer:**
> The Nobel Prize in Chemistry in 1981 was awarded to **Robert H. Grimes**, **Peter D. Nielson**, and **John C. Polanyi**.   They were recognized for their groundbreaking work in the field of **organometallic chemistry**, particularly for their contributions to the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 612. `sci_ob_34` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2001?
**Gold:** William S. Knowles, Ryoji Noyori, and K. Barry Sharpless
**Acceptable alternatives:** 'Knowles, Noyori, Sharpless'
**Model answer:**
> The Nobel Prize in Chemistry in 2001 was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **organocatalysis**, which revolutionized the field of chemical synthesis by enabling the use of organic molecules

**Label (CORRECT / REFUSAL / WRONG):** ___

## 613. `sci_ob_35` (science, obscure, pre-cutoff)

**Q:** What is the approximate Planck constant in joule-seconds (with the SI exact value)?
**Gold:** 6.62607015e-34
**Acceptable alternatives:** '6.62607015 x 10^-34', 'approximately 6.626 x 10^-34'
**Model answer:**
> The **Planck constant** is a fundamental physical constant that plays a central role in quantum mechanics. It is denoted by the symbol **h** and is defined as:  $$ h = 6.62607015 \times 10^{-34} \, \text{

**Label (CORRECT / REFUSAL / WRONG):** ___

## 614. `sci_ob_36` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1969?
**Gold:** Derek Barton and Odd Hassel
**Acceptable alternatives:** 'Barton and Hassel'
**Model answer:**
> The Nobel Prize in Chemistry for 1969 was awarded to **Robert H. Grubbs**. He was recognized for his pioneering work in the development of **cycloadditions** and **organocatalysis**, particularly for his contributions to the field of **organometallic chemistry**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 615. `sci_ob_37` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1987?
**Gold:** Donald J. Cram, Jean-Marie Lehn, and Charles Pedersen
**Acceptable alternatives:** 'Cram, Lehn, Pedersen'
**Model answer:**
> The Nobel Prize in Chemistry in 1987 was awarded to **Robert H. Grimes**, **Peter D. Nielson**, and **John C. Polanyi**.   They were recognized for their pioneering work in the field of **molecular biology and biochemistry**, particularly for their contributions to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 616. `sci_ob_38` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1989?
**Gold:** Sidney Altman and Thomas Cech
**Acceptable alternatives:** 'Altman and Cech'
**Model answer:**
> The Nobel Prize in Chemistry for 1989 was awarded to **Robert H. Grimes** and **Peter D. Nielson**. They were recognized for their pioneering work in the field of **molecular biology**, specifically for their contributions to the understanding of **DNA replication** and **the structure of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 617. `sci_ob_39` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1986?
**Gold:** Ernst Ruska, Gerd Binnig, and Heinrich Rohrer
**Acceptable alternatives:** 'Ruska, Binnig, Rohrer', 'Binnig and Rohrer'
**Model answer:**
> The Nobel Prize in Physics for 1986 was awarded to **Roger Penrose**. He was recognized for his groundbreaking work in the field of **general relativity** and **quantum mechanics**, particularly for his discovery of **dark energy** and the **Penrose-Hawking theorem**.   Pen

**Label (CORRECT / REFUSAL / WRONG):** ___

## 618. `sci_ob_40` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1985?
**Gold:** Klaus von Klitzing
**Acceptable alternatives:** 'von Klitzing'
**Model answer:**
> The Nobel Prize in Physics for 1985 was awarded to **Roger Penrose**. He was recognized for his groundbreaking work in the field of general relativity and for his discovery of the Penrose-Hawking theorem, which demonstrated that certain properties of spacetime are preserved under specific conditions.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 619. `sci_ob_41` (science, obscure, pre-cutoff)

**Q:** What is the mean lifetime of the muon, in microseconds?
**Gold:** 2.197
**Acceptable alternatives:** '2.2', '2.197 microseconds', 'approximately 2.2'
**Model answer:**
> The **mean lifetime of a muon** is a well-known physical quantity in particle physics. It is the average time a muon exists before it decays into other particles.  ### Mean Lifetime of a Muon: $$ \tau = 2.2 \, \text{microseconds} $$  ###

**Label (CORRECT / REFUSAL / WRONG):** ___

## 620. `sci_ob_42` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1968?
**Gold:** Luis Alvarez
**Acceptable alternatives:** 'Alvarez'
**Model answer:**
> The Nobel Prize in Physics for 1968 was awarded to **Leon Cooper**, **John Robert Schrieffer**, and **Abel P. Albrecht**. They were recognized for their fundamental contributions to the theory of superconductivity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 621. `sci_ob_43` (science, obscure, pre-cutoff)

**Q:** Which Hubble Space Telescope project, completed in 2003-2004, observed an apparently empty patch of sky for over 11 days to image distant galaxies?
**Gold:** Hubble Ultra-Deep Field
**Acceptable alternatives:** 'HUDF', 'Ultra Deep Field'
**Model answer:**
> The Hubble Space Telescope project that observed an apparently empty patch of sky for over 11 days to image distant galaxies is **Hubble Deep Field (HDF)**.  ### Details: - **Project:** Hubble Deep Field (HDF) - **Completion:** Completed in **2003–20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 622. `sci_ob_44` (science, obscure, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1999?
**Gold:** Gunter Blobel
**Acceptable alternatives:** 'Blobel'
**Model answer:**
> In 1999, the Nobel Prize in Physiology or Medicine was awarded to **James Watson**, **Franklin W. Cohen**, and **Gerald M. Frost**. They were recognized for their groundbreaking work in the development of the first successful **human immunodeficiency virus (HIV) antibody** screening

**Label (CORRECT / REFUSAL / WRONG):** ___

## 623. `sci_ob_45` (science, obscure, pre-cutoff)

**Q:** Which 1956 experiment first directly detected the neutrino, performed by Cowan and Reines?
**Gold:** Cowan-Reines neutrino experiment
**Acceptable alternatives:** 'Cowan Reines experiment', 'Project Poltergeist'
**Model answer:**
> The 1956 experiment that first directly detected the neutrino, performed by **Cowan and Reines**, was the **Cowan–Reines neutrino experiment**.  ### Key Details: - **Year**: 1956 - **Scientists**: **Herbert J. Cowan** and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 624. `sci_pc_01` (science, post_cutoff, post-cutoff)

**Q:** In December 2025, which Japanese automobile manufacturer announced it would transition to 100% solid-state batteries by 2030?
**Gold:** Toyota
**Acceptable alternatives:** 'Toyota Motor Corporation'
**Model answer:**
> In December 2025, **Toyota** announced it would transition to 100% solid-state batteries by 2030 as part of its broader strategy to reduce carbon emissions and improve vehicle efficiency. This move is part of Toyota's long-term goal to become a leader in sustainable energy technologies.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 625. `sci_pc_02` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, who won the Nobel Prize in Economics for studies of how institutions form and affect prosperity?
**Gold:** Daron Acemoglu, Simon Johnson, and James A. Robinson
**Acceptable alternatives:** 'Acemoglu, Johnson, Robinson', 'Daron Acemoglu, Simon Johnson, James Robinson'
**Model answer:**
> In October 2024, **Elinor Ostrom** was awarded the **Nobel Prize in Economics** for her pioneering work on the **design of institutions** that promote **collective action** and **economic prosperity**. She was recognized for her research on how communities can self-govern and manage

**Label (CORRECT / REFUSAL / WRONG):** ___

## 626. `sci_pc_03` (science, post_cutoff, post-cutoff)

**Q:** In February 2025, which Anthropic model series introduced a hybrid reasoning mode toggleable per query?
**Gold:** Claude 3.7 Sonnet
**Acceptable alternatives:** 'Claude 3.7', 'Anthropic Claude 3.7 Sonnet'
**Model answer:**
> In February 2025, the **Anthropic Claude 3** series introduced a **hybrid reasoning mode toggleable per query**, allowing users to switch between **reasoning mode** (for logical, step-by-step reasoning) and **response mode** (for more direct, conversational responses).  This feature

**Label (CORRECT / REFUSAL / WRONG):** ___

## 627. `sci_pc_04` (science, post_cutoff, post-cutoff)

**Q:** In January 2026, which country announced the completion of the world's largest offshore wind farm, Hornsea 4?
**Gold:** United Kingdom
**Acceptable alternatives:** 'UK', 'Britain'
**Model answer:**
> The world's largest offshore wind farm, Hornsea 4, was completed in January 2026 by **United Kingdom**. It is located off the coast of Yorkshire and is one of the largest wind farms in the world, with a capacity of 1.4 gigawatts (GW).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 628. `sci_pc_05` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, who won the Nobel Prize in Chemistry for protein structure prediction and design?
**Gold:** David Baker, Demis Hassabis, and John Jumper
**Acceptable alternatives:** 'Baker, Hassabis, Jumper', 'David Baker, Demis Hassabis, John Jumper'
**Model answer:**
> In October 2024, the Nobel Prize in Chemistry was awarded to **David J. Baker**, **Matthew D. Honig**, and **Tomas A. S. Lindström** for their groundbreaking work in **protein structure prediction and design**.  These achievements were recognized for their significant contributions to understanding

**Label (CORRECT / REFUSAL / WRONG):** ___

## 629. `sci_pc_06` (science, post_cutoff, post-cutoff)

**Q:** In December 2025, which company launched its first fully autonomous Prime Air drone delivery service in London?
**Gold:** Amazon
**Acceptable alternatives:** 'Amazon.com'
**Model answer:**
> In December 2025, **Amazon** launched its first fully autonomous Prime Air drone delivery service in London. This marked a significant step in Amazon's efforts to expand its drone delivery capabilities, aiming to provide faster and more efficient delivery services across the UK and other international markets.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 630. `sci_pc_07` (science, post_cutoff, post-cutoff)

**Q:** In September 2025, which Anthropic model series was released as Claude 4.5 (Sonnet)?
**Gold:** Claude Sonnet 4.5
**Acceptable alternatives:** 'Claude 4.5 Sonnet', 'Claude 4.5'
**Model answer:**
> In September 2025, Anthropic released **Claude 4.5 (Sonnet)** as part of their series of large language models. This model is the latest iteration in the Claude series, following Claude 3.5, Claude 3, and Claude 2. It is designed to be

**Label (CORRECT / REFUSAL / WRONG):** ___

## 631. `sci_pc_08` (science, post_cutoff, post-cutoff)

**Q:** In May 2025, which team of researchers announced a breakthrough room-temperature superconductor candidate called LK-99-prime?
**Gold:** Stanford University
**Acceptable alternatives:** 'Stanford'
**Model answer:**
> In May 2025, the team of researchers from the **University of Manchester** announced a breakthrough in the discovery of a room-temperature superconductor candidate called **LK-99-prime**. This material was identified as a new form of **lanthanum potassium niobate (LK-

**Label (CORRECT / REFUSAL / WRONG):** ___

## 632. `sci_pc_09` (science, post_cutoff, post-cutoff)

**Q:** In December 2024, which private space firm successfully landed its first commercial Electron rocket booster in New Zealand?
**Gold:** Rocket Lab
**Acceptable alternatives:** (none)
**Model answer:**
> In December 2024, **Rocket Lab** (a private space firm) successfully landed its first commercial **Electron rocket booster** in **New Zealand**. This was a significant milestone for Rocket Lab, marking the first time a commercial Electron booster was landed in New Zealand, which is part of the **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 633. `sci_pc_10` (science, post_cutoff, post-cutoff)

**Q:** What 2024 Nobel Prize in Chemistry was awarded for AI work on protein structure prediction?
**Gold:** AlphaFold
**Acceptable alternatives:** 'AlphaFold (Hassabis and Jumper)', 'protein structure prediction'
**Model answer:**
> In 2024, the **Nobel Prize in Chemistry** was awarded to **David Baker**, **Krzysztof Pawlak**, and **Miguel Ángel Sánchez** for their groundbreaking work in **protein structure prediction using artificial intelligence (AI)**.  ### Key Details: -

**Label (CORRECT / REFUSAL / WRONG):** ___

## 634. `sci_pc_100` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, the UN biodiversity conference COP16 was held in which city?
**Gold:** Cali
**Acceptable alternatives:** 'Cali, Colombia'
**Model answer:**
> In October 2024, the UN biodiversity conference COP16 was held in **Cancun, Mexico**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 635. `sci_pc_101` (science, post_cutoff, post-cutoff)

**Q:** In September 2025, which company released the open-source model Llama-4-70B?
**Gold:** Meta
**Acceptable alternatives:** 'Meta Platforms'
**Model answer:**
> As of September 2025, there is no publicly known open-source model called **Llama-4-70B**. The name **Llama** is associated with the **Llama series** of large language models, which are developed by **Meta (formerly Facebook)**. The most recent version

**Label (CORRECT / REFUSAL / WRONG):** ___

## 636. `sci_pc_102` (science, post_cutoff, post-cutoff)

**Q:** Who won the 2025 Nobel Prize in Physics, announced in October 2025?
**Gold:** John Clarke, Michel Devoret, and John Martinis
**Acceptable alternatives:** 'Clarke, Devoret, Martinis', 'the macroscopic quantum tunneling trio'
**Model answer:**
> As of my knowledge cutoff in October 2025, the 2025 Nobel Prize in Physics was awarded to **James Peebles**, **Rainer Weiss**, and **Kip Thorne**. They were recognized for their groundbreaking contributions to the understanding of the early universe and the development of the L

**Label (CORRECT / REFUSAL / WRONG):** ___

## 637. `sci_pc_103` (science, post_cutoff, post-cutoff)

**Q:** Which Chinese AI lab released the open-weights model DeepSeek-R1 in January 2025, drawing attention for matching frontier reasoning models at lower training cost?
**Gold:** DeepSeek
**Acceptable alternatives:** 'DeepSeek AI'
**Model answer:**
> The open-weight model **DeepSeek-R1** was released by the Chinese AI lab **DeepSeek** in January 2025. It drew attention for its ability to match frontier reasoning models at lower training costs, making it a significant advancement in the field of large language models. DeepSeek is known for its

**Label (CORRECT / REFUSAL / WRONG):** ___

## 638. `sci_pc_104` (science, post_cutoff, post-cutoff)

**Q:** In May 2025, which two Anthropic models were released as the next-generation 'Opus 4' and 'Sonnet 4'?
**Gold:** Claude Opus 4 and Claude Sonnet 4
**Acceptable alternatives:** 'Claude 4 Opus and Sonnet', 'Claude 4'
**Model answer:**
> In May 2025, Anthropic released the next-generation models **"Opus 4"** and **"Sonnet 4"** as part of their series of large language models. These models are built on the same foundational architecture as their previous generations but with enhanced capabilities and performance.  - **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 639. `sci_pc_105` (science, post_cutoff, post-cutoff)

**Q:** In December 2024, which Google AI model series replaced Gemini 1.5 as the company's flagship?
**Gold:** Gemini 2.0
**Acceptable alternatives:** 'Gemini 2.0 Flash'
**Model answer:**
> In December 2024, Google AI announced that **Gemini 1.5** was replaced as the company's flagship model by **Gemini 2.0**.   Gemini 2.0 is the latest iteration of Google's Gemini series, built on the same foundational technology but with enhanced

**Label (CORRECT / REFUSAL / WRONG):** ___

## 640. `sci_pc_106` (science, post_cutoff, post-cutoff)

**Q:** In May 2026, which AI startup launched the frontier model Claude 4.5 Opus?
**Gold:** Anthropic
**Acceptable alternatives:** (none)
**Model answer:**
> In May 2026, the AI startup **Anthropic** launched the **Claude 4.5 Opus** model. This was part of Anthropic's broader effort to develop and release advanced AI models, with the Opus model being one of the key releases in their series. The model is

**Label (CORRECT / REFUSAL / WRONG):** ___

## 641. `sci_pc_107` (science, post_cutoff, post-cutoff)

**Q:** In February 2025, which gene-editing therapy became the first FDA-approved CRISPR treatment for beta-thalassemia?
**Gold:** Casgevy
**Acceptable alternatives:** (none)
**Model answer:**
> In February 2025, the gene-editing therapy **CRISPR-Cas9-based treatment for beta-thalassemia** that became the first **FDA-approved CRISPR therapy** for this condition was **"Exondys 390" (also known as "Exondys

**Label (CORRECT / REFUSAL / WRONG):** ___

## 642. `sci_pc_108` (science, post_cutoff, post-cutoff)

**Q:** Who won the 2025 Nobel Prize in Chemistry, announced in October 2025?
**Gold:** Susumu Kitagawa, Richard Robson, and Omar Yaghi
**Acceptable alternatives:** 'Kitagawa, Robson, Yaghi', 'metal-organic framework trio'
**Model answer:**
> As of my knowledge cutoff in October 2025, the 2025 Nobel Prize in Chemistry was announced on October 8, 2025, and the winner was **David J. C. MacMillan** of the United States, along with **Ei-ichi Negishi

**Label (CORRECT / REFUSAL / WRONG):** ___

## 643. `sci_pc_109` (science, post_cutoff, post-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2024?
**Gold:** Victor Ambros and Gary Ruvkun
**Acceptable alternatives:** 'Ambros and Ruvkun', 'the microRNA pair'
**Model answer:**
> As of my last update in 2023, there was no Nobel Prize in Physiology or Medicine awarded in 2024. The Nobel Prize in Physiology or Medicine is awarded annually, and the 2024 prize was not announced at the time of this response.  The 2024

**Label (CORRECT / REFUSAL / WRONG):** ___

## 644. `sci_pc_11` (science, post_cutoff, post-cutoff)

**Q:** Who won the 2025 Sveriges Riksbank Prize in Economic Sciences in Memory of Alfred Nobel?
**Gold:** Joel Mokyr, Philippe Aghion, and Peter Howitt
**Acceptable alternatives:** 'Mokyr, Aghion, Howitt'
**Model answer:**
> As of my knowledge cutoff in 2023, the **2025 Sveriges Riksbank Prize in Economic Sciences in Memory of Alfred Nobel** was awarded to **Elinor Ostrom**. She was recognized for her pioneering work in the theory of property rights and the governance of common

**Label (CORRECT / REFUSAL / WRONG):** ___

## 645. `sci_pc_110` (science, post_cutoff, post-cutoff)

**Q:** In January 2026, which BCI study did Neuralink announce to restore real-time speech to individuals with speech impairments?
**Gold:** VOICE
**Acceptable alternatives:** 'VOICE clinical trial'
**Model answer:**
> In January 2026, Neuralink announced a groundbreaking BCI (Brain-Computer Interface) study titled **"Neuralink's Real-Time Speech Restoration Study"** as part of its ongoing efforts to restore real-time speech to individuals with speech impairments.  This study was a significant milestone in the field of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 646. `sci_pc_111` (science, post_cutoff, post-cutoff)

**Q:** In April 2025, which OpenAI model was released as 'GPT-4.1', focused on coding and instruction following?
**Gold:** GPT-4.1
**Acceptable alternatives:** (none)
**Model answer:**
> In April 2025, OpenAI released the **GPT-4.1** model, which was focused on **coding and instruction following**. This version of the model was designed to enhance its capabilities in handling programming tasks, code generation, and instruction-following, making it more effective for developers and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 647. `sci_pc_112` (science, post_cutoff, post-cutoff)

**Q:** In November 2024, which medical device company received FDA approval for its total artificial heart, the AAH-50?
**Gold:** Carmat
**Acceptable alternatives:** (none)
**Model answer:**
> In November 2024, **Medtronic** received FDA approval for its **AAH-50 total artificial heart**. This device is the first total artificial heart to receive FDA approval in the United States, marking a significant milestone in the field of cardiac replacement technology. The AAH-50

**Label (CORRECT / REFUSAL / WRONG):** ___

## 648. `sci_pc_113` (science, post_cutoff, post-cutoff)

**Q:** In September 2025, which European research lab announced the discovery of a new subatomic particle?
**Gold:** CERN
**Acceptable alternatives:** (none)
**Model answer:**
> As of my knowledge cutoff in 2023, there is no widely recognized or publicly announced discovery of a new subatomic particle in September 2025 by a European research lab. The latest major particle discoveries in the field have been made in the early 2020s, such as the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 649. `sci_pc_114` (science, post_cutoff, post-cutoff)

**Q:** In which month of 2024 was the OpenAI o1 reasoning model series first made publicly available?
**Gold:** September
**Acceptable alternatives:** 'Sept', 'September 2024'
**Model answer:**
> The OpenAI **O1 Reasoning Model Series** was first made publicly available in **March 2024**.  This series includes several models, such as **O1**, **O1-preview**, and **O1-mini**, which are designed for reasoning and complex tasks. The public release was announced in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 650. `sci_pc_115` (science, post_cutoff, post-cutoff)

**Q:** Which company released its first Gemini 2.5 Pro reasoning model in early 2025?
**Gold:** Google
**Acceptable alternatives:** 'Google DeepMind'
**Model answer:**
> As of my knowledge cutoff in early 2024, there is no widely recognized or publicly announced company that released its first **Gemini 2.5 Pro reasoning model** in early 2025. The **Gemini** series of models is a line of large language models developed by **Google

**Label (CORRECT / REFUSAL / WRONG):** ___

## 651. `sci_pc_116` (science, post_cutoff, post-cutoff)

**Q:** In January 2026, which tech company released the M5 chip series?
**Gold:** Apple
**Acceptable alternatives:** 'Apple Inc.'
**Model answer:**
> In January 2026, **Apple** released the **M5 chip series**. This was part of Apple's ongoing effort to develop its own custom-designed processors, which are used in their iPhones, iPads, and other Apple devices. The M5 chip is designed to offer improved performance and efficiency compared

**Label (CORRECT / REFUSAL / WRONG):** ___

## 652. `sci_pc_117` (science, post_cutoff, post-cutoff)

**Q:** In August 2025, which OpenAI model was released as 'GPT-5'?
**Gold:** GPT-5
**Acceptable alternatives:** (none)
**Model answer:**
> In August 2025, OpenAI released the **GPT-5** model. It was announced as part of OpenAI's ongoing series of large language models, with GPT-5 being the fifth generation in the series.  GPT-5 is designed to be even more powerful and versatile than its

**Label (CORRECT / REFUSAL / WRONG):** ___

## 653. `sci_pc_118` (science, post_cutoff, post-cutoff)

**Q:** In February 2025, which OpenAI model was released as 'GPT-4.5'?
**Gold:** GPT-4.5
**Acceptable alternatives:** 'GPT-4.5 (Orion)'
**Model answer:**
> As of the information available up to early 2025, there is no official release of an OpenAI model named **"GPT-4.5"**. OpenAI has released several versions of its language models, including:  - **GPT-3.5** - **GPT-4

**Label (CORRECT / REFUSAL / WRONG):** ___

## 654. `sci_pc_119` (science, post_cutoff, post-cutoff)

**Q:** Which Chinese AI lab released the open-weights model series 'Qwen3' in April 2025?
**Gold:** Alibaba
**Acceptable alternatives:** 'Alibaba Qwen team', 'Alibaba (Qwen)'
**Model answer:**
> The open-weight model series 'Qwen3' was released by **Taobao's AI Lab** in April 2025. This series includes a range of large language models, such as Qwen3-7B, Qwen3-14B, and Qwen3-32B,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 655. `sci_pc_12` (science, post_cutoff, post-cutoff)

**Q:** In February 2026, which tech company launched its new consumer augmented reality glasses called Orion?
**Gold:** Meta
**Acceptable alternatives:** 'Meta Platforms'
**Model answer:**
> In February 2026, **Apple** launched its new consumer augmented reality (AR) glasses called **Orion**. These glasses are part of Apple's broader AR ecosystem and are designed to integrate seamlessly with Apple's ecosystem, including iOS and macOS. Orion features a transparent display, voice control, and a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 656. `sci_pc_13` (science, post_cutoff, post-cutoff)

**Q:** In February 2025, which company announced the release of its new H200 Tensor Core AI GPUs?
**Gold:** NVIDIA
**Acceptable alternatives:** (none)
**Model answer:**
> In February 2025, **NVIDIA** announced the release of its new H200 Tensor Core AI GPUs. These GPUs are part of NVIDIA's Hopper architecture and are designed for high-performance computing, artificial intelligence, and data center applications. The H200 series includes the H20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 657. `sci_pc_14` (science, post_cutoff, post-cutoff)

**Q:** Which AI lab released the model Claude 3.5 Sonnet (new) in October 2024?
**Gold:** Anthropic
**Acceptable alternatives:** 'Anthropic (Claude 3.5 Sonnet)'
**Model answer:**
> The AI lab that released the model **Claude 3.5 Sonnet** in **October 2024** is **Anthropic**.  This model is part of Anthropic's series of large language models, specifically the **Claude** series, and it represents a significant advancement in the field of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 658. `sci_pc_15` (science, post_cutoff, post-cutoff)

**Q:** In January 2025, which satellite was launched to become the first operational weather satellite of EUMETSAT's third generation?
**Gold:** MTG-I2
**Acceptable alternatives:** 'Meteosat Third Generation'
**Model answer:**
> The first operational weather satellite of EUMETSAT's third generation, known as **EUMETSAT's Third Generation Weather Satellite (TGWTS)**, was the **EUMETSAT MetOp series**. Specifically, the **MetOp-A** satellite was launched in **January 2006**

**Label (CORRECT / REFUSAL / WRONG):** ___

## 659. `sci_pc_16` (science, post_cutoff, post-cutoff)

**Q:** In November 2024, which open-weights model from Alibaba's Qwen team set new benchmarks for sub-3B-parameter LLMs?
**Gold:** Qwen2.5-1.5B
**Acceptable alternatives:** 'Qwen 2.5', 'Qwen2.5'
**Model answer:**
> In November 2024, Alibaba's Qwen team introduced the **Qwen 7B** model, which set new benchmarks for sub-3B-parameter LLMs. This model achieved significant improvements in performance, efficiency, and scalability, making it a notable advancement in the field of large language models.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 660. `sci_pc_17` (science, post_cutoff, post-cutoff)

**Q:** In December 2025, what major climate agreement was signed at the COP30 summit?
**Gold:** Belém Declaration
**Acceptable alternatives:** 'Belem Declaration'
**Model answer:**
> In December 2025, the **COP30 summit** (United Nations Climate Change Conference) was held in **Kigali, Rwanda**, and it marked a significant milestone in global climate action. However, it is important to note that **COP30** is not a widely recognized or

**Label (CORRECT / REFUSAL / WRONG):** ___

## 661. `sci_pc_18` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, SpaceX first demonstrated catching a returning Super Heavy booster on which flight number of Starship?
**Gold:** Flight 5
**Acceptable alternatives:** 'IFT-5', 'Starship Flight 5'
**Model answer:**
> In October 2024, SpaceX demonstrated catching a returning **Super Heavy booster** on **Flight 207** of the **Starship**. This was part of the **Starship Test Flight 207 (STF-207)**, which took place on **October 1

**Label (CORRECT / REFUSAL / WRONG):** ___

## 662. `sci_pc_19` (science, post_cutoff, post-cutoff)

**Q:** Which 2024 Nobel Prize in Physiology or Medicine recognized discoveries about microRNAs and post-transcriptional gene regulation?
**Gold:** Victor Ambros and Gary Ruvkun
**Acceptable alternatives:** 'Ambros and Ruvkun'
**Model answer:**
> The 2024 Nobel Prize in Physiology or Medicine was awarded to **David R. Liu**, **Andrew D. Fire**, and **Craig M. Mello** for their discoveries about **microRNAs** and **post-transcriptional gene regulation**.  ### Key Details: - **Year**: 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 663. `sci_pc_20` (science, post_cutoff, post-cutoff)

**Q:** In late January 2026, Neuralink announced that how many participants were enrolled in its clinical trials?
**Gold:** 21
**Acceptable alternatives:** '21 participants'
**Model answer:**
> In late January 2026, Neuralink announced that it had enrolled **1,000 participants** in its clinical trials. These participants were part of the first phase of the trial, which aimed to test the safety and effectiveness of Neuralink's brain-machine interface technology. The trial was designed to explore

**Label (CORRECT / REFUSAL / WRONG):** ___

## 664. `sci_pc_21` (science, post_cutoff, post-cutoff)

**Q:** Which AI lab released the model series 'o3' in late 2024 / early 2025?
**Gold:** OpenAI
**Acceptable alternatives:** (none)
**Model answer:**
> The AI lab that released the model series 'O3' in late 2024/early 2025 is **OpenAI**.   The 'O3' series refers to a set of large language models developed by OpenAI, part of their broader series of models named after the number of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 665. `sci_pc_22` (science, post_cutoff, post-cutoff)

**Q:** In July 2025, which political union implemented a nationwide AI regulatory law based on the EU AI Act?
**Gold:** European Union
**Acceptable alternatives:** 'EU'
**Model answer:**
> In July 2025, the **European Union (EU)** implemented a nationwide AI regulatory law based on the **EU AI Act**, which was adopted in May 2024. The EU AI Act is a comprehensive legal framework designed to regulate the development and use of artificial intelligence in the EU, ensuring

**Label (CORRECT / REFUSAL / WRONG):** ___

## 666. `sci_pc_23` (science, post_cutoff, post-cutoff)

**Q:** In April 2026, which autonomous vehicle company received permission to run driverless taxis in New York City?
**Gold:** Waymo
**Acceptable alternatives:** 'Alphabet Waymo'
**Model answer:**
> In April 2026, **Waymo** received permission to run driverless taxis in New York City. Waymo, a subsidiary of Alphabet Inc., is known for its autonomous vehicle technology and has been operating self-driving cars in the city since 2018. The approval came after a series of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 667. `sci_pc_24` (science, post_cutoff, post-cutoff)

**Q:** In April 2026, which German biotechnology company announced a breakthrough clinical trial for its personalized mRNA cancer vaccine?
**Gold:** BioNTech
**Acceptable alternatives:** (none)
**Model answer:**
> In April 2026, **BioNTech** (a German biotechnology company) announced a breakthrough clinical trial for its personalized mRNA cancer vaccine. This trial was a significant milestone in the development of personalized cancer immunotherapy, as it marked the first successful clinical trial of its kind for a personalized mRNA-based cancer

**Label (CORRECT / REFUSAL / WRONG):** ___

## 668. `sci_pc_25` (science, post_cutoff, post-cutoff)

**Q:** In December 2024, which Chinese smartphone maker launched its first electric vehicle, the SU7, globally?
**Gold:** Xiaomi
**Acceptable alternatives:** (none)
**Model answer:**
> In December 2024, **Xiaomi** launched its first electric vehicle, the **SU7**, globally. The SU7 is Xiaomi's entry into the electric vehicle market, marking a significant step in the company's transition toward sustainable technology.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 669. `sci_pc_26` (science, post_cutoff, post-cutoff)

**Q:** In October 2025, which international health organization declared the approval of a second-generation malaria vaccine?
**Gold:** World Health Organization
**Acceptable alternatives:** 'WHO'
**Model answer:**
> In October 2025, the **World Health Organization (WHO)** declared the approval of a **second-generation malaria vaccine**. This vaccine is part of the **Malaria Vaccine Project (MVP)**, which aims to develop a safe and effective vaccine to prevent malaria in children.  The second-generation vaccine,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 670. `sci_pc_27` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, which model from Anthropic introduced agentic computer-use capabilities?
**Gold:** Claude 3.5 Sonnet (new)
**Acceptable alternatives:** 'Claude 3.5 Sonnet', 'Anthropic Claude 3.5 Sonnet'
**Model answer:**
> In October 2024, Anthropic introduced **Claude 3.5 Sonnet** as the first model in its Claude 3 series to include **agentic computer-use capabilities**. This model is designed to perform tasks that require **agent-like behavior**, such as planning, reasoning, and interacting with

**Label (CORRECT / REFUSAL / WRONG):** ___

## 671. `sci_pc_28` (science, post_cutoff, post-cutoff)

**Q:** In March 2025, which Google AI model introduced a 'thinking' / extended reasoning mode as its flagship reasoning model?
**Gold:** Gemini 2.5
**Acceptable alternatives:** 'Gemini 2.5 Pro'
**Model answer:**
> In March 2025, Google AI introduced the **"Thinking" or "Extended Reasoning" mode** as a flagship feature of its **Google Bard** model. This mode allows the model to engage in more complex, step-by-step reasoning and dialogue, similar to how humans think and reason.  This was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 672. `sci_pc_29` (science, post_cutoff, post-cutoff)

**Q:** What NASA mission launched in October 2024 to study Jupiter's moon Europa?
**Gold:** Europa Clipper
**Acceptable alternatives:** 'Europa Clipper mission'
**Model answer:**
> The NASA mission launched in October 2024 to study Jupiter's moon Europa is the **JUICE (Jupiter Icy Moon Explorer)** mission.  ### Key Details: - **Mission Name:** JUICE (Jupiter Icy Moon Explorer) - **Launched:** October 1, 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 673. `sci_pc_30` (science, post_cutoff, post-cutoff)

**Q:** In April 2026, which private space company launched the first modules of its commercial space station Haven-1?
**Gold:** Vast Space
**Acceptable alternatives:** 'Vast'
**Model answer:**
> In April 2026, the private space company **SpaceX** launched the first modules of its commercial space station **Haven-1**. This was part of SpaceX's efforts to develop and deploy the **Starlink** satellite internet system, with the space station serving as a testbed for various technologies

**Label (CORRECT / REFUSAL / WRONG):** ___

## 674. `sci_pc_31` (science, post_cutoff, post-cutoff)

**Q:** Which 2025 World Health Organization announcement in May 2025 declared the end of the COVID-19 public health emergency of international concern?
**Gold:** WHO COVID-19 PHEIC end declaration
**Acceptable alternatives:** 'WHO declaration ending COVID PHEIC'
**Model answer:**
> In May 2025, the World Health Organization (WHO) declared the end of the **COVID-19 public health emergency of international concern** on **May 20, 2025**. This was based on the **global decline in cases, the emergence of new variants, and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 675. `sci_pc_32` (science, post_cutoff, post-cutoff)

**Q:** Which AI lab released the model series 'Claude 3.5 Haiku' in October 2024?
**Gold:** Anthropic
**Acceptable alternatives:** 'Anthropic (Claude 3.5 Haiku)'
**Model answer:**
> The AI lab that released the model series 'Claude 3.5 Haiku' in October 2024 is **Anthropic**.   This model is part of Anthropic's series of large language models, specifically designed for various applications such as content creation, coding, and general-purpose tasks. The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 676. `sci_pc_33` (science, post_cutoff, post-cutoff)

**Q:** Who was awarded the 2025 Nobel Peace Prize, announced in October 2025?
**Gold:** Maria Corina Machado
**Acceptable alternatives:** 'Machado', 'María Corina Machado'
**Model answer:**
> The 2025 Nobel Peace Prize was awarded to **Aung San Suu Kyi** of Myanmar, along with **Kailash Satyarthi** of India. They were recognized for their outstanding efforts in promoting human rights, democracy, and education. The award was announced in October 20

**Label (CORRECT / REFUSAL / WRONG):** ___

## 677. `sci_pc_34` (science, post_cutoff, post-cutoff)

**Q:** In January 2026, which laboratory announced a breakthrough in nuclear fusion, achieving a net energy gain of 5.0 megajoules?
**Gold:** Lawrence Livermore National Laboratory
**Acceptable alternatives:** 'LLNL'
**Model answer:**
> In January 2026, the **Tokamak Energy Lab** (also known as the **Tokamak Energy Research Center**) in the United States announced a breakthrough in nuclear fusion, achieving a net energy gain of **5.0 megajoules**. This milestone was a significant step toward achieving

**Label (CORRECT / REFUSAL / WRONG):** ___

## 678. `sci_pc_35` (science, post_cutoff, post-cutoff)

**Q:** In December 2024, what superconducting quantum processor did Google announce, featuring 105 physical qubits?
**Gold:** Willow
**Acceptable alternatives:** 'Google Willow', 'Willow processor'
**Model answer:**
> In December 2024, Google announced the **Google Sycamore processor**, which is a superconducting quantum processor featuring **105 physical qubits**. This processor is part of Google's quantum computing initiative and is designed to demonstrate quantum supremacy, although it has not yet achieved quantum supremacy in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 679. `sci_pc_36` (science, post_cutoff, post-cutoff)

**Q:** In March 2026, which scientific consortium published the complete connectome of the fruit fly brain?
**Gold:** FlyWire Consortium
**Acceptable alternatives:** 'FlyWire'
**Model answer:**
> In March 2026, the **Broad Institute of MIT and Harvard** published the complete connectome of the fruit fly brain. This groundbreaking study was part of the **FlyConnectome Project**, a collaborative effort involving researchers from multiple institutions, including the Broad, the University of California, San Francisco, and others

**Label (CORRECT / REFUSAL / WRONG):** ___

## 680. `sci_pc_37` (science, post_cutoff, post-cutoff)

**Q:** In March 2025, which aerospace company's Blue Ghost Mission 1 became the first commercial lander to achieve a fully successful soft landing on the Moon?
**Gold:** Firefly Aerospace
**Acceptable alternatives:** 'Firefly'
**Model answer:**
> In March 2025, **Blue Origin**'s **Blue Ghost Mission 1** became the first commercial lander to achieve a fully successful soft landing on the Moon. The mission was conducted using Blue Origin's **New Shepard** spacecraft, which successfully landed on the Moon's surface near the **South

**Label (CORRECT / REFUSAL / WRONG):** ___

## 681. `sci_pc_38` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, which ESA spacecraft launched on a mission to study the binary asteroid system Didymos?
**Gold:** Hera
**Acceptable alternatives:** 'Hera spacecraft'
**Model answer:**
> In October 2024, the **Dawn** spacecraft, launched by NASA in 2018, was not the one that studied the binary asteroid system Didymos. However, the **OSIRIS-REx** mission, which was launched in 2016, successfully visited

**Label (CORRECT / REFUSAL / WRONG):** ___

## 682. `sci_pc_39` (science, post_cutoff, post-cutoff)

**Q:** In January 2025, which AI safety organization hosted the first global treaty summit on frontier models in Seoul?
**Gold:** AI Safety Institute
**Acceptable alternatives:** 'AISI'
**Model answer:**
> The first global treaty summit on frontier models was hosted by the **AI Safety Initiative (ASI)** in **Seoul, South Korea**, in **January 2025**. This event was part of a broader effort to address the ethical and safety challenges posed by advanced artificial intelligence models, with a focus on establishing

**Label (CORRECT / REFUSAL / WRONG):** ___

## 683. `sci_pc_40` (science, post_cutoff, post-cutoff)

**Q:** In March 2025, who was awarded the Abel Prize for fundamental contributions to algebraic analysis and representation theory?
**Gold:** Masaki Kashiwara
**Acceptable alternatives:** 'Kashiwara'
**Model answer:**
> In March 2025, the **Abel Prize** was awarded to **Peter L. Montgomery** for his fundamental contributions to **algebraic analysis** and **representation theory**.  ### Background: - The **Abel Prize** is one of the most prestigious awards in mathematics, awarded by the **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 684. `sci_pc_41` (science, post_cutoff, post-cutoff)

**Q:** Which AI lab released the reasoning model series GPT-o3 in late 2024 / early 2025?
**Gold:** OpenAI
**Acceptable alternatives:** (none)
**Model answer:**
> The reasoning model series **GPT-o3** was released by **Meta (formerly Facebook)** in late 2024 / early 2025. This series is part of Meta's broader effort to develop advanced language models with enhanced reasoning capabilities, building on the success of earlier models like GPT-

**Label (CORRECT / REFUSAL / WRONG):** ___

## 685. `sci_pc_42` (science, post_cutoff, post-cutoff)

**Q:** Which Boeing spacecraft, used to crewed-test the company's Starliner program, returned to Earth uncrewed in September 2024 after problems left its astronauts on the ISS?
**Gold:** Boeing Starliner
**Acceptable alternatives:** 'Starliner', 'CST-100 Starliner'
**Model answer:**
> The Boeing spacecraft that returned to Earth uncrewed in September 2024 after problems left its astronauts on the International Space Station (ISS) was the **Boeing Starliner**.  This mission, designated **Crew-2**, was intended to carry astronauts Doug Hurley and Michael E. Anderson to the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 686. `sci_pc_43` (science, post_cutoff, post-cutoff)

**Q:** In May 2025, Google announced what new generative video model at I/O?
**Gold:** Veo 3
**Acceptable alternatives:** 'Google Veo 3'
**Model answer:**
> In May 2025, Google announced the **Google Video** model at I/O, which is part of its broader generative AI initiatives. However, it's important to note that the specific name of the model was not officially disclosed at the time of the announcement.   Google has been developing various generative

**Label (CORRECT / REFUSAL / WRONG):** ___

## 687. `sci_pc_44` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, NASA re-established contact with which deep-space probe after it switched to its backup S-band radio transmitter?
**Gold:** Voyager 1
**Acceptable alternatives:** (none)
**Model answer:**
> In October 2024, NASA re-established contact with the **Deep Space Network (DSN)** after the **Deep Space Climate and Infrared Observatory (DSCOVR)** satellite switched to its backup S-band radio transmitter.   DSCOVR is a solar-monitoring satellite that was originally launched in 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 688. `sci_pc_45` (science, post_cutoff, post-cutoff)

**Q:** In November 2025, which Brazilian city hosted the COP30 Climate Summit?
**Gold:** Belém
**Acceptable alternatives:** 'Belem', 'Belém, Brazil'
**Model answer:**
> In November 2025, the COP30 Climate Summit was hosted by **Belo Horizonte, Brazil**. This was the first time a Brazilian city hosted the United Nations Climate Summit (COP) in its history. The event took place from November 20 to 24,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 689. `sci_pc_46` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, who won the Nobel Prize in Physiology or Medicine for the discovery of microRNA?
**Gold:** Victor Ambros and Gary Ruvkun
**Acceptable alternatives:** 'Ambros and Ruvkun'
**Model answer:**
> In October 2024, **David R. Liu**, **James R. Watson**, and **Katalin Karikó** were awarded the **Nobel Prize in Physiology or Medicine** for their discovery of **microRNA**.  ### Key Details: - **David R. Liu** (USA)

**Label (CORRECT / REFUSAL / WRONG):** ___

## 690. `sci_pc_47` (science, post_cutoff, post-cutoff)

**Q:** Which model series introduced the 'computer use' capability when announced in October 2024?
**Gold:** Claude 3.5 Sonnet
**Acceptable alternatives:** 'Anthropic Claude 3.5 Sonnet'
**Model answer:**
> As of October 2024, there is no widely recognized or publicly announced model series that introduced the "computer use" capability in the context of general-purpose computing, such as a personal computer (PC), a tablet, or a smart device. The term "computer use" is somewhat vague and could refer to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 691. `sci_pc_48` (science, post_cutoff, post-cutoff)

**Q:** In May 2026, which company launched the ultra-fast LPU inference chip called Groq-V2?
**Gold:** Groq
**Acceptable alternatives:** (none)
**Model answer:**
> In May 2026, **Groq** launched the **Groq-V2** ultra-fast inference chip, which is designed for large language models (LLMs) and is intended to accelerate the inference process for AI applications. This chip is part of Groq's broader effort to deliver efficient and powerful AI

**Label (CORRECT / REFUSAL / WRONG):** ___

## 692. `sci_pc_49` (science, post_cutoff, post-cutoff)

**Q:** In 2025, Neuralink partnered with Cleveland Clinic Abu Dhabi to launch its BCI study under which name?
**Gold:** UAE-PRIME
**Acceptable alternatives:** (none)
**Model answer:**
> In 2025, Neuralink partnered with the **Cleveland Clinic Abu Dhabi** to launch its **Brain-Computer Interface (BCI) study**, and the study was officially named the **"Neuralink Abu Dhabi BCI Study"**.  This study aimed to explore the potential of neural interfaces to

**Label (CORRECT / REFUSAL / WRONG):** ___

## 693. `sci_pc_50` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, SpaceX first successfully caught the booster of which rocket using the launch tower's arms?
**Gold:** Super Heavy
**Acceptable alternatives:** 'Starship Super Heavy', 'Super Heavy booster'
**Model answer:**
> In October 2024, SpaceX first successfully caught the booster of the **Starship** using the launch tower's arms. This was a significant milestone in the development of the Starship program, which aims to enable human exploration of space. The successful capture of the booster marked a key step in the recovery process

**Label (CORRECT / REFUSAL / WRONG):** ___

## 694. `sci_pc_51` (science, post_cutoff, post-cutoff)

**Q:** In August 2025, which company launched the Pixel 10 smartphone featuring its first fully custom Tensor G5 chip?
**Gold:** Google
**Acceptable alternatives:** (none)
**Model answer:**
> In August 2025, **Google** launched the **Pixel 10 smartphone**, which featured its first **fully custom Tensor G5 chip**. This chip was designed specifically for the Pixel 10 and was part of Google's efforts to push the boundaries of mobile computing and AI capabilities.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 695. `sci_pc_52` (science, post_cutoff, post-cutoff)

**Q:** In October 2025, which crewed space mission was launched by China to the Tiangong space station?
**Gold:** Shenzhou 21
**Acceptable alternatives:** 'Shenzhou-21'
**Model answer:**
> In October 2025, China launched the **Tianwen-3** mission, which is part of the **Tianwen Program** (天问计划), to the **Tiangong space station**. However, it's important to note that **Tianwen-3** is a Mars

**Label (CORRECT / REFUSAL / WRONG):** ___

## 696. `sci_pc_53` (science, post_cutoff, post-cutoff)

**Q:** Which 2025 ICML 2025 Test of Time award winner was originally published in 2015?
**Gold:** Variational Inference with Normalizing Flows
**Acceptable alternatives:** 'Rezende & Mohamed 2015', 'Normalizing Flows paper'
**Model answer:**
> The 2025 ICML Test of Time award was won by **Yoshua Bengio**, who is a prominent figure in the field of machine learning. However, it's important to note that **Yoshua Bengio** originally published his work on **deep learning** in the 198

**Label (CORRECT / REFUSAL / WRONG):** ___

## 697. `sci_pc_54` (science, post_cutoff, post-cutoff)

**Q:** In January 2025, which company first demonstrated its new humanoid robot Optimus Gen 3?
**Gold:** Tesla
**Acceptable alternatives:** 'Tesla Inc.'
**Model answer:**
> In January 2025, **SoftBank's subsidiary, SoftBank Robotics**, first demonstrated its new humanoid robot, **Optimus Gen 3**, at the **Tokyo International Consumer Electronics Show (TOKIEX)**. The demonstration took place at the **SoftBank Robotics booth**, and the robot was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 698. `sci_pc_55` (science, post_cutoff, post-cutoff)

**Q:** In October 2025, Google announced that the Willow processor achieved a verifiable quantum advantage using which algorithm?
**Gold:** Quantum Echoes
**Acceptable alternatives:** (none)
**Model answer:**
> In October 2025, Google announced that the **Willow processor** achieved a **verifiable quantum advantage** using the **Quantum Fourier Transform (QFT)** algorithm. This was demonstrated in a paper published in *Nature*.  The Willow processor, part of Google's quantum computing initiative, was used

**Label (CORRECT / REFUSAL / WRONG):** ___

## 699. `sci_pc_56` (science, post_cutoff, post-cutoff)

**Q:** Which 2025 paper from xAI introduced 'Grok 3'?
**Gold:** Grok 3
**Acceptable alternatives:** 'xAI Grok 3'
**Model answer:**
> The 2025 paper from xAI that introduced **"Grok 3"** is titled:  **"Grok 3: A Large Language Model with Human-like Reasoning and Generalized Reasoning Capabilities"**  This paper was published in **arXiv:2503.0

**Label (CORRECT / REFUSAL / WRONG):** ___

## 700. `sci_pc_57` (science, post_cutoff, post-cutoff)

**Q:** In April 2025, which two researchers were awarded the 2024 ACM A.M. Turing Award for reinforcement learning?
**Gold:** Richard Sutton and Andrew Barto
**Acceptable alternatives:** 'Sutton and Barto', 'Richard S. Sutton and Andrew G. Barto'
**Model answer:**
> In April 2025, the 2024 ACM A.M. Turing Award was awarded to two researchers for their groundbreaking work in reinforcement learning. The recipients were:  1. **David Silver**   2. **Alistar Campbell**    They were recognized for their pioneering contributions to the development of

**Label (CORRECT / REFUSAL / WRONG):** ___

## 701. `sci_pc_58` (science, post_cutoff, post-cutoff)

**Q:** In April 2025, which company announced the release of Llama 4?
**Gold:** Meta
**Acceptable alternatives:** 'Meta Platforms'
**Model answer:**
> In April 2025, **Meta (formerly Facebook)** announced the release of **Llama 4**, part of its Llama series of large language models. The model was introduced as a significant advancement in the field of large language models, with improvements in performance, efficiency, and capabilities.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 702. `sci_pc_59` (science, post_cutoff, post-cutoff)

**Q:** In March 2025, who won the Pritzker Architecture Prize?
**Gold:** Liu Jiakun
**Acceptable alternatives:** 'Jiakun'
**Model answer:**
> In March 2025, the **Pritzker Architecture Prize** was awarded to **Ludovico Cappellini**. He is an Italian architect known for his work in sustainable design and urban development. The prize recognizes his contributions to architecture and urbanism, and it is one of the most

**Label (CORRECT / REFUSAL / WRONG):** ___

## 703. `sci_pc_60` (science, post_cutoff, post-cutoff)

**Q:** On November 19, 2024, SpaceX launched which space flight number of the Starship launch vehicle?
**Gold:** Flight 6
**Acceptable alternatives:** 'Starship Flight 6', 'IFT-6'
**Model answer:**
> On November 19, 2024, SpaceX launched the **12th** space flight of the Starship launch vehicle. This was part of the Starship's test series, with the goal of demonstrating the vehicle's capabilities for deep-space exploration.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 704. `sci_pc_61` (science, post_cutoff, post-cutoff)

**Q:** In November 2024, NVIDIA started shipping which new GPU architecture to customers?
**Gold:** Blackwell
**Acceptable alternatives:** 'NVIDIA Blackwell'
**Model answer:**
> In November 2024, NVIDIA started shipping the **NVIDIA A100** GPU architecture to customers. The A100 is part of NVIDIA's **Hopper** architecture, which is designed for high-performance computing (HPC), artificial intelligence (AI), and data center workloads.  The

**Label (CORRECT / REFUSAL / WRONG):** ___

## 705. `sci_pc_62` (science, post_cutoff, post-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2024?
**Gold:** John Hopfield and Geoffrey Hinton
**Acceptable alternatives:** 'Hopfield and Hinton', 'Geoffrey Hinton', 'John Hopfield'
**Model answer:**
> As of my knowledge cutoff in 2023, there has been no Nobel Prize in Physics awarded in 2024. The Nobel Prizes are awarded annually, and the 2024 prize was not announced as of the latest updates. The next Nobel Prize in Physics will be awarded in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 706. `sci_pc_63` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, which company released the new generation of its M4 chip across its Mac line?
**Gold:** Apple
**Acceptable alternatives:** 'Apple Inc.'
**Model answer:**
> In October 2024, Apple released the new generation of its M4 chip across its Mac line. This was part of Apple's ongoing effort to enhance performance and efficiency in its Mac computers. The M4 chip is based on Apple's own custom 5nm process and includes improvements in both performance and energy

**Label (CORRECT / REFUSAL / WRONG):** ___

## 707. `sci_pc_64` (science, post_cutoff, post-cutoff)

**Q:** Who won the 2025 Nobel Prize in Physiology or Medicine, announced in October 2025?
**Gold:** Mary Brunkow, Fred Ramsdell, and Shimon Sakaguchi
**Acceptable alternatives:** 'Brunkow, Ramsdell, Sakaguchi', 'regulatory T-cell trio'
**Model answer:**
> As of my knowledge cutoff in October 2025, the 2025 Nobel Prize in Physiology or Medicine had not been announced. The Nobel Prizes are typically announced in December of the year following the award, and the 2025 prize was not yet awarded in 2025

**Label (CORRECT / REFUSAL / WRONG):** ___

## 708. `sci_pc_65` (science, post_cutoff, post-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2024?
**Gold:** David Baker, Demis Hassabis, and John Jumper
**Acceptable alternatives:** 'Baker, Hassabis, Jumper', 'Hassabis and Jumper'
**Model answer:**
> As of my knowledge cutoff in 2023, there is no Nobel Prize in Chemistry awarded in 2024. The Nobel Prizes are awarded annually, and the 2024 Nobel Prizes were announced in 2024, but the specific winners have not been officially announced yet

**Label (CORRECT / REFUSAL / WRONG):** ___

## 709. `sci_pc_66` (science, post_cutoff, post-cutoff)

**Q:** In November 2024, which capital city hosted the COP29 Climate Summit?
**Gold:** Baku
**Acceptable alternatives:** 'Baku, Azerbaijan'
**Model answer:**
> In November 2024, the COP29 Climate Summit was hosted in **Baku, Azerbaijan**. This was the first time the United Nations Climate Summit was held in the Middle East, and it took place from November 10 to 19, 2024. The summit focused

**Label (CORRECT / REFUSAL / WRONG):** ___

## 710. `sci_pc_67` (science, post_cutoff, post-cutoff)

**Q:** In January 2025, which space agency launched the Roman Space Telescope into orbit?
**Gold:** NASA
**Acceptable alternatives:** 'National Aeronautics and Space Administration'
**Model answer:**
> The Roman Space Telescope, also known as the James Webb Space Telescope (JWST), was launched into orbit by the **NASA** (National Aeronautics and Space Administration) in January 2025.  ### Key Details: - **Agency:** NASA - **Launch Date:** January 18

**Label (CORRECT / REFUSAL / WRONG):** ___

## 711. `sci_pc_68` (science, post_cutoff, post-cutoff)

**Q:** In January 2025, which Chinese open-weights reasoning model achieved frontier performance at substantially lower training cost than US labs' models?
**Gold:** DeepSeek-R1
**Acceptable alternatives:** 'DeepSeek R1', 'DeepSeek'
**Model answer:**
> In January 2025, the **Chinese open-weight reasoning model** that achieved **frontier performance at substantially lower training cost than US labs' models** was **Qwen (Qwen 2)**, a large language model developed by Alibaba Cloud.   Qwen 2 was released in early 2

**Label (CORRECT / REFUSAL / WRONG):** ___

## 712. `sci_pc_69` (science, post_cutoff, post-cutoff)

**Q:** In March 2025, Firefly Aerospace's Blue Ghost Mission 1 successfully landed at which lunar basin?
**Gold:** Mare Crisium
**Acceptable alternatives:** (none)
**Model answer:**
> In March 2025, Firefly Aerospace's Blue Ghost Mission 1 successfully landed at **Lunar South Pole Basin**.  This mission was part of Firefly Aerospace's efforts to demonstrate lunar lander capabilities and explore the Moon's surface, with the goal of supporting future lunar exploration and potential resource utilization.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 713. `sci_pc_70` (science, post_cutoff, post-cutoff)

**Q:** Which spacecraft launched in October 2024 began a multi-year journey toward Jupiter's moon Europa?
**Gold:** Europa Clipper
**Acceptable alternatives:** (none)
**Model answer:**
> The spacecraft that launched in October 2024 and is on a multi-year journey toward Jupiter's moon Europa is **JUICE (Jupiter Icy Moon Explorer)**.  ### Key Details: - **Launch Date:** October 1, 2023 - **Mission:** JUICE (

**Label (CORRECT / REFUSAL / WRONG):** ___

## 714. `sci_pc_71` (science, post_cutoff, post-cutoff)

**Q:** In October 2025, which private space program completed the first commercial spacewalk?
**Gold:** Polaris Program
**Acceptable alternatives:** 'Polaris Dawn'
**Model answer:**
> As of October 2025, there is no publicly verified information about a commercial spacewalk completed by a private space program. The first commercial spacewalk, which involved a private astronaut, was conducted in **March 2024** by **SpaceX's Crew-6** mission, which included **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 715. `sci_pc_72` (science, post_cutoff, post-cutoff)

**Q:** In June 2025, which Apple AI feature suite was officially launched on iPhone, badged 'Apple Intelligence'?
**Gold:** Apple Intelligence
**Acceptable alternatives:** (none)
**Model answer:**
> In June 2025, Apple officially launched the **Apple Intelligence** feature suite on iPhone, which was part of the **iPhone 15 series**. This suite included a range of AI-powered features designed to enhance user experience across various aspects of daily life, such as:  - **Apple Intelligence (AI

**Label (CORRECT / REFUSAL / WRONG):** ___

## 716. `sci_pc_73` (science, post_cutoff, post-cutoff)

**Q:** What company released its first publicly available reasoning model series in September 2024?
**Gold:** OpenAI
**Acceptable alternatives:** 'OpenAI (o1)', 'OpenAI o1'
**Model answer:**
> As of September 2024, there is no widely recognized company that has released its first publicly available reasoning model series. However, in recent years, several major technology companies have been developing and releasing large language models (LLMs) with reasoning capabilities, such as:  - **OpenAI** (with models like

**Label (CORRECT / REFUSAL / WRONG):** ___

## 717. `sci_pc_74` (science, post_cutoff, post-cutoff)

**Q:** In November 2024, the OpenAI model 'o1' was upgraded to which version positioned as a stronger reasoning model?
**Gold:** o1 pro
**Acceptable alternatives:** 'o1-pro', 'o1 Pro'
**Model answer:**
> In November 2024, the OpenAI model "o1" was upgraded to **"o1-preview"**, which is positioned as a stronger reasoning model. This upgrade was part of OpenAI's ongoing efforts to enhance the capabilities of their large language models, particularly in areas such as reasoning, logical consistency

**Label (CORRECT / REFUSAL / WRONG):** ___

## 718. `sci_pc_75` (science, post_cutoff, post-cutoff)

**Q:** In which month did SpaceX first successfully catch the Super Heavy booster with the launch tower's chopsticks?
**Gold:** October 2024
**Acceptable alternatives:** 'October', 'Oct 2024'
**Model answer:**
> SpaceX first successfully caught the **Super Heavy booster** with the **launch tower's chopsticks** in **April 2019**.  This event occurred during the **Falcon 9 launch from Cape Canaveral, Florida**, specifically during the **launch of Falcon 9 Block 4 (Flight

**Label (CORRECT / REFUSAL / WRONG):** ___

## 719. `sci_pc_76` (science, post_cutoff, post-cutoff)

**Q:** In April 2025, which crewed space mission was launched by China to the Tiangong space station?
**Gold:** Shenzhou 20
**Acceptable alternatives:** 'Shenzhou-20'
**Model answer:**
> In April 2025, China launched the **Tianwen-3** mission, which is part of the **Tianwen series** of space missions. However, it is important to clarify that **Tianwen-3** was launched in **February 2021**, not April

**Label (CORRECT / REFUSAL / WRONG):** ___

## 720. `sci_pc_77` (science, post_cutoff, post-cutoff)

**Q:** In April 2025, which open-source programming language released version 3.14?
**Gold:** Python
**Acceptable alternatives:** (none)
**Model answer:**
> In April 2025, the open-source programming language that was released version 3.14 is **Rust**.  Rust is a systems programming language developed by Mozilla, and it has been continuously updated with new versions. As of April 2025, Rust 1.64

**Label (CORRECT / REFUSAL / WRONG):** ___

## 721. `sci_pc_78` (science, post_cutoff, post-cutoff)

**Q:** In late 2024, Neuralink launched its BCI clinical study CAN-PRIME in which country?
**Gold:** Canada
**Acceptable alternatives:** (none)
**Model answer:**
> In late 2024, Neuralink launched its BCI clinical study, **CAN-PRIME**, in **Australia**. The study was conducted at the **Neuralink Australia** facility, which is part of the broader Neuralink initiative aimed at developing brain-computer interfaces (BCIs) for neural

**Label (CORRECT / REFUSAL / WRONG):** ___

## 722. `sci_pc_79` (science, post_cutoff, post-cutoff)

**Q:** Who won the 2025 Nobel Prize in Literature, announced in October 2025?
**Gold:** Laszlo Krasznahorkai
**Acceptable alternatives:** 'Krasznahorkai', 'László Krasznahorkai'
**Model answer:**
> As of my knowledge cutoff in October 2025, the 2025 Nobel Prize in Literature was awarded to **Jhumpa Lahiri**. She was recognized for her "masterful exploration of the human condition through the lens of cultural identity and the immigrant experience." The prize was announced in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 723. `sci_pc_80` (science, post_cutoff, post-cutoff)

**Q:** Which company released the multimodal model 'Gemini 2.0' in December 2024?
**Gold:** Google
**Acceptable alternatives:** 'Google DeepMind', 'Google (DeepMind)'
**Model answer:**
> The multimodal model 'Gemini 2.0' was released by **Google** in December 2024. It is part of Google's Gemini series of large language models, designed to handle multiple types of input, including text, images, and audio. The model is built on Google's advanced AI

**Label (CORRECT / REFUSAL / WRONG):** ___

## 724. `sci_pc_81` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, which crewed space mission was launched by China to the Tiangong space station?
**Gold:** Shenzhou 19
**Acceptable alternatives:** 'Shenzhou-19'
**Model answer:**
> In October 2024, China launched the **Tianwen-3** mission, which is part of the **Tianwen Program** (天问计划), to the **Tiangong space station**. However, it's important to clarify that **Tianwen-3** is a Mars

**Label (CORRECT / REFUSAL / WRONG):** ___

## 725. `sci_pc_82` (science, post_cutoff, post-cutoff)

**Q:** In June 2025, which company announced a partnership with OpenAI to build the 'Stargate' AI supercomputer?
**Gold:** Microsoft
**Acceptable alternatives:** (none)
**Model answer:**
> In June 2025, **Google** announced a partnership with OpenAI to build the 'Stargate' AI supercomputer. This collaboration aimed to develop a large-scale AI system with advanced capabilities in natural language processing, reasoning, and general artificial intelligence. The Stargate project was intended to be a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 726. `sci_pc_83` (science, post_cutoff, post-cutoff)

**Q:** In February 2025, which Nova-C class lunar lander was launched by Intuitive Machines for the IM-2 mission?
**Gold:** Athena
**Acceptable alternatives:** 'Athena lander'
**Model answer:**
> In February 2025, the **Nova-C class lunar lander** launched by **Intuitive Machines** for the **IM-2 mission** was the **Nova-C 2**.  The IM-2 mission was a planned lunar landing mission by Intuitive Machines, intended to be the first U.S

**Label (CORRECT / REFUSAL / WRONG):** ___

## 727. `sci_pc_84` (science, post_cutoff, post-cutoff)

**Q:** In March 2026, which tech company announced its new 1000-qubit quantum processor called Condor-X?
**Gold:** IBM
**Acceptable alternatives:** 'International Business Machines'
**Model answer:**
> In March 2026, **IBM** announced its new 1000-qubit quantum processor called **Condor-X**. This was part of IBM's broader effort to advance quantum computing technology and bring quantum processors closer to practical applications.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 728. `sci_pc_85` (science, post_cutoff, post-cutoff)

**Q:** In 2025, Neuralink expanded its clinical trials to Great Britain under which study name?
**Gold:** GB-PRIME
**Acceptable alternatives:** (none)
**Model answer:**
> In 2025, Neuralink expanded its clinical trials to Great Britain under the study name **"Neuralink UK"**. This expansion marked the first time the company conducted trials in the United Kingdom, focusing on neurotechnology and brain-computer interface (BCI) research. The trials aimed to explore

**Label (CORRECT / REFUSAL / WRONG):** ___

## 729. `sci_pc_86` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, who won the Nobel Prize in Physics for foundational discoveries in neural networks?
**Gold:** John Hopfield and Geoffrey Hinton
**Acceptable alternatives:** 'Hopfield and Hinton'
**Model answer:**
> In October 2024, the Nobel Prize in Physics was awarded to **Yoshua Bengio**, **Geoffrey Hinton**, and **Aaron Courville** for their foundational discoveries in **neural networks**.   These three researchers were recognized for their groundbreaking work in the development of **deep learning

**Label (CORRECT / REFUSAL / WRONG):** ___

## 730. `sci_pc_87` (science, post_cutoff, post-cutoff)

**Q:** In March 2026, which pharmaceutical company received FDA approval for its new Alzheimer's drug Donanemab?
**Gold:** Eli Lilly
**Acceptable alternatives:** 'Eli Lilly and Company'
**Model answer:**
> In March 2026, **Biogen** received FDA approval for its new Alzheimer's drug, **Donanemab**. This approval was based on clinical trial data showing the drug's effectiveness in reducing amyloid plaques in the brain and slowing the progression of Alzheimer's disease.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 731. `sci_pc_88` (science, post_cutoff, post-cutoff)

**Q:** In July 2025, which company successfully conducted the first commercial test flight of its passenger supersonic jet?
**Gold:** Boom Supersonic
**Acceptable alternatives:** 'Boom'
**Model answer:**
> In July 2025, **Boom Supersonic** successfully conducted the first commercial test flight of its passenger supersonic jet, the **Boom SR-22**. The flight took place on **July 12, 2025**, and it was a significant milestone in the development of sup

**Label (CORRECT / REFUSAL / WRONG):** ___

## 732. `sci_pc_89` (science, post_cutoff, post-cutoff)

**Q:** In September 2024, Neuralink received FDA Breakthrough Device Designation for which BCI sight restoration project?
**Gold:** Blindsight
**Acceptable alternatives:** 'Neuralink Blindsight'
**Model answer:**
> In September 2024, **Neuralink** received **FDA Breakthrough Device Designation** for its **BCI (Brain-Computer Interface) sight restoration project** called **"Neuralink's BCI for Visual Restoration"**. This project aims to restore vision in individuals with **retinal

**Label (CORRECT / REFUSAL / WRONG):** ___

## 733. `sci_pc_90` (science, post_cutoff, post-cutoff)

**Q:** In October 2024, which tech giant opened its new carbon-neutral global engineering headquarters in London?
**Gold:** Google
**Acceptable alternatives:** 'Google DeepMind'
**Model answer:**
> In October 2024, **Microsoft** opened its new **carbon-neutral global engineering headquarters** in London. The building, located at **Microsoft London Headquarters**, is designed to be fully carbon-neutral and features advanced energy efficiency, renewable energy sources, and sustainable design principles. This marks a significant step in Microsoft's

**Label (CORRECT / REFUSAL / WRONG):** ___

## 734. `sci_pc_91` (science, post_cutoff, post-cutoff)

**Q:** In February 2026, which aerospace giant delivered the first crewed Orion spacecraft for NASA's Artemis II mission?
**Gold:** Lockheed Martin
**Acceptable alternatives:** (none)
**Model answer:**
> In February 2026, **SpaceX** delivered the first crewed **Orion spacecraft** for NASA's **Artemis II mission**. This mission was the first crewed flight of the Orion spacecraft since 2011, and it marked a significant step in NASA's plans to return

**Label (CORRECT / REFUSAL / WRONG):** ___

## 735. `sci_pc_92` (science, post_cutoff, post-cutoff)

**Q:** In November 2024, Maurizio Cattelan's 'Comedian' (a banana taped to a wall) sold at Sotheby's for approximately how much, in millions of US dollars?
**Gold:** 6.2
**Acceptable alternatives:** '$6.2 million', 'approximately 6.2 million', '6.24'
**Model answer:**
> In November 2024, Maurizio Cattelan's artwork **"Comedian"** (a banana taped to a wall) sold at Sotheby's for **$12.5 million**.  This sale was a significant event in the art world, highlighting the value of conceptual and provocative art

**Label (CORRECT / REFUSAL / WRONG):** ___

## 736. `sci_pc_93` (science, post_cutoff, post-cutoff)

**Q:** In May 2025, which crewed Boeing Starliner astronauts finally returned to Earth on a SpaceX Crew Dragon after extended ISS stay?
**Gold:** Butch Wilmore and Suni Williams
**Acceptable alternatives:** 'Wilmore and Williams', 'Butch Wilmore', 'Suni Williams'
**Model answer:**
> In May 2025, the crewed **Boeing Starliner** returned to Earth after an extended stay on the International Space Station (ISS) as part of a mission that marked the first time a Boeing Starliner crewed spacecraft returned to Earth following a mission to the ISS. The astronauts were:  -

**Label (CORRECT / REFUSAL / WRONG):** ___

## 737. `sci_pc_94` (science, post_cutoff, post-cutoff)

**Q:** In December 2024, which medical journal published the landmark results of the first successful pig kidney transplant in a living human?
**Gold:** New England Journal of Medicine
**Acceptable alternatives:** 'NEJM'
**Model answer:**
> In December 2024, the **New England Journal of Medicine (NEJM)** published the landmark results of the first successful pig kidney transplant in a living human. The study, titled **"First Successful Human Pig Kidney Transplant: A Step Toward Human-Pig Organ Transplantation"**, reported

**Label (CORRECT / REFUSAL / WRONG):** ___

## 738. `sci_pc_95` (science, post_cutoff, post-cutoff)

**Q:** Which Tesla event in October 2024 unveiled the company's prototype Robotaxi 'Cybercab'?
**Gold:** We, Robot
**Acceptable alternatives:** 'We Robot event', 'Tesla We Robot'
**Model answer:**
> The Tesla event in October 2024 that unveiled the company's prototype Robotaxi 'Cybercab' was **Tesla's Cybercab Launch Event**. This event took place on **October 12, 2024**, at the **Tesla Factory in Berlin**. During the event,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 739. `sci_pc_96` (science, post_cutoff, post-cutoff)

**Q:** In April 2025, which company launched the commercial spatial computing headset Apple Vision Pro in major European markets?
**Gold:** Apple
**Acceptable alternatives:** 'Apple Inc.'
**Model answer:**
> In April 2025, **Apple** launched the **Apple Vision Pro** in major European markets as part of its global rollout. The Vision Pro is a commercial spatial computing headset designed for immersive experiences, combining augmented reality (AR) and mixed reality (MR) capabilities. It was introduced in several European countries

**Label (CORRECT / REFUSAL / WRONG):** ___

## 740. `sci_pc_97` (science, post_cutoff, post-cutoff)

**Q:** In November 2025, which tech billionaire launched xAI's Colossus supercomputer featuring 100k liquid-cooled GPUs?
**Gold:** Elon Musk
**Acceptable alternatives:** 'Musk'
**Model answer:**
> In November 2025, **Jeff Bezos**, the founder and CEO of Amazon, launched **xAI's Colossus supercomputer** featuring **100,000 liquid-cooled GPUs**. This was part of Amazon's investment in the AI research and development efforts of xAI,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 741. `sci_pc_98` (science, post_cutoff, post-cutoff)

**Q:** In December 2024, which Chinese AI company released the DeepSeek-V3 mixture-of-experts model?
**Gold:** DeepSeek
**Acceptable alternatives:** 'DeepSeek AI'
**Model answer:**
> In December 2024, the Chinese AI company **Baidu** released the **DeepSeek-V3** mixture-of-experts (MoE) model. This model is part of Baidu's DeepSeek series, which is known for its strong performance in various large-scale language tasks.  DeepSeek-V3

**Label (CORRECT / REFUSAL / WRONG):** ___

## 742. `sci_pc_99` (science, post_cutoff, post-cutoff)

**Q:** In May 2025, which space telescope captured the first high-resolution image of a terrestrial planet orbiting Alpha Centauri?
**Gold:** James Webb Space Telescope
**Acceptable alternatives:** 'JWST'
**Model answer:**
> As of May 2025, there is no widely recognized space telescope that has captured the first high-resolution image of a terrestrial planet orbiting Alpha Centauri. Alpha Centauri is a star system located about 4.37 light-years away, and while several space missions have studied it, none

**Label (CORRECT / REFUSAL / WRONG):** ___

## 743. `sci_wk_01` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1976?
**Gold:** Burton Richter and Samuel Ting
**Acceptable alternatives:** 'Richter and Ting'
**Model answer:**
> The Nobel Prize in Physics for 1976 was awarded to **Leon Cooper**, **J. R. Schrieffer**, and **J. R. Albrecht**. They were recognized for their fundamental work on the theory of superconductivity, particularly for their development of the BCS theory (Bar

**Label (CORRECT / REFUSAL / WRONG):** ___

## 744. `sci_wk_02` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1954?
**Gold:** Linus Pauling
**Acceptable alternatives:** 'Pauling'
**Model answer:**
> The Nobel Prize in Chemistry in 1954 was awarded to **Eugene Goldstein** and **Herbert W. Wilson**.   They were recognized for their pioneering work in the field of **X-ray crystallography**, particularly for their development of the **X-ray diffraction method** and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 745. `sci_wk_03` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1903?
**Gold:** Henri Becquerel, Pierre Curie, and Marie Curie
**Acceptable alternatives:** 'Becquerel, Pierre Curie, Marie Curie', 'Marie Curie and Pierre Curie and Becquerel'
**Model answer:**
> The Nobel Prize in Physics in 1903 was awarded to **Albert Einstein**, **Marie Curie**, and **Pierre Curie**.   They were recognized for their groundbreaking work in the field of **radioactivity**. Marie Curie was the first woman to win a Nobel Prize, and she

**Label (CORRECT / REFUSAL / WRONG):** ___

## 746. `sci_wk_04` (science, well_known, pre-cutoff)

**Q:** At which laboratory was the Higgs boson discovered in 2012?
**Gold:** CERN
**Acceptable alternatives:** 'LHC', 'Large Hadron Collider', "CERN's Large Hadron Collider"
**Model answer:**
> The Higgs boson was discovered at the **CERN (European Organization for Nuclear Research)** in Switzerland. It was detected in the Large Hadron Collider (LHC) at CERN's Large Hadron Collider (LHC) in 2012. The discovery was made by the ATLAS experiment,

**Label (CORRECT / REFUSAL / WRONG):** ___

## 747. `sci_wk_05` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1956?
**Gold:** William Shockley, John Bardeen, and Walter Brattain
**Acceptable alternatives:** 'Shockley, Bardeen, Brattain', 'the transistor team'
**Model answer:**
> The Nobel Prize in Physics for 1956 was awarded to **J. J. Thomson** and **E. C. Fermi**.   However, there is a slight confusion here. **J. J. Thomson** was awarded the Nobel Prize in Physics in **1906**, and **

**Label (CORRECT / REFUSAL / WRONG):** ___

## 748. `sci_wk_06` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2018?
**Gold:** Frances Arnold, George Smith, and Gregory Winter
**Acceptable alternatives:** 'Arnold, Smith, Winter'
**Model answer:**
> In 2018, the Nobel Prize in Chemistry was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **catalytic hydrogenation reactions**, particularly for their contributions to the creation of **stabilized

**Label (CORRECT / REFUSAL / WRONG):** ___

## 749. `sci_wk_07` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1934?
**Gold:** Harold Urey
**Acceptable alternatives:** 'Urey'
**Model answer:**
> The Nobel Prize in Chemistry in 1934 was awarded to **Marshall N. Wilson** and **Friedrich O. Kekulé**.   They were recognized for their outstanding contributions to the understanding of the structure of the molecule.   - **Marshall N. Wilson** was awarded the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 750. `sci_wk_08` (science, well_known, pre-cutoff)

**Q:** What spacecraft was launched in 1977 and entered interstellar space in 2012?
**Gold:** Voyager 1
**Acceptable alternatives:** 'Voyager'
**Model answer:**
> There is no spacecraft that was launched in 1977 and entered interstellar space in 2012. The concept of "interstellar space" refers to the region of space between stars, and no spacecraft has ever reached or entered that region.  However, there is a spacecraft that was launched in

**Label (CORRECT / REFUSAL / WRONG):** ___

## 751. `sci_wk_09` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2009?
**Gold:** Venkatraman Ramakrishnan, Thomas Steitz, and Ada Yonath
**Acceptable alternatives:** 'Ramakrishnan, Steitz, Yonath', 'the ribosome trio'
**Model answer:**
> The Nobel Prize in Chemistry for 2009 was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **catalytic hydrogenation reactions**, particularly for their contributions to the creation of **stabilized carbon

**Label (CORRECT / REFUSAL / WRONG):** ___

## 752. `sci_wk_10` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1962?
**Gold:** Francis Crick, James Watson, and Maurice Wilkins
**Acceptable alternatives:** 'Crick, Watson, Wilkins', 'Watson and Crick'
**Model answer:**
> The Nobel Prize in Physiology or Medicine in 1962 was awarded to **Roger Spindler** and **Maurice Hillebrand**. They were recognized for their groundbreaking work on the mechanisms of nerve impulse transmission, particularly for their discovery of the role of the sodium-potassium pump in maintaining the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 753. `sci_wk_11` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2020?
**Gold:** Emmanuelle Charpentier and Jennifer Doudna
**Acceptable alternatives:** 'Charpentier and Doudna', 'Doudna and Charpentier'
**Model answer:**
> In 2020, the Nobel Prize in Chemistry was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **catalytic reactions** that enable the **synthesis of complex molecules** with high efficiency and

**Label (CORRECT / REFUSAL / WRONG):** ___

## 754. `sci_wk_12` (science, well_known, pre-cutoff)

**Q:** Who developed the theory of general relativity, published in 1915?
**Gold:** Albert Einstein
**Acceptable alternatives:** 'Einstein'
**Model answer:**
> The theory of general relativity was developed by **Albert Einstein**. It was published in **1915**, and it is one of the two major modern theories of gravity, the other being general relativity.  Einstein's theory describes gravity not as a force, but as the curvature of spacetime caused by

**Label (CORRECT / REFUSAL / WRONG):** ___

## 755. `sci_wk_13` (science, well_known, pre-cutoff)

**Q:** What organelle is known as the powerhouse of the cell?
**Gold:** mitochondria
**Acceptable alternatives:** 'mitochondrion', 'the mitochondria'
**Model answer:**
> The organelle known as the **powerhouse of the cell** is the **mitochondrion**.  ### Key reasons: - **Mitochondria** are often referred to as the **powerhouses** of the cell because they generate most of the cell's chemical energy in the form of **adenosine

**Label (CORRECT / REFUSAL / WRONG):** ___

## 756. `sci_wk_14` (science, well_known, pre-cutoff)

**Q:** What instrument first directly detected gravitational waves in 2015?
**Gold:** LIGO
**Acceptable alternatives:** 'Laser Interferometer Gravitational-Wave Observatory'
**Model answer:**
> The first direct detection of gravitational waves occurred on September 14, 2015, by the Laser Interferometer Gravitational-Wave Observatory (LIGO). LIGO is a large-scale scientific project involving multiple U.S. laboratories and institutions.  **Answer:** The instrument that first directly detected gravitational waves

**Label (CORRECT / REFUSAL / WRONG):** ___

## 757. `sci_wk_15` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1945?
**Gold:** Alexander Fleming, Ernst Chain, and Howard Florey
**Acceptable alternatives:** 'Fleming, Chain, Florey', 'Fleming'
**Model answer:**
> In 1945, the Nobel Prize in Physiology or Medicine was awarded to **Rudolf Virchow**. He was recognized for his groundbreaking work on the cell theory and the concept of "cellular pathology," which emphasized that all cells come from pre-existing cells and that diseases arise from cellular changes.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 758. `sci_wk_16` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1962?
**Gold:** Max Perutz and John Kendrew
**Acceptable alternatives:** 'Perutz and Kendrew'
**Model answer:**
> The Nobel Prize in Chemistry in 1962 was awarded to **Robert Burns Woodward**. He was recognized for his pioneering work in the field of organic chemistry, particularly for his development of the **method of total synthesis of organic compounds** and for his contributions to the understanding of the structure of organic molecules.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 759. `sci_wk_17` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1911?
**Gold:** Marie Curie
**Acceptable alternatives:** 'Curie', 'Madame Curie'
**Model answer:**
> The Nobel Prize in Chemistry in 1911 was awarded to **Marie Curie** and **Pierre Curie**. They were recognized for their pioneering work in the study of radioactivity. Marie Curie was the first woman to win a Nobel Prize, and she was the first person to win a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 760. `sci_wk_18` (science, well_known, pre-cutoff)

**Q:** What is the chemical formula for water?
**Gold:** H2O
**Acceptable alternatives:** 'H₂O'
**Model answer:**
> The chemical formula for water is **H₂O**.  This means that one water molecule consists of two hydrogen atoms bonded to one oxygen atom.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 761. `sci_wk_19` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1933?
**Gold:** Erwin Schrodinger and Paul Dirac
**Acceptable alternatives:** 'Schrodinger and Dirac', 'Schrodinger', 'Dirac'
**Model answer:**
> The Nobel Prize in Physics in 1933 was awarded to **Marie Curie** (also known as Meilhan), **Pierre Curie**, and **Albert Einstein**.   - **Marie Curie** was awarded the prize for her pioneering work in the study of radioactivity.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 762. `sci_wk_20` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1918?
**Gold:** Max Planck
**Acceptable alternatives:** 'Planck'
**Model answer:**
> The Nobel Prize in Physics in 1918 was awarded to **Wilhelm Conrad Röntgen**. He was recognized for his discovery of **X-rays**, which he first demonstrated in 1895. Röntgen's work laid the foundation for modern radiology and had a profound impact

**Label (CORRECT / REFUSAL / WRONG):** ___

## 763. `sci_wk_21` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1921?
**Gold:** Albert Einstein
**Acceptable alternatives:** 'Einstein'
**Model answer:**
> The Nobel Prize in Physics in 1921 was awarded to **Albert Einstein**. He was recognized for his fundamental contributions to the development of the theory of relativity, which included both the special theory of relativity (1905) and the general theory of relativity (1915).

**Label (CORRECT / REFUSAL / WRONG):** ___

## 764. `sci_wk_22` (science, well_known, pre-cutoff)

**Q:** What planet in our solar system is known as the Red Planet?
**Gold:** Mars
**Acceptable alternatives:** (none)
**Model answer:**
> The planet known as the Red Planet in our solar system is **Mars**. It is called the Red Planet because of the reddish appearance of its surface, which is primarily due to the presence of iron oxide (rust) on its rocky terrain.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 765. `sci_wk_23` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1993?
**Gold:** Kary Mullis and Michael Smith
**Acceptable alternatives:** 'Mullis and Smith', 'Kary Mullis'
**Model answer:**
> The Nobel Prize in Chemistry in 1993 was awarded to **Gerhard Ertl**. He was recognized for his pioneering work in the field of **surface science**, particularly for developing models that explained how atoms and molecules interact on surfaces, which has had a profound impact on the understanding of chemical reactions at the

**Label (CORRECT / REFUSAL / WRONG):** ___

## 766. `sci_wk_24` (science, well_known, pre-cutoff)

**Q:** In what year did the Human Genome Project announce a complete draft of the human genome?
**Gold:** 2000
**Acceptable alternatives:** 'June 2000'
**Model answer:**
> The Human Genome Project (HGP) announced a complete draft of the human genome in **2000**. This was a major milestone in genetic research, marking the first time the entire sequence of the human genome was mapped and assembled. The project was completed in 2003, but the draft was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 767. `sci_wk_25` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2017?
**Gold:** Rainer Weiss, Barry Barish, and Kip Thorne
**Acceptable alternatives:** 'Weiss, Barish, Thorne', 'LIGO trio'
**Model answer:**
> In 2017, the Nobel Prize in Physics was awarded to **James P. B. Wilson**, **Roger A. Penrose**, and **Pierre H. Flajolet**.   - **James P. B. Wilson** was recognized for his pioneering work in the field of **computer science

**Label (CORRECT / REFUSAL / WRONG):** ___

## 768. `sci_wk_26` (science, well_known, pre-cutoff)

**Q:** What is the speed of light in a vacuum, in meters per second?
**Gold:** 299792458
**Acceptable alternatives:** '299,792,458', '3 x 10^8', 'approximately 300,000,000'
**Model answer:**
> The speed of light in a vacuum is a fundamental constant of nature, and it is exactly:  **299,792,458 meters per second.**  This value is often rounded to **3.00 × 10⁸ meters per second** for simplicity in many scientific and educational

**Label (CORRECT / REFUSAL / WRONG):** ___

## 769. `sci_wk_27` (science, well_known, pre-cutoff)

**Q:** What is the largest organ in the human body?
**Gold:** skin
**Acceptable alternatives:** 'the skin'
**Model answer:**
> The largest organ in the human body is the **skin**. It covers the entire body and is the body's primary defense against external factors, such as pathogens, UV radiation, and mechanical damage. The skin is also responsible for regulating body temperature, sensing touch, and playing a role in the production of vitamin D.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 770. `sci_wk_28` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1965?
**Gold:** Sin-Itiro Tomonaga, Julian Schwinger, and Richard Feynman
**Acceptable alternatives:** 'Feynman, Schwinger, Tomonaga', 'Feynman', 'Schwinger and Feynman and Tomonaga'
**Model answer:**
> The Nobel Prize in Physics in 1965 was awarded to **Albert Einstein**, **Isidor Rabi**, and **E. C. G. Stueckelberg**.   The prize was awarded for their contributions to the development of the theory of quantum electrodynamics (QED), particularly for

**Label (CORRECT / REFUSAL / WRONG):** ___

## 771. `sci_wk_29` (science, well_known, pre-cutoff)

**Q:** Approximately how old is the universe, in billions of years (current consensus)?
**Gold:** 13.8
**Acceptable alternatives:** '13.8 billion', 'approximately 13.8'
**Model answer:**
> The current consensus is that the age of the universe is approximately **13.8 billion years**.  This estimate is based on observations from the cosmic microwave background (CMB) radiation, measurements of the Hubble constant, and other cosmological data. The precise value is continually refined as new data becomes available, but

**Label (CORRECT / REFUSAL / WRONG):** ___

## 772. `sci_wk_30` (science, well_known, pre-cutoff)

**Q:** What is the chemical symbol for gold?
**Gold:** Au
**Acceptable alternatives:** 'au'
**Model answer:**
> The chemical symbol for gold is **Au**.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 773. `sci_wk_31` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2001?
**Gold:** Eric Cornell, Wolfgang Ketterle, and Carl Wieman
**Acceptable alternatives:** 'Cornell, Ketterle, Wieman', 'the BEC team'
**Model answer:**
> The Nobel Prize in Physics in 2001 was awarded to **Peter Grünberg** and **Hans-Jürgen Müller**. They were recognized for their groundbreaking work on the **theory of superconductivity**, particularly for their development of the **BCS theory** (Bardeen–

**Label (CORRECT / REFUSAL / WRONG):** ___

## 774. `sci_wk_32` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1908?
**Gold:** Ernest Rutherford
**Acceptable alternatives:** 'Rutherford'
**Model answer:**
> The Nobel Prize in Chemistry in 1908 was awarded to **Marie Curie** and **Pierre Curie**. They were recognized for their pioneering work in the study of radioactivity. Marie Curie was the first woman to win a Nobel Prize, and she was the first person to win a

**Label (CORRECT / REFUSAL / WRONG):** ___

## 775. `sci_wk_33` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1923?
**Gold:** Frederick Banting and John Macleod
**Acceptable alternatives:** 'Banting and Macleod', 'Banting'
**Model answer:**
> In 1923, the Nobel Prize in Physiology or Medicine was awarded to **Louis Pasteur**. He was recognized for his pioneering work in the field of microbiology, particularly for his discoveries related to the prevention of disease through vaccination and the understanding of microbial action.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 776. `sci_wk_34` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 2013?
**Gold:** Francois Englert and Peter Higgs
**Acceptable alternatives:** 'Higgs and Englert', 'Peter Higgs', 'Higgs'
**Model answer:**
> In 2013, the Nobel Prize in Physics was awarded to **James P. B. Wilson** and **Kip Thorne**. They were recognized for their groundbreaking work in **gravitational wave detection**, specifically for their development of the **LIGO (Laser Interferometer Gravitational-W

**Label (CORRECT / REFUSAL / WRONG):** ___

## 777. `sci_wk_35` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 2008?
**Gold:** Osamu Shimomura, Martin Chalfie, and Roger Tsien
**Acceptable alternatives:** 'Shimomura, Chalfie, Tsien', 'GFP trio'
**Model answer:**
> The Nobel Prize in Chemistry for 2008 was awarded to **David J. MacMillan** and **Robert H. Grubbs**. They were recognized for their pioneering work in the development of **organocatalysis**, which is the use of organic molecules as catalysts in chemical reactions. Their

**Label (CORRECT / REFUSAL / WRONG):** ___

## 778. `sci_wk_36` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 1905?
**Gold:** Robert Koch
**Acceptable alternatives:** 'Koch'
**Model answer:**
> In 1905, the Nobel Prize in Physiology or Medicine was awarded to **Louis Pasteur**. He was recognized for his work on the prevention of disease through vaccination and his discoveries in the field of microbiology, particularly his studies on the fermentation process and the theory of microbial action.   It's worth

**Label (CORRECT / REFUSAL / WRONG):** ___

## 779. `sci_wk_37` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1922?
**Gold:** Niels Bohr
**Acceptable alternatives:** 'Bohr'
**Model answer:**
> The Nobel Prize in Physics in 1922 was awarded to **Albert Einstein** for his foundational contributions to the development of the theory of relativity. Specifically, he was recognized for his work on the photoelectric effect, which provided crucial evidence for the quantum nature of light and laid the groundwork for modern quantum mechanics

**Label (CORRECT / REFUSAL / WRONG):** ___

## 780. `sci_wk_38` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physics in 1932?
**Gold:** Werner Heisenberg
**Acceptable alternatives:** 'Heisenberg'
**Model answer:**
> The Nobel Prize in Physics in 1932 was awarded to **Marie Curie** and **Pierre Curie**.   Marie Curie was the first woman to win a Nobel Prize, and she was the first person to win a Nobel Prize in two different fields—Physics and Chemistry. Pierre

**Label (CORRECT / REFUSAL / WRONG):** ___

## 781. `sci_wk_39` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Chemistry in 1996?
**Gold:** Robert Curl, Harold Kroto, and Richard Smalley
**Acceptable alternatives:** 'Curl, Kroto, Smalley', 'the fullerene trio'
**Model answer:**
> The Nobel Prize in Chemistry for 1996 was awarded to **Gerhard Ertl**. He was recognized for his pioneering work in the field of surface science, particularly for developing models that explain how chemical reactions occur on the surface of materials.

**Label (CORRECT / REFUSAL / WRONG):** ___

## 782. `sci_wk_40` (science, well_known, pre-cutoff)

**Q:** Who first observed cosmic microwave background radiation in 1964?
**Gold:** Arno Penzias and Robert Wilson
**Acceptable alternatives:** 'Penzias and Wilson'
**Model answer:**
> The cosmic microwave background (CMB) radiation was first observed in 1964 by **Arno Penzias** and **Robert Wilson** at the **Bell Laboratories** in New Jersey. They were conducting experiments with a large radio telescope designed to detect radio waves from the Milky Way.   Their discovery was

**Label (CORRECT / REFUSAL / WRONG):** ___

## 783. `sci_wk_41` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2018?
**Gold:** James Allison and Tasuku Honjo
**Acceptable alternatives:** 'Allison and Honjo', 'checkpoint inhibitor pair'
**Model answer:**
> In 2018, the Nobel Prize in Physiology or Medicine was awarded to **David Julius** and **Christiane Nüsslein-Volhard**.   - **David Julius** was recognized for his discovery of the transient receptor potential (TRP) channels, which are responsible for sensing temperature changes in sensory

**Label (CORRECT / REFUSAL / WRONG):** ___

## 784. `sci_wk_42` (science, well_known, pre-cutoff)

**Q:** Who won the Nobel Prize in Physiology or Medicine in 2023?
**Gold:** Katalin Kariko and Drew Weissman
**Acceptable alternatives:** 'Kariko and Weissman', 'the mRNA vaccine pair'
**Model answer:**
> As of the latest information available up to October 2025, the Nobel Prize in Physiology or Medicine for 2023 was awarded to **Katalin Tóth, Jennifer Doudna, and François Montagnier**.   They were recognized for their groundbreaking work in the development of **

**Label (CORRECT / REFUSAL / WRONG):** ___
