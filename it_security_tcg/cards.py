"""Kartendefinitionen fuer das IT-Security-TCG.

Jede Karte steht fuer einen realen Angriffsvektor aus der IT-Sicherheit.
Die vier Werte bilden die Grundlage fuer das Quartett-Minispiel:

    schaden       - Wie gross ist der potenzielle Schaden? (1-100)
    verbreitung   - Wie schnell/weit breitet sich der Angriff aus? (1-100)
    tarnung       - Wie schwer ist der Angriff zu entdecken? (1-100)
    komplexitaet  - Wie viel Know-how braucht der Angreifer? (1-100)

Die Seltenheit (Rarity) einer Karte richtet sich grob nach ihrer
Gesamtstaerke - starke, gefaehrliche Angriffe sind seltener.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass


class Rarity(enum.Enum):
    """Seltenheitsstufen der Karten."""

    HAEUFIG = ("Haeufig", 1, "\033[37m")      # weiss/grau
    SELTEN = ("Selten", 2, "\033[34m")        # blau
    EPISCH = ("Episch", 3, "\033[35m")        # violett
    LEGENDAER = ("Legendaer", 4, "\033[33m")  # gold/gelb

    def __init__(self, label: str, stars: int, color: str):
        self.label = label
        self.stars = stars
        self.color = color

    @property
    def symbol(self) -> str:
        """Sternchen-Darstellung der Seltenheit, z. B. '***'."""
        return "*" * self.stars


# Kategorien in der Reihenfolge, in der sie im Spiel angezeigt werden.
CATEGORIES = {
    "schaden": "Schaden",
    "verbreitung": "Verbreitung",
    "tarnung": "Tarnung",
    "komplexitaet": "Komplexitaet",
}


@dataclass(frozen=True)
class Card:
    """Eine einzelne Angriffs-Karte."""

    name: str
    typ: str          # Kategorie des Angriffs (z. B. "Malware", "Netzwerk")
    rarity: Rarity
    schaden: int
    verbreitung: int
    tarnung: int
    komplexitaet: int
    beschreibung: str

    def value(self, category: str) -> int:
        """Wert einer Kategorie abrufen (fuer das Quartett-Duell)."""
        return getattr(self, category)

    @property
    def gesamtstaerke(self) -> int:
        """Summe aller Werte - Grundlage fuer die Seltenheit."""
        return self.schaden + self.verbreitung + self.tarnung + self.komplexitaet


# ---------------------------------------------------------------------------
# Das Kartendeck: 20 Angriffsvektoren aus der IT-Sicherheit
# ---------------------------------------------------------------------------

DECK: list[Card] = [
    # ---------------------- LEGENDAER (sehr stark/selten) ------------------
    Card(
        name="Zero-Day-Exploit",
        typ="Exploit",
        rarity=Rarity.LEGENDAER,
        schaden=95, verbreitung=60, tarnung=95, komplexitaet=98,
        beschreibung=(
            "Nutzt eine bislang unbekannte Sicherheitsluecke aus, fuer die es "
            "noch keinen Patch gibt. Extrem gefaehrlich, da keine Abwehr existiert."
        ),
    ),
    Card(
        name="Ransomware",
        typ="Malware",
        rarity=Rarity.LEGENDAER,
        schaden=98, verbreitung=80, tarnung=55, komplexitaet=70,
        beschreibung=(
            "Verschluesselt die Daten des Opfers und fordert Loesegeld fuer die "
            "Entschluesselung. Kann ganze Unternehmen und Krankenhaeuser lahmlegen."
        ),
    ),
    Card(
        name="Advanced Persistent Threat",
        typ="Kampagne",
        rarity=Rarity.LEGENDAER,
        schaden=90, verbreitung=45, tarnung=97, komplexitaet=95,
        beschreibung=(
            "Langfristiger, gezielter Angriff (oft staatlich), der sich unbemerkt "
            "im Netzwerk einnistet und ueber Monate Daten abzieht."
        ),
    ),

    # ---------------------- EPISCH ----------------------------------------
    Card(
        name="Rootkit",
        typ="Malware",
        rarity=Rarity.EPISCH,
        schaden=80, verbreitung=40, tarnung=96, komplexitaet=88,
        beschreibung=(
            "Nistet sich tief im Betriebssystem ein, verschafft Angreifern "
            "Admin-Rechte und versteckt sich vor Virenscannern."
        ),
    ),
    Card(
        name="DDoS-Angriff",
        typ="Netzwerk",
        rarity=Rarity.EPISCH,
        schaden=75, verbreitung=90, tarnung=30, komplexitaet=50,
        beschreibung=(
            "Ueberflutet einen Server mit Anfragen (oft ueber ein Botnetz), "
            "bis dieser zusammenbricht und nicht mehr erreichbar ist."
        ),
    ),
    Card(
        name="Botnetz",
        typ="Netzwerk",
        rarity=Rarity.EPISCH,
        schaden=70, verbreitung=95, tarnung=65, komplexitaet=72,
        beschreibung=(
            "Ein Netz aus gekaperten Rechnern ('Zombies'), das ferngesteuert "
            "fuer DDoS, Spam oder Krypto-Mining missbraucht wird."
        ),
    ),
    Card(
        name="SQL-Injection",
        typ="Web",
        rarity=Rarity.EPISCH,
        schaden=78, verbreitung=50, tarnung=60, komplexitaet=65,
        beschreibung=(
            "Schleust ueber unsichere Eingabefelder Datenbank-Befehle ein und "
            "kann so Passwoerter und ganze Datenbanken auslesen."
        ),
    ),
    Card(
        name="Wurm",
        typ="Malware",
        rarity=Rarity.EPISCH,
        schaden=72, verbreitung=98, tarnung=45, komplexitaet=60,
        beschreibung=(
            "Verbreitet sich selbststaendig ueber Netzwerke, ohne dass eine "
            "Datei ausgefuehrt werden muss. Kann sich rasend schnell ausbreiten."
        ),
    ),

    # ---------------------- SELTEN ----------------------------------------
    Card(
        name="Trojaner",
        typ="Malware",
        rarity=Rarity.SELTEN,
        schaden=68, verbreitung=55, tarnung=80, komplexitaet=50,
        beschreibung=(
            "Tarnt sich als nuetzliches Programm, oeffnet im Hintergrund aber "
            "eine Hintertuer fuer Angreifer."
        ),
    ),
    Card(
        name="Man-in-the-Middle",
        typ="Netzwerk",
        rarity=Rarity.SELTEN,
        schaden=65, verbreitung=40, tarnung=85, komplexitaet=70,
        beschreibung=(
            "Klinkt sich unbemerkt in die Kommunikation zweier Parteien ein "
            "und liest oder manipuliert den Datenverkehr."
        ),
    ),
    Card(
        name="Phishing",
        typ="Social Engineering",
        rarity=Rarity.SELTEN,
        schaden=55, verbreitung=88, tarnung=50, komplexitaet=25,
        beschreibung=(
            "Gefaelschte E-Mails oder Webseiten locken Opfer dazu, Passwoerter "
            "oder Bankdaten preiszugeben."
        ),
    ),
    Card(
        name="Spyware",
        typ="Malware",
        rarity=Rarity.SELTEN,
        schaden=58, verbreitung=60, tarnung=82, komplexitaet=45,
        beschreibung=(
            "Spioniert heimlich das Nutzerverhalten aus und sendet Daten wie "
            "Surfverhalten oder Zugangsdaten an Dritte."
        ),
    ),
    Card(
        name="Keylogger",
        typ="Malware",
        rarity=Rarity.SELTEN,
        schaden=60, verbreitung=45, tarnung=88, komplexitaet=48,
        beschreibung=(
            "Zeichnet jede Tastatureingabe auf und faengt so Passwoerter, "
            "PINs und Nachrichten ab."
        ),
    ),
    Card(
        name="Cross-Site-Scripting",
        typ="Web",
        rarity=Rarity.SELTEN,
        schaden=52, verbreitung=58, tarnung=62, komplexitaet=55,
        beschreibung=(
            "Schleust Schadcode in Webseiten ein, der im Browser anderer "
            "Besucher ausgefuehrt wird (z. B. um Sitzungen zu kapern)."
        ),
    ),
    Card(
        name="Cryptojacking",
        typ="Malware",
        rarity=Rarity.SELTEN,
        schaden=45, verbreitung=65, tarnung=78, komplexitaet=50,
        beschreibung=(
            "Missbraucht heimlich die Rechenleistung des Opfers zum Schuerfen "
            "von Kryptowaehrung."
        ),
    ),

    # ---------------------- HAEUFIG ---------------------------------------
    Card(
        name="Virus",
        typ="Malware",
        rarity=Rarity.HAEUFIG,
        schaden=50, verbreitung=70, tarnung=40, komplexitaet=35,
        beschreibung=(
            "Haengt sich an Dateien an und verbreitet sich, sobald diese "
            "geoeffnet werden. Der Klassiker unter den Schadprogrammen."
        ),
    ),
    Card(
        name="Adware",
        typ="Malware",
        rarity=Rarity.HAEUFIG,
        schaden=25, verbreitung=72, tarnung=35, komplexitaet=20,
        beschreibung=(
            "Blendet ungewollt Werbung ein und sammelt nebenbei Daten. "
            "Meist mehr laestig als gefaehrlich."
        ),
    ),
    Card(
        name="Brute-Force-Angriff",
        typ="Zugang",
        rarity=Rarity.HAEUFIG,
        schaden=48, verbreitung=35, tarnung=25, komplexitaet=30,
        beschreibung=(
            "Probiert automatisiert unzaehlige Passwoerter durch, bis das "
            "richtige gefunden ist. Starke Passwoerter helfen dagegen."
        ),
    ),
    Card(
        name="Social Engineering",
        typ="Social Engineering",
        rarity=Rarity.HAEUFIG,
        schaden=55, verbreitung=50, tarnung=68, komplexitaet=30,
        beschreibung=(
            "Manipuliert Menschen statt Technik - etwa durch Vortaeuschen "
            "einer Identitaet am Telefon, um an Informationen zu kommen."
        ),
    ),
    Card(
        name="Backdoor",
        typ="Malware",
        rarity=Rarity.HAEUFIG,
        schaden=62, verbreitung=30, tarnung=75, komplexitaet=52,
        beschreibung=(
            "Eine versteckte Hintertuer, die den Zugang zu einem System auch "
            "ohne regulaeres Passwort ermoeglicht."
        ),
    ),
]


def get_deck() -> list[Card]:
    """Gibt eine (flache) Kopie des vollstaendigen Decks zurueck."""
    return list(DECK)
