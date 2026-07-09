# Einleitung

Im Kontext generativer künstlicher Intelligenz (KI) nimmt das Thema Datenschutz und Privatsphäre ein prominentes Thema ein. Neben dem Schutz personenbezogener Daten, ist im Kontext lernender Large Language Models (LLMs) insbesondere auch die Achtung von Rechten an geistigem Eigentum gemeint.

## Problemstellung und Motivation

Für viele Daten und Dateien, sowohl im privatwirtschaftlichen Kontext, als auch besonders in der Forschung, scheidet eine Speicherung in der Cloud oder gar die Übertragung an externe LLM-Dienstleister aus. Das kann zur Wahrung des Geschäftsgeheimnisses dienen oder bei Dokumenten wie wissenschaftlichen Artikeln, Abhandlungen und Lehrbüchern aus lizenzrechtlichen Gründen untersagt sein.

Dennoch kann insbesondere in der Forschung ein großer Nutzen aus der Abfrage bestehender Wissensbestände mittels KI-Assistent gezogen werden. Dieses Projekt erforscht eine Möglichkeit, dieses Bedürfnis in Konformität mit Lizenzbestimmungen lokal umzusetzen, ohne dass die zu durchsuchenden Dokumente selbst Teil des Prompts sind.

Alle Dateien mittels eins lokalen LLMs zu indizieren und als Kontext zu verwenden, ist für umfangreiche Datenmengen mit herkömmlichen Rechnern aufgrund der entstehenden Wartezeiten unwirtschaftlich. Daher wird eine hybride Lösung mit ElasticSearch als Suchprovider untersucht.

## Zielsetzung und Forschungsfrage

Ziel der Arbeit ist die Entwicklung eines Prototypen, der gemäß der Problemstellung einen lokal operierenden Chatbot implementiert. Dieser soll mittels Model Context Protocol auf einen ElasticSearch Server zugreifen, um Fragen des Nutzers wahrheitsgemäß und fundiert beantworten und mit Textstellen belegen zu können. Zu Zwecken des prototypischen Entwicklung wird ein externes Modell verwendet, um den Test- und Iterationsprozess zu beschleunigen. Der Prototyp muss per Anforderung aber auch lokal ausgeführt werden können.

Es soll im Anschluss ermittelt werden, wie akkurat die Retrievalarchitektur auf vorhandene Textstellen zurückgreift und ob die Interpretation durch das LLM zu einer sinnvollen und korrekten Beantwortung der Frage führt. Hierzu wird die Genauigkeit anhand von Precision- und Recall Metriken untersucht und zusammen mit einer manuellen Bewertung der LLM-Antwort dargestellt. Der Fokus liegt hierbei auf der Korrektheit der finalen Antwort, sowie dem Vergleich verschiedener Suchansätze untereinander.

Daraus ergibt sich die folgende Forschungsfrage: *Kann ElasticSearch via Model Context Protocol als Grundlage für einen KI-gestützten, lokalen Dokumentzugriff dienen?*

## Aufbau der Arbeit

Nach der Einleitung und Beschreibung der Zielsetzung im ersten Kapitel, wird im zweiten Kapitel zunächst eine einheitliche Verständnisgrundlage für das Thema Retrieval-Augmented Generation (RAG) und Agentic-RAG geschaffen. Dafür ist es notwendig, das Konzept Model Context Protocol und die Technik ElasticSearch einzuordnen. Das dritte Kapitel behandelt die Anforderungsanalyse und legt die Zielarchitektur schematisch dar. Kapitel vier befasst sich anschließend mit der Implementation des Prototypen und beleuchtet Herausforderungen und Probleme, die im Laufe des Prozesses aufgetreten sind. Das fünfte Kapitel behandelt die verschiedenen verwendeten Retrieval-Strategien und bildet damit die Basis für Kapitel sechs, in dem die verwendete Testbench und das zugrundeliegende Evaluationsdesign beschrieben werden. Im siebten Kapitel werden die experimentellen Messergebnisse dargelegt und erläutert, bevor sich die letzten beiden Kapitel mit der Einordnung der erzielten Ergebnisse und dem Fazit des Softwareprojekts widmen.

