# IT-Security-TCG

Ein Sammelkartenspiel (Trading Card Game) rund um Angriffsvektoren aus der
IT-Sicherheit – umgesetzt in Python als Terminal-Spiel.

Dieses Projekt erfüllt den kompletten Auftrag:

1. **Recherche** der verschiedenen Angriffsvektoren (Trojaner, Viren, DDoS, …)
2. **Konzept** eines Sammelkartenspiels, das die Angriffe kurz beschreibt
3. **Karten-Design** inklusive Seltenheit (Rarity)
4. **Minispiel** zum Bespielen der Karten (Quartett / Top-Trumps nach dem
   Stein-Schere-Papier-Prinzip)

---

## Schnellstart

```bash
# Spiel starten (Quartett gegen den Computer)
python3 -m it_security_tcg

# Nur die Kartensammlung ansehen
python3 -m it_security_tcg --cards

# Mit festem Seed (reproduzierbares Mischen)
python3 -m it_security_tcg --seed 42
```

Es werden **keine externen Bibliotheken** benötigt – reines Python 3.10+.

---

## 1. Angriffsvektoren (Recherche)

Ein *Angriffsvektor* ist der Weg oder die Methode, über die ein Angreifer in
ein IT-System eindringt. Die wichtigsten Kategorien im Spiel:

| Kategorie            | Beispiele im Spiel                                   |
|----------------------|------------------------------------------------------|
| **Malware**          | Virus, Wurm, Trojaner, Ransomware, Spyware, Rootkit, Keylogger, Adware, Backdoor, Cryptojacking |
| **Netzwerk**         | DDoS-Angriff, Botnetz, Man-in-the-Middle             |
| **Web**              | SQL-Injection, Cross-Site-Scripting (XSS)            |
| **Social Engineering** | Phishing, Social Engineering                       |
| **Zugang / Exploit** | Brute-Force, Zero-Day-Exploit, Advanced Persistent Threat |

Kurz erklärt (Auswahl):

- **Virus** – hängt sich an Dateien und verbreitet sich beim Öffnen.
- **Wurm** – verbreitet sich selbstständig über Netzwerke, ohne dass eine
  Datei ausgeführt werden muss.
- **Trojaner** – tarnt sich als nützliches Programm und öffnet heimlich eine
  Hintertür.
- **Ransomware** – verschlüsselt Daten und fordert Lösegeld.
- **DDoS** – überlastet einen Server mit Anfragen, bis er nicht mehr
  erreichbar ist (oft über ein **Botnetz**).
- **Phishing** – gefälschte E-Mails/Webseiten stehlen Zugangsdaten.
- **SQL-Injection / XSS** – schleusen Schadcode über unsichere Web-Eingaben ein.
- **Zero-Day-Exploit** – nutzt eine noch unbekannte Lücke aus, für die es noch
  keinen Patch gibt.

Die vollständigen Beschreibungen stehen direkt auf den Karten
(`python3 -m it_security_tcg --cards`).

---

## 2. Kartenkonzept

Jede Karte steht für einen Angriff und hat **vier Werte** (0–100), die die
Grundlage für das Quartett-Duell bilden:

| Wert            | Bedeutung                                              |
|-----------------|--------------------------------------------------------|
| **Schaden**     | Wie groß ist der potenzielle Schaden?                  |
| **Verbreitung** | Wie schnell/weit breitet sich der Angriff aus?         |
| **Tarnung**     | Wie schwer ist der Angriff zu entdecken?               |
| **Komplexität** | Wie viel Know-how braucht der Angreifer?               |

So sieht eine Karte im Terminal aus:

```
+------------------------------------------+
| Zero-Day-Exploit                    **** |
| Exploit | Legendaer                      |
| ---------------------------------------- |
| Schaden       95  [##########]           |
| Verbreitung   60  [######....]           |
| Tarnung       95  [##########]           |
| Komplexitaet  98  [##########]           |
| ---------------------------------------- |
| Nutzt eine bislang unbekannte            |
| Sicherheitsluecke aus, fuer die es noch  |
| keinen Patch gibt. ...                   |
+------------------------------------------+
```

---

## 3. Seltenheit (Rarity)

Es gibt vier Seltenheitsstufen. Faustregel: **Je stärker/gefährlicher ein
Angriff, desto seltener die Karte.** Die Stufe richtet sich nach der
Gesamtstärke (Summe der vier Werte) und wird farblich dargestellt.

| Seltenheit    | Symbol | Farbe    | Karten (Beispiele)                    |
|---------------|--------|----------|---------------------------------------|
| **Legendär**  | `****` | Gold     | Zero-Day-Exploit, Ransomware, APT     |
| **Episch**    | `***`  | Violett  | Rootkit, DDoS, Botnetz, SQL-Injection, Wurm |
| **Selten**    | `**`   | Blau     | Trojaner, MITM, Phishing, Spyware, …  |
| **Häufig**    | `*`    | Weiß     | Virus, Adware, Brute-Force, Backdoor, … |

Der Test `test_legendary_cards_are_stronger_on_average` prüft automatisch,
dass legendäre Karten im Schnitt stärker sind als epische und diese stärker
als häufige.

---

## 4. Minispiel: Quartett (Top-Trumps-Prinzip)

Das Spiel funktioniert nach dem **Stein-Schere-Papier-Prinzip eines
Wertevergleichs** (Autoquartett / Top Trumps):

1. Das Deck wird gemischt und gleichmäßig auf **dich** und den **Computer**
   verteilt.
2. Wer am Zug ist, wählt eine **Kategorie** (Schaden, Verbreitung, Tarnung,
   Komplexität).
3. Die oberste Karte beider Stapel wird verglichen – der **höhere Wert
   gewinnt** und nimmt beide Karten.
4. Bei **Gleichstand** wandern die Karten in einen **Pott**, der beim nächsten
   Gewinn dazukommt.
5. Wer am Ende **alle Karten** besitzt, gewinnt. Der Computer wählt clever
   immer seine stärkste Kategorie.

---

## Projektstruktur

```
Schule/
├── it_security_tcg/
│   ├── __init__.py       # Paket-Metadaten
│   ├── __main__.py       # Start via python -m it_security_tcg
│   ├── cards.py          # 20 Karten + Seltenheiten (Punkt 1–3)
│   ├── display.py        # ASCII-Karten mit Farben
│   ├── game.py           # Spiellogik / Quartett-Engine (Punkt 4)
│   └── main.py           # interaktive Terminal-Oberfläche
├── tests/
│   └── test_game.py      # 10 Tests für Karten & Spiellogik
└── README.md
```

## Tests ausführen

```bash
pip install pytest
python3 -m pytest tests/ -q
```
