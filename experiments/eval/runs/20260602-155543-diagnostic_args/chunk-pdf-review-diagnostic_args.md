# Chunk-to-PDF Review

Run ID: 20260602-155543-diagnostic_args
Eval Mode: diagnostic_args
PDF: data/dsa-regelwerk.pdf

Hinweis: Seite stammt aus dem Index-Feld 'page'. Chunk-ID enthält ebenfalls die Seite als Muster _p<seite>_.

## Q1: Wer regiert laut dem Regelwerk das Mittelreich und wie heisst dessen Hauptstadt?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | aventurischer_almanach_p206_c000 | 206 | 29.741117 | aventurischer_almanach | **Rohaja von Gareth Kaiserin des Mittelreiches** _»Endlich haben Wir den Heptarchen Einhalt geboten, nun müssen Wir das Reich wieder aufbauen. Selbst Wir als Kaiserin sind Uns dafür nicht zu schade. Wir nehmen unsere göttergegebene Aufgabe nicht nur ernst, ... |
| 2 | aventurischer_almanach_p263_c004 | 263 | 27.237085 | aventurischer_almanach | ## **Lang lebe der Kaiser!** Rohaja von Gareth ist im ofiziellen Aventurien Kaiserin des Mittelreiches. Es spricht aber nichts dagegen, in eurem Aventurien einen anderen Kaiser zu krönen: Kaiser Hal oder Answin von Rabenmund könnten etwa noch immer auf dem ... |
| 3 | aventurischer_almanach_p33_c005 | 33 | 26.83697 | aventurischer_almanach | **Politische Zugehörigkeit:** Provinzen des Mittelreichs: Königreich Garetien (Königin Rohaja von Gareth), Markgrafschaft Rommilyser Mark (Markgräin Swantje von Rabenmund) **Regierungsform:** Feudalherrschaft mit starrem Lehnssystem; die Kaiserin ist immer ... |
| 4 | aventurische_namen_p32_c002 | 32 | 26.15245 | aventurische_namen | Brin(ya), Emer, Rohaja, Selindian oder Yppolita häufiger vor. **Helden & Heilige:** Brin von Gareth (Reichsbehüter, kämpfte gegen Orks, den Usurpator Answin von Rabenmund und Borbarad, Vater Rohajas), Danos von Luring (Graf von Reichsforst, genannt ,König d... |
| 5 | aventurischer_almanach_p12_c006 | 12 | 23.891088 | aventurischer_almanach | ## **Das Mittelreich** Unter allen Reichen Aventuriens nimmt das Raulsche Reich, auch Mittelreich oder Neues Reich genannt, die größte Fläche ein. Von der sturmgepeitschten Küste des Meeres der Sieben Winde im Westen bis zur Tobrischen See und dem Golf von ... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p108_c000 | 108 | 48.614166 | regelwerk | Hauptstadt Elenvina. Traditionell sind die unverbrüchlich treuen Nordmärker und die freiheitsliebenden Albernier sich spinnefeind. Orks Menschenblut opfern, um ihren Götzen zu huldigen. Östlich des Kosch kommt nun das **Königreich Garetien** , die zentrale ... |
| 2 | kodex_der_helden_p58_c000 | 58 | 45.153725 | kodex_der_helden | und gut versteckte Kultplätze gibt, an denen Orks Menschenblut opfern, um ihren Götzen zu huldigen. Östlich des Kosch kommt nun das Königreich Garetien, die zentrale Provinz des Mittelreiches, auf der sich auch die Hausmacht der Kaiser des Mittelreiches grü... |
| 3 | aventurischer_almanach_p12_c006 | 12 | 36.46881 | aventurischer_almanach | ## **Das Mittelreich** Unter allen Reichen Aventuriens nimmt das Raulsche Reich, auch Mittelreich oder Neues Reich genannt, die größte Fläche ein. Von der sturmgepeitschten Küste des Meeres der Sieben Winde im Westen bis zur Tobrischen See und dem Golf von ... |
| 4 | aventurischer_almanach_p206_c001 | 206 | 35.85229 | aventurischer_almanach | Rohaja von Gareth ist die junge Kaiserin des Mittelreiches. Sie gilt als Heldenkaiserin, die tatkräftig selbst mit anpackt und aufrechte Streiter um sich schart, die ihrem Willen folgen. Durch die Schlachten der Vergangenheit ist sie zu einer umsichtigen He... |
| 5 | aventurischer_almanach_p230_c005 | 230 | 35.28108 | aventurischer_almanach | Dann endlich holte Kaiserin Rohaja zum Gegenschlag aus. 1039 BF brach ein mächtiger Schwertzug von Gallys aus auf, um Mendena zu erobern. Nach heftiger Schlacht iel Haffax’ Hauptstadt schließlich Ende des Jahres an die Kaiserlichen. Der Fürstkomtur aber hat... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | arkane_schmieden_und_labore_p79_c005 | 79 | 16.829746 | arkane_schmieden_und_labore | **==> picture [11 x 7] intentionally omitted <==** **Art:** Zauberspeicher **Struktur:** Arcanovi + Psychostabilis + (Gardianum) + (Armatrutz) **Namhafte Exemplare:** Amuletum ultima protectio (Khadil Okharim, am Hals von Kaiserin Rohaja) 75 |
| 2 | aventurisches_animatorium_p38_c006 | 38 | 15.569681 | aventurisches_animatorium | . Kurz bevor Kaiserin Rohaja im Rahja des Jahres 1039 BF die Stadt Mendena eroberte, soll dieser Lignolith-Schiffsgolem jedoch mit unbekanntem Ziel ausgelaufen sein. In Myranor wird Lignolith schon seit Hunderten von Jahren verwendet. Dort wird der Stoff ni... |
| 3 | aventurischer_almanach_p199_c000 | 199 | 15.007853 | aventurischer_almanach | ## **Das Auge des Morgens** **==> picture [300 x 145] intentionally omitted <==** **Beschreibung:** Das Auge des Morgens genannte Schwarze Auge ist etwa kindskopfgroß und von tiefschwarzer Farbe. Das Artefakt beindet sich seit der Zeit der Friedenskaiser im... |
| 4 | aventurischer_almanach_p204_c002 | 204 | 14.900319 | aventurischer_almanach | . Doch wir wollen nicht mit Derartigem im Sinn auseinandergehen, also besinnt euch auf den guten Kaiser Hal, der das Reich ordnete und sicher machte, seinen Sohn Brin, der sein Leben gab, um Orks und Dämonenanbetern zu widerstehen, und seine Tochter, die gu... |
| 5 | aventurischer_almanach_p205_c005 | 205 | 14.092508 | aventurischer_almanach | **König** : Könige sind essenziellfür den Fortgang der LebendigenGeschichte. Entweder sind sie tragenderTeil einer Erzählung oder sie setzenEreignisse in Gang, die den aventurischenHintergrund oder eine Abenteuerhandlungvorantreiben. Diese Figuren spielenei... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q2: Welche Entitaeten gelten im aventurischen Hintergrund als die groessten Widersacher der Zwoelfgoetter?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | archiv_der_da_monen_p41_c001 | 41 | 17.902073 | archiv_der_da_monen | **Feindbilder:** Die Zwölfgötter und ihre Verbündeten, die Erzdämonen und ihre Verbündeten **Diener:** u. a. Atesh’Seruhn, Ghon’chmur, Grakvaloth, Ivash, Maruk-Methai, Nab’Pashakoth, Zhylwyraq ## **Frevlergewand:** Die Dämonenkrone (?) **Magnum Opus:** kein... |
| 2 | archiv_der_da_monen_p41_c000 | 41 | 17.65438 | archiv_der_da_monen | ## Namenloser / Der Abgrund **==> picture [298 x 518] intentionally omitted <==** Obgleich der Gott ohne Namen kein Erzdämon ist, hat er sich mit einigen Dämonen verbündet und belegt eine Domäne, die wie er keinen Namen trägt, sondern einfach nur „Der Abgru... |
| 3 | regelwerk_p316_c000 | 316 | 17.651924 | regelwerk | Feindselige Götter, Tempel des Namenlosen oder Unheiligtümer von Erzdämonen oder gar Erzdämonen, die ein Gegenpart zum eigenen Gott darstellen, erschweren die Probe. Der Zeitpunkt kann ebenfalls die Probe modifizieren. Jeder der Zwölfgötter hat einen eigene... |
| 4 | kodex_des_go_tterwirkens_p16_c003 | 16 | 16.62388 | kodex_des_go_tterwirkens | **==> picture [11 x 7] intentionally omitted <==** _Beispiel: Der Ackersegen wirkt auf Pflanzen. Hilbert hat sich einige Samen herausgesucht, auf die er die Zeremonie anwenden möchte. Auch die Reichweite stellt mit Sicht kein Problem dar._ ## **Modifikatore... |
| 5 | aventurischer_almanach_p185_c003 | 185 | 13.415142 | aventurischer_almanach | _—aus der echsischen Originalfassung des Daimonicons, im Besitz von Pardona_ Neben dem Namenlosen gibt es weitere bedrohliche Gegenspieler der Götter, nämlich jene, die außerhalb der Schöpfung stehen: die Widersacher aller Götter, die Schrecken aus der Sieb... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | aventurischer_almanach_p185_c003 | 185 | 34.64039 | aventurischer_almanach | _—aus der echsischen Originalfassung des Daimonicons, im Besitz von Pardona_ Neben dem Namenlosen gibt es weitere bedrohliche Gegenspieler der Götter, nämlich jene, die außerhalb der Schöpfung stehen: die Widersacher aller Götter, die Schrecken aus der Sieb... |
| 2 | archiv_der_da_monen_p41_c001 | 41 | 12.53145 | archiv_der_da_monen | **Feindbilder:** Die Zwölfgötter und ihre Verbündeten, die Erzdämonen und ihre Verbündeten **Diener:** u. a. Atesh’Seruhn, Ghon’chmur, Grakvaloth, Ivash, Maruk-Methai, Nab’Pashakoth, Zhylwyraq ## **Frevlergewand:** Die Dämonenkrone (?) **Magnum Opus:** kein... |
| 3 | archiv_der_da_monen_p41_c000 | 41 | 12.358066 | archiv_der_da_monen | ## Namenloser / Der Abgrund **==> picture [298 x 518] intentionally omitted <==** Obgleich der Gott ohne Namen kein Erzdämon ist, hat er sich mit einigen Dämonen verbündet und belegt eine Domäne, die wie er keinen Namen trägt, sondern einfach nur „Der Abgru... |
| 4 | regelwerk_p316_c000 | 316 | 12.356346 | regelwerk | Feindselige Götter, Tempel des Namenlosen oder Unheiligtümer von Erzdämonen oder gar Erzdämonen, die ein Gegenpart zum eigenen Gott darstellen, erschweren die Probe. Der Zeitpunkt kann ebenfalls die Probe modifizieren. Jeder der Zwölfgötter hat einen eigene... |
| 5 | die_winterwacht_p91_c001 | 91 | 12.027191 | die_winterwacht | Die zunehmende Anbetung von **Kor** im Bornland kann ebenso in die Klauen des Namenlosen oder des Erzdämons **Belhalhar** führen – verstehen es doch beide meisterlich, die Grenze zwischen gutem Kampf und sinnlosem Töten verschwimmen zu lassen. Selbst gefest... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | das_wu_stenreich_p104_c007 | 104 | 11.912957 | das_wu_stenreich | Nur sehr wenige Gläubige hat der **Namenlose** in dieser Region. Der traditionelle Widersacher der Zwölfgötter ist hier schwächer als seine Feinde und fast scheint es, dass sein Kult diese Region meidet oder für Menschen hier uninteressant ist. Er gilt wede... |
| 2 | das_dornenreich_p95_c005 | 95 | 9.372373 | das_dornenreich | ## . Die Widersacher , In vielen Ländern gilt der abtrünnige Namenlose (siehe **Aventurischer Almanach** Seite **230** ) als größter Widersacher der Zwölfgötter. Im Königreich Aranien treten im Verhältnis zu anderen Regionen die Diener des Goldenen Gottes n... |
| 3 | aventurischer_almanach_p185_c003 | 185 | 2.7193546 | aventurischer_almanach | _—aus der echsischen Originalfassung des Daimonicons, im Besitz von Pardona_ Neben dem Namenlosen gibt es weitere bedrohliche Gegenspieler der Götter, nämlich jene, die außerhalb der Schöpfung stehen: die Widersacher aller Götter, die Schrecken aus der Sieb... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q3: Aus welchen Schritten und Wuerfen setzt sich eine Fertigkeitsprobe zusammen und welche Funktion erfuellt dabei der Fertigkeitswert (FW)?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | kodex_des_schwertes_p16_c004 | 16 | 20.687267 | kodex_des_schwertes | ## **Eigenschaftsproben vs. Fertigkeitsproben** Eigenschaftsproben sollten nur selten verlangt werden und Fertigkeitsproben sollten immer den Vorzug erhalten. Talente decken so gut wie alle Tätigkeiten ab, die ein Held ausführen kann. Nur wenn kein Talent p... |
| 2 | regelwerk_p24_c005 | 24 | 18.416328 | regelwerk | - Bei jedem Talent, jedem Zauber und jeder Liturgie sind drei Eigenschaftswerte angegeben. Ein Held muss nacheinander auf diese drei Eigenschaften würfeln. Die Reihenfolge, in der du auf die bei der Probe beteiligten Eigenschaften würfelst, ist dir überlass... |
| 3 | regelwerk_p314_c002 | 314 | 16.066671 | regelwerk | _Beispiel: Hilbert ist die Probe auf_ Selbstbeherrschung (Störungen ignorieren) _gelungen und er hat das Eichhörnchen ignoriert (es ist mit den Nüssen entkommen). Nun ist es Zeit für die Fertigkeitsprobe. Hilbert muss auf drei Eigenschaften würfeln, die bei... |
| 4 | regelwerk_p267_c002 | 267 | 15.724104 | regelwerk | _Beispiel: Mirhibans Spieler würfelt die modifizierte Fertigkeitsprobe auf DSCHINNENRUF. Die Probe gelingt, ohne das Mirhiban auch nur einen einzigen FP ausgeben musste. Sie behält alle 12 FP und hat damit 4 QS._ ## **Beschworene Wesen verbessern** Jede Ver... |
| 5 | kodex_des_schwertes_p17_c002 | 17 | 15.702135 | kodex_des_schwertes | **==> picture [11 x 7] intentionally omitted <==** ## **Schnellerer Fertigkeitsprobenwurf** _Optionale Regel_ Eine Fertigkeitsprobe dauert wesentlich länger als eine Eigenschaftsprobe. Schließlich würfelst du drei Würfel und musst das Ergebnis mit den einze... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | kodex_des_schwertes_p19_c004 | 19 | 8.456507 | kodex_des_schwertes | **Kein Bestätigungswurf bei Fertigkeitsproben?** Anders als bei Eigenschaftsproben gibt es bei Fertigkeitsproben keine Bestätigungswürfe bei Kritischen Erfolgen oder Patzern. Das liegt daran, dass die Wahrscheinlichkeiten für Kritische Erfolge bei den beide... |
| 2 | regelwerk_p27_c004 | 27 | 8.456507 | regelwerk | ## **Kein Bestätigungswurf bei Fertigkeitsproben?** Anders als bei Eigenschaftsproben gibt es bei Fertigkeitsproben keine Bestätigungswürfe bei Kritischen Erfolgen oder Patzern. Das liegt daran, dass die Wahrscheinlichkeiten für Kritische Erfolge bei den be... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q4: Welche mechanischen Konsequenzen hat ein Patzer (20) bei einer Nahkampf-Attacke, wenn der Bestaetigungswurf ebenfalls misslingt?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p234_c003 | 234 | 37.099365 | regelwerk | Wenn der Bestätigungswurf misslingt, geschieht Folgendes: - Der Held erleidet 1W6+2 SP. _Beispiel: Hätte der Spieler von Arbosch weniger Glück gehabt und bei seiner Attacke eine 20 gewürfelt, hätte dies für ihn schlimm enden können. Es wäre ein Bestätigungs... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | kodex_des_schwertes_p68_c004 | 68 | 19.60953 | kodex_des_schwertes | ## **Patzer** Auf der anderen Seite gibt es im Kampf auch Patzer. Hier muss ebenfalls ein Bestätigungswurf erfolgen. Wenn der Bestätigungswurf gelingt, geschieht Folgendes: gewöhnliches Misslingen Wenn der Bestätigungswurf misslingt, geschieht Folgendes: De... |
| 2 | regelwerk_p234_c003 | 234 | 19.388817 | regelwerk | Wenn der Bestätigungswurf misslingt, geschieht Folgendes: - Der Held erleidet 1W6+2 SP. _Beispiel: Hätte der Spieler von Arbosch weniger Glück gehabt und bei seiner Attacke eine 20 gewürfelt, hätte dies für ihn schlimm enden können. Es wäre ein Bestätigungs... |
| 3 | ru_stkammer_der_dampfenden_dschungel_p11_c005 | 11 | 17.241394 | ru_stkammer_der_dampfenden_dschungel | **Waffenvorteil:** Nach einem Patzer bei der Attacke wird das Würfelergebnis des Bestätigungswurfes um 1 gesenkt. **Waffennachteil:** Nach einem kritischen Erfolg auf Attacke oder Parade wird das Würfelergebnis des Bestätigungswurfes um 1 erhöht. 9 |
| 4 | regelwerk_p248_c000 | 248 | 16.856073 | regelwerk | ## **Patzer** Auf der anderen Seite gibt es bei der Verteidigung im Fernkampf auch Patzer. Hier muss ebenfalls ein Bestätigungswurf erfolgen. Wenn der Bestätigungswurf gelingt, geschieht Folgendes: ## • gewöhnliches Misslingen Wenn der Bestätigungswurf miss... |
| 5 | regelwerk_p234_c000 | 234 | 16.596695 | regelwerk | ## **Patzer** ## **Lange Waffe** _Vorteil:_ Kurze und mittlere Waffen erleiden Erschwernisse gegen lange Waffen. _Nachteil:_ Lange Waffen erleiden bei beengter Umgebung eine Erschwernis von 8 auf Attacke und Parade. Auf der anderen Seite gibt es im Kampf au... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | archiv_der_ausru_stung_p146_c005 | 146 | 12.628064 | archiv_der_ausru_stung | **Waffenvorteil:** Die Abzüge für Schüsse auf Ziele der Größenkategorie _klein_ und _winzig_ sinken um 1. **Waffennachteil:** Bei einer gewürfelten 20, egal ob der Patzer bestätigt wird oder nicht, kommt es zu einer schweren Ladehemmung Der Schütze benötigt... |
| 2 | archiv_der_ausru_stung_p299_c003 | 299 | 11.881991 | archiv_der_ausru_stung | .<br>Waffennachteil: Bei einer gewürfelten 20, egal ob der Patzer bestätigt wird oder nicht, kommt es zu einer schweren Lade-<br>hemmung. Der Schütze benötigt 2 Aktionen, um die Ladehemmung zu beseitigen. Spielst du mit der Optionalregel der<br>Patzertabell... |
| 3 | archiv_der_ausru_stung_p146_c004 | 146 | 9.750899 | archiv_der_ausru_stung | **Waffenvorteil:** Die Abzüge für Schüsse auf Ziele der Größenkategorie _klein_ und _winzig_ sinken um 1. **Waffennachteil:** Bei einer gewürfelten 20, egal ob der Patzer bestätigt wird oder nicht, kommt es zu einer schweren Ladehemmung. Der Schütze benötig... |
| 4 | archiv_der_ausru_stung_p142_c005 | 142 | 9.129389 | archiv_der_ausru_stung | **Waffennachteil:** Nach einem bestätigten Patzer bei einer Attacke oder Parade erhält der Träger zusätzlich 1 Stufe _Betäubung_ . 140 Waffen und Ausrüstungen |
| 5 | archiv_der_ausru_stung_p149_c005 | 149 | 9.127049 | archiv_der_ausru_stung | **----- End of picture text -----**<br> **Waffenvorteil:** Beim Zielen erhält der Schütze einen Bonus von 3 (jedoch wie üblich nur bis zu einem Maximum von 4). **Waffennachteil:** Bei einer gewürfelten 20, egal ob der Patzer bestätigt wird oder nicht, kommt... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q5: Welche maximalen Obergrenzen gelten bei der Heldenerschaffung fuer Erfahrungsgrad Erfahren bei Eigenschaften, Fertigkeiten und Kampftechniken?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p42_c004 | 42 | 40.713604 | regelwerk | Die Obergrenze verändert sich, wenn der Held einen höheren Erfahrungsgrad erreicht (was mit dem Erwerb von AP einhergeht) und könnte auf EG Legendär ein absolutes Maximum von 20 (18 + 2) erreichen. Durch den Einsatz dieser Optionalregel wird das Spiel etwas... |
| 2 | kodex_der_helden_p10_c004 | 10 | 38.384872 | kodex_der_helden | Durch den Einsatz dieser Optionalregel wird das Spiel etwas komplexer. ## **Maximalwerte bei Heldenerschaffung** \|**Erfahrungsgrad**\|**AP-Konto**\|**Höchstwert**<br>**Eigenschaft**\|**Höchstwert**<br>**Fertigkeit**\|**Höchstwert**<br>**Kampf-**<br>**technik**\|... |
| 3 | kodex_der_helden_p10_c002 | 10 | 15.939685 | kodex_der_helden | ## **Begrenzung von Eigenschaften, Fertigkeiten und Kampftechniken** Während der Heldenerschaffung zählt die in der Tabelle unten angegebene Grenze nach Erfahrungsgrad für Eigenschaften, Fertigkeiten und Kampftechniken. Eigenschaften sind nach Spielbeginn n... |
| 4 | regelwerk_p42_c001 | 42 | 15.411348 | regelwerk | - Unabhängig vom Erfahrungsgrad kann ein Held maximal 80 AP in Vorteile investieren und 80 AP durch Nachteile erlangen. _Beispiel: Louisa, Chris und Sarah möchten alle auf dem Erfahrungsgrad Erfahren starten. Dementsprechend erhält jeder 1.100 Abenteuerpunk... |
| 5 | regelwerk_p48_c002 | 48 | 14.416399 | regelwerk | ## **Erfahrungsgrad und Profession** Die Professionspakete ab Seite **129** sind für Helden mit dem Erfahrungsgrad Erfahren gedacht. Wenn du Spielercharaktere mit höherem Erfahrungsgrad spielen willst, kannst du das Professionspaket als Grundlage nehmen, ab... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | kodex_der_helden_p10_c003 | 10 | 14.579065 | kodex_der_helden | **Eigenschaftsobergrenze** _Optionale Regel_ Wenn du kein offenes Maximum in den Eigenschaftswerten nach Spielbeginn zulassen möchtest, kannst du als Obergrenze die Höchstwerte aus der Tabelle unten nach Erfahrungsgrad +2 festlegen. Ein _Kompetenter_ Held k... |
| 2 | kodex_der_helden_p10_c004 | 10 | 11.149794 | kodex_der_helden | Durch den Einsatz dieser Optionalregel wird das Spiel etwas komplexer. ## **Maximalwerte bei Heldenerschaffung** \|**Erfahrungsgrad**\|**AP-Konto**\|**Höchstwert**<br>**Eigenschaft**\|**Höchstwert**<br>**Fertigkeit**\|**Höchstwert**<br>**Kampf-**<br>**technik**\|... |
| 3 | regelwerk_p42_c004 | 42 | 10.3065605 | regelwerk | Die Obergrenze verändert sich, wenn der Held einen höheren Erfahrungsgrad erreicht (was mit dem Erwerb von AP einhergeht) und könnte auf EG Legendär ein absolutes Maximum von 20 (18 + 2) erreichen. Durch den Einsatz dieser Optionalregel wird das Spiel etwas... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q6: Ab welchem Lebenspunkte-Verlust erhaelt ein Held die erste Stufe Schmerz und wann verschwindet diese wieder?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p37_c001 | 37 | 23.130215 | regelwerk | ## **Schmerz** Durch Verletzungen, Gifte, Zauber und andere Unannehmlichkeiten kann ein Held Schmerzen erleiden, die ihn im schlimmsten Falle handlungsunfähig machen. Um trotz immenser Schmerzen (Stufe IV) handlungsfähig zu bleiben, ist eine Probe auf _Selb... |
| 2 | kodex_des_schwertes_p27_c003 | 27 | 22.427643 | kodex_des_schwertes | ## **Schmerz** Durch Verletzungen, Gifte, Zauber und andere Unannehmlichkeiten kann ein Held Schmerzen erleiden, die ihn im schlimmsten Falle handlungsunfähig machen. Um trotz immenser Schmerzen (Stufe IV) handlungsfähig zu bleiben, ist eine Probe auf _Selb... |
| 3 | kodex_des_schwertes_p64_c002 | 64 | 20.62948 | kodex_des_schwertes | - _Kampftechnikwert (KTW):_ Der Kampftechnikwert stellt die Kompetenz eines Kämpfers im Umgang mit einer Art von Waffen dar. Jeder Waffe ist einer Kampftechnik zugeordnet. - _Lebensenergie (LE)_ : Die Lebensenergie stellt die Gesundheit eines Helden dar. Im... |
| 4 | kodex_der_helden_p22_c002 | 22 | 19.781626 | kodex_der_helden | ## **Leiteigenschaft** **Kampftechnik und Einsatz Leiteigenschaft Attacke für alle Kampf­** MU **techniken (außer Peitschen) Attacke für Peitschen** FF **Parade für Raufen, Schwerter,** GE oder KK **Stangenwaffen Parade für Dolche, Fächer,** GE **Fechtwaffe... |
| 5 | regelwerk_p237_c004 | 237 | 18.58192 | regelwerk | _Beispiel: Der Ork hat Arbosch mit seiner Axt getroffen. Der Spielleiter würfelt die Trefferpunkte der orkischen Axt aus. Die Axt verursacht 1W6+5 Trefferpunkte. Da der Spielleiter hier eine 5 würfelt, erzielt er so 10 (5 + 5) Trefferpunkte. Hiervon wird nu... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | grimorum_cantiones_p95_c000 | 95 | 10.937296 | grimorum_cantiones | ## **orpofesso C** Durch den CORPOFESSO kann der Zauberer Schmerzen verursachen. Der Zauberspruch ist als Kampfzauber entwickelt worden, der einen Gegner ausschalten soll, ohne ihn zu töten. _Probe:_ KL/IN/KO (modifiziert um ZK) _Wirkung:_ Der Verzauberte e... |
| 2 | grimorum_cantiones_p275_c001 | 275 | 10.446413 | grimorum_cantiones | _QS 1:_ 1 Stufe Schmerz _QS 2:_ 1 Stufe Schmerz, +1 KO für 1 Minute _QS 3:_ 2 Stufen Schmerz, +1 KO für 1 Minute _QS 4:_ 3 Stufen Schmerz, +1 KO für 1 Minute _QS 5:_ 4 Stufen Schmerz, +1 KO für 1 Minute _QS 6:_ 4 Stufen Schmerz, +2 KO für 1 Minute _Zauberda... |
| 3 | grimorum_cantiones_p179_c000 | 179 | 10.054377 | grimorum_cantiones | ## **öllenpein H** Durch diesen Zauberspruch wird der Geist des Ziels mit Schmerz durchflutet. Er gilt in manchen Kreisen als formidabler Ersatz für körperliche Folter. _Probe:_ MU/IN/CH (modifiziert um SK) _Wirkung:_ Der Verzauberte erleidet Schmerzen, die... |
| 4 | grimorum_cantiones_p322_c001 | 322 | 8.82069 | grimorum_cantiones | - # Halbkreis (FW 12, 6 AP): Der Zauber wirkt nur in einem Halbkreis vor dem Zauberer. - # Anhaltende Agonie (FW 14, 6 AP): Die Stufe Schmerz baut sich erst nach QS/2 Stunden ab. # Peinigender Schmerz (FW 16, 9 AP): Der Zauber verursacht stattdessen 2 Stufe... |
| 5 | grimorum_cantiones_p413_c000 | 413 | 8.82069 | grimorum_cantiones | ## **tandhafter Wächter S** # Schmerzloser Wächter (FW 12, 4 AP): Das Ziel kann die Auswirkungen der höchsten Stufe Schmerz ignorieren. Verfügt es über weitere Fähigkeiten, um Auswirkungen von Schmerz zu ignorieren, dann addieren sich diese Wirkungen. Es ka... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q7: In welche drei grossen Gilden sind Gildenmagier Aventuriens organisiert und wie unterscheiden sie sich in ihrer Haltung zur Magie?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | rohals_erben_p5_c003 | 5 | 23.615355 | rohals_erben | . Obergeschoss 73<br>Medienhinweise 9 Dachgeschoss 73<br>Die Magie der Gildenmagier 9 Das Institut der Arkanen Analysen 73<br>Kleines Magierglossar 11 Forschung am IAA 74<br>Das Aventurien der Magier 13 Zu Gast am IAA 75<br>Magierakademien Aventuriens 13 Da... |
| 2 | rohals_erben_p95_c000 | 95 | 22.999771 | rohals_erben | Die Weltsicht der Magier ist nicht per se verschiedenen von der ihrer nichtmagischen Zeitgenossen. Auch unter ihnen gibt es treue Anhänger der Götter und sogar Geweihte, sie folgen oft den gleichen moralischen Grundsätzen, können aber auch sehr eigene Ansic... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | rohals_erben_p51_c002 | 51 | 14.792843 | rohals_erben | ## **Akademische Grade & Ränge** Die Karrierestufen der aventurischen Gildenmagie beginnen mit den _Prägradualien._ Das sind Bezeichnungen für Studienstufen eines Magiers, bevor er nach seiner **==> picture [129 x 179] intentionally omitted <==** **----- St... |
| 2 | rohals_erben_p5_c005 | 5 | 13.922867 | rohals_erben | 92<br>Akademische Grade & Ränge 50<br>Ehrungen der Gildenmagie 51 Religion & Weltsicht 93<br>Kleidung & Tracht 52 Religion 94<br>Gesetzliche Kleidungsvorschriften 52 Innerhalb des Zwölfgötterglaubens 94<br>Kleidungsstile 54 Innerhalb anderer Religionen 97<b... |
| 3 | rohals_erben_p131_c000 | 131 | 13.88905 | rohals_erben | Probe auf _Magiekunde_ ## **Große Graue Gilde des Geistes (Graue Gilde)** **QS 1** – Gildenmagische Magie unterscheidet sich von anderen Arten der Magie. Manche Zauberstäbe können Zauber speichern. **QS 2** – Der Held weiß, wie sich Gildenmagie von anderen ... |
| 4 | rohals_erben_p61_c002 | 61 | 13.740797 | rohals_erben | . Die Art der Unterbringung ihrer kollegialen Gäste variiert dabei je nach Schule. Der Bund des Weißen Pentagramms hat das Vorhandensein eines speziellen Gästezimmers auf dem Gelände einer Akademie zum Kriterium für eine Gildenmitgliedschaft gemacht. Besond... |
| 5 | rohals_erben_p44_c000 | 44 | 13.562005 | rohals_erben | über den sie konkret nichts wissen, wenigstens ein wenig zu tun hat. Das soll zwar meistens den Zuhörern bei der Suche nach einer Antwort helfen, aber oftmals vermutlich nur die eigene Unwissenheit überspielen. Allgemein ist eine gewisse Beredsamkeit bei de... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | kodex_der_magie_p80_c000 | 80 | 15.460629 | kodex_der_magie | Gilde legen ihren Fokus üblicherweise auf Antimagie, Hellsicht, Heilung und einige Kampfzauber. Die als **Große Graue Gilde des Geistes** bekannte Graue Gilde steht für Forschung und Wissenschaft, aber auch für einen freigeistigen Umgang mit Magie und den m... |
| 2 | rohals_erben_p26_c000 | 26 | 15.460629 | rohals_erben | ## Die Graue Gilde **Vollständiger Name:** Große Graue Gilde des Geistes **Symbol:** schwarzes, halb geschlossenes Auge, umgeben von einem Hexagramm **Grundsatz:** Wissen führt zu Erleuchtung. **Verbreitung:** vor allem im Horasreich und den Tulamidenlanden... |
| 3 | rohals_erben_p81_c001 | 81 | 14.960277 | rohals_erben | _Die Anconiter (FCA) verstehen sich auf die Heilkunst, die Me­ phaliten (OM) auf das Aufspüren Magiebegabter und der Or­ den der Schlange der Erkenntnis (SHI) auf das Sammeln von Wissen._ _In der Großen Grauen Gilde des Geistes erfüllt der Ordo Defen­ sores... |
| 4 | rohals_erben_p135_c000 | 135 | 14.560168 | rohals_erben | **==> picture [257 x 363] intentionally omitted <==** oder versucht einen Weg zu finden, künftige Umbrüche am Firmament vorhersagen zu können. - Als Angehöriger der Großen Grauen Gilde des Geistes hat sich der Held der Erforschung und Kartographierung der M... |
| 5 | die_gestade_des_gottwals_p97_c003 | 97 | 14.368035 | die_gestade_des_gottwals | ## **Die Halle des Windes zu Olport** Die Olporter Magierschule, die sich selbst _Runajasko_ nennt, ist eine Besonderheit unter den Schulen Aventuriens. Im Jahr 1025 BF wurde sie auf Beschluss des Gildenrats aus der Großen Grauen Gilde des Geistes ausgeschl... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q8: Welche Einsatzmoeglichkeiten hat ein Spieler mit einem Schicksalspunkt, um in Wuerfel- oder Kampfgeschehen einzugreifen? Nenne vier Optionen.

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p33_c004 | 33 | 26.124958 | regelwerk | - _Verteidigung_ : Wer seine Verteidigung im Kampf stärken will, der gibt 1 Schip aus und erhält bis zum Ende der aktuellen Kampfrunde einen Bonus von 4 auf alle Verteidigungen. Dies kann zu einem beliebigen Zeitpunkt der Kampfrunde erfolgen (aber vor dem W... |
| 2 | kodex_des_schwertes_p24_c005 | 24 | 24.467499 | kodex_des_schwertes | - _Verteidigung stärken_ : Wer seine Verteidigung im Kampf stärken will, der gibt 1 Schip aus und erhält bis zum Ende der aktuellen Kampfrunde einen Bonus von 4 auf alle Verteidigungen. Dies kann zu einem beliebigen Zeitpunkt der Kampfrunde erfolgen (aber v... |
| 3 | kodex_des_go_tterwirkens_p91_c002 | 91 | 22.323965 | kodex_des_go_tterwirkens | - **Voraussetzungen:** Sonderfertigkeit Weg des Stabträgers, keine Sonderfertigkeit Gegenwehr des Stabträgers **Aspekt:** Reise **AP-Wert:** 8 Abenteuerpunkte **Wirkung:** Der Avesgeweihte kann einen Kulturschaffenden mit dem Avesstab segnen. Der Gesegnete ... |
| 4 | kodex_des_schwertes_p276_c005 | 276 | 21.376247 | kodex_des_schwertes | **Voraussetzungen:** keine **AP-Wert:** 15 Abenteuerpunkte _Beispiel: Carolans Spielerin möchte bei einer Probe auf_ Verbergen _ihr unglückliches Ergebnis von 19, 19, 20 noch einmal würfeln. Sie gibt 1 Schip aus und würfelt alle drei Würfel erneut. Das Erge... |
| 5 | kodex_des_schwertes_p24_c006 | 24 | 21.170654 | kodex_des_schwertes | **==> picture [11 x 7] intentionally omitted <==** _Beispiel: Einige Kampfrunden später hat sich die Lage verschlechtert. Mirhiban ist mittlerweile schwer verletzt und hat zwei Stufen des Zustands_ Schmerz _und eine Stufe des Zustands_ Betäubung _erlitten. ... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | kodex_der_magie_p146_c004 | 146 | 12.887837 | kodex_der_magie | **Wirkung:** Der Träger der Schicksalsrune kann die Rune wie einen Schicksalspunkt einsetzen. Nach dem Einsatz erlischt die Rune. **AsP-Kosten:** 20 AsP - **Herstellungszeit (langsam / schnell):** 4 Tage / 4 Aktionen - **Wirkungsdauer (langsam / schnell):**... |
| 2 | kodex_des_schwertes_p65_c000 | 65 | 11.164433 | kodex_des_schwertes | **==> picture [159 x 31] intentionally omitted <==** ## **Reihenfolge des Handelns** > Um zu Beginn eines **Handelns** > Kampfes sofort handeln zu höchster INI-Wert können, kannst du einen bei Gleichstand: Schicksalspunkt einsetzen höchste INI-Basis und als... |
| 3 | archiv_der_da_monen_p282_c004 | 282 | 11.017109 | archiv_der_da_monen | - _Unglück:_ In einem Radius von 130 Schritt um den Dämon kann kein Held Schicksalspunkte einsetzen. - _Unkontrollierbar:_ Wenn der Dämon einen Dienst ausgeführt hat, beginnt er automatisch, Lebewesen in seiner Nähe anzugreifen und Objekte zu verwüsten, bis... |
| 4 | helden_des_gottwals_p44_c003 | 44 | 10.464743 | helden_des_gottwals | - **Herstellungszeit (langsam / schnell):** 2 Tage / 2 Aktionen - **Wirkungsdauer (normal / schnell):** QS Monate / QS x 3 KR **Merkmal:** Heilung **Steigerungsfaktor:** C ## **Schicksalsrune** (Wyrdruna) ## **Probe:** IN/IN/CH **Wirkung:** Der Träger der S... |
| 5 | archiv_der_da_monen_p282_c003 | 282 | 9.732783 | archiv_der_da_monen | - **QS 1:** Shihayazad ist einer der mächtigsten Dämonen überhaupt. Er ist angeblich einer der Tagesherrscher der Namenlosen Tage. - **QS 2:** Shihayazads Sinn und Zweck ist das Zerstückeln und Zerfleischen allen Lebens in seiner näheren Umgebung. - **QS 3+... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q9: Welche Grundwerte in LE, SK, ZK und GS erhaelt ein Spielercharakter als Spezies Zwerg?

### Tool: search_exact_keyword

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p43_c004 | 43 | 21.185629 | regelwerk | ## **Spezies in der Übersicht** \|**Spezies**\|**LE**\|**SK**\|**ZK**\|**GS**\|**Eigenschaften**\|**Vorteile**\|**Nachteile**\|**AP-Wert**\| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \|**Mensch**\|5\|–5\|–5\|8\|eine beliebige +1\|keine\|keine\|0 AP\| \|**Elf**\|2\|–4\|_–_6\|8\|IN und GE... |
| 2 | regelwerk_p97_c003 | 97 | 17.285686 | regelwerk | ## **Augenfarbe (1W20)** dunkelbraun (1-2), braun (3-5), grün (6-9), blau (10), grau (11-14), schwarz (15-20) ## **Körpergröße** 128 Halbfinger + 2W6 (1,30 bis 1,40 Schritt) ## **Gewicht** Größe – 80 – 1W6 + 2W6 Stein ## **Spezies in der Übersicht** \|**Spez... |
| 3 | kodex_der_helden_p11_c003 | 11 | 13.879118 | kodex_der_helden | \|\|\|\|\|\|**Spezies in der Übersicht**\|**Spezies in der Übersicht**\|\|\| \|---\|---\|---\|---\|---\|---\|---\|---\|---\| \|**Spezies**\|**LE**\|**SK **\|**ZK **\|**GS**\|**Eigenschaften**\|**Vorteile**\|**Nachteile**\|**AP-Wert**\| \|**Achaz**\|5\|–4\|–5\|8\|IN und KO +1; MU oder KK\|Dunke... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p43_c001 | 43 | 69.511345 | regelwerk | ## **Schritt 3: Spezies wählen** Als Nächstes muss eine _Spezies_ für den Helden ausgewählt werden. Die Spezies ist das Volk, dem dein Held angehört, also z.B. Mensch, Elf oder Zwerg. Damit legst du nicht nur den Rahmen des Aussehens deines Charakters fest,... |
| 2 | regelwerk_p91_c001 | 91 | 34.074524 | regelwerk | ## **Werte** Zusätzlich zur Speziesbeschreibung ist ein Wertekasten aufgeführt, der regeltechnische Informationen über die Spezies enthält. - **AP-Wert:** Wie viele Abenteuerpunkte kostet die Spezies bei der Heldenerschaffung? Darin enthalten sind sowohl di... |
| 3 | regelwerk_p60_c001 | 60 | 33.311066 | regelwerk | ## **Ausweichen** Gewandtheit / 2 ## **Initiative** (Mut + Gewandtheit) / 2 +/– Punkte aus Vor- und Nachteilen ## **Geschwindigkeit** Geschwindigkeit-Grundwert der Spezies +/– Punkte aus Vor- und Nachteilen _Louisa:_ _Lebensenergie Basiswert: Lebensenergie-... |
| 4 | kodex_der_helden_p23_c001 | 23 | 32.22166 | kodex_der_helden | Basiswert: Seelenkraft-Grundwert der Spezies + (Mut + Klugheit + Intuition) / 6 +/– Punkte aus Vor- und Nachteilen ## **Ausweichen** Gewandtheit / 2 ## **Initiative** (Mut + Gewandtheit) / 2 \|**Seelenkraft-Berechnung**\|\| \|---\|---\| \|**Summe von MU + KL + IN*... |
| 5 | kodex_der_helden_p32_c001 | 32 | 31.679825 | kodex_der_helden | **==> picture [12 x 7] intentionally omitted <==** ## **Werte** Zusätzlich zur Speziesbeschreibung ist ein Wertekasten aufgeführt, der regeltechnische Informationen über die Spezies enthält. - **AP-Wert:** Wie viele Abenteuerpunkte kostet die Spezies bei de... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | regelwerk_p68_c003 | 68 | 12.4049635 | regelwerk | **Spezies:** Zwerg **Kultur:** Erzzwerge **Profession:** Krieger **Erfahrungsgrad:** Erfahren **==> picture [302 x 742] intentionally omitted <==** |
| 2 | kodex_der_helden_p439_c003 | 439 | 11.539991 | kodex_der_helden | \|**Gareth-Stil**\|GE 13,Lanzenangriff\|Lanzen\|10 AP\| \|**Gladiatoren-Stil**\|GE 13 oder KK 13\|Raufen\|5 AP\| \|**Hammerfaust-Stil**\|KK 13\|Raufen\|10 AP\| \|**Hand Borons-Stil**\|GE 13\|Dolche,Raufen\|15 AP\| \|**Hardas-Stil**\|KK 13, Spezies Zwerg\|Hiebwaffen, Raufen,\|15 AP... |
| 3 | kodex_der_helden_p439_c001 | 439 | 9.263478 | kodex_der_helden | \|**Sonderfertigkeit**\|**Voraussetzungen**\|**Kampftechnik**\|**AP-Wert**\| \|---\|---\|---\|---\| \|**Adersin-Stil**\|GE 13\|Zweihandschwerter (nur\|15 AP\| \|\|\|Anderthalbhänder)\|\| \|**Al’Drakorhim-Stil**\|GE 13\|Schwerter,Stangenwaffen\|10 AP\| \|**Ardariten-Stil**\|GE 13\|alle... |
| 4 | helden_des_wolfsfrosts_p40_c002 | 40 | 9.055775 | helden_des_wolfsfrosts | - Brobim-Geoden können eines der folgenden Vertrautentiere an sich binden (abhängig vom gewählten Element): Wildkatze (Feuer), Falke (Luft) und Hund (Erz). Die Leiteigenschaft der Tradition ist Charisma. **Voraussetzungen:** Vorteil _Zauberer_ , kein Vortei... |
| 5 | kodex_des_schwertes_p333_c003 | 333 | 9.055775 | kodex_des_schwertes | **Regel:** Ein Xorloscher Krieger muss im Kampf gegen Wesen des Typus Drachen oder solche der Größenkategorie _riesig_ nur 1 freie Aktion aufwenden, um gegenüber seinem Gegner in eine _vorteilhafte Position_ zu gelangen (siehe Seite **75** ). Außerdem ist d... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.


## Q10: Welches Ritual wird benoetigt, um einen Spruchzauber in einen profanen Gegenstand zu binden und ein Zauberspeicher-Artefakt zu erschaffen?

### Tool: search_exact_keyword

Keine Treffer.

### Tool: search_fuzzy

| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |
|---:|---|---:|---:|---|---|
| 1 | arkane_schmieden_und_labore_p35_c002 | 35 | 29.281994 | arkane_schmieden_und_labore | \|\|Zauberspruch sowie 25-fache AsP-Kosten des Zauberspruchs\| \|**_Permanent wirkendes_**\|Für unendliche Ladungen/Wirkung zusätzlich INFINITUM IMMERDAR auf Artefaktverzaube-\| \|**_Artefakt (optional):_**\|rer wirken. Die Probe des ARCANOVI ist zusätzlich um 10 –... |
| 2 | arkane_schmieden_und_labore_p35_c001 | 35 | 26.81752 | arkane_schmieden_und_labore | \|**Übersicht der Artefaktarten**\|**Übersicht der Artefaktarten**\| \|---\|---\| \|**Art**\|**Verzauberung**\| \|**Zauberspeicher**\|ARCANOVI + Zauberspruch/Zaubertrick/Ritual oder APPLICATUS + Zauberspruch/Zaubertrick/Ritual\| \|**_Voraussetzung:_**\|ggf. SF_Zaubertric... |
| 3 | regelwerk_p270_c003 | 270 | 25.304382 | regelwerk | ## **Zauberspeicher-Artefakte** Bei der einfachsten Variante der Artefakterschaffung werden ein oder mehrere Zaubersprüche im Artefakt gespeichert. Hierzu wird im ARCANOVI-Ritual zuerst das Objekt vorbereitet und dann der nötige Zauberspruch im Objekt veran... |
| 4 | arkane_schmieden_und_labore_p33_c002 | 33 | 22.974092 | arkane_schmieden_und_labore | Die Herstellung von göttlichen Artefakten durch Sterbliche ist mittels der Liturgie Objektweihe und der Sonderfertigkeit _Liturgiebindung_ möglich. Mehr dazu findet sich im Regelerweiterungsband **Kodex des Götterwirkens** . Der vorliegende Band konzentrier... |
| 5 | kodex_der_magie_p304_c004 | 304 | 21.134567 | kodex_der_magie | ## **Spielarten der Artefaktmagie** Grundlegend lassen sich zwei Arten von Artefakten unterscheiden: Solche, die Zaubersprüche in sich tragen und freisetzen können, und magische Waffen. Während Erstere häufig als Schmuckstücke oder Gebrauchsgegenstände und ... |

Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.

### Tool: search_phrase_proximity

Keine Treffer.