# Technische und fachliche Grundlagen

Als Basis für die folgende Implementation, Analyse und Diskussion wird in diesem Kapitel eine Einordnung der zugrundeliegenden Konzepte und Technologien vorgenommen.

## Retrieval-Augmented Generation und Agentic-RAG

Die Retrieval-Augmented Generation (RAG), versteht sich als eine Erweiterung künstlicher Intelligenz in Form von LLMs um die Fähigkeit Datenmengen außerhalb des Kontext zu durchsuchen und daraus Antworten zu generieren. Dabei ist es unwichtig, woher die Daten stammen, Datenbanken sind ebenso wie die im folgenden verwendete Dokumentensammlung im Rahmen der Definition möglich. Entscheidender Vorteil dieses Verfahrens zur herkömmlichen Generativen KI ist, dass Wissen abgerufen werden kann, welches nicht als Teil eines Trainingssets im LLM selbst vorhanden ist, sondern aus den externen Quellen stammt [@honroth2024rag]. Das LLM trägt die gefunden Testpassagen im Anschluss zusammen und transformiert das Wissen im Sinne des Prompts. Solche Systeme werden häufig als RAG AI bezeichnet [@honroth2024rag].

Durch RAG ergänzte LLMs überbieten herkömmliche generative KI dabei in Spezifizität, Diversität und Genauigkeit [@lewis2020rag] und tragen zur Vermeidung von Halluzination, also der eigenmächtigen Generierung erfundener Tatsachen durch die KI bei [@ji2023hallucination]. Die *dependability* des Modells steigt unter diesen Gesichtspunkten enorm. Als dependability zusammengefasst werden die Eigenschaften der Verfügbarkeit, der Zuverlässigkeit, Wartbarkeit, Zugriffssicherheit (security), und der funktionalen Sicherheit (safety) im Sinne der Vermeidung schwerwiegender Konsequenzen als Resultat fehlerhafter Antworten [@fraunhoferDependableAI2026]. 

Eine RAG-Architektur kann in drei Hauptkomponenten zerlegt werden: Abruf, Augmentation und Generierung [@singh2025agentic]. Ersteres ist dabei für die Bereitstellung relevanter Daten durch Durchsuchen des externen Informationssystem verantwortlich. Die Augmentationskomponente bereite diese anschließend auf, indem Informationen im Kontext der Prompt zusammengefasst werden. Die Generierung nutzt abschließend das LLM, um fundierte Antworten im Sinne der Anfrage zu generieren. 

![Funktionsweise von RAG AI (eigene Darstellung, nach [@honroth2024ragInfographic])](assets/img/rag.png)

Jedes moderne und hinreichend große LLM kann mit RAG ausgestattet werden, um auf Grundlage von LLM externen Datenmengen zu antworten. Eigenes, dem LLM-Kontext fernes, Wissen kann so genutzt werden, ohne das LLM selbst neu zu trainieren oder fine-tuning zu betreiben [@honroth2024rag].

Trotz der genannten Vorteile sind RAG AI Systeme durch den statischen Wissenskern des vortrainierten Modells eingeschränkt. Zwar sind sie im Vergleich zu regulären LLMs überlegen, aber dennoch nicht immun gegen Halluzination und durch veraltete Trainingsdaten verfälschte Antworten [@ji2023hallucination].

Neben der Erweiterung des LLMs um externe Wissensquellen, besteht der Bedarf das monolithische System, um externe Mechanismen zur Entscheidungsfindung und Kontrolle zu erweitern. Dieses Konzept ist als Agentic Intelligence bekannt und beschreibt die Fähigkeit eines KI-Systems, mehrstufige Aufgaben zu bewältigen. Dies geschieht, indem, möglicherweise verschiedene, LLMs in Form von Software-Agenten kooperieren. Dadurch kann zum einen autonom geplant werden, zum anderen können auch im Laufe des Prozesse Entscheidungen getroffen und nach eigenem ermessen auf externe Werkzeuge zugegriffen werden [@mitSloan2025agentic].

