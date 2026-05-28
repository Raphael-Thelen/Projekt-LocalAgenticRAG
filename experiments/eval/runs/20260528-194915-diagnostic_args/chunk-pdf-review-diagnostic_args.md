# Chunk-to-PDF Review

Run ID: 20260528-194915-diagnostic_args
Eval Mode: diagnostic_args
PDF: ../../data/dsa-regelwerk.pdf

Hinweis: Seite stammt aus dem Index-Feld 'page'. Chunk-ID enthält ebenfalls die Seite als Muster _p<seite>_.

## Q1: Wer regiert laut dem Regelwerk das Mittelreich und wie heisst dessen Hauptstadt?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p10_c002 | 10 | 24.925377 | dsa_regelwerk | ## **Eine Welt der Abenteuer** Das Herz von Aventurien wird vom **Mittelreich** (1) eingenommen. Beherrscht von mächtigen Provinzherren und zusammengehalten von der jungen Kaiserin Rohaja, ist das Mittelreich Heimat kühner Ritter und anderer Heldinnen, die ... |
| 2 | dsa_regelwerk_p107_c003 | 107 | 20.432808 | dsa_regelwerk | - **Untypische Vorteile:** Kälteresistenz **Untypische Nachteile:** Angst vor … (engen Räumen, Menschenmassen) **Verbreitung und Lebensweise:** Unter allen Ländern Aventuriens nimmt das Raulsche Reich, auch Mittelreich oder Neues Reich genannt, die größte F... |
| 3 | dsa_regelwerk_p108_c000 | 108 | 20.115473 | dsa_regelwerk | Hauptstadt Elenvina. Traditionell sind die unverbrüchlich treuen Nordmärker und die freiheitsliebenden Albernier sich spinnefeind. Orks Menschenblut opfern, um ihren Götzen zu huldigen. Östlich des Kosch kommt nun das **Königreich Garetien** , die zentrale ... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p108_c000 | 108 | 48.038326 | dsa_regelwerk | Hauptstadt Elenvina. Traditionell sind die unverbrüchlich treuen Nordmärker und die freiheitsliebenden Albernier sich spinnefeind. Orks Menschenblut opfern, um ihren Götzen zu huldigen. Östlich des Kosch kommt nun das **Königreich Garetien** , die zentrale ... |
| 2 | dsa_regelwerk_p10_c002 | 10 | 12.591856 | dsa_regelwerk | ## **Eine Welt der Abenteuer** Das Herz von Aventurien wird vom **Mittelreich** (1) eingenommen. Beherrscht von mächtigen Provinzherren und zusammengehalten von der jungen Kaiserin Rohaja, ist das Mittelreich Heimat kühner Ritter und anderer Heldinnen, die ... |
| 3 | dsa_regelwerk_p107_c003 | 107 | 9.758979 | dsa_regelwerk | - **Untypische Vorteile:** Kälteresistenz **Untypische Nachteile:** Angst vor … (engen Räumen, Menschenmassen) **Verbreitung und Lebensweise:** Unter allen Ländern Aventuriens nimmt das Raulsche Reich, auch Mittelreich oder Neues Reich genannt, die größte F... |
| 4 | dsa_regelwerk_p108_c002 | 108 | 8.163317 | dsa_regelwerk | Die südlichste Provinz des Mittelreichs ist das **Fürstentum Almada** am Fluss Yaquir, und wenn man den Liedern der Barden Glauben schenken will, ist dieses Land so schön, aber auch so wehrhaft wie eine Rose. Die Almadaner verstehen sich als Bastion gegen d... |
| 5 | dsa_regelwerk_p109_c000 | 109 | 7.5194197 | dsa_regelwerk | ## **Mittelreich** **Sprache:** Garethi (je nach Provinz) **Schrift:** Kusliker Zeichen (2 AP) **Ortskenntnis:** je nach Heimatort (z.B. Angbar, Elenvina, Gareth, Greifenfurt, Havena, Punin) **Sozialstatus:** Adel, Unfrei **Übliche Professionen:** - _Weltli... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p10_c002 | 10 | 12.194456 | dsa_regelwerk | ## **Eine Welt der Abenteuer** Das Herz von Aventurien wird vom **Mittelreich** (1) eingenommen. Beherrscht von mächtigen Provinzherren und zusammengehalten von der jungen Kaiserin Rohaja, ist das Mittelreich Heimat kühner Ritter und anderer Heldinnen, die ... |
| 2 | dsa_regelwerk_p341_c005 | 341 | 11.867005 | dsa_regelwerk | So erwartet man beispielsweise im Mittelreich von einem Ritter, also einem Niederadligen, dass er zu Pferd reist, ordentliche, am besten mit seinem Wappen versehene Kleidung trägt und zumindest ein Schwert oder eine andere standesgemäße Waffe mit sich führt... |
| 3 | dsa_regelwerk_p107_c003 | 107 | 11.709786 | dsa_regelwerk | - **Untypische Vorteile:** Kälteresistenz **Untypische Nachteile:** Angst vor … (engen Räumen, Menschenmassen) **Verbreitung und Lebensweise:** Unter allen Ländern Aventuriens nimmt das Raulsche Reich, auch Mittelreich oder Neues Reich genannt, die größte F... |
| 4 | dsa_regelwerk_p340_c001 | 340 | 10.847516 | dsa_regelwerk | _Denken wir doch zurück: Die Queste nach dem heiligen Licht des Quanion. Die Herausforderung des Haffax an Kaiserin Rohaja. Und nicht zu vergessen, unser schwerster Verlust: Der Stab des Vergessens, das Erzartefakt unseres Herren und Eigentum unserer Kirche... |
| 5 | dsa_regelwerk_p108_c000 | 108 | 10.339916 | dsa_regelwerk | Hauptstadt Elenvina. Traditionell sind die unverbrüchlich treuen Nordmärker und die freiheitsliebenden Albernier sich spinnefeind. Orks Menschenblut opfern, um ihren Götzen zu huldigen. Östlich des Kosch kommt nun das **Königreich Garetien** , die zentrale ... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q2: Welche Entitaeten gelten im aventurischen Hintergrund als die groessten Widersacher der Zwoelfgoetter?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p316_c000 | 316 | 17.705679 | dsa_regelwerk | Feindselige Götter, Tempel des Namenlosen oder Unheiligtümer von Erzdämonen oder gar Erzdämonen, die ein Gegenpart zum eigenen Gott darstellen, erschweren die Probe. Der Zeitpunkt kann ebenfalls die Probe modifizieren. Jeder der Zwölfgötter hat einen eigene... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p316_c000 | 316 | 12.393975 | dsa_regelwerk | Feindselige Götter, Tempel des Namenlosen oder Unheiligtümer von Erzdämonen oder gar Erzdämonen, die ein Gegenpart zum eigenen Gott darstellen, erschweren die Probe. Der Zeitpunkt kann ebenfalls die Probe modifizieren. Jeder der Zwölfgötter hat einen eigene... |
| 2 | dsa_regelwerk_p13_c003 | 13 | 9.869362 | dsa_regelwerk | Widersacher der Götter sind der **Namenlose** , der in fast allen Kulturen und unter unterschiedlichsten Bezeichnungen bekannt ist, und die **Erzdämonen** , groteske Zerrbilder der Götter. Die Zwerge verehren vor allem **Angrosch** , der bei den Zwölfgötter... |
| 3 | dsa_regelwerk_p13_c000 | 13 | 7.399234 | dsa_regelwerk | Finstere Schwarzmagier erschaffen hier Untote und beschwören Dämonen, die Angst und Schrecken unter den Götterdienern säen. Und neben den Erzdämonen ist es vor allem der _Gott ohne Namen_ , der die Macht der anderen Götter heimlich unterwandert und seine Di... |
| 4 | dsa_regelwerk_p319_c004 | 319 | 7.280565 | dsa_regelwerk | ## Die Tradition der Praiosgeweihten Die Geweihten des Götterfürsten dienen der Gerechtigkeit und Ordnung. Sie helfen den Menschen gegen die Machenschaften der Diener der Erzdämonen und gehen gegen alles Namenlose vor. Ihre Liturgien sind oftmals Waffen geg... |
| 5 | dsa_regelwerk_p404_c003 | 404 | 6.979942 | dsa_regelwerk | Rahjas) 10<br>Brennend (Status) 35, 341<br>Aufmerksamkeit Belshirash (Erzdämon,<br>(Sonderfertigkeit) 246 Gegenspieler Firuns) 10 C<br>Aura verbergen Belzhorash (Erzdämonin,<br>Calijnaar (Erzdämonin,<br>(Sonderfertigkeit) 284 Gegenspielerin Peraines) 10 Geg... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

Keine Treffer.


## Q3: Aus welchen Schritten und Wuerfen setzt sich eine Fertigkeitsprobe zusammen und welche Funktion erfuellt dabei der Fertigkeitswert (FW)?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p24_c005 | 24 | 16.06939 | dsa_regelwerk | ## Fertigkeitsprobe Im Unterschied zu der Eigenschaftsprobe kommt bei einer _Fertigkeitsprobe_ nicht nur 1W20 zum Einsatz, sondern es sind gleich 3W20. Die Ergebnisse der Würfe werden aber nicht addiert, sondern jeder einzelne Wurf mit einem Eigenschaftswer... |
| 2 | dsa_regelwerk_p314_c003 | 314 | 13.638443 | dsa_regelwerk | _Beispiel: Hilbert ist die Probe auf_ Selbstbeherrschung (Störungen ignorieren) _gelungen und er hat das Eichhörnchen ignoriert (es ist mit den Nüssen entkommen). Nun ist es Zeit für die Fertigkeitsprobe. Hilbert muss auf drei Eigenschaften würfeln, die bei... |
| 3 | dsa_regelwerk_p270_c002 | 270 | 12.024603 | dsa_regelwerk | Um den gespeicherten Zauberspruch zu aktivieren, ist üblicherweise das Aussprechen eines Schlüsselwortes oder die Ausführung einer Schlüsselgeste nötig. Dazu ist eine freie Aktion notwendig. Das Artefakt würfelt die Zauberprobe des ausgelösten Zaubers und z... |
| 4 | dsa_regelwerk_p25_c003 | 25 | 11.300587 | dsa_regelwerk | ## **Schnellerer Fertigkeitsprobenwurf** _Optionale Regel_ Eine Fertigkeitsprobe dauert wesentlich länger als eine Eigenschaftsprobe. Schließlich würfelst du drei Würfel und musst das Ergebnis mit den einzelnen Spielwerten vergleichen. Es gibt jedoch versch... |
| 5 | dsa_regelwerk_p26_c002 | 26 | 11.208414 | dsa_regelwerk | ## **Qualitätsstufen** \|**Fertigkeitspunkte**\|**Qualitätstufe**\| \|---\|---\| \|**0-3**\|1\| \|**4-6**\|2\| \|**7-9**\|3\| \|**10-12**\|4\| \|**13-15**\|5\| \|**16+**\|6\| ## **Probe mit 0 FP bestanden** Es kann passieren, dass ein Held eine Probe besteht, allerdings keine FP ü... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p27_c004 | 27 | 6.2412157 | dsa_regelwerk | ## **Kein Bestätigungswurf bei Fertigkeitsproben?** Anders als bei Eigenschaftsproben gibt es bei Fertigkeitsproben keine Bestätigungswürfe bei Kritischen Erfolgen oder Patzern. Das liegt daran, dass die Wahrscheinlichkeiten für Kritische Erfolge bei den be... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q4: Welche mechanischen Konsequenzen hat ein Patzer (20) bei einer Nahkampf-Attacke, wenn der Bestaetigungswurf ebenfalls misslingt?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p234_c004 | 234 | 30.328283 | dsa_regelwerk | Wenn der Bestätigungswurf misslingt, geschieht Folgendes: - Der Held erleidet 1W6+2 SP. _Beispiel: Hätte der Spieler von Arbosch weniger Glück gehabt und bei seiner Attacke eine 20 gewürfelt, hätte dies für ihn schlimm enden können. Es wäre ein Bestätigungs... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p61_c005 | 61 | 17.405062 | dsa_regelwerk | \|**Startalter**\|**Startalter**\|**Startalter**\|**Startalter**\|**Startalter**\|**Startalter**\|**Startalter**\|**Startalter**\| \|---\|---\|---\|---\|---\|---\|---\|---\| \|**Erfahrungsgrad**\|\|\|\|\|\|\|\| \|**Spezies**\|**Unerfahren**\|**Durchschnitt**\|**Erfahren**\|**Kompetent**\|*... |
| 2 | dsa_regelwerk_p234_c004 | 234 | 15.268663 | dsa_regelwerk | Wenn der Bestätigungswurf misslingt, geschieht Folgendes: - Der Held erleidet 1W6+2 SP. _Beispiel: Hätte der Spieler von Arbosch weniger Glück gehabt und bei seiner Attacke eine 20 gewürfelt, hätte dies für ihn schlimm enden können. Es wäre ein Bestätigungs... |
| 3 | dsa_regelwerk_p236_c006 | 236 | 12.60882 | dsa_regelwerk | - Der Verteidiger verteidigt ganz normal. ## **Patzer** Auf der anderen Seite gibt es im Kampf auch Patzer. Hier muss ebenfalls ein Bestätigungswurf erfolgen. Wenn der Bestätigungswurf gelingt, geschieht Folgendes: - gewöhnliches Misslingen Wenn der Bestäti... |
| 4 | dsa_regelwerk_p234_c000 | 234 | 12.197865 | dsa_regelwerk | ## **Patzer** ## **Lange Waffe** _Vorteil:_ Kurze und mittlere Waffen erleiden Erschwernisse gegen lange Waffen. _Nachteil:_ Lange Waffen erleiden bei beengter Umgebung eine Erschwernis von 8 auf Attacke und Parade. Auf der anderen Seite gibt es im Kampf au... |
| 5 | dsa_regelwerk_p246_c001 | 246 | 11.874561 | dsa_regelwerk | Wenn der Bestätigungswurf gelingt, geschieht Folgendes: - gewöhnliches Misslingen Wenn der Bestätigungswurf misslingt, geschieht Folgendes: ## • Der Held erleidet 1W6+2 SP. _Beispiel: Hätte Gerons Spieler bei dem Schuss auf den Orkräuber weniger Glück und w... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

Keine Treffer.


## Q5: Welche maximalen Obergrenzen gelten bei der Heldenerschaffung fuer Erfahrungsgrad Erfahren bei Eigenschaften, Fertigkeiten und Kampftechniken?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p42_c004 | 42 | 33.12564 | dsa_regelwerk | Die Obergrenze verändert sich, wenn der Held einen höheren Erfahrungsgrad erreicht (was mit dem Erwerb von AP einhergeht) und könnte auf EG Legendär ein absolutes Maximum von 20 (18 + 2) erreichen. Durch den Einsatz dieser Optionalregel wird das Spiel etwas... |
| 2 | dsa_regelwerk_p42_c001 | 42 | 13.151568 | dsa_regelwerk | - Jeder Held startet mit 3 Schicksalspunkten, egal welchen Erfahrungsgrad er wählt. Dieser Wert kann über Vor- und Nachteile modifiziert werden. - Unabhängig vom Erfahrungsgrad kann ein Held maximal 80 AP in Vorteile investieren und 80 AP durch Nachteile er... |
| 3 | dsa_regelwerk_p48_c002 | 48 | 11.401721 | dsa_regelwerk | ## **Erfahrungsgrad und Profession** Die Professionspakete ab Seite **129** sind für Helden mit dem Erfahrungsgrad Erfahren gedacht. Wenn du Spielercharaktere mit höherem Erfahrungsgrad spielen willst, kannst du das Professionspaket als Grundlage nehmen, ab... |
| 4 | dsa_regelwerk_p84_c007 | 84 | 11.326644 | dsa_regelwerk | **Spezies:** Mensch (Thorwaler) **Kultur:** Thorwal **Profession:** Seefahrer **Erfahrungsgrad:** Erfahren 81 |
| 5 | dsa_regelwerk_p46_c001 | 46 | 11.034406 | dsa_regelwerk | Im Falle des Erfahrungsgrades Erfahren würde dies bedeuten, dass Helden zu Spielbeginn in der Summe bis zu 100 Eigenschaftspunkte erreichen dürfen und ihre Eigenschaftswerte sich in einem Rahmen von 8 bis 14 bewegen müssen (eventuell noch durch Eigenschafts... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p42_c004 | 42 | 7.344718 | dsa_regelwerk | Die Obergrenze verändert sich, wenn der Held einen höheren Erfahrungsgrad erreicht (was mit dem Erwerb von AP einhergeht) und könnte auf EG Legendär ein absolutes Maximum von 20 (18 + 2) erreichen. Durch den Einsatz dieser Optionalregel wird das Spiel etwas... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q6: Ab welchem Lebenspunkte-Verlust erhaelt ein Held die erste Stufe Schmerz und wann verschwindet diese wieder?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p37_c001 | 37 | 20.10804 | dsa_regelwerk | ## **Schmerz** Durch Verletzungen, Gifte, Zauber und andere Unannehmlichkeiten kann ein Held Schmerzen erleiden, die ihn im schlimmsten Falle handlungsunfähig machen. Um trotz immenser Schmerzen (Stufe IV) handlungsfähig zu bleiben, ist eine Probe auf _Selb... |
| 2 | dsa_regelwerk_p59_c002 | 59 | 16.204742 | dsa_regelwerk | ## **LeP-Verlust und Schmerz** Werden Helden schwer verletzt, verlieren sie einen Teil ihrer Lebensenergie. Verletzungen sind außerdem mit Schmerzen verbunden und haben weitere Auswirkungen. - Sind die Lebenspunkte auf Dreiviertel, die Hälfte oder ein Viert... |
| 3 | dsa_regelwerk_p237_c004 | 237 | 15.704628 | dsa_regelwerk | _Beispiel: Der Ork hat Arbosch mit seiner Axt getroffen. Der Spielleiter würfelt die Trefferpunkte der orkischen Axt aus. Die Axt verursacht 1W6+5 Trefferpunkte. Da der Spielleiter hier eine 5 würfelt, erzielt er so 10 (5 + 5) Trefferpunkte. Hiervon wird nu... |
| 4 | dsa_regelwerk_p230_c002 | 230 | 13.878363 | dsa_regelwerk | - _Kampftechnikwert (KTW):_ Der Kampftechnikwert stellt die Kompetenz eines Kämpfers im Umgang mit einer Art von Waffen dar. Jeder Waffe ist einer Kampftechnik zugeordnet. - _Lebensenergie (LE)_ : Die Lebensenergie stellt die Gesundheit eines Helden dar. Im... |
| 5 | dsa_regelwerk_p212_c003 | 212 | 12.369775 | dsa_regelwerk | Außerdem kann der Heiler dem Patienten Schmerzen nehmen, die durch LE-Verlust entstanden sind. Für je 1 QS wird eine Stufe des Zustands Schmerz ignoriert. Eine solche Behandlung dauert ebenfalls 15 Minuten (siehe Seite **340** ). Diese Wirkung hält bis zum ... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p172_c004 | 172 | 7.2291327 | dsa_regelwerk | ## **Zäher Hund** Durch diesen Vorteil erlangt der Held eine beeindruckende Widerstandsfähigkeit gegenüber Verletzungen bzw. Schmerzen. **Regel:** Dieser Vorteil sorgt dafür, dass der Held die Auswirkungen der höchsten Stufe des Zustands _Schmerz_ ignoriere... |
| 2 | dsa_regelwerk_p397_c003 | 397 | 6.3960786 | dsa_regelwerk | ## **Routinevoraussetzungen** \|**Modifkator-**\|**Fertigkeitswert-**\| \|---\|---\| \|**Maximum**\|**Minimum**\| \|**+3 und höher**\|1\| \|**+2**\|4\| \|**+1**\|7\| \|**+/–0**\|10\| \|**–1**\|13\| \|**–2**\|16\| \|**–3**\|19\| ## **Schmerzstufe Auswirkung** \|**Stufe I**\|leichte Schmerz... |
| 3 | dsa_regelwerk_p345_c003 | 345 | 5.696358 | dsa_regelwerk | ## **Kelmon** Ein von einer fleischfressenden Pflanze gewonnenes Jagdgift **Stufe:** 2 **Art:** Kontakt- und Waffengift, pflanzlich **Widerstand:** Zähigkeit **Wirkung:** 4W6 SP; 4 Stufen _Paralyse_ / 2W6 SP; 1 Stufe _Paralyse_ **Beginn:** 5 KR **Dauer:** 3... |
| 4 | dsa_regelwerk_p33_c005 | 33 | 5.0879116 | dsa_regelwerk | - _Zustand ignorieren_ : Es kostet ebenfalls 1 Schip, alle Zustände, durch die man betroffen ist, für eine Kampfrunde zu ignorieren. _Beispiel: Einige Kampfrunden später hat sich die Lage verschlechtert. Mirhiban ist mittlerweile schwer verletzt und hat zwe... |
| 5 | dsa_regelwerk_p37_c002 | 37 | 4.879594 | dsa_regelwerk | ## **Schmerz** \|**Schmerzstufe**\|**Auswirkung**\| \|---\|---\| \|**Stufe I**<br>**Stufe II**\|leichte Schmerzen,<br>alle Proben –1,GS –1<br>ablenkende Schmerzen,\| \|**Stufe III**\|alle Proben –2,GS –2<br>starke Schmerzen,<br>alle Proben –3,GS –3\| \|**Stufe IV**\|hand... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q7: In welche drei grossen Gilden sind Gildenmagier Aventuriens organisiert und wie unterscheiden sie sich in ihrer Haltung zur Magie?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p153_c001 | 153 | 9.169404 | dsa_regelwerk | Der alte Magister Alrik Dagabor ist in jungen Jahren selbst ein reisender Abenteurer gewesen, der sich in fortgeschrittenem Alter in den ruhigen Kosch zurückgezogen hat. In seinem Turm widmet er sich nun der Forschung und der Ausbildung begabter Schüler. Se... |
| 2 | dsa_regelwerk_p278_c000 | 278 | 8.243102 | dsa_regelwerk | ## Die Tradition der Gildenmagier Den Magiern der aventurischen Magierakademien eilt der Ruf voraus, geheimes Wissen über so ziemlich alle Bereiche des Lebens gesammelt zu haben. Ob Astronomie, Philosophie, Sphärologie oder Alchimie, der gemeine Bürger erwa... |
| 3 | dsa_regelwerk_p278_c003 | 278 | 7.915319 | dsa_regelwerk | Die meisten Akademien und entsprechend ihre Abgänger, aber auch die Schüler privater Lehrmeister sind in einer der drei großen Gilden organisiert: Der Bund des weißen Pentagramms wird einfach die Weiße Gilde genannt. Ihre Mitglieder sind den Zwölfen treu un... |
| 4 | dsa_regelwerk_p386_c001 | 386 | 7.765046 | dsa_regelwerk | _— Rohal der Weise zu einer Gruppe von Scholaren, um 570 nach Bosparans Fall_ Mittlerweile kennst du alle Regeln des Spiels: Du weißt, wie du Fertigkeitsproben ablegst, welche Möglichkeiten dir im Kampf offenstehen, über welche Zaubersprüche dein Magier ver... |
| 5 | dsa_regelwerk_p93_c002 | 93 | 7.629614 | dsa_regelwerk | - _Utulus:_ schwarz (1-17), blauschwarz (18-20) ## **Augenfarbe (1W20)** - _Mittelländer:_ dunkelbraun (1-2), braun (3-9), grün (10-11), blau (12-17), grau (18-19), schwarz (20) - _Nivese:_ braun (1-2), hellbraun (3-9), bernsteinfarben (10-14), grün (15-17)... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p278_c004 | 278 | 22.495811 | dsa_regelwerk | Die als Große Graue Gilde des Geistes bekannte Graue Gilde steht für Forschung und Wissenschaft, aber auch für einen freigeistigen Umgang mit Magie und den mit ihr verbundenen Regeln. Unter dem Dach der Gilde sammeln sich verschiedene philosophische Strömun... |
| 2 | dsa_regelwerk_p154_c001 | 154 | 16.283863 | dsa_regelwerk | ## **Graumagierin (Schule der Verformungen zu Lowangen)** _Professionspaket_ ## **Graumagierin** Die Eleven aus der Schule der Verformungen zu Lowangen werden in der Heil- und Verwandlungsmagie ausgebildet. Sie gehören der Großen Grauen Gilde des Geistes an... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q8: Welche Einsatzmoeglichkeiten hat ein Spieler mit einem Schicksalspunkt, um in Wuerfel- oder Kampfgeschehen einzugreifen? Nenne vier Optionen.

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p33_c004 | 33 | 21.55503 | dsa_regelwerk | - _Verteidigung_ : Wer seine Verteidigung im Kampf stärken will, der gibt 1 Schip aus und erhält bis zum Ende der aktuellen Kampfrunde einen Bonus von 4 auf alle Verteidigungen. Dies kann zu einem beliebigen Zeitpunkt der Kampfrunde erfolgen (aber vor dem W... |
| 2 | dsa_regelwerk_p33_c001 | 33 | 18.06194 | dsa_regelwerk | - _Neuer Wurf:_ Wer einen, zwei oder alle Würfel bei einer Eigenschafts- oder Fertigkeitsprobe oder bei einer Probe auf Attacke, Verteidigung und Fernkampf wiederholen will, darf 1 Schip zum nochmaligen Würfeln investieren. Dabei ist es egal, ob der Held be... |
| 3 | dsa_regelwerk_p34_c000 | 34 | 16.485891 | dsa_regelwerk | _Durch die Schmerzen und die Betäubung wäre ihre Probe um 3 erschwert. Sie überlegt, wie sie ihren letzten Schip einsetzt. Sie könnte – falls ihr der Zauber misslingt – hohe Würfelergebnisse noch einmal würfeln oder die Zustände unterdrücken und ohne Erschw... |
| 4 | dsa_regelwerk_p33_c005 | 33 | 15.430922 | dsa_regelwerk | - _Zustand ignorieren_ : Es kostet ebenfalls 1 Schip, alle Zustände, durch die man betroffen ist, für eine Kampfrunde zu ignorieren. _Beispiel: Einige Kampfrunden später hat sich die Lage verschlechtert. Mirhiban ist mittlerweile schwer verletzt und hat zwe... |
| 5 | dsa_regelwerk_p34_c003 | 34 | 14.512395 | dsa_regelwerk | - _Das Ende eines Abenteuers:_ Am Ende eines Abenteuers sollten alle überlebenden Helden ihre gesamten Schicksalspunkte zurückbekommen. - _Heldentat:_ Die Gruppe hat eine schwierige Aufgabe gemeistert, ihren Erzfeind bezwungen oder sich durch eine Heldentat... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p230_c006 | 230 | 7.431772 | dsa_regelwerk | - _Zustand Belastung (BE):_ Rüstungen, aber auch Gepäck und andere Lasten erzeugen Belastung. Der Zustand _Belastung_ erzeugt wie andere Zustände auch Abzüge auf verschiedene Kampfwerte. - _Zustand Schmerz:_ Werden Kämpfer im Gefecht ernsthaft verletzt, erl... |
| 2 | dsa_regelwerk_p23_c001 | 23 | 6.2015495 | dsa_regelwerk | ## **Kritische Erfolge** Fällt bei einer Eigenschaftsprobe eine 1, muss der Spieler noch einmal mit 1W20 würfeln und auf die Eigenschaft proben. Diese zweite Probe, der sogenannte _Bestätigungswurf_ , ist um die gleichen Modifikatoren erschwert bzw. erleich... |
| 3 | dsa_regelwerk_p225_c000 | 225 | 5.6999683 | dsa_regelwerk | ## **Attacke verbessern** Einige Helden verfügen über ein besonderes Quäntchen Glück im Nahkampf. **Regel:** Mittels dieser Sonderfertigkeit kann der Held Schicksalspunkte für Ergebnis verbessern (Attacke) einsetzen. **Voraussetzungen:** keine **AP-Wert:** ... |
| 4 | dsa_regelwerk_p33_c000 | 33 | 2.5800714 | dsa_regelwerk | _Beispiel: Obwohl Layariels Spielerin nur eine schlechte Initiative von 10 gewürfelt hat, möchte sie im Kampf gegen einen Oger zuerst zuschlagen, da sie befürchtet, ansonsten nicht zu überleben. Sie setzt einen Schicksalspunkt ein und ist vor dem Oger mit s... |
| 5 | dsa_regelwerk_p225_c001 | 225 | 2.4311209 | dsa_regelwerk | **Regel:** Erleidet ein Held den Status _Überrascht_ , kann er einen Schip ausgeben, um den Status sofort aufzuheben. **Voraussetzungen:** keine **AP-Wert:** 10 Abenteuerpunkte **Voraussetzungen:** keine **AP-Wert:** 5 Abenteuerpunkte ## **Eigenschaft verbe... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q9: Welche Grundwerte in LE, SK, ZK und GS erhaelt ein Spielercharakter als Spezies Zwerg?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p43_c005 | 43 | 17.775871 | dsa_regelwerk | Im Kapitel **Kulturen** ab Seite **95** ist eine große Auswahl der Kulturen des Regelwerks aufgeführt, ebenso alle wertetechnischen Angaben und Beschreibungen. ## **Spezies in der Übersicht** \|**Spezies**\|**LE**\|**SK**\|**ZK**\|**GS**\|**Eigenschaften**\|**Vort... |
| 2 | dsa_regelwerk_p97_c003 | 97 | 14.137375 | dsa_regelwerk | ## **Haarfarbe (1W20)** blond (1-5), schwarz (6-9), dunkelgrau (10-11), hellgrau (12-13), salzweiß (14), silberweiß (15), feuerrot (16-17), kupferrot (18-20) ## **Augenfarbe (1W20)** dunkelbraun (1-2), braun (3-5), grün (6-9), blau (10), grau (11-14), schwa... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p91_c001 | 91 | 26.183228 | dsa_regelwerk | ## **Werte** Zusätzlich zur Speziesbeschreibung ist ein Wertekasten aufgeführt, der regeltechnische Informationen über die Spezies enthält. - **AP-Wert:** Wie viele Abenteuerpunkte kostet die Spezies bei der Heldenerschaffung? Darin enthalten sind sowohl di... |
| 2 | dsa_regelwerk_p60_c001 | 60 | 23.26905 | dsa_regelwerk | \|**Zähigkeit-Berechnung**\|**Zähigkeit-Berechnung**\| \|---\|---\| \|**Summe von KO + KO + KK**<br>**Ergebnis**\|\| \|24-26\|4\| \|27-32\|5\| \|33-38\|6\| \|39-44\|7\| \|45-50\|8\| \|51-56\|9\| \|57-62\|10\| _Anmerkung:_ Das Ergebnis muss noch mit dem Grundwert der Zähigkeit des Helden... |
| 3 | dsa_regelwerk_p60_c002 | 60 | 20.494385 | dsa_regelwerk | _Chris:_ _Lebensenergie Basiswert: Lebensenergie-Grundwert 5 + KO 12 + KO 12 + Vorteil Hohe Lebenskraft III = 32 Karmaenergie Basiswert: Karmaenergie-Grundwert des Vorteils Geweihter 20 + Leiteigenschaft MU 14 = 34 Basiswert: Seelenkraft-Grundwert –5 + (MU ... |
| 4 | dsa_regelwerk_p43_c002 | 43 | 19.546791 | dsa_regelwerk | Du bekommst durch die Spezies Folgendes: - Grundwert der Lebensenergie - Grundwert der Seelenkraft - Grundwert der Zähigkeit - Grundwert der Geschwindigkeit (eventuell) Eigenschaftsänderungen durch die Spezies Außerdem sind noch einige Empfehlungen beigefüg... |
| 5 | dsa_regelwerk_p97_c000 | 97 | 19.538277 | dsa_regelwerk | ## **Zwerg** **AP-Wert:** 61 Abenteuerpunkte **Lebensenergie-Grundwert:** 8 **Seelenkraft-Grundwert:** _–_ 4 **Zähigkeit-Grundwert:** _–_ 4 **Geschwindigkeit-Grundwert:** 6 **Eigenschaftsänderungen:** KO und KK +1; CH oder GE –2 **Dringend empfohlene Vor- u... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p68_c003 | 68 | 9.800339 | dsa_regelwerk | **Spezies:** Zwerg **Kultur:** Erzzwerge **Profession:** Krieger **Erfahrungsgrad:** Erfahren **==> picture [302 x 742] intentionally omitted <==** |
| 2 | dsa_regelwerk_p167_c001 | 167 | 2.7325735 | dsa_regelwerk | **==> picture [273 x 532] intentionally omitted <==** **Voraussetzungen:** kein Nachteil Unfähig für diese Fertigkeit, nicht mehr als drei Begabungen pro Person **AP-Wert:** A-/B-/C-/D-Fertigkeit: 6/12/18/24 Abenteuerpunkte ## **Beidhändig** Durch den Vorte... |
| 3 | dsa_regelwerk_p167_c002 | 167 | 2.7325735 | dsa_regelwerk | Es gibt Wesen auf Dere, die trotz wenig Licht beinahe so gut sehen können wie am Tag. Über Dunkelsicht verfügen vor allem nichtmenschliche Spezies wie Elfen, Zwerge, Orks und Goblins. **Regel:** Auf Stufe I werden Erschwernisse durch Dunkelheit um eine Stuf... |
| 4 | dsa_regelwerk_p47_c000 | 47 | 2.4678802 | dsa_regelwerk | aus, dass wie üblich alle Eigenschaften auf 8 starten und alle übrigen Punkte mit AP bezahlt werden müssen. _Anmerkung:_ Die Pakete der ersten Tabelle kosten **540 AP** und gehen davon aus, dass der Spieler keinen Wert von Tabelle 3 hat für Spezies 15 verte... |
| 5 | dsa_regelwerk_p97_c002 | 97 | 1.5071478 | dsa_regelwerk | ## **Vermehrung und Alterung** Zwerge gehören zu den langlebigsten Spezies Aventuriens und erreichen ein Alter von 300 bis 400 Jahren. Es ist keine Seltenheit, dass Zwerge selbst dieses hohe Alter noch übertreffen. Ihre Zahl ist jedoch trotz der hohen Leben... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q10: Welches Ritual wird benoetigt, um einen Spruchzauber in einen profanen Gegenstand zu binden und ein Zauberspeicher-Artefakt zu erschaffen?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | dsa_regelwerk_p270_c005 | 270 | 19.161964 | dsa_regelwerk | Bei der einfachsten Variante der Artefakterschaffung werden ein oder mehrere Zaubersprüche im Artefakt gespeichert. Hierzu wird im ARCANOVI-Ritual zuerst das Objekt vorbereitet und dann der nötige Zauberspruch im Objekt verankert. Der ARCANOVI und der ansch... |
| 2 | dsa_regelwerk_p270_c000 | 270 | 17.298054 | dsa_regelwerk | ## **Spielarten der Artefaktmagie** Grundlegend lassen sich zwei Arten von Artefakten unterscheiden: Solche, die Zaubersprüche in sich tragen und freisetzen können, und magische Waffen. Während Erstere häufig als Schmuckstücke oder Gebrauchsgegenstände und ... |
| 3 | dsa_regelwerk_p270_c006 | 270 | 16.255934 | dsa_regelwerk | Misslingt eine der Proben, so misslingt die gesamte Verzauberung. In diesem Falle fällt kein Verlust permanenter AsP an. Mehr als 7 Ladungen können in kein Artefakt gespeichert werden. _Beispiel: Mirhiban hat sich dazu entschieden, den Zauberspruch PSYCHOST... |
| 4 | dsa_regelwerk_p270_c001 | 270 | 16.179281 | dsa_regelwerk | **==> picture [105 x 75] intentionally omitted <==** ## **Magische Artefakte** Um einen Zauberspruch in einen Gegenstand zu binden, ist das Ritual ARCANOVI nötig. Die Erschwernis der Probe und die AsP-Kosten sind abhängig vom Zauberspruch, der Art, wie der ... |
| 5 | dsa_regelwerk_p265_c002 | 265 | 14.244177 | dsa_regelwerk | ## **Permanenter Verlust von Astralpunkten** Mit manchen Ritualen kann man Magie dauerhaft in Objekte bannen. Ein Zauberer, der diesen Schritt geht, muss Astralpunkte permanent ausgeben, damit die Magie nicht ihre Kraft verliert. Diese permanent ausgegebene... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

Keine Treffer.


