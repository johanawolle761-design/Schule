"""Darstellung der Karten im Terminal (ASCII-Art mit Farben)."""

from __future__ import annotations

import textwrap

from .cards import CATEGORIES, Card

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CARD_WIDTH = 40  # Innenbreite der Karte


def _line(content: str = "") -> str:
    """Eine Karteninnen-Zeile auf feste Breite bringen (ohne Farbcodes zu zaehlen)."""
    visible = _strip_ansi(content)
    padding = CARD_WIDTH - len(visible)
    if padding < 0:
        # Zu lang: hart abschneiden (sollte selten passieren)
        content = content[:CARD_WIDTH]
        padding = 0
    return f"| {content}{' ' * padding} |"


def _strip_ansi(text: str) -> str:
    """Entfernt ANSI-Farbcodes, um die sichtbare Laenge zu bestimmen."""
    out = []
    i = 0
    while i < len(text):
        if text[i] == "\033":
            # bis 'm' ueberspringen
            while i < len(text) and text[i] != "m":
                i += 1
            i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def render_card(card: Card, highlight: str | None = None) -> str:
    """Rendert eine Karte als mehrzeiligen String.

    highlight: Name einer Kategorie, die hervorgehoben werden soll.
    """
    color = card.rarity.color
    border = f"{color}+{'-' * (CARD_WIDTH + 2)}+{RESET}"
    lines = [border]

    # Kopf: Name + Seltenheits-Sterne
    stars = f"{color}{card.rarity.symbol}{RESET}"
    name = f"{BOLD}{card.name}{RESET}"
    header = f"{name}"
    # Sterne rechtsbuendig
    visible_len = len(_strip_ansi(header)) + len(card.rarity.symbol)
    gap = CARD_WIDTH - visible_len
    header_line = f"{color}| {RESET}{header}{' ' * max(gap, 1)}{stars}{color} |{RESET}"
    lines.append(header_line)

    lines.append(f"{color}{_line(f'{DIM}{card.typ} | {card.rarity.label}{RESET}')}{RESET}")
    lines.append(f"{color}{_line('-' * CARD_WIDTH)}{RESET}")

    # Werte
    for key, label in CATEGORIES.items():
        val = card.value(key)
        bar = _bar(val)
        row = f"{label:<13}{val:>3}  {bar}"
        if highlight == key:
            row = f"{BOLD}\033[32m{row}{RESET}"  # gruen hervorgehoben
        lines.append(f"{color}{_line(row)}{RESET}")

    lines.append(f"{color}{_line('-' * CARD_WIDTH)}{RESET}")

    # Beschreibung (umgebrochen)
    for wrapped in textwrap.wrap(card.beschreibung, CARD_WIDTH):
        lines.append(f"{color}{_line(f'{DIM}{wrapped}{RESET}')}{RESET}")

    lines.append(border)
    return "\n".join(lines)


def _bar(value: int, width: int = 10) -> str:
    """Kleine Balkenanzeige fuer einen Wert von 0-100."""
    filled = round(value / 100 * width)
    return "[" + "#" * filled + "." * (width - filled) + "]"


def print_card(card: Card, highlight: str | None = None) -> None:
    print(render_card(card, highlight))


def cards_side_by_side(left: Card, right: Card,
                       highlight: str | None = None) -> str:
    """Zwei Karten nebeneinander darstellen (auf gleiche Hoehe aufgefuellt)."""
    l_lines = render_card(left, highlight).split("\n")
    r_lines = render_card(right, highlight).split("\n")
    height = max(len(l_lines), len(r_lines))
    blank = " " * (CARD_WIDTH + 4)  # Breite einer Karte inkl. Rahmen
    l_lines += [blank] * (height - len(l_lines))
    r_lines += [blank] * (height - len(r_lines))
    return "\n".join(f"{a}   {b}" for a, b in zip(l_lines, r_lines))