In Kombination mit einer *RAG-Architektur* bildet eine *Agentic AI* ein *Agentic RAG*, indem autonome KI-Agenten in die RAG-Pipeline eingesetz werden, um durch die Kombination aus Planung, Tool-Nutzung, Reflexion und der Zusammenarbeit mehrerer Agenten das RAG-System und die Suchstrategien vollkommen dynamisch zu steuern. Dies erzeugt eine einzigartige Flexibilität der Arbeitsabläufe. Daraus resultiert, dass Agentic RAG-Systeme in der Praxis eine unübertroffene Flexibilität, Skalierbarkeit und ein noch tieferes Kontextverständnis liefern [@singh2025agentic].

## ElasticSearch als lokale Retrieval-Komponente

Während Architekturen für RAG zur Durchsuchung von Dokumentensammlungen häufig auf semantischen Vektorsuchen basieren, wirkt im vorliegenden Anwendungsfall eine unscharfe (fuzzy) String-Suche zielführender. Deshalb wird im folgenden auf ElasticSearch zurückgegriffen. Für diese Entscheidung sprechen mehrere technische und konzeptionelle Gründe.
ElasticSearch ist als quelloffene, verteilte Such- und Analytics-Engine, die gezielt auf Geschwindigkeit und Skalierbarkeit ausgelegt ist, hervorragend für den Einsatz in KI-Anwendungen geeignet.

Die eigentliche Suchfunktionalität von ElasticSearch basiert dabei auf Lucene, einer in Java geschriebenen Programmbibliothek der Apache Software Foundation. Ziel der Bibliothek ist die Bereitstellung einer leistungsfähigen Volltextsuche, die es erlaubt, aus einem frei formulierten Text eine Trefferliste zu erzeugen. Dabei ist Lucene in der Lage, mit fehlerhaften Schreibweisen, Synonymen und Formulierungen sowie grammatikalischen Formen, wie Singular und Plural, umzugehen. Gesuchte Begriffe werden zuverlässig in Texten identifiziert [@elasticFullText2026]. Der Vorteil einer solchen Freitextsuche liegt in der Fähigkeit, dem Nutzer auch bei ungenauer oder fehlerhafter Eingabe ein passendes Suchergebnis bereitzustellen, was für die verwendete fuzzy Suche von zentraler Bedeutung ist [@elasticFullText2026].

Die aus den Quelldaten erzeugte Vektordatenbank speichert mühelos große Mengen an halbstrukturierten Daten als schemalose JSON-Dokumente [@elasticVectorDatabase2026] und ermöglicht Sprachmodellen so den Zugriff auf lokale Informationen, ohne dass das Modell selbst die Quelle verarbeiten muss [@elasticVectorDatabase2026]. So gelingt das Retrieval in Echtzeit.
Selbst bei umfangreichen Datenbeständen liefert die Suche innerhalb von Millisekunden deterministische Ergebnisse die dem Sprachmodell mit präzisen Kontextinformationen, wie beispielsweise die Quelldatei und die Zeilennummer, bereitgestellt werden [@elasticVectorDatabase2026]. Zum anderen erlaubt ElasticSearch eine hybride Suche, die die klassische Volltextsuche mit dichten und dünn besetzten Vektoreinbettungen (Dense und Sparse Vectors) kombiniert und so ein hohes semantisches Verständnis erreicht [@elasticHybridSearch2026]. Darüber hinaus besteht keine zwingende Framework-Abhängigkeit, da sich vollständige RAG-Pipelines direkt innerhalb des Elastic-Ökosystems umsetzen lassen, ohne dass zusätzliche externe Werkzeuge wie LangChain zwingend erforderlich wären [@elasticProduct2026].

## Model Context Protocol als Werkzeugschicht für LLM-Systeme

Um im Rahmen einer RAG-Architektur auf die fehlertolerante Sucheoperation über die externen Datenquellen zugreifen zu können, die mit ElasticSearch in Form der Retrieval-Komponente bereitgestellt wird, ist eine übergeordnete Struktur nötig. Diese muss die Interaktion zwischen dem Sprachmodell und ElasticSearch sowohl koordinieren als auch standartisieren.

