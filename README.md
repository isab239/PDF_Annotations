Masterprojekt
Masterprojekt Data Science 2024

Dieses Tool analysiert wissenschaftliche Arbeiten, indem es Text aus PDF-Dokumenten extrahiert, Inkonsistenzen in Definitionen und Erklärungen erkennt und diese direkt im PDF-Dokument annotiert. Zusätzlich erstellt es vergleichende Diagramme für verschiedene Textmetriken und bietet eine benutzerfreundliche Oberfläche zur Datenverwaltung.

Inhaltsverzeichnis
Features
Installation
Anwendung
Konfiguration
Projektstruktur
Lizenz
Features
PDF-Text-Extraktion: Extrahiert und verarbeitet Text aus PDF-Dateien.
Definitionen- & Erklärungserkennung: Identifiziert Definitionen und Erklärungen mithilfe regulärer Ausdrücke und NLP.
Feedback-Annotationen: Annotiert das PDF mit Hervorhebungen und Kommentaren für inkonsistente Definitionen.
Visuelle Analyse: Erstellt visuelle Vergleichsdiagramme (Balkendiagramme, Violinplots, Boxplots) für verschiedene Metriken wie Satzanzahl, durchschnittliche Wortlänge und Satzlänge.
Unterstützung mehrerer PDF-Dateien: Ermöglicht die Batch-Analyse mehrerer PDF-Dateien.
CSV-Verwaltung: Ermöglicht das Speichern und Laden von Analysedaten aus einer CSV-Datei.
Benutzeroberfläche mit Streamlit: Benutzerfreundliche grafische Oberfläche zur Verwaltung des gesamten Workflows.
Installation
Voraussetzungen Stelle sicher, dass folgende Software auf deinem System installiert ist:

Python 3.7 oder höher
pip (Python-Paketmanager)
Repository klonen

Klone das GitHub-Repository auf deinen lokalen Rechner:
git clone https://github.com/DeinBenutzername/Projektname.git cd Projektname

Installiere die notwendigen Abhängigkeiten aus der requirements.txt-Datei:

pip install -r requirements.txt Zusätzliche NLP-Modelle herunterladen:

Für nltk:

import nltk nltk.download('punkt')

Für spaCy (deutsches Sprachmodell):

python -m spacy download de_core_news_sm

Anwendung
Anwendung starten Starte die Streamlit-App mit dem folgenden Befehl:

streamlit run app.py Die App wird im Standard-Webbrowser geöffnet. Du kannst die folgenden Funktionen über die Seitenleiste nutzen:

PDF-Dateien hochladen: Lade eine oder mehrere PDF-Dateien zur Analyse hoch.
Extrahierter Text und Diagramme: Sieh dir den extrahierten Text, erkannte Inkonsistenzen und generierte Vergleichsdiagramme an.
Annotierte PDF-Dateien herunterladen: Lade die annotierten PDF-Dateien mit Kommentaren und Hervorhebungen herunter.
Erklärung der GUI

Reset-Button: Setzt die aktuelle Analyse zurück und löscht den aktuellen Sitzungsstatus.
Load CSV: Lädt zuvor gespeicherte Analysedaten.
Save to CSV: Speichert die aktuell analysierten Daten in einer CSV-Datei.
Upload PDF Files: Ermöglicht das Hochladen einer oder mehrerer PDF-Dateien zur Analyse und zum Vergleich.
Load Own Thesis: Lade deine eigene wissenschaftliche Arbeit zur detaillierten Analyse und Feedback ein.
Konfiguration
Die Konfigurationsoptionen können in der Hauptanwendungsdatei angepasst werden:

Definitionen- und Erklärungsmuster: Passe die definition_patterns in der identify_definitions_explanations()-Funktion an, wenn du andere Muster für die Texterkennung verwenden möchtest. Visualisierungstypen: Aktiviere oder deaktiviere bestimmte Visualisierungstypen (z.B. Scatterplots, Violinplots) über die Checkboxen in der Streamlit-GUI. Projektstruktur Das Projekt ist folgendermaßen organisiert:

├── app.py # Hauptanwendungsdatei

├── analyse.py # Modul zur Textanalyse

├── feedback.py # Modul zur Erstellung von Feedback

├── readfiles.py # Modul zum Lesen von PDF-Dateien

├── storage.py # Modul zur Verwaltung und Speicherung von Daten

├── gui.py # Modul zur GUI-Verwaltung

├── data/ # Verzeichnis zur Speicherung von CSV-Dateien

│ └── thesis.csv # Beispiel-CSV-Datei zur Speicherung der Analyseergebnisse

├── requirements.txt # Liste der Abhängigkeiten für das Projekt

├── README.md # Dokumentationsdatei

└── LICENSE # Lizenzdatei

Hauptmodule

app.py: Die Hauptdatei der Streamlit-App, die alle Funktionen integriert.
analyse.py: Enthält die Funktionen zur Analyse von Texten auf Inkonsistenzen und Muster.
feedback.py: Verwaltet die Erstellung und Darstellung von Feedback in den PDFs.
readfiles.py: Liest PDF-Dateien ein und extrahiert deren Inhalte.
storage.py: Verarbeitet und speichert die analysierten Daten.
gui.py: Beinhaltet den Code zur Erstellung und Verwaltung der GUI-Komponenten in der Streamlit-App.
Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die Datei LICENSE.md für Details.