Herkömmliche Integrationsschnittstellen wie klassische REST- oder fixed-schema RPC-APIs stoßen hierbei an systemische Grenzen. Sie agieren prinzipiell zustandslos und unterstützen keine native Sitzungshistorie, weshalb ihre starren Verträge den dynamischen Anforderungen moderner KI-Systeme nicht gerecht  werden [@ray2025mcp]. Diese technologische Lücke schließt das von Anthropic entwickelte Model Context Protocol (MCP) als eine universelle Ebene, die als sitzungsorientiertes Framework die Integration von Werkzeugen, Prompts und Kontexten in LLMs vereinheitlicht [@sanikommu2025mcp; @ray2025mcp].

Das MCP basiert architektonisch auf einem modularen Host-Client-Server-Paradigma und gewährleistet so eine strikte Funktionstrennung sowie die isolationstechnische Absicherung einzelner Systemkomponenten, indem der MCP Host als zentrale, vertrauenswürdige Instanz agiert [@ray2025mcp]. Dieser steuert den Lebenszyklus von Client-Instanzen und überwacht Sicherheitsrichtlinien sowie Benutzergenehmigungen via OAuth 2.1 und koordiniert die Kontextaggregation aus verschiedenen Quellen. Die MCP Clients sind so isoliert voneinander und halten dedizierte Punkt-zu-Punkt-Verbindungen zu den jeweiligen Servern [@ray2025mcp].
Auf Protkollebene erfolgt der Nachrichtenaustausch über das minimalistische JSON-RPC 2.0-Protokoll. Als Transportschichten dienen entweder standard input/output (stdio) für lokale Subprozesse oder Streamable HTTP mit Server-Sent Events (SSE) für cloud-native Netzwerkumgebungen [@ray2025mcp].

Um Services bereitzustellen, exponieren die MCP Server spezifische Fähigkeiten über vier standardisierte Primitive nach außen [@ray2025mcp]:

1. Prompts: Vordefinierte, benutzergesteuerte Eingabetemplates werden dynamisch über Argumente parametrisiert, um das Modellverhalten zu steuern [@ray2025mcp].

2. Resources: Anwendungsgesteuerte Datenkomponenten, die über eindeutige Uniform Resource Identifiers (URIs) identifiziert werden. Sie stellen strukturierte oder unstrukturierte Kontexte wie Text- oder Binärdaten bereit [@ray2025mcp].

3. Tools: Modellgesteuerte, ausführbare Funktionen oder Remote-APIs, die mit JSON-Schema-basierten Parametern definiert sind und LLMs die autonome Ausführung von Aktionen in externen Systeme erlauben [@ray2025mcp].

4. Utilities: Querschnittsfunktionen wie zum Beispiel standardisiertes Logging nach dem Syslog-Standard (RFC 5424), Argumentvervollständigungen und Cursor-basierte Paginierungsmechanismen zur Optimierung der Wartbarkeit [@ray2025mcp].

Durch dieses strukturierte Zusammenspiel befähigte MCP LLM-Systeme können kontextuelle Datenströme in Echtzeit verarbeiten [@sanikommu2025mcp]. Mittels intelligenter Filterung, hierarchischer Repräsentationen und progressiver Ladetechniken können kritische Limitierungen wie der Zustand des Context Overload oder hardwareseitige Token-Fenster-Beschränkungen effektiv kompensiert werden [@sanikommu2025mcp].

Das Protokoll fungiert folglich als eine Art universelle Werkzeugschicht, vergleichbar mit einem „USB-C-Standard für KI-Anwendungen“ [@ray2025mcp].

## PDF-Ingestion, Chunking und Metadaten

Das Fundament unstrukturierter Datenbestände bildet die Verarbeitung moderner Architekturen zur wissensbasierten Textgenerierung. Im Zentrum dieser Vorbereitung steht die sogenannte Ingestion, deren primäres Ziel es ist, heterogene Dokumente wie lokale PDF-Bestände, oft rekursiv, so aufzubereiten, dass sie präzise durchsuchbar und zitierbar werden [@gao2024ragllm].

Der kritische Teilschritt innerhalb dieser Pipeline ist die Extraktion des Rohtextes und dessen Zerlegung in kleinere, semantische Einheiten (chunks). Diese Aufteilung ist notwendig, um sicherzustellen, dass die Treffer klein genug für präzises Retrieval bleiben [@barnett2024failurepoints]. Das Chunking wird dabei als konfigurierbares Systemelement verstanden: Die Parameter der Chunk-Größe (Chunk Size) und des Überlappungsbereichs (Overlap) müssen so gewählt werden, das eine Balance zwischen der Kontextqualität und der Treffergenauigkeit gewährleistet wird [@gao2024ragllm].

Für die spätere Nachvollziehbarkeit und Evaluierung ist es zudem unerlässlich, pro Chunk einen persistenten Satz an strukturierten Metadaten zu speichern. Dieser Datensatz umfasst wenigstens Identifikatoren wie die doc_id und chunk_id sowie inhaltliche Orientierungspunkte wie den Dokumententitel, den Datei- bzw. Quellpfad, die konkrete Seite und den extrahierten Textinhalt. Insbesondere die exakten Seitenmetadaten sind für die spätere Belegstellenprüfung und das manuelle Review von fundamentaler Bedeutung [@manning2008informationretrieval].

Als strukturierte Ablage dieser Chunks und ihrer Metadaten dient ein invertierter Index, wie er in modernen Suchmaschinen-Architekturen wie ElasticSearch realisiert ist. Ein solcher Index bildet die informationstechnische Grundlage, um komplexe Such- und Retrieval-Strategien performant auszuführen [@manning2008informationretrieval].

## Evaluationsmetriken für Retrieval und Antwortqualität

Die Validierung eines kombinierten Such- und Generierungssystems erfordert eine strikte Trennung zwischen der Leistungsfähigkeit des Suchverfahrens (Retrieval-Qualität) und der Performanz des nachgelagerten Sprachmodells (Antwortqualität) [@es2025ragas]. Beide Komponenten agieren auf unterschiedlichen Ebenen und müssen mit verschiedenen, passenden Instrumenten gemessen werden.

Das Retrieval, also die reine Informationsbeschaffung, wird klassisch über die informationstheoretischen Standardmetriken Präzision (Precision@k) und Sensitivität (Recall@k) bewertet, ergänzt durch die Trefferquote (Hit-Rate) bei einem definierten Schwellenwert k [@manning2008informationretrieval].
Bei der Evaluation dünn besetzter oder sparsamer Treffermengen ist es wichtig, nicht nur zu erfassen, ob ein relevantes Dokument gefunden wurde, sondern auch in welchem Verhältnis die relevanten Treffer zur gesamten Menge an gelieferten Resultaten stehen. Um eine Verzerrung der Evaluationsergebnisse durch extreme Ausreißer in beide Richtungen zu verhindern, müssen die gefunden Werte über die Gesamtheit aller Testfragen gemittelt werden. Dies wird als Macro-Aggregation bezeichnet [@manning2008informationretrieval].
Konzeptionell sollte sich eine solche Evaluation zudem über verschiedene operative Modi erstrecken – von kontrollierten Nutzeranfragen (user) über realistische Parameterkonfigurationen (realistic_args) bis hin zu erweiterten Diagnoseeinstellungen (diagnostic_args), um das Systemverhalten unter variierenden Randbedingungen zu analysieren.
Die methodische Basis für diese quantitative Überprüfung bildet das sogenannte Goldtruth-Konzept. Hierbei wird jeder Testfrage vorab manuell eine Menge erwarteter Chunk-IDs oder relevante Belegstellen zugewiesen. Für die Retrieval-Stufe ist dann entscheidend, ob diese erwarteten Ziel-Chunks in den Suchergebnisse auftauchen [@craswell2020overviewtrec].

Für die finale Antwortgenerierung hingegen ist entscheidend, ob das LLM die bereitgestellten Treffer syntaktisch und semantisch korrekt verarbeitet.
Da automatisierte textuelle Metriken die Nuancen natürlicher Sprache nicht ausreichend abbilden, muss die Evaluation um eine manuelle Bewertung der Antwortqualität erweitert werden [@es2025ragas]. Diese qualitative Überprüfung erfolgt anhand formaler Kriterien wie der sachlichen Korrektheit, der inhaltlichen Vollständigkeit und der logischen Widerspruchsfreiheit der Antwort. Die Ergebnisse dieser Bewertung werden idealerweise in einem mathematisch gewichteten Antwortscore zusammengefasst. Dieser erlaubt es anschließend, verschiedene algorithmische Suchstrategien direkt miteinander zu vergleichen. Methodisch wertvoll ist hierbei auch die separate Ausweisung von sogenannten Zero-Hit-Fällen (Suchen, die keinerlei Ergebnisse liefern), da diese bei der Interpretation der Systemleistung grundlegend anders zu bewerten sind als eine lediglich suboptimale Rangfolge (Ranking) der Treffer [@barnett2024failurepoints].

Abschließend ist die Erkenntnis zentral, dass hervorragende Retrieval-Metriken nicht automatisch eine hohe Antwortqualität garantieren [@es2025ragas; @lewis2020rag]. Wenn das LLM an der Interpretation der Suchergebnisse scheitert oder in Halluzination verfällt, führen selbst perfekte Retrieval-Werte zu einem fehlerhaften Ergebnis. Aus diesem Grund müssen zu einer ganzheitlichen Evaluation des Systems immer beide Metriken betrachtet werden.


# Anforderungsanalyse und Zielarchitektur (ca. 1 Seiten, mit UML Diagramm, Komponenten Diagramm, Squence Diagramm)

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Lorem ipsum dolor sit amet, consectetuer

## Anforderungen an ein lokales und privatsphaerisches Assistenzsystem

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Funktionale Anforderungen

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Nicht-funktionale Anforderungen

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Zielarchitektur des Systems

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  


# Systementwurf und Implementierung (ca. 1 Seiten, Klassendiagramm, Sourcecode snippets, Dokumentation im SC)

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Gesamtpipeline vom PDF-Dokument bis zur Antwort

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Dateningestion und Indexaufbau

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## ElasticSearch-Mapping und Dokumentstruktur

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## MCP-Server und Such-Tools

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## LLM-Client, Tool-Nutzung und Antwortgenerierung

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Reproduzierbarkeit, Logging und Artefaktstruktur

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  


# Entwicklung der Retrieval-Strategien (ca. 3 Seiten)

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Ausgangspunkt: einfacher Einzel-PDF-Prototyp

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Exact Retrieval und Query-Rewrite

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Phrase- und Proximity-Retrieval

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Fuzzy Retrieval als robuster Baseline-Ansatz (prüfen)

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## KI-gestuetztes Smart Retrieval: Idee, Umsetzung und Grenzen

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  


# Evaluationsdesign (ca. 3 Seiten)

## Aufbau der Testbench

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Fragenset, Modi und Goldtruth-Konzept

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Bewertungslogik fuer Retrieval

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Manuelle Bewertung der Antwortqualitaet

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

## Versuchsaufbau und Vergleichbarkeit der Runs

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  

Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  


# Experimentelle Ergebnisse (ca. 3 Seiten)

## Ergebnisse der fruehen Runs und Iterationen

## Verbesserungen durch Exact-Rewrite

## Vergleich von Exact, Proximity und Fuzzy

## Vergleich Fuzzy vs. Smart im User-Mode

## Vergleich Gemini API vs. Lokale Modelle

## Zusammenfassung der zentralen quantitativen Befunde


# Diskussion (ca. 3 Seiten)

## Einordnung der Retrieval-Ergebnisse

## Warum Fuzzy aktuell der staerkste Ansatz ist

## Grenzen von Exact und Proximity

## Grenzen des aktuellen Smart-Retrieval-Ansatzes

## Validitaet der Metriken und Grenzen der Goldtruth


# Fazit und Ausblick (ca. 1 Seiten)

## Beantwortung der Forschungsfrage

## Wichtigste technische und methodische Erkenntnisse

## Konkrete naechste Entwicklungsschritte

## Perspektiven fuer weiterfuehrende Forschung